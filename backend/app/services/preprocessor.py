"""
DI-2D Enhanced Image Preprocessor
Özellikle 2D teknik resimler için optimize edilmiş görüntü ön işleme

Özellikler:
- Otomatik parlaklık/kontrast ayarlama
- Çizgi netleştirme (line enhancement)
- Gürültü temizleme
- Boyut okuma için OCR hazırlık
- Adaptif threshold ile keskin kenarlarda iyileştirme
"""
import cv2
import numpy as np
from PIL import Image
import io
import base64
import logging
from typing import Dict, Any, Optional, Tuple
from pdf2image import convert_from_bytes

logger = logging.getLogger(__name__)

class DrawingPreprocessor:
    """2D teknik resim ön işleme sınıfı"""
    
    def __init__(self, dpi: int = 400, enhance_mode: str = "balanced"):
        """
        Args:
            dpi: PDF render çözünürlüğü (300-600 arası önerilir)
            enhance_mode: "fast", "balanced", "aggressive"
        """
        self.dpi = dpi
        self.enhance_mode = enhance_mode
        
    def process_file(self, file_bytes: bytes, file_ext: str) -> Dict[str, Any]:
        """
        Dosyayı işle (PDF veya görüntü)
        
        Args:
            file_bytes: Ham dosya baytları
            file_ext: Dosya uzantısı (.pdf, .png, .jpg)
            
        Returns:
            İşlenmiş görüntüler ve metadata
        """
        logger.info(f"🔧 Processing {file_ext} file with DPI={self.dpi}, mode={self.enhance_mode}")
        
        if file_ext.lower() == '.pdf':
            return self._process_pdf(file_bytes)
        else:
            return self._process_image(file_bytes)
    
    def _process_pdf(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """PDF'i işle ve her sayfayı optimize et"""
        try:
            # PDF'i görüntülere dönüştür
            images = convert_from_bytes(
                pdf_bytes,
                dpi=self.dpi,
                fmt='png',
                thread_count=4
            )
            
            logger.info(f"✅ PDF converted: {len(images)} pages at {self.dpi} DPI")
            
            processed_pages = []
            
            for idx, img in enumerate(images):
                # PIL Image'ı numpy array'e çevir
                img_array = np.array(img)
                
                # BGR formatına çevir (OpenCV için)
                if len(img_array.shape) == 3:
                    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                else:
                    img_cv = img_array
                
                # Görüntüyü iyileştir
                enhanced = self._enhance_drawing(img_cv)
                
                # Base64'e çevir
                img_base64 = self._image_to_base64(enhanced)
                
                processed_pages.append({
                    "page": idx + 1,
                    "image_base64": img_base64,
                    "width": enhanced.shape[1],
                    "height": enhanced.shape[0]
                })
            
            return {
                "status": "success",
                "total_pages": len(images),
                "dpi": self.dpi,
                "pages": processed_pages,
                "enhance_mode": self.enhance_mode
            }
            
        except Exception as e:
            logger.error(f"❌ PDF processing failed: {e}")
            raise
    
    def _process_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """Tek görüntüyü işle"""
        try:
            # Bayt akışından görüntü oku
            image = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(image)
            
            # BGR formatına çevir
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            elif len(img_array.shape) == 3 and img_array.shape[2] == 4:
                img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
            else:
                img_cv = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
            
            # Görüntüyü iyileştir
            enhanced = self._enhance_drawing(img_cv)
            
            # Base64'e çevir
            img_base64 = self._image_to_base64(enhanced)
            
            return {
                "status": "success",
                "total_pages": 1,
                "dpi": self.dpi,
                "pages": [{
                    "page": 1,
                    "image_base64": img_base64,
                    "width": enhanced.shape[1],
                    "height": enhanced.shape[0]
                }],
                "enhance_mode": self.enhance_mode
            }
            
        except Exception as e:
            logger.error(f"❌ Image processing failed: {e}")
            raise
    
    def _enhance_drawing(self, image: np.ndarray) -> np.ndarray:
        """
        Teknik resmi iyileştir
        
        Pipeline:
        1. Gürültü temizleme
        2. Kontrast iyileştirme
        3. Çizgi netleştirme
        4. Adaptif threshold (opsiyonel)
        """
        logger.info(f"🎨 Enhancing image: {image.shape}")
        
        # Gri tonlamaya çevir
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # 1. Gürültü temizleme (hafif)
        denoised = cv2.fastNlMeansDenoising(gray, None, h=10, templateWindowSize=7, searchWindowSize=21)
        logger.info("✓ Noise reduction applied")
        
        # 2. Kontrast iyileştirme (CLAHE - Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrasted = clahe.apply(denoised)
        logger.info("✓ Contrast enhanced (CLAHE)")
        
        if self.enhance_mode == "aggressive":
            # 3. Agresif keskinleştirme
            kernel = np.array([[-1, -1, -1],
                               [-1,  9, -1],
                               [-1, -1, -1]])
            sharpened = cv2.filter2D(contrasted, -1, kernel)
            logger.info("✓ Aggressive sharpening applied")
            result = sharpened
            
        elif self.enhance_mode == "balanced":
            # 3. Dengeli keskinleştirme
            blurred = cv2.GaussianBlur(contrasted, (0, 0), 3)
            sharpened = cv2.addWeighted(contrasted, 1.5, blurred, -0.5, 0)
            logger.info("✓ Balanced sharpening applied")
            result = sharpened
            
        else:  # fast
            # Minimal işleme
            result = contrasted
            logger.info("✓ Fast mode: minimal processing")
        
        # Tekrar BGR'ye çevir (AI modeli için)
        result_bgr = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        
        logger.info(f"✅ Enhancement complete: {result_bgr.shape}")
        return result_bgr
    
    def _image_to_base64(self, image: np.ndarray) -> str:
        """Numpy görüntüsünü base64 PNG string'e çevir"""
        try:
            # BGR'den RGB'ye çevir
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # PIL Image'a çevir
            pil_img = Image.fromarray(image_rgb)
            
            # Bayt buffer'a kaydet
            buffer = io.BytesIO()
            pil_img.save(buffer, format="PNG", optimize=True)
            buffer.seek(0)
            
            # Base64'e encode et
            img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            
            return img_base64
            
        except Exception as e:
            logger.error(f"❌ Base64 conversion failed: {e}")
            raise


def preprocess_drawing(file_bytes: bytes, file_ext: str, dpi: int = 400, enhance_mode: str = "balanced") -> Dict[str, Any]:
    """
    Kolaylık fonksiyonu - teknik resim ön işleme
    
    Args:
        file_bytes: Ham dosya baytları
        file_ext: Dosya uzantısı (.pdf, .png, .jpg)
        dpi: PDF render çözünürlüğü
        enhance_mode: "fast", "balanced", "aggressive"
    
    Returns:
        İşlenmiş görüntüler ve metadata
    """
    preprocessor = DrawingPreprocessor(dpi=dpi, enhance_mode=enhance_mode)
    return preprocessor.process_file(file_bytes, file_ext)

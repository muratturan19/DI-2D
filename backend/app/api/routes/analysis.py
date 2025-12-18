"""
DI-2D Analysis API Endpoints
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import logging
from typing import Optional, Dict, Any

from app.services.analyzer import analyzer
from app.services.werk24_analyzer import werk24_analyzer
from app.models.analysis import DrawingAnalysisResult, AnalysisRequest
from app.core.exceptions import AIKeyError, FileProcessingError, AnalysisError

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/analyze", response_model=DrawingAnalysisResult)
async def analyze_drawing(
    file: UploadFile = File(..., description="2D teknik resim dosyası (PDF, PNG, JPG)"),
    model: str = Form("gpt-5.2", description="AI modeli"),
    max_tokens: int = Form(150000, description="Maksimum token"),
    reasoning_level: str = Form("high", description="Düşünme seviyesi (medium|high|xhigh)"),
    enhance_mode: str = Form("balanced", description="Görüntü iyileştirme (fast|balanced|aggressive)")
):
    """
    2D teknik resim analizi
    
    **Desteklenen Formatlar:** PDF, PNG, JPG, JPEG
    
    **AI Modelleri:**
    - `werk24-professional` (Werk24) - **Profesyonel, en doğru** 🏆
    - `gpt-5.2` (OpenAI) - **En gelişmiş reasoning** ⭐ (Yeni - Aralık 2025)
    - `gpt-5.2-chat` (OpenAI) - Chat optimize edilmiş versiyon
    - `gpt-4-vision-preview` (OpenAI) - Geri uyumluluk
    - `claude-3-5-sonnet-20241022` (Anthropic) - Hızlı ve güvenilir
    
    **Reasoning Level (GPT-5.2 için):**
    - `medium`: Orta seviye analiz (~2-3 dk)
    - `high`: Detaylı analiz (~5-7 dk) - Önerilen ⭐
    - `xhigh`: En derin analiz (~10-15 dk) - Karmaşık resimler için
    
    **Enhance Mode:**
    - `fast`: Minimal işleme
    - `balanced`: Dengeli iyileştirme - Önerilen
    - `aggressive`: Maksimum keskinleştirme
    """
    try:
        # Dosya kontrolü
        if not file.filename:
            raise FileProcessingError("Dosya adı bulunamadı")
        
        # Uzantı kontrolü
        allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
        file_ext = file.filename.lower()[-4:]
        if not any(file_ext.endswith(ext) for ext in allowed_extensions):
            raise FileProcessingError(f"Desteklenmeyen dosya formatı. İzin verilenler: {', '.join(allowed_extensions)}")
        
        # Dosyayı oku
        file_bytes = await file.read()
        
        if len(file_bytes) == 0:
            raise FileProcessingError("Boş dosya")
        
        if len(file_bytes) > 20 * 1024 * 1024:  # 20MB limit
            raise FileProcessingError("Dosya çok büyük (max 20MB)")
        
        logger.info(f"📄 Received file: {file.filename} ({len(file_bytes)} bytes)")
        
        # Model seçimine göre analiz yap
        if model == "werk24-professional":
            # Werk24 ile analiz
            logger.info("🔧 Using Werk24 Professional API")
            result = await werk24_analyzer.analyze(
                file_bytes=file_bytes,
                filename=file.filename,
                confidence_threshold=0.7
            )
        else:
            # Standart AI modelleri ile analiz
            result = await analyzer.analyze(
                file_bytes=file_bytes,
                filename=file.filename,
                model=model,
                max_tokens=max_tokens,
                reasoning_level=reasoning_level,
                enhance_mode=enhance_mode
            )
        
        return result
        
    except AIKeyError as e:
        logger.error(f"❌ AI Key Error: {e.detail}")
        raise HTTPException(status_code=401, detail=e.detail)
    except FileProcessingError as e:
        logger.error(f"❌ File Processing Error: {e.detail}")
        raise HTTPException(status_code=422, detail=e.detail)
    except AnalysisError as e:
        logger.error(f"❌ Analysis Error: {e.detail}")
        raise HTTPException(status_code=500, detail=e.detail)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Beklenmeyen hata: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Servis sağlık kontrolü
    """
    return {
        "status": "healthy",
        "service": "DI-2D Analysis API",
        "version": "1.0.0",
        "models_available": {
            "openai": analyzer.openai_client is not None,
            "anthropic": analyzer.anthropic_client is not None
        }
    }


@router.get("/models")
async def list_models():
    """
    Desteklenen AI modellerini listele
    """
    models = []
    
    # Werk24 Professional (her zaman listede)
    models.append({
        "id": "werk24-professional",
        "name": "Werk24 Professional 🏆",
        "provider": "Werk24",
        "description": "Profesyonel, en yüksek doğruluk - 100 deneme lisansı",
        "recommended": True,
        "features": [
            "Yüksek doğruluklu boyut okuma",
            "GD&T tolerans analizi",
            "Malzeme tanıma",
            "Yüzey pürüzlülüğü",
            "Diş özellikleri"
        ]
    })
    
    # GPT-5.2 (Aralık 2025 - Yeni!)
    if analyzer.openai_client:
        models.extend([
            {
                "id": "gpt-5.2",
                "name": "GPT-5.2 ⭐ (Yeni!)",
                "provider": "OpenAI",
                "description": "En gelişmiş reasoning, derin analiz - Aralık 2025",
                "recommended": True,
                "features": [
                    "xHigh reasoning modu",
                    "Responses API",
                    "Chain-of-thought korunumu",
                    "Çok adımlı muhakeme"
                ]
            },
            {
                "id": "gpt-5.2-chat",
                "name": "GPT-5.2 Chat",
                "provider": "OpenAI",
                "description": "Chat optimize edilmiş versiyon",
                "recommended": False
            },
            {
                "id": "gpt-4-vision-preview",
                "name": "GPT-4 Vision (Legacy)",
                "provider": "OpenAI",
                "description": "Geri uyumluluk için",
                "recommended": False
            }
        ])
    
    if analyzer.anthropic_client:
        models.extend([
            {
                "id": "claude-3-5-sonnet-20241022",
                "name": "Claude 3.5 Sonnet",
                "provider": "Anthropic",
                "description": "Hızlı ve güvenilir analiz",
                "recommended": False
            }
        ])
    
    return {
        "models": models,
        "total": len(models)
    }


@router.post("/compare", response_model=Dict[str, Any])
async def compare_analysis(
    file: UploadFile = File(...),
    model1: str = Form("werk24-professional"),
    model2: str = Form("gpt-5.2"),
    reasoning_level: str = Form("medium"),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    İki farklı modelle aynı teknik resmi analiz et ve sonuçları karşılaştır
    
    - **file**: Teknik resim dosyası (PDF, PNG, JPEG)
    - **model1**: İlk model (varsayılan: werk24-professional)
    - **model2**: İkinci model (varsayılan: gpt-5.2)
    - **reasoning_level**: GPT-5.2 için reasoning seviyesi (low/medium/high/xhigh)
    
    Returns:
        Karşılaştırmalı analiz sonuçları
    """
    try:
        logger.info(f"Karşılaştırmalı analiz başlatıldı: {model1} vs {model2}")
        
        # Dosya kontrolü
        if not file.filename:
            raise FileProcessingError("Dosya adı bulunamadı")
        
        # Uzantı kontrolü
        allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
        file_ext = file.filename.lower()[-4:]
        if not any(file_ext.endswith(ext) for ext in allowed_extensions):
            raise FileProcessingError(f"Desteklenmeyen dosya formatı. İzin verilenler: {', '.join(allowed_extensions)}")
        
        # Dosyayı oku
        file_bytes = await file.read()
        
        if len(file_bytes) == 0:
            raise FileProcessingError("Boş dosya")
        
        if len(file_bytes) > 20 * 1024 * 1024:  # 20MB limit
            raise FileProcessingError("Dosya çok büyük (max 20MB)")
        
        logger.info(f"📄 Received file: {file.filename} ({len(file_bytes)} bytes)")
        
        # Model 1 analizi
        logger.info(f"🔍 Model 1 analizi başlıyor: {model1}")
        if model1 == "werk24-professional":
            result1 = await werk24_analyzer.analyze(
                file_bytes=file_bytes,
                filename=file.filename,
                confidence_threshold=0.7
            )
        else:
            result1 = await analyzer.analyze(
                file_bytes=file_bytes,
                filename=file.filename,
                model=model1,
                reasoning_level=reasoning_level
            )
        
        # Pydantic model'i dict'e çevir
        result1_dict = result1.model_dump() if hasattr(result1, 'model_dump') else result1
        logger.info(f"✅ Model 1 tamamlandı ({result1_dict.get('metadata', {}).get('processing_time', 0):.2f}s)")
        
        # Model 2 analizi
        logger.info(f"🔍 Model 2 analizi başlıyor: {model2}")
        if model2 == "werk24-professional":
            result2 = await werk24_analyzer.analyze(
                file_bytes=file_bytes,
                filename=file.filename,
                confidence_threshold=0.7
            )
        else:
            result2 = await analyzer.analyze(
                file_bytes=file_bytes,
                filename=file.filename,
                model=model2,
                reasoning_level=reasoning_level
            )
        
        # Pydantic model'i dict'e çevir
        result2_dict = result2.model_dump() if hasattr(result2, 'model_dump') else result2
        logger.info(f"✅ Model 2 tamamlandı ({result2_dict.get('metadata', {}).get('processing_time', 0):.2f}s)")
        
        # Karşılaştırma raporu oluştur
        comparison = {
            "timestamp": result1_dict.get("metadata", {}).get("timestamp", ""),
            "model1": {
                "name": model1,
                "provider": result1_dict.get("metadata", {}).get("model_provider", ""),
                "processing_time": result1_dict.get("metadata", {}).get("processing_time", 0),
                "confidence": result1_dict.get("metadata", {}).get("confidence_score", 0),
                "result": result1_dict
            },
            "model2": {
                "name": model2,
                "provider": result2_dict.get("metadata", {}).get("model_provider", ""),
                "processing_time": result2_dict.get("metadata", {}).get("processing_time", 0),
                "confidence": result2_dict.get("metadata", {}).get("confidence_score", 0),
                "result": result2_dict
            },
            "comparison_notes": {
                "time_difference": abs(
                    result1_dict.get("metadata", {}).get("processing_time", 0) - 
                    result2_dict.get("metadata", {}).get("processing_time", 0)
                ),
                "confidence_difference": abs(
                    result1_dict.get("metadata", {}).get("confidence_score", 0) - 
                    result2_dict.get("metadata", {}).get("confidence_score", 0)
                ),
                "faster_model": model1 if result1_dict.get("metadata", {}).get("processing_time", 0) < result2_dict.get("metadata", {}).get("processing_time", 0) else model2,
                "higher_confidence": model1 if result1_dict.get("metadata", {}).get("confidence_score", 0) > result2_dict.get("metadata", {}).get("confidence_score", 0) else model2
            }
        }
        
        logger.info(f"Karşılaştırma tamamlandı: {comparison['comparison_notes']}")
        return comparison
        
    except AIKeyError as e:
        logger.error(f"❌ AI Key Error: {e.detail}")
        raise HTTPException(status_code=401, detail=e.detail)
    except FileProcessingError as e:
        logger.error(f"❌ File Processing Error: {e.detail}")
        raise HTTPException(status_code=422, detail=e.detail)
    except AnalysisError as e:
        logger.error(f"❌ Analysis Error: {e.detail}")
        raise HTTPException(status_code=500, detail=e.detail)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Karşılaştırma hatası: {str(e)}")

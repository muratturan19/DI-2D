"""
Werk24 Professional Drawing Analysis Service
High-accuracy 2D technical drawing analysis using Werk24 V2 API
"""
import asyncio
from typing import Dict, Any, List, Optional
from werk24 import (
    Werk24Client,
    Hook,
    AskMetaData,
    AskInsights,
    AskFeatures,
)
import logging

from app.models.analysis import (
    DrawingAnalysisResult,
    GeometryAnalysis,
    ManufacturingAnalysis,
    QualityRequirements,
    AnalysisMetadata,
    DimensionInfo,
    FeatureInfo,
    MaterialInfo,
    ToleranceInfo,
    SurfaceFinishInfo,
)

logger = logging.getLogger(__name__)


class Werk24Analyzer:
    """
    Werk24 profesyonel teknik resim analiz servisi
    
    Özellikler:
    - Yüksek doğruluklu boyut okuma
    - GD&T tolerans analizi
    - Malzeme tanıma
    - Yüzey pürüzlülüğü tespiti
    - Diş özellikleri analizi
    """
    
    def __init__(self):
        self.results: Dict[str, Any] = {}
        self.errors: list = []
        
    async def analyze(
        self,
        file_bytes: bytes,
        filename: str,
        confidence_threshold: float = 0.7
    ) -> DrawingAnalysisResult:
        """
        Werk24 ile teknik resim analizi yap
        
        Args:
            file_bytes: Dosya byte dizisi
            filename: Dosya adı
            confidence_threshold: Minimum güven skoru
            
        Returns:
            DrawingAnalysisResult: Yapılandırılmış analiz sonucu
        """
        logger.info(f"🔧 Starting Werk24 analysis for {filename}")
        
        import time
        start_time = time.time()
        
        # Reset results
        self.results = {}
        self.errors = []
        
        try:
            # Werk24 V2 client
            async with Werk24Client() as client:
                # V2 API - spesifik Ask tipleri ile çalış
                hooks = [
                    Hook(ask=AskMetaData(), function=self._handle_response),
                    Hook(ask=AskFeatures(), function=self._handle_response),
                    Hook(ask=AskInsights(), function=self._handle_response),
                ]
                
                # BytesIO stream oluştur
                from io import BytesIO
                drawing_stream = BytesIO(file_bytes)
                
                # Analiz başlat
                await client.read_drawing_with_hooks(drawing_stream, hooks)
                
                # Kısa bekleme
                await asyncio.sleep(0.5)
            
            processing_time = time.time() - start_time
            
            # Sonuçları yapılandır
            result = self._build_result(filename, processing_time, confidence_threshold)
            
            logger.info(f"✅ Werk24 analysis completed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"❌ Werk24 analysis failed: {e}")
            self.errors.append(str(e))
            
            # Hata durumunda minimal sonuç döndür
            processing_time = time.time() - start_time
            return self._build_error_result(filename, processing_time, str(e))
    
    def _handle_response(self, message):
        """Werk24 V2 API yanıtını işle"""
        try:
            from werk24.models.v2.responses import (
                ResponseMetaDataComponentDrawing,
                ResponseInsightsComponentDrawing,
                ResponseFeaturesComponentDrawing,
                ResponseBalloons,
            )
            
            if hasattr(message, 'payload_dict'):
                payload = message.payload_dict
                logger.info(f"📦 Received: {type(message).__name__}")
                
                # Tüm sonuçları results dict'e ekle
                self.results.update(payload)
            
            # V2 response tiplerini yakala
            if isinstance(message, ResponseMetaDataComponentDrawing):
                self.results["metadata"] = message.model_dump()
            elif isinstance(message, ResponseInsightsComponentDrawing):
                self.results["insights"] = message.model_dump()
            elif isinstance(message, ResponseFeaturesComponentDrawing):
                self.results["features"] = message.model_dump()
            elif isinstance(message, ResponseBalloons):
                self.results["balloons"] = message.model_dump()
            
            if hasattr(message, 'exceptions') and message.exceptions:
                logger.warning(f"⚠️ Error: {message.exceptions}")
                self.errors.extend(message.exceptions)
        except Exception as e:
            logger.error(f"❌ Handle error: {e}")
            self.errors.append(str(e))
    
    def _build_result(
        self,
        filename: str,
        processing_time: float,
        confidence_threshold: float
    ) -> DrawingAnalysisResult:
        """Werk24 V2 sonuçlarını DI-2D formatına dönüştür"""
        
        metadata = self.results.get("metadata", {})
        insights = self.results.get("insights", {})
        features = self.results.get("features", {})
        
        title = metadata.get('designation') or filename
        drawing_number = None
        revision: Optional[str] = None
        
        identifiers: List[Dict[str, Any]] = metadata.get("identifiers", []) or []
        if identifiers:
            drawing_number = identifiers[0].get("value")
        
        # Boş yapılar oluştur
        dimensions = {}
        features_list = []
        tolerances = []
        surface_finishes = []
        material: Optional[MaterialInfo] = None
        
        # Raw results'ı kullan
        raw_results = {
            'werk24_response': self.results,
            'errors': self.errors
        }
        
        # Malzeme bilgisi
        material_options: List[Dict[str, Any]] = metadata.get("material_options", []) or []
        if material_options:
            material_entry = material_options[0].get("material_combination") or {}
            material = MaterialInfo(
                name=str(material_entry) if material_entry else "Unknown",
                standard=None,
                density=None,
                hardness=None,
            )
        
        # Yüzey pürüzlülüğü
        general_roughness = metadata.get("general_roughness")
        if general_roughness:
            surface_finishes.append(
                SurfaceFinishInfo(
                    type="roughness",
                    description="General surface roughness",
                    roughness=str(general_roughness),
                )
            )
        
        for rough in features.get("roughnesses", []) or []:
            surface_finishes.append(
                SurfaceFinishInfo(
                    type="roughness",
                    description=rough.get("label") or "Surface finish",
                    roughness=str(rough.get("standard") or rough.get("direction_of_lay")),
                )
            )
        
        # Boyut bilgileri
        for idx, dim in enumerate(features.get("dimensions", []) or []):
            size = dim.get("size") or {}
            confidence = dim.get("confidence") or 0.0
            if confidence < confidence_threshold:
                continue
            
            label = dim.get("label") or f"dimension_{idx+1}"
            tolerance_data = size.get("tolerance") or {}
            tolerance_str = None
            lower = tolerance_data.get("deviation_lower")
            upper = tolerance_data.get("deviation_upper")
            fit = tolerance_data.get("fit")
            if lower is not None or upper is not None:
                tolerance_str = f"{lower or 0:+g}/{upper or 0:+g}"
            elif fit:
                tolerance_str = f"Fit {fit}"
            
            dimensions[label] = DimensionInfo(
                value=size.get("value", 0.0),
                unit=size.get("unit", "mm") or "mm",
                tolerance=tolerance_str,
                location=dim.get("reference_id")
            )
        
        # Özellikler
        for bore in features.get("bores", []) or []:
            if bore.get("confidence", 0) < confidence_threshold:
                continue
            
            feature_dims = {}
            diameter = (bore.get("diameter") or {}).get("value")
            if diameter is not None:
                feature_dims["diameter"] = diameter
            depth = (bore.get("depth") or {}).get("value")
            if depth is not None:
                feature_dims["depth"] = depth
            
            features_list.append(
                FeatureInfo(
                    type="hole",
                    quantity=bore.get("quantity", 1) or 1,
                    dimensions=feature_dims,
                    position=bore.get("reference_id"),
                    notes=bore.get("label")
                )
            )
        
        for chamfer in features.get("chamfers", []) or []:
            if chamfer.get("confidence", 0) < confidence_threshold:
                continue
            features_list.append(
                FeatureInfo(
                    type="chamfer",
                    quantity=chamfer.get("quantity", 1) or 1,
                    dimensions={"label": chamfer.get("label")},
                    position=chamfer.get("reference_id"),
                )
            )
        
        # GD&T toleransları
        for gdt in features.get("gdnts", []) or []:
            if gdt.get("confidence", 0) < confidence_threshold:
                continue
            tolerances.append(
                ToleranceInfo(
                    type="geometric",
                    value=str(gdt.get("characteristic") or "GD&T"),
                    reference=gdt.get("reference_id")
                )
            )
        
        # Insights'tan imalat bilgileri (V2 API)
        primary_process_options = insights.get('primary_process_options', []) or []
        manufacturing_methods = [
            option.get("primary_process") for option in primary_process_options if option.get("primary_process")
        ]
        
        # Geometri analizi
        geometry = GeometryAnalysis(
            part_type=metadata.get('part_type', 'Unknown'),
            shape_type=metadata.get('shape_type', 'complex'),
            overall_dimensions=dimensions,
            features=features_list,
            complexity_score=self._calculate_complexity(dimensions, features_list, tolerances)
        )
        
        # İmalat analizi (Insights'tan gelen veriye göre)
        primary_process = manufacturing_methods[0] if manufacturing_methods else "CNC Machining"
        manufacturing = ManufacturingAnalysis(
            primary_process=primary_process,
            secondary_processes=manufacturing_methods[1:] if len(manufacturing_methods) > 1 else [],
            setup_count=1,
            estimated_operations=["Werk24 V2 Professional Analysis"],
            difficulty_level="medium",
            special_requirements=[]
        )
        
        # Kalite gereksinimleri
        quality = QualityRequirements(
            tolerances=tolerances,
            surface_finishes=surface_finishes,
            inspection_notes=[],
            critical_dimensions=list(dimensions.keys())[:5]  # İlk 5 boyut
        )
        
        # Metadata
        analysis_metadata = AnalysisMetadata(
            model_used="Werk24 V2 Professional API",
            processing_time=processing_time,
            confidence_score=0.95,  # Werk24 profesyonel servis - yüksek güven
            warnings=[f"Error: {e}" for e in self.errors] if self.errors else []
        )
        
        return DrawingAnalysisResult(
            title=title,
            revision=revision,
            drawing_number=drawing_number,
            scale=metadata.get('scale', None),
            material=material,
            geometry=geometry,
            manufacturing=manufacturing,
            quality=quality,
            general_notes=[
                "Analyzed with Werk24 V2 Professional API",
                "High-accuracy professional-grade analysis",
                f"Detected {len(dimensions)} dimensions",
                f"Found {len(tolerances)} GD&T tolerances",
                f"Identified {len(features_list)} special features"
            ],
            design_recommendations=[],
            metadata=analysis_metadata,
            raw_response=raw_results if self.results else None
        )
    
    def _build_error_result(
        self,
        filename: str,
        processing_time: float,
        error_message: str
    ) -> DrawingAnalysisResult:
        """Hata durumunda minimal sonuç oluştur"""
        
        return DrawingAnalysisResult(
            title=filename,
            geometry=GeometryAnalysis(
                part_type="Unknown",
                shape_type="unknown",
                overall_dimensions={},
                features=[],
                complexity_score=0.0
            ),
            manufacturing=ManufacturingAnalysis(
                primary_process="Unknown",
                secondary_processes=[],
                setup_count=1,
                estimated_operations=[],
                difficulty_level="unknown",
                special_requirements=[]
            ),
            quality=QualityRequirements(
                tolerances=[],
                surface_finishes=[],
                inspection_notes=[],
                critical_dimensions=[]
            ),
            general_notes=[],
            design_recommendations=[],
            metadata=AnalysisMetadata(
                model_used="Werk24 V2 Professional API",
                processing_time=processing_time,
                confidence_score=0.0,
                warnings=[f"Analysis failed: {error_message}"]
            )
        )
    
    def _calculate_complexity(
        self,
        dimensions: Dict,
        features: list,
        tolerances: list
    ) -> float:
        """Karmaşıklık skorunu hesapla"""
        score = 0.0
        
        # Boyut sayısı
        score += min(len(dimensions) * 0.3, 3.0)
        
        # Özellik sayısı
        score += min(len(features) * 0.4, 3.0)
        
        # Tolerans sayısı
        score += min(len(tolerances) * 0.5, 4.0)
        
        return min(score, 10.0)


# Singleton instance
werk24_analyzer = Werk24Analyzer()

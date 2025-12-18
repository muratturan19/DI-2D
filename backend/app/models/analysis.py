"""
Data models for DI-2D Analysis
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class DimensionInfo(BaseModel):
    """Boyut bilgisi"""
    value: float
    unit: str = "mm"
    tolerance: Optional[str] = None
    location: Optional[str] = None

class FeatureInfo(BaseModel):
    """Özellik bilgisi (delik, cep, kanal, vb.)"""
    type: str  # "hole", "pocket", "slot", "groove", "fillet", "chamfer"
    quantity: int
    dimensions: Dict[str, Any] = {}
    position: Optional[str] = None
    notes: Optional[str] = None

class MaterialInfo(BaseModel):
    """Malzeme bilgisi"""
    name: str
    standard: Optional[str] = None
    density: Optional[float] = None
    hardness: Optional[str] = None

class SurfaceFinishInfo(BaseModel):
    """Yüzey işlemi bilgisi"""
    type: str  # "anodize", "paint", "coating", "plating"
    description: str
    roughness: Optional[str] = None
    color: Optional[str] = None

class ToleranceInfo(BaseModel):
    """Tolerans bilgisi"""
    type: str  # "dimensional", "geometric", "surface"
    value: str
    reference: Optional[str] = None

class GeometryAnalysis(BaseModel):
    """Geometrik analiz sonuçları"""
    part_type: str = Field(..., description="Parça tipi (flanş, somun, kapak, vb.)")
    shape_type: str = Field(..., description="Genel şekil (silindirik, kutusal, karmaşık)")
    overall_dimensions: Dict[str, DimensionInfo] = Field(default_factory=dict)
    features: List[FeatureInfo] = Field(default_factory=list)
    complexity_score: float = Field(..., ge=0, le=10, description="Karmaşıklık skoru (0-10)")

class ManufacturingAnalysis(BaseModel):
    """İmalat analizi"""
    primary_process: str = Field(..., description="Ana işleme yöntemi")
    secondary_processes: List[str] = Field(default_factory=list)
    setup_count: int = Field(..., ge=1, description="Takma sayısı")
    estimated_operations: List[str] = Field(default_factory=list)
    difficulty_level: str = Field(..., description="Zorluk seviyesi (kolay, orta, zor)")
    special_requirements: List[str] = Field(default_factory=list)

class QualityRequirements(BaseModel):
    """Kalite gereksinimleri"""
    tolerances: List[ToleranceInfo] = Field(default_factory=list)
    surface_finishes: List[SurfaceFinishInfo] = Field(default_factory=list)
    inspection_notes: List[str] = Field(default_factory=list)
    critical_dimensions: List[str] = Field(default_factory=list)

class AnalysisMetadata(BaseModel):
    """Analiz metadata"""
    model_used: str
    processing_time: float = Field(..., description="İşlem süresi (saniye)")
    confidence_score: float = Field(..., ge=0, le=1, description="Güven skoru")
    tokens_used: Optional[int] = None
    warnings: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)

class DrawingAnalysisResult(BaseModel):
    """Tam analiz sonucu"""
    # Temel bilgiler
    title: str = Field(..., description="Resim başlığı/parça numarası")
    revision: Optional[str] = None
    drawing_number: Optional[str] = None
    scale: Optional[str] = None
    
    # Malzeme ve yüzey işlemi
    material: Optional[MaterialInfo] = None
    surface_finish: Optional[SurfaceFinishInfo] = None
    
    # Analiz sonuçları
    geometry: GeometryAnalysis
    manufacturing: ManufacturingAnalysis
    quality: QualityRequirements
    
    # Ek notlar
    general_notes: List[str] = Field(default_factory=list)
    design_recommendations: List[str] = Field(default_factory=list)
    
    # Metadata
    metadata: AnalysisMetadata
    
    # Ham AI yanıtı (opsiyonel, debugging için)
    raw_response: Optional[Dict[str, Any]] = None

class AnalysisRequest(BaseModel):
    """Analiz isteği"""
    model: str = "gpt-4-vision-preview"
    max_tokens: int = 150000
    temperature: float = 0.1
    include_raw_response: bool = False
    reasoning_level: str = "high"  # "medium", "high", "xhigh"

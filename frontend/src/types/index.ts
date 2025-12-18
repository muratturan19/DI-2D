// Type definitions for DI-2D
export interface DimensionInfo {
  value: number
  unit: string
  tolerance?: string
  location?: string
}

export interface FeatureInfo {
  type: string
  quantity: number
  dimensions: Record<string, any>
  position?: string
  notes?: string
}

export interface MaterialInfo {
  name: string
  standard?: string
  density?: number
  hardness?: string
}

export interface SurfaceFinishInfo {
  type: string
  description: string
  roughness?: string
  color?: string
}

export interface ToleranceInfo {
  type: string
  value: string
  reference?: string
}

export interface GeometryAnalysis {
  part_type: string
  shape_type: string
  overall_dimensions: Record<string, DimensionInfo>
  features: FeatureInfo[]
  complexity_score: number
}

export interface ManufacturingAnalysis {
  primary_process: string
  secondary_processes: string[]
  setup_count: number
  estimated_operations: string[]
  difficulty_level: string
  special_requirements: string[]
}

export interface QualityRequirements {
  tolerances: ToleranceInfo[]
  surface_finishes: SurfaceFinishInfo[]
  inspection_notes: string[]
  critical_dimensions: string[]
}

export interface AnalysisMetadata {
  model_used: string
  processing_time: number
  confidence_score: number
  tokens_used?: number
  warnings: string[]
  timestamp: string
}

export interface DrawingAnalysisResult {
  title: string
  revision?: string
  drawing_number?: string
  scale?: string
  material?: MaterialInfo
  surface_finish?: SurfaceFinishInfo
  geometry: GeometryAnalysis
  manufacturing: ManufacturingAnalysis
  quality: QualityRequirements
  general_notes: string[]
  design_recommendations: string[]
  metadata: AnalysisMetadata
  raw_response?: Record<string, any>
}

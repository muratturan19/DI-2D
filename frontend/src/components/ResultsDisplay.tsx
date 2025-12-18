import { Package, Ruler, Wrench, CheckSquare, Clock, Brain } from 'lucide-react'
import type { DrawingAnalysisResult } from '../types'
import './ResultsDisplay.css'

interface ResultsDisplayProps {
  result: DrawingAnalysisResult
}

const ResultsDisplay = ({ result }: ResultsDisplayProps) => {
  return (
    <div className="results-container">
      <h2 className="results-title">📊 Analiz Sonuçları</h2>

      {/* Metadata Card */}
      <div className="result-card metadata-card">
        <div className="card-header">
          <Clock size={24} />
          <h3>Analiz Bilgileri</h3>
        </div>
        <div className="metadata-grid">
          <div className="metadata-item">
            <span className="label">Model:</span>
            <span className="value">{result.metadata.model_used}</span>
          </div>
          <div className="metadata-item">
            <span className="label">İşlem Süresi:</span>
            <span className="value">{result.metadata.processing_time.toFixed(2)}s</span>
          </div>
          <div className="metadata-item">
            <span className="label">Güven Skoru:</span>
            <span className="value confidence-score">
              {(result.metadata.confidence_score * 100).toFixed(0)}%
            </span>
          </div>
          {result.metadata.tokens_used && (
            <div className="metadata-item">
              <span className="label">Token Kullanımı:</span>
              <span className="value">{result.metadata.tokens_used.toLocaleString()}</span>
            </div>
          )}
        </div>
      </div>

      {/* Basic Info */}
      <div className="result-card">
        <div className="card-header">
          <Package size={24} />
          <h3>Temel Bilgiler</h3>
        </div>
        <div className="info-grid">
          <div className="info-item">
            <strong>Başlık:</strong>
            <span>{result.title}</span>
          </div>
          {result.drawing_number && (
            <div className="info-item">
              <strong>Çizim No:</strong>
              <span>{result.drawing_number}</span>
            </div>
          )}
          {result.revision && (
            <div className="info-item">
              <strong>Revizyon:</strong>
              <span>{result.revision}</span>
            </div>
          )}
          {result.scale && (
            <div className="info-item">
              <strong>Ölçek:</strong>
              <span>{result.scale}</span>
            </div>
          )}
          {result.material && (
            <div className="info-item">
              <strong>Malzeme:</strong>
              <span>{result.material.name} {result.material.standard && `(${result.material.standard})`}</span>
            </div>
          )}
        </div>
      </div>

      {/* Geometry Analysis */}
      <div className="result-card">
        <div className="card-header">
          <Ruler size={24} />
          <h3>Geometri Analizi</h3>
        </div>
        <div className="geometry-content">
          <div className="geometry-row">
            <strong>Parça Tipi:</strong>
            <span className="badge">{result.geometry.part_type}</span>
          </div>
          <div className="geometry-row">
            <strong>Şekil:</strong>
            <span className="badge">{result.geometry.shape_type}</span>
          </div>
          <div className="geometry-row">
            <strong>Karmaşıklık:</strong>
            <span className="complexity-score">
              {result.geometry.complexity_score}/10
            </span>
          </div>

          {Object.keys(result.geometry.overall_dimensions).length > 0 && (
            <div className="dimensions-section">
              <h4>Ana Boyutlar</h4>
              <div className="dimensions-grid">
                {Object.entries(result.geometry.overall_dimensions).map(([key, dim]) => (
                  <div key={key} className="dimension-item">
                    <span className="dim-label">{key}:</span>
                    <span className="dim-value">
                      {dim.value} {dim.unit}
                      {dim.tolerance && <span className="tolerance"> ({dim.tolerance})</span>}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {result.geometry.features.length > 0 && (
            <div className="features-section">
              <h4>Özellikler</h4>
              <div className="features-list">
                {result.geometry.features.map((feature, idx) => (
                  <div key={idx} className="feature-item">
                    <span className="feature-type">{feature.type}</span>
                    <span className="feature-quantity">×{feature.quantity}</span>
                    {feature.notes && <span className="feature-notes">{feature.notes}</span>}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Manufacturing Analysis */}
      <div className="result-card">
        <div className="card-header">
          <Wrench size={24} />
          <h3>İmalat Analizi</h3>
        </div>
        <div className="manufacturing-content">
          <div className="manufacturing-row">
            <strong>Ana İşlem:</strong>
            <span className="badge badge-primary">{result.manufacturing.primary_process}</span>
          </div>
          <div className="manufacturing-row">
            <strong>Zorluk Seviyesi:</strong>
            <span className={`badge badge-${result.manufacturing.difficulty_level === 'kolay' ? 'success' : result.manufacturing.difficulty_level === 'orta' ? 'warning' : 'danger'}`}>
              {result.manufacturing.difficulty_level}
            </span>
          </div>
          <div className="manufacturing-row">
            <strong>Takma Sayısı:</strong>
            <span>{result.manufacturing.setup_count}</span>
          </div>

          {result.manufacturing.secondary_processes.length > 0 && (
            <div className="processes-section">
              <h4>İkincil İşlemler</h4>
              <div className="tags-list">
                {result.manufacturing.secondary_processes.map((process, idx) => (
                  <span key={idx} className="tag">{process}</span>
                ))}
              </div>
            </div>
          )}

          {result.manufacturing.estimated_operations.length > 0 && (
            <div className="operations-section">
              <h4>Tahmini Operasyonlar</h4>
              <ol className="operations-list">
                {result.manufacturing.estimated_operations.map((op, idx) => (
                  <li key={idx}>{op}</li>
                ))}
              </ol>
            </div>
          )}

          {result.manufacturing.special_requirements.length > 0 && (
            <div className="special-req-section">
              <h4>Özel Gereksinimler</h4>
              <ul className="requirements-list">
                {result.manufacturing.special_requirements.map((req, idx) => (
                  <li key={idx}>{req}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {/* Quality Requirements */}
      <div className="result-card">
        <div className="card-header">
          <CheckSquare size={24} />
          <h3>Kalite Gereksinimleri</h3>
        </div>
        <div className="quality-content">
          {result.quality.tolerances.length > 0 && (
            <div className="tolerances-section">
              <h4>Toleranslar</h4>
              <div className="tolerances-list">
                {result.quality.tolerances.map((tol, idx) => (
                  <div key={idx} className="tolerance-item">
                    <span className="tol-type">{tol.type}:</span>
                    <span className="tol-value">{tol.value}</span>
                    {tol.reference && <span className="tol-ref">({tol.reference})</span>}
                  </div>
                ))}
              </div>
            </div>
          )}

          {result.quality.surface_finishes.length > 0 && (
            <div className="surface-section">
              <h4>Yüzey İşlemleri</h4>
              <div className="surface-list">
                {result.quality.surface_finishes.map((sf, idx) => (
                  <div key={idx} className="surface-item">
                    <strong>{sf.type}:</strong> {sf.description}
                    {sf.roughness && <span> (Ra: {sf.roughness})</span>}
                  </div>
                ))}
              </div>
            </div>
          )}

          {result.quality.critical_dimensions.length > 0 && (
            <div className="critical-dims-section">
              <h4>Kritik Boyutlar</h4>
              <div className="tags-list">
                {result.quality.critical_dimensions.map((dim, idx) => (
                  <span key={idx} className="tag tag-critical">{dim}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Notes and Recommendations */}
      {(result.general_notes.length > 0 || result.design_recommendations.length > 0) && (
        <div className="result-card">
          <div className="card-header">
            <Brain size={24} />
            <h3>Notlar ve Öneriler</h3>
          </div>
          <div className="notes-content">
            {result.general_notes.length > 0 && (
              <div className="notes-section">
                <h4>Genel Notlar</h4>
                <ul>
                  {result.general_notes.map((note, idx) => (
                    <li key={idx}>{note}</li>
                  ))}
                </ul>
              </div>
            )}

            {result.design_recommendations.length > 0 && (
              <div className="recommendations-section">
                <h4>Tasarım Önerileri</h4>
                <ul>
                  {result.design_recommendations.map((rec, idx) => (
                    <li key={idx}>{rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Warnings */}
      {result.metadata.warnings.length > 0 && (
        <div className="result-card warnings-card">
          <div className="card-header">
            <h3>⚠️ Uyarılar</h3>
          </div>
          <ul className="warnings-list">
            {result.metadata.warnings.map((warning, idx) => (
              <li key={idx}>{warning}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default ResultsDisplay

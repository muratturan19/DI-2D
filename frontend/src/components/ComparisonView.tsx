import { useState } from 'react'
import { Upload, Loader2, CheckCircle, AlertCircle, GitCompare, FileText } from 'lucide-react'
import { useMutation } from '@tanstack/react-query'
import axios from 'axios'
import './DrawingAnalyzer.css'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

interface ComparisonResult {
  timestamp: string
  file_info: any
  model1: {
    name: string
    provider: string
    processing_time: number
    confidence: number
    analysis: any
    raw_response: string
  }
  model2: {
    name: string
    provider: string
    processing_time: number
    confidence: number
    analysis: any
    raw_response: string
  }
  comparison_notes: {
    time_difference: number
    confidence_difference: number
    faster_model: string
    higher_confidence: string
  }
}

const ComparisonView = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string>('')
  const [model1, setModel1] = useState('werk24-professional')
  const [model2, setModel2] = useState('gpt-5.2')
  const [reasoningLevel, setReasoningLevel] = useState('high')

  const comparisonMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('model1', model1)
      formData.append('model2', model2)
      formData.append('reasoning_level', reasoningLevel)

      const response = await axios.post<ComparisonResult>(
        `${API_BASE_URL}/api/analysis/compare`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      )
      return response.data
    },
  })

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      
      const reader = new FileReader()
      reader.onload = (e) => {
        setPreviewUrl(e.target?.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleCompare = () => {
    if (selectedFile) {
      comparisonMutation.mutate(selectedFile)
    }
  }

  const handleReset = () => {
    setSelectedFile(null)
    setPreviewUrl('')
    comparisonMutation.reset()
  }

  const getModelDisplayName = (modelId: string) => {
    const names: Record<string, string> = {
      'werk24-professional': '🏆 Werk24 Professional',
      'gpt-5.2': '⭐ GPT-5.2',
      'gpt-5.2-chat': 'GPT-5.2 Chat',
      'gpt-4-vision-preview': 'GPT-4 Vision',
      'claude-3-5-sonnet-20241022': 'Claude 3.5 Sonnet'
    }
    return names[modelId] || modelId
  }

  return (
    <div className="analyzer-container">
      {/* Upload Section */}
      <div className="upload-section">
        <div className="upload-card">
          <div className="upload-header">
            <GitCompare size={28} />
            <h2>Model Karşılaştırma</h2>
          </div>

          <div className="upload-area">
            {!selectedFile ? (
              <label htmlFor="file-input" className="upload-label">
                <Upload size={48} />
                <p className="upload-text">
                  Teknik resim yükle
                </p>
                <p className="upload-hint">
                  PDF, PNG, JPG (max 20MB)
                </p>
                <input
                  id="file-input"
                  type="file"
                  accept=".pdf,.png,.jpg,.jpeg"
                  onChange={handleFileSelect}
                  className="file-input"
                />
              </label>
            ) : (
              <div className="file-preview">
                {previewUrl && (
                  <img src={previewUrl} alt="Preview" className="preview-image" />
                )}
                <div className="file-info">
                  <p className="file-name">{selectedFile.name}</p>
                  <p className="file-size">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Model Selection */}
          <div className="settings-section">
            <div className="settings-panel" style={{ display: 'block' }}>
              <div className="setting-group">
                <label>Model 1</label>
                <select value={model1} onChange={(e) => setModel1(e.target.value)}>
                  <option value="werk24-professional">🏆 Werk24 Professional</option>
                  <option value="gpt-5.2">⭐ GPT-5.2</option>
                  <option value="gpt-5.2-chat">GPT-5.2 Chat</option>
                  <option value="gpt-4-vision-preview">GPT-4 Vision</option>
                  <option value="claude-3-5-sonnet-20241022">Claude 3.5 Sonnet</option>
                </select>
              </div>

              <div className="setting-group">
                <label>Model 2</label>
                <select value={model2} onChange={(e) => setModel2(e.target.value)}>
                  <option value="gpt-5.2">⭐ GPT-5.2</option>
                  <option value="werk24-professional">🏆 Werk24 Professional</option>
                  <option value="gpt-5.2-chat">GPT-5.2 Chat</option>
                  <option value="gpt-4-vision-preview">GPT-4 Vision</option>
                  <option value="claude-3-5-sonnet-20241022">Claude 3.5 Sonnet</option>
                </select>
              </div>

              <div className="setting-group">
                <label>Analiz Seviyesi</label>
                <select 
                  value={reasoningLevel} 
                  onChange={(e) => setReasoningLevel(e.target.value)}
                >
                  <option value="low">Basit</option>
                  <option value="medium">Hızlı</option>
                  <option value="high">Detaylı ⭐</option>
                  <option value="xhigh">Çok Detaylı</option>
                </select>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="action-buttons">
            {selectedFile && !comparisonMutation.isPending && !comparisonMutation.isSuccess && (
              <>
                <button onClick={handleReset} className="btn btn-secondary">
                  Temizle
                </button>
                <button onClick={handleCompare} className="btn btn-primary">
                  Karşılaştır
                </button>
              </>
            )}
            
            {comparisonMutation.isSuccess && (
              <button onClick={handleReset} className="btn btn-primary">
                Yeni Karşılaştırma
              </button>
            )}
          </div>

          {/* Status Messages */}
          {comparisonMutation.isPending && (
            <div className="status-message status-loading">
              <Loader2 className="spinning" size={24} />
              <span>Her iki modelle analiz ediliyor...</span>
            </div>
          )}

          {comparisonMutation.isSuccess && (
            <div className="status-message status-success">
              <CheckCircle size={24} />
              <span>Karşılaştırma tamamlandı!</span>
            </div>
          )}

          {comparisonMutation.isError && (
            <div className="status-message status-error">
              <AlertCircle size={24} />
              <span>
                Hata: {comparisonMutation.error instanceof Error ? comparisonMutation.error.message : 'Bilinmeyen hata'}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Comparison Results */}
      {comparisonMutation.isSuccess && comparisonMutation.data && (
        <div className="comparison-results">
          <div className="comparison-summary">
            <h3>Karşılaştırma Özeti</h3>
            <div className="summary-grid">
              <div className="summary-card">
                <span className="summary-label">Hız Farkı</span>
                <span className="summary-value">
                  {comparisonMutation.data.comparison_notes.time_difference.toFixed(2)}s
                </span>
                <span className="summary-winner">
                  🏃 {getModelDisplayName(comparisonMutation.data.comparison_notes.faster_model)}
                </span>
              </div>
              <div className="summary-card">
                <span className="summary-label">Güven Farkı</span>
                <span className="summary-value">
                  {(comparisonMutation.data.comparison_notes.confidence_difference * 100).toFixed(1)}%
                </span>
                <span className="summary-winner">
                  💪 {getModelDisplayName(comparisonMutation.data.comparison_notes.higher_confidence)}
                </span>
              </div>
            </div>
          </div>

          <div className="comparison-grid">
            {/* Model 1 Results */}
            <div className="model-result">
              <div className="model-header">
                <h3>{getModelDisplayName(comparisonMutation.data.model1.name)}</h3>
                <span className="model-provider">{comparisonMutation.data.model1.provider}</span>
              </div>
              
              <div className="model-metrics">
                <div className="metric">
                  <span className="metric-label">İşlem Süresi</span>
                  <span className="metric-value">
                    {comparisonMutation.data.model1.processing_time.toFixed(2)}s
                  </span>
                </div>
                <div className="metric">
                  <span className="metric-label">Güven Skoru</span>
                  <span className="metric-value">
                    {(comparisonMutation.data.model1.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>

              <div className="model-analysis">
                <h4>Analiz Sonucu</h4>
                <div className="analysis-content">
                  {comparisonMutation.data.model1.analysis && Object.keys(comparisonMutation.data.model1.analysis).length > 0 ? (
                    <pre>{JSON.stringify(comparisonMutation.data.model1.analysis, null, 2)}</pre>
                  ) : (
                    <p className="raw-response">{comparisonMutation.data.model1.raw_response}</p>
                  )}
                </div>
              </div>
            </div>

            {/* Model 2 Results */}
            <div className="model-result">
              <div className="model-header">
                <h3>{getModelDisplayName(comparisonMutation.data.model2.name)}</h3>
                <span className="model-provider">{comparisonMutation.data.model2.provider}</span>
              </div>
              
              <div className="model-metrics">
                <div className="metric">
                  <span className="metric-label">İşlem Süresi</span>
                  <span className="metric-value">
                    {comparisonMutation.data.model2.processing_time.toFixed(2)}s
                  </span>
                </div>
                <div className="metric">
                  <span className="metric-label">Güven Skoru</span>
                  <span className="metric-value">
                    {(comparisonMutation.data.model2.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>

              <div className="model-analysis">
                <h4>Analiz Sonucu</h4>
                <div className="analysis-content">
                  {comparisonMutation.data.model2.analysis && Object.keys(comparisonMutation.data.model2.analysis).length > 0 ? (
                    <pre>{JSON.stringify(comparisonMutation.data.model2.analysis, null, 2)}</pre>
                  ) : (
                    <p className="raw-response">{comparisonMutation.data.model2.raw_response}</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ComparisonView

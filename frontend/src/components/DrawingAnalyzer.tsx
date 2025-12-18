import { useState } from 'react'
import { Upload, Loader2, CheckCircle, AlertCircle, FileText, Settings } from 'lucide-react'
import { useMutation } from '@tanstack/react-query'
import axios from 'axios'
import './DrawingAnalyzer.css'
import type { DrawingAnalysisResult } from '../types'
import ResultsDisplay from './ResultsDisplay'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

const DrawingAnalyzer = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string>('')
  const [model, setModel] = useState('gpt-5.2')
  const [reasoningLevel, setReasoningLevel] = useState('high')
  const [enhanceMode, setEnhanceMode] = useState('balanced')
  const [showSettings, setShowSettings] = useState(false)

  const analysisMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('model', model)
      formData.append('reasoning_level', reasoningLevel)
      formData.append('enhance_mode', enhanceMode)
      formData.append('max_tokens', '150000')

      const response = await axios.post<DrawingAnalysisResult>(
        `${API_BASE_URL}/api/analysis/analyze`,
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
      
      // Önizleme URL'i oluştur
      const reader = new FileReader()
      reader.onload = (e) => {
        setPreviewUrl(e.target?.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleAnalyze = () => {
    if (selectedFile) {
      analysisMutation.mutate(selectedFile)
    }
  }

  const handleReset = () => {
    setSelectedFile(null)
    setPreviewUrl('')
    analysisMutation.reset()
  }

  return (
    <div className="analyzer-container">
      {/* Upload Section */}
      <div className="upload-section">
        <div className="upload-card">
          <div className="upload-header">
            <FileText size={28} />
            <h2>Teknik Resim Yükle</h2>
          </div>

          <div className="upload-area">
            {!selectedFile ? (
              <label htmlFor="file-input" className="upload-label">
                <Upload size={48} />
                <p className="upload-text">
                  Dosya seç veya sürükle bırak
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

          {/* Settings */}
          <div className="settings-section">
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="settings-toggle"
            >
              <Settings size={20} />
              Ayarlar
            </button>

            {showSettings && (
              <div className="settings-panel">
                <div className="setting-group">
                  <label>AI Modeli</label>
                  <select value={model} onChange={(e) => setModel(e.target.value)}>
                    <option value="werk24-professional">🏆 Werk24 Professional</option>
                    <option value="gpt-5.2">⭐ GPT-5.2 (Yeni!) - Önerilen</option>
                    <option value="gpt-5.2-chat">GPT-5.2 Chat</option>
                    <option value="gpt-4-vision-preview">GPT-4 Vision (Legacy)</option>
                    <option value="claude-3-5-sonnet-20241022">Claude 3.5 Sonnet</option>
                  </select>
                  {model === 'werk24-professional' && (
                    <p style={{ fontSize: '0.8rem', color: '#10b981', marginTop: '0.25rem' }}>
                      ✅ Profesyonel servis - En yüksek doğruluk
                    </p>
                  )}
                  {model === 'gpt-5.2' && (
                    <p style={{ fontSize: '0.8rem', color: '#fbbf24', marginTop: '0.25rem' }}>
                      🚀 Aralık 2025 - xHigh reasoning, Responses API
                    </p>
                  )}
                </div>

                <div className="setting-group">
                  <label>Analiz Seviyesi</label>
                  <select 
                    value={reasoningLevel} 
                    onChange={(e) => setReasoningLevel(e.target.value)}
                    disabled={model === 'werk24-professional'}
                  >
                    <option value="low">Basit (~30sn)</option>
                    <option value="medium">Hızlı (~1-2 dk)</option>
                    <option value="high">Detaylı (~2-3 dk) ⭐</option>
                    <option value="xhigh">Çok Detaylı (~5+ dk) - GPT-5.2</option>
                  </select>
                  {model === 'werk24-professional' && (
                    <p style={{ fontSize: '0.8rem', color: '#718096', marginTop: '0.25rem' }}>
                      Werk24 otomatik optimize edilir
                    </p>
                  )}
                  {reasoningLevel === 'xhigh' && model.startsWith('gpt-5') && (
                    <p style={{ fontSize: '0.8rem', color: '#fbbf24', marginTop: '0.25rem' }}>
                      ⚡ Chain-of-thought korunuyor
                    </p>
                  )}
                </div>

                <div className="setting-group">
                  <label>Görüntü İyileştirme</label>
                  <select 
                    value={enhanceMode} 
                    onChange={(e) => setEnhanceMode(e.target.value)}
                    disabled={model === 'werk24-professional'}
                  >
                    <option value="fast">Hızlı</option>
                    <option value="balanced">Dengeli ⭐</option>
                    <option value="aggressive">Agresif</option>
                  </select>
                  {model === 'werk24-professional' && (
                    <p style={{ fontSize: '0.8rem', color: '#718096', marginTop: '0.25rem' }}>
                      Werk24 otomatik işler
                    </p>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="action-buttons">
            {selectedFile && !analysisMutation.isPending && !analysisMutation.isSuccess && (
              <>
                <button onClick={handleReset} className="btn btn-secondary">
                  Temizle
                </button>
                <button onClick={handleAnalyze} className="btn btn-primary">
                  Analiz Et
                </button>
              </>
            )}
            
            {analysisMutation.isSuccess && (
              <button onClick={handleReset} className="btn btn-primary">
                Yeni Analiz
              </button>
            )}
          </div>

          {/* Status Messages */}
          {analysisMutation.isPending && (
            <div className="status-message status-loading">
              <Loader2 className="spinning" size={24} />
              <span>Analiz ediliyor... Bu birkaç dakika sürebilir</span>
            </div>
          )}

          {analysisMutation.isSuccess && (
            <div className="status-message status-success">
              <CheckCircle size={24} />
              <span>Analiz tamamlandı!</span>
            </div>
          )}

          {analysisMutation.isError && (
            <div className="status-message status-error">
              <AlertCircle size={24} />
              <span>
                Hata: {analysisMutation.error instanceof Error ? analysisMutation.error.message : 'Bilinmeyen hata'}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Results Section */}
      {analysisMutation.isSuccess && analysisMutation.data && (
        <ResultsDisplay result={analysisMutation.data} />
      )}
    </div>
  )
}

export default DrawingAnalyzer

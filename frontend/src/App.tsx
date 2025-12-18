import { useState } from 'react'
import DrawingAnalyzer from './components/DrawingAnalyzer'
import ComparisonView from './components/ComparisonView'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState<'analyze' | 'compare'>('analyze')

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎯 DI-2D</h1>
        <p>2D Drawing Intelligence System</p>
        
        <div className="tabs">
          <button 
            className={activeTab === 'analyze' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('analyze')}
          >
            📊 Tekil Analiz
          </button>
          <button 
            className={activeTab === 'compare' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('compare')}
          >
            🔍 Model Karşılaştırma
          </button>
        </div>
      </header>
      <main className="app-main">
        {activeTab === 'analyze' && <DrawingAnalyzer />}
        {activeTab === 'compare' && <ComparisonView />}
      </main>
    </div>
  )
}

export default App

# 🎯 DI-2D Kurulum ve Çalıştırma Kılavuzu

## Hızlı Başlangıç

### 1. Gereksinimler
- Python 3.10-3.13 (CPython)
- Node.js 18+
- **Werk24 API (Önerilen)** - 100 deneme lisansı
- OpenAI API Key (opsiyonel)
- Anthropic API Key (opsiyonel)

### 2. Backend Kurulumu

```bash
cd backend

# Virtual environment oluştur (önerilen)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# pip'i güncelle
python -m pip install --upgrade pip

# Bağımlılıkları yükle
pip install -r requirements.txt

# Werk24'ü initialize et (trial lisans alır)
werk24 init

# Werk24 bağlantısını test et
werk24 health-check

# .env dosyası oluştur (backend dizininde)
cp ../.env.example .env

# .env dosyasını düzenle
notepad .env  # Windows
# nano .env   # Linux/Mac
```

**backend/.env** dosyası içeriği (ZORUNLU):
```env
# GPT-5.2 için ZORUNLU
OPENAI_API_KEY=sk-your-actual-key-here

# OPSİYONEL: Diğer modeller
# ANTHROPIC_API_KEY=sk-ant-your-key-here
# GEMINI_API_KEY=your-key-here
```

**Önemli:** `.env` dosyası `backend/` dizininde olmalı!

**⚠️ Önemli Werk24 Notları:**
- `werk24 init` komutu otomatik olarak trial lisans alır (100 deneme)
- Corporate firewall varsa WSS (port 443) bağlantısına izin verin
- Endpoint: `wss://ws-api.w24.co`

### 3. Frontend Kurulumu

```bash
cd frontend

# Bağımlılıkları yükle
npm install

# .env dosyası oluştur
cp .env.example .env
```

### 4. Uygulamayı Çalıştır

#### Otomatik Başlatma (Önerilen)

**Windows:**
```powershell
.\start.ps1
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

#### Manuel Başlatma

**Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Erişim Adresleri

- 🎨 **Frontend UI**: http://localhost:3001
- 🔧 **Backend API**: http://localhost:8001
- 📚 **API Docs**: http://localhost:8001/docs

---

## Kullanım

1. Frontend'e giriş yapın (http://localhost:3001)
2. "Teknik Resim Yükle" bölümünden PDF/PNG/JPG dosyanızı seçin
3. **AI Modeli Seçin:**
   - 🏆 **Werk24 Professional** (Önerilen) - En yüksek doğruluk
   - GPT-4 Vision - Detaylı analiz
   - Claude 3.5 Sonnet - Hızlı analiz
4. "Analiz Et" butonuna tıklayın
5. Sonuçları inceleyin

### Werk24 vs Diğer Modeller

| Özellik | Werk24 Professional | GPT-4 Vision | Claude 3.5 |
|---------|-------------------|--------------|------------|
| Boyut Okuma | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| GD&T Tolerans | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Malzeme Tanıma | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Hız | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Lisans | 100 deneme | API Key | API Key |

---

## API Kullanımı

### Endpoint: POST /api/v1/analyze

**Werk24 ile analiz:**
```bash
curl -X POST http://localhost:8001/api/v1/analyze \
  -F "file=@drawing.pdf" \
  -F "model=werk24-professional"
```

**GPT-4 Vision ile analiz:**

```bash
curl -X POST http://localhost:8001/api/v1/analyze \
  -F "file=@drawing.pdf" \
  -F "model=gpt-4-vision-preview" \
  -F "reasoning_level=high" \
  -F "enhance_mode=balanced"
```

### Python İstemci Örneği

**Werk24 ile:**
```python
import requests

with open("drawing.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8001/api/v1/analyze",
        files={"file": f},
        data={
            "model": "werk24-professional"
        }
    )

result = response.json()
print(f"Parça: {result['title']}")
print(f"Malzeme: {result['material']['name']}")
print(f"Boyut sayısı: {len(result['geometry']['overall_dimensions'])}")
print(f"GD&T sayısı: {len(result['quality']['tolerances'])}")
```

**GPT-4 Vision ile:**
```python
import requests

with open("drawing.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8001/api/v1/analyze",
        files={"file": f},
        data={
            "model": "gpt-4-vision-preview",
            "reasoning_level": "high",
            "enhance_mode": "balanced"
        }
    )

result = response.json()
print(result["title"])
print(result["geometry"]["part_type"])
```

---

## MQ_V3 Entegrasyon Planı

### Adım 1: Backend Servisleri Kopyala
```bash
# DI-2D servislerini MQ_V3'e kopyala
cp backend/app/services/preprocessor.py ../MQ_v3/backend/app/services/
cp backend/app/services/analyzer.py ../MQ_v3/backend/app/services/
cp backend/app/services/prompts.py ../MQ_v3/backend/app/services/
cp backend/app/services/werk24_analyzer.py ../MQ_v3/backend/app/services/
```

### Adım 2: Model Tanımlarını Ekle
```bash
# Model tanımlarını kopyala
cp backend/app/models/analysis.py ../MQ_v3/backend/app/models/drawing_analysis.py
```

### Adım 3: API Route Entegrasyonu
`MQ_V3/backend/app/api/routes/ai_analysis.py` dosyasını güncelleyin:

```python
from app.services.analyzer import DrawingAnalyzer
from app.services.werk24_analyzer import Werk24Analyzer
from app.models.drawing_analysis import DrawingAnalysisResult

analyzer = DrawingAnalyzer()
werk24 = Werk24Analyzer()

@router.post("/analyze-drawing-advanced")
async def analyze_drawing_advanced(
    file: UploadFile = File(...),
    model: str = Form("werk24-professional"),  # Varsayılan Werk24
    reasoning_level: str = Form("high"),
    enhance_mode: str = Form("balanced")
):
    file_bytes = await file.read()
    
    # Model seçimine göre analiz
    if model == "werk24-professional":
        result = await werk24.analyze(
            file_bytes=file_bytes,
            filename=file.filename
        )
    else:
        result = await analyzer.analyze(
            file_bytes=file_bytes,
            filename=file.filename,
            model=model,
            reasoning_level=reasoning_level,
            enhance_mode=enhance_mode
        )
    return result
```

### Adım 4: Frontend Entegrasyonu
`MQ_V3/frontend/src/pages/AIGeometryAnalyzerPage.tsx` içinde yeni endpoint'i kullanın:

```typescript
const response = await axios.post(
  '/api/ai-analysis/analyze-drawing-advanced',
  formData,
  { headers: { 'Content-Type': 'multipart/form-data' } }
)
```

### Adım 5: Bağımlılık Güncellemesi
`MQ_V3/backend/requirements.txt` dosyasına ekleyin:
```
opencv-python>=4.10.0
pdf2image>=1.17.0
pytesseract>=0.3.10
werk24>=2.3.0
```

### Adım 6: Werk24 Kurulumu (MQ_V3'te)
```bash
cd MQ_v3/backend
pip install werk24
werk24 init  # Trial lisans al
werk24 health-check  # Test et
pytesseract>=0.3.10
```

---

## Sorun Giderme

### Werk24 Sorunları

**Health Check Başarısız:**
```bash
# 1. Python versiyonunu kontrol et
python --version  # 3.10-3.13 olmalı

# 2. pip versiyonunu kontrol et
python -m pip --version

# 3. Werk24'ü yeniden initialize et
werk24 init

# 4. Test et
werk24 health-check
```

**WSS Bağlantı Hatası:**
- Corporate firewall WSS (WebSocket Secure) bağlantılarını engelliyor olabilir
- Port 443'ü açın
- `wss://ws-api.w24.co` adresine izin verin

**Trial Lisans Bitti:**
- 100 deneme lisansı bitti
- Werk24'ten ücretli lisans alın veya diğer modelleri kullanın

### Backend Başlamıyor
- `.env` dosyasının `backend/` dizininde olduğundan emin olun (backend/.env)
- API keylerinin geçerli olduğunu kontrol edin
- Port 8001'in kullanılabilir olduğunu kontrol edin

### Frontend Başlamıyor
- `npm install` komutunu çalıştırdığınızdan emin olun
- Port 3001'in kullanılabilir olduğunu kontrol edin

### Analiz Çalışmıyor
- API keylerinin doğru olduğundan emin olun
- Dosya boyutunun 20MB'ın altında olduğunu kontrol edin
- Backend loglarını kontrol edin

### CORS Hataları
- Frontend'in backend'i doğru adres üzerinden çağırdığından emin olun
- `vite.config.ts` içindeki proxy ayarlarını kontrol edin

---

## Geliştirme

### Backend Test
```bash
cd backend
pytest tests/
```

### Frontend Build
```bash
cd frontend
npm run build
```

### Production Deployment
- Backend: `uvicorn main:app --host 0.0.0.0 --port 8001`
- Frontend: `npm run build` sonrasında `dist/` klasörünü serve edin

---

## Özellikler

✅ Multi-model AI desteği (GPT-4 Vision, Claude 3.5)  
✅ Gelişmiş görüntü ön işleme (CLAHE, noise reduction)  
✅ 3 seviyeli reasoning (medium/high/xhigh)  
✅ Yapılandırılmış JSON çıktısı  
✅ Türkçe dilbilgisi düzeltmeleri  
✅ Detaylı boyut okuma (değer + birim + tolerans)  
✅ Özellik tanıma (delik, cep, kanal, vb.)  
✅ İmalat analizi ve öneri sistemi  
✅ Kalite gereksinimi tespiti  
✅ Modüler mimari (MQ_V3 entegrasyonu için hazır)

---

## Lisans

Bu proje özel kullanım içindir.

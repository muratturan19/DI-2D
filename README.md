# 🎯 DI-2D - 2D Drawing Intelligence

**MQ_V3 için geliştirilmiş standalone 2D teknik resim analiz sistemi**

## 🎯 Hedef

Müşteri testlerinde MQ_V3'ün 2D teknik resim okuma performansının yetersiz olduğu tespit edildi. DI-2D, bu sorunu çözmek için özel olarak tasarlanmış, odaklanmış bir çözümdür.

## ✨ Özellikler

- 🏆 **Werk24 Professional API**: Endüstri standardı, en yüksek doğruluk - 100 deneme lisansı
- ⭐ **GPT-5.2 Support**: OpenAI'ın en yeni modeli (Aralık 2025) - xHigh reasoning, Responses API
- 🤖 **Multi-Model AI**: GPT-5.2, GPT-5.2-Chat, GPT-4 Vision (legacy), Claude 3.5 Sonnet
- 🔍 **Model Karşılaştırma**: Aynı resmi iki modelle analiz et, sonuçları yan yana gör
- 📐 **Gelişmiş Görüntü İşleme**: CLAHE, noise reduction, adaptive thresholding
- 🎯 **Özelleştirilmiş Promptlar**: 2D teknik resim okuma için optimize edilmiş
- 📊 **Yapılandırılmış Çıktı**: JSON formatında detaylı analiz sonuçları
- 🔧 **Modüler Mimari**: MQ_V3'e kolayca entegre edilebilir tasarım
- 🌐 **Modern UI**: React + TypeScript ile kullanıcı dostu arayüz
- 🇹🇷 **Türkçe Desteği**: Tam Türkçe UI ve dilbilgisi düzeltmeleri

## 📁 Proje Yapısı

```
DI-2D/
├── backend/                      # Python FastAPI backend
│   ├── main.py                  # Ana uygulama (Port 8001)
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── analysis.py  # POST /analyze endpoint
│   │   ├── core/
│   │   │   ├── config.py        # Pydantic Settings
│   │   │   └── exceptions.py    # Custom exceptions
│   │   ├── models/
│   │   │   └── analysis.py      # Pydantic data models
│   │   └── services/
│   │       ├── preprocessor.py  # Görüntü ön işleme (OpenCV)
│   │       ├── analyzer.py      # Multi-model AI analyzer
│   │       ├── werk24_analyzer.py  # Werk24 Professional API
│   │       └── prompts.py       # Optimize edilmiş promptlar
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                     # React TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── DrawingAnalyzer.tsx      # Ana analiz bileşeni
│   │   │   └── ResultsDisplay.tsx       # Sonuç görüntüleme
│   │   ├── types/
│   │   │   └── index.ts                 # TypeScript tipleri
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts          # Vite yapılandırması (Port 3001)
│   └── .env.example
│
├── README.md                    # Bu dosya
├── QUICKSTART.md                # ⭐ Hızlı başlangıç kılavuzu
├── SETUP.md                     # Detaylı kurulum kılavuzu
├── GPT52_UPGRADE.md             # GPT-5.2 upgrade raporu
├── WERK24_INTEGRATION.md        # Werk24 entegrasyon dokümantasyonu
├── start.sh                     # Linux/Mac başlatma scripti
└── start.ps1                    # Windows başlatma scripti
```

## 🚀 Hızlı Başlangıç

**⚡ 5 dakikada başla:** [QUICKSTART.md](QUICKSTART.md) - Adım adım kurulum

### Gereksinimler
- Python 3.10-3.13 (CPython)
- Node.js 18+
- **OpenAI SDK >= 1.99.0** (GPT-5.2 için zorunlu)
- **OpenAI API Key** (GPT-5.2 için ZORUNLU)
- **Werk24 API** - 100 deneme lisansı (önerilen)
- OpenAI API Key (GPT-5.2/GPT-4 için)
- Anthropic API Key (opsiyonel)

### 1. Backend Kurulumu
```bash
cd backend

# pip'i güncelle
python -m pip install --upgrade pip

# Bağımlılıkları yükle (OpenAI SDK >= 1.99.0 dahil)
pip install -r requirements.txt

# Werk24'ü initialize et (trial lisans alır)
werk24 init

# Bağlantıyı test et
werk24 health-check

# .env dosyası oluştur (kök dizindeki .env.example'dan)
# Windows:
Copy-Item ..\\.env.example .env
# Linux/Mac:
# cp ../.env.example .env

# .env dosyasını düzenle ve OpenAI API keyini ekle
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

**Önemli:** 
- ✅ `.env` dosyası `backend/` dizininde olmalı (backend/.env)
- ✅ OpenAI API key ZORUNLU (GPT-5.2 için)
- ✅ Werk24 otomatik configure edilir (`werk24 init`)
- ⚠️ Anthropic/Gemini opsiyonel (sadece o modelleri kullanacaksanız)

### 2. Frontend Kurulumu
```bash
cd frontend
npm install
cp .env.example .env
```

### 3. Çalıştırma

**Otomatik (Önerilen):**
```bash
# Linux/Mac
chmod +x start.sh
./start.sh

# Windows PowerShell
.\start.ps1
```

**Manuel:**
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 4. Erişim
- 🎨 **Frontend UI**: http://localhost:3001
- 🔧 **Backend API**: http://localhost:8001
- 📚 **API Docs**: http://localhost:8001/docs

## 💡 Kullanım

### 📊 Tekil Analiz Modu
1. Frontend'e giriş yapın (http://localhost:3001)
2. "Tekil Analiz" sekmesinde "Teknik Resim Yükle" bölümünden PDF/PNG/JPG dosyanızı seçin
3. **AI Modeli** seçin:
   - ⭐ **GPT-5.2** (Önerilen - Aralık 2025): xHigh reasoning, chain-of-thought
   - 🏆 **Werk24 Professional**: En yüksek doğruluk (100 deneme)
   - **GPT-4 Vision**: Legacy destek
   - **Claude 3.5 Sonnet**: Hızlı alternatif
4. **Analiz Seviyesi** seçin (GPT-5.2 için):
   - **low**: Basit (~30sn)
   - **medium**: Hızlı (~1-2 dk)
   - **high**: Detaylı (~2-3 dk) ⭐
   - **xhigh**: Çok Detaylı (~5+ dk) - Chain-of-thought korunur
5. "Analiz Et" butonuna tıklayın
6. Detaylı sonuçları inceleyin

### 🔍 Model Karşılaştırma Modu
1. "Model Karşılaştırma" sekmesine geçin
2. Aynı teknik resmi yükleyin
3. **Model 1** ve **Model 2** seçin (örn: Werk24 vs GPT-5.2)
4. "Karşılaştır" butonuna tıklayın
5. Yan yana sonuçları inceleyin:
   - İşlem süresi karşılaştırması
   - Güven skoru farkı
   - Hızlı ve güvenilir model önerileri
   - Her iki modelin detaylı analiz sonuçları

**🎯 Örnek Karşılaştırma:** Werk24 Professional (yüksek doğruluk) vs GPT-5.2 (derin reasoning)

## 📊 Analiz Çıktısı

- **Temel Bilgiler**: Parça adı, çizim no, malzeme
- **Geometri**: Tip, şekil, boyutlar, özellikler, karmaşıklık
- **İmalat**: İşlem yöntemleri, operasyonlar, zorluk seviyesi
- **Kalite**: Toleranslar, yüzey işlemleri, kritik boyutlar

## 🔗 MQ_V3 Entegrasyon Planı

Detaylı entegrasyon adımları için [SETUP.md](SETUP.md) dosyasına bakın.

**Özet:**
1. Backend servislerini kopyala (`preprocessor.py`, `analyzer.py`, `prompts.py`)
2. Model tanımlarını ekle (`analysis.py`)
3. API endpoint oluştur (`/analyze-drawing-advanced`)
4. Frontend'de yeni endpoint'i kullan
5. Bağımlılıkları güncelle (`opencv-python`, `pdf2image`)

## 🛠️ Teknoloji Stack

**Backend**: 
- FastAPI 0.115.0
- OpenAI SDK >= 1.99.0 (GPT-5.2 Responses API)
- Werk24 SDK 2.3.0+
- Anthropic SDK
- OpenCV 4.10
- pdf2image
- Pydantic

**Frontend**: 
- React 18.2
- TypeScript 5.2
- Vite 5.0
- TanStack Query
- Axios

## 🌟 GPT-5.2 Özellikleri (Yeni!)

**Aralık 2025** itibarıyla OpenAI'ın en gelişmiş modeli:

- **Responses API**: `client.responses.create()` - yeni API paradigması
- **xHigh Reasoning**: 6 seviyeli reasoning (none → xhigh)
- **Chain-of-Thought**: Reasoning süreçleri korunur
- **Verbosity Control**: Çıktı detay seviyesi ayarlanabilir
- **No Temperature**: Tutarlılık için temperature/top_p yok
- **SDK Requirement**: openai >= 1.99.0 ZORUNLU

**GPT-5.2 vs GPT-4 Vision:**
| Özellik | GPT-5.2 | GPT-4 Vision |
|---------|---------|--------------|
| API | Responses API | Chat Completions |
| Reasoning | xHigh (6 seviye) | Yok |
| Chain-of-Thought | ✅ Korunur | ❌ Yok |
| Temperature | ❌ Yok | ✅ Var |
| Speed | 5+ dakika (xhigh) | 2-3 dakika |
| Accuracy | 🏆 En yüksek | İyi |

## 📝 API Kullanımı

### Tekil Analiz
```python
import requests

with open("drawing.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8001/api/v1/analyze",
        files={"file": f},
        data={
            "model": "gpt-5.2",  # veya "werk24-professional"
            "reasoning_level": "high",  # low/medium/high/xhigh
            "enhance_mode": "balanced"
        }
    )

result = response.json()
print(f"Parça: {result['title']}")
print(f"Tip: {result['geometry']['part_type']}")
print(f"Süre: {result['processing_time']}s")
```

### Model Karşılaştırma
```python
import requests

with open("drawing.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8001/api/v1/compare",
        files={"file": f},
        data={
            "model1": "werk24-professional",
            "model2": "gpt-5.2",
            "reasoning_level": "high"
        }
    )

comparison = response.json()
print(f"Hız Farkı: {comparison['comparison_notes']['time_difference']}s")
print(f"Hızlı Model: {comparison['comparison_notes']['faster_model']}")
print(f"Güvenilir Model: {comparison['comparison_notes']['higher_confidence']}")
```

## 📖 Dökümantasyon

- **Kurulum Kılavuzu**: [SETUP.md](SETUP.md)
- **API Dokümantasyonu**: http://localhost:8001/docs
- **MQ_V3 Entegrasyon**: [SETUP.md](SETUP.md)

## 🐛 Sorun Giderme

Yaygın sorunlar ve çözümleri için [SETUP.md](SETUP.md) dosyasına bakın.

---

**🔥 DI-2D ile 2D teknik resim okuma performansınızı 10x artırın!**

**Not:** Bu proje, MQ_V3'ün 2D teknik resim okuma yeteneklerini geliştirmek amacıyla oluşturulmuştur.

# 🚀 DI-2D Hızlı Başlangıç

## ✅ Ön Kontrol

**Gereksinimler:**
- ✅ Python 3.10+ yüklü
- ✅ Node.js 18+ yüklü
- ✅ OpenAI API Key hazır

## 📝 Adım 1: Backend .env Dosyası

`.env` dosyası **backend/** dizininde olmalı:

```bash
cd backend
```

**backend/.env** dosyası oluştur:
```env
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

**Önemli:** 
- ✅ Dosya adı: `.env` (nokta ile başlar)
- ✅ Konum: `backend/.env` (backend dizini içinde)
- ✅ İçinde sadece OpenAI API key olması yeterli

## 📦 Adım 2: Backend Kurulum

```bash
cd backend
pip install -r requirements.txt
werk24 init  # 100 trial lisans alır
```

## 🎨 Adım 3: Frontend Kurulum

```bash
cd frontend
npm install
```

## 🚀 Adım 4: Çalıştırma

### Otomatik (Önerilen)

**Windows:**
```powershell
.\start.ps1
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Manuel

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## 🎯 Erişim

- **Frontend UI:** http://localhost:3001
- **Backend API:** http://localhost:8001
- **API Docs:** http://localhost:8001/docs

## 🔍 Sorun Giderme

### ❌ "OpenAI API key not found"
```bash
# .env dosyasının doğru konumda olduğunu kontrol et
cd backend
dir .env  # Windows
ls -la .env  # Linux/Mac

# İçeriği kontrol et
notepad .env  # Windows
cat .env  # Linux/Mac
```

### ❌ Backend başlamıyor
```bash
# Python versiyonunu kontrol et
python --version  # 3.10+ olmalı

# Bağımlılıkları tekrar yükle
pip install -r requirements.txt

# OpenAI SDK versiyonunu kontrol et
pip list | grep openai  # 1.99.0+ olmalı
```

### ❌ Frontend başlamıyor
```bash
# Node versiyonunu kontrol et
node --version  # 18+ olmalı

# Bağımlılıkları tekrar yükle
cd frontend
npm install
```

## ✅ Başarılı Kurulum Testi

Backend çalışıyorsa şu komut başarılı olmalı:

```bash
curl http://localhost:8001/health
# Cevap: {"status":"healthy","service":"DI-2D"}
```

Frontend çalışıyorsa tarayıcıda görmelisin:
- ✅ "🎯 DI-2D" başlığı
- ✅ "Tekil Analiz" ve "Model Karşılaştırma" sekmeleri
- ✅ "Teknik Resim Yükle" alanı

## 🎬 İlk Analiz

1. Frontend'e git: http://localhost:3001
2. "Tekil Analiz" sekmesinde kal
3. **AI Modeli:** GPT-5.2 seçili olmalı ⭐
4. Bir teknik resim yükle (PDF/PNG/JPG)
5. "Analiz Et" butonuna tıkla
6. 2-5 dakika bekle
7. Sonuçları incele!

## 📚 Daha Fazla

- **Detaylı Setup:** [SETUP.md](SETUP.md)
- **GPT-5.2 Özellikler:** [GPT52_UPGRADE.md](GPT52_UPGRADE.md)
- **Werk24 Entegrasyonu:** [WERK24_INTEGRATION.md](WERK24_INTEGRATION.md)

---

**✨ DI-2D ile 2D teknik resim analizine başla!**

# 📁 .env Konfigürasyon Özeti

## ✅ Doğru Kurulum

### Dosya Konumu
```
DI-2D/
├── backend/
│   ├── .env          ← BURASI! ✅
│   ├── main.py
│   └── app/
├── frontend/
├── .env.example      ← Örnek şablon
└── README.md
```

### Dosya İçeriği

**backend/.env** (ZORUNLU):
```env
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

**Sadece bu!** Diğer ayarlar opsiyonel:
```env
# OPSİYONEL: Sadece kullanacaksanız ekleyin
# ANTHROPIC_API_KEY=sk-ant-your-key-here
# GEMINI_API_KEY=your-key-here
```

## 🔧 Nasıl Çalışır?

### Backend Konfigürasyonu

**backend/app/core/config.py:**
```python
class Settings(BaseSettings):
    openai_api_key: str = ""  # .env'den okunur
    # ...
    
    class Config:
        env_file = ".env"  # Göreceli yol: backend/.env
        case_sensitive = False
```

Backend `backend/` dizininden çalıştırıldığında:
```bash
cd backend
python -m uvicorn main:app --reload
# .env dosyasını backend/.env konumunda arar ✅
```

### Werk24 Konfigürasyonu

Werk24 **ayrı** bir config kullanır:
```bash
werk24 init
# ~/.werk24/config.json oluşturur
```

**Önemli:** Werk24 `.env` dosyası kullanmaz!

## ✅ Test Etme

### 1. .env Dosyasının Varlığını Kontrol

**Windows:**
```powershell
cd backend
dir .env
```

**Linux/Mac:**
```bash
cd backend
ls -la .env
```

### 2. OpenAI Key Okunduğunu Doğrula

```bash
cd backend
python -c "from app.core.config import settings; print('OK' if settings.openai_api_key else 'YOK')"
# Çıktı: OK ✅
```

### 3. Analyzer Servisini Test Et

```bash
cd backend
python -c "from app.services.analyzer import DrawingAnalyzer; print('OK')"
# Çıktı: OK ✅
# (⚠️ Anthropic API key not found - Normal, opsiyonel)
```

### 4. Backend API Test

```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8001
# Başka terminal:
curl http://localhost:8001/health
# Çıktı: {"status":"healthy","service":"DI-2D"}
```

## ❌ Yaygın Hatalar

### Hata 1: "OpenAI API key not found"

**Neden:** `.env` dosyası yanlış konumda veya yok

**Çözüm:**
```bash
cd backend
# .env var mı?
dir .env  # Windows
ls .env   # Linux/Mac

# Yoksa oluştur:
echo OPENAI_API_KEY=sk-proj-your-key > .env
```

### Hata 2: ".env dosyası okumuyor"

**Neden:** Backend yanlış dizinden çalıştırılıyor

**Yanlış:**
```bash
# DI-2D/ dizininden
python -m uvicorn backend.main:app  # ❌ .env'i bulamaz
```

**Doğru:**
```bash
# backend/ dizinine gir
cd backend
python -m uvicorn main:app  # ✅ .env'i bulur
```

### Hata 3: "OPENAI_API_KEY geçersiz"

**Neden:** API key yanlış veya eksik

**Kontrol:**
```bash
cd backend
notepad .env  # Windows
cat .env      # Linux/Mac

# İçeriği kontrol et:
OPENAI_API_KEY=sk-proj-...  # 'sk-proj-' ile başlamalı
```

## 🎯 Özet Checklist

Sistem çalışması için gereken **TEK** şey:

- [x] `backend/.env` dosyası var
- [x] İçinde `OPENAI_API_KEY=sk-proj-...` var
- [x] Backend `cd backend` ile çalıştırılıyor
- [x] OpenAI SDK >= 1.99.0 yüklü

**Bu kadar!** 🎉

## 📚 İlgili Dokümantasyon

- **Hızlı Başlangıç:** [QUICKSTART.md](QUICKSTART.md)
- **Detaylı Setup:** [SETUP.md](SETUP.md)
- **GPT-5.2 Özellikler:** [GPT52_UPGRADE.md](GPT52_UPGRADE.md)

---

**✅ .env doğru konumda, sistem hazır!**

"""
Werk24 Lisans ve Sistem Durumu Kontrolü
========================================

Bu script Werk24 lisans durumunuzu ve sistem bağlantısını kontrol eder.
"""

import asyncio
from werk24 import Werk24Client
import json
from pathlib import Path
import os


async def check_system_status():
    """Werk24 sistem durumunu kontrol et"""
    print("🔍 Werk24 sistem durumu kontrol ediliyor...")
    try:
        status = await Werk24Client.get_system_status()
        print(f"✅ Durum: {status.status_indicator}")
        if status.status_description:
            print(f"📝 Açıklama: {status.status_description}")
        return True
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False


def check_config():
    """Werk24 config dosyasını kontrol et"""
    print("\n📄 Werk24 yapılandırması kontrol ediliyor...")
    
    # Windows için config dosyası genellikle %USERPROFILE%\.werk24\config.json
    # Linux/Mac için ~/.werk24/config.json
    home = Path.home()
    config_path = home / ".werk24" / "config.json"
    
    if config_path.exists():
        print(f"✅ Config dosyası bulundu: {config_path}")
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            print("\n📊 Lisans Bilgileri:")
            
            # Token bilgisi varsa göster (güvenlik için kısalt)
            if 'token' in config:
                token = config['token']
                masked_token = token[:10] + "..." + token[-10:] if len(token) > 20 else "***"
                print(f"  🔑 Token: {masked_token}")
            
            # Endpoint bilgisi
            if 'endpoint' in config:
                print(f"  🌐 Endpoint: {config['endpoint']}")
            
            # Diğer ayarlar
            if 'max_requests' in config:
                print(f"  📈 Max İstek: {config['max_requests']}")
            
            # Trial bilgisi (varsa)
            if 'trial' in config:
                print(f"  🆓 Trial: {config['trial']}")
            
            if 'requests_remaining' in config:
                print(f"  ✅ Kalan İstek: {config['requests_remaining']}")
            
            return True
            
        except Exception as e:
            print(f"⚠️  Config dosyası okunamadı: {e}")
            return False
    else:
        print(f"❌ Config dosyası bulunamadı: {config_path}")
        print("\n💡 Çözüm:")
        print("   werk24 init")
        return False


async def test_simple_analysis():
    """Basit bir test analizi yap"""
    print("\n🧪 Test analizi yapılıyor...")
    try:
        from werk24 import get_test_drawing, read_drawing_sync, AskMetaData
        
        # Test çizimi al
        test_drawing = get_test_drawing()
        print("✅ Test çizimi alındı")
        
        # Basit analiz yap
        results = read_drawing_sync(test_drawing, [AskMetaData()])
        print(f"✅ Test analizi başarılı ({len(results)} sonuç)")
        
        # İlk sonucu göster
        if results and len(results) > 0:
            first_result = results[0]
            print(f"\n📊 Test Sonucu:")
            print(f"  Tip: {type(first_result).__name__}")
            if hasattr(first_result, 'is_successful'):
                print(f"  Başarılı: {first_result.is_successful}")
        
        return True
    except Exception as e:
        print(f"❌ Test analizi başarısız: {e}")
        return False


def print_quick_start():
    """Hızlı başlangıç talimatları"""
    print("\n" + "="*70)
    print("  HIZLI BAŞLANGIÇ TALİMATLARI")
    print("="*70)
    
    print("\n1️⃣  Werk24 Kurulumu (İlk Kez):")
    print("   pip install werk24")
    print("   werk24 init          # Trial lisans alır")
    print("   werk24 health-check  # Bağlantıyı test et")
    
    print("\n2️⃣  Backend Başlatma:")
    print("   cd backend")
    print("   python -m uvicorn main:app --reload --port 8001")
    
    print("\n3️⃣  Karşılaştırma Testi:")
    print("   python compare_analysis.py <your_drawing.pdf>")
    
    print("\n4️⃣  Lisans Durumu Kontrolü:")
    print("   python check_werk24.py")


async def main():
    """Ana fonksiyon"""
    print("="*70)
    print("  WERK24 LİSANS VE SİSTEM DURUMU")
    print("="*70)
    
    # Config kontrolü
    config_ok = check_config()
    
    # Sistem durumu kontrolü
    system_ok = await check_system_status()
    
    # Test analizi
    if config_ok and system_ok:
        test_ok = await test_simple_analysis()
    
    # Özet
    print("\n" + "="*70)
    print("  ÖZET")
    print("="*70)
    
    print(f"\n📄 Config Dosyası:  {'✅ OK' if config_ok else '❌ Bulunamadı'}")
    print(f"🌐 Sistem Durumu:   {'✅ OK' if system_ok else '❌ Bağlantı Hatası'}")
    
    if config_ok and system_ok:
        print(f"🧪 Test Analizi:    {'✅ OK' if test_ok else '❌ Başarısız'}")
        
        if test_ok:
            print("\n🎉 Werk24 kullanıma hazır!")
            print("\n💡 Sonraki Adım:")
            print("   python compare_analysis.py <your_drawing.pdf>")
        else:
            print("\n⚠️  Test analizi başarısız. Lütfen kurulumu kontrol edin.")
    else:
        print("\n❌ Werk24 henüz yapılandırılmamış.")
        print_quick_start()


if __name__ == "__main__":
    asyncio.run(main())

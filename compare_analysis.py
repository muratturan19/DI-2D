"""
DI-2D vs Werk24 Karşılaştırma Test Scripti
==========================================

Bu script aynı teknik resmi hem DI-2D'nin kendi AI modelleriyle 
hem de Werk24 ile analiz edip sonuçları karşılaştırır.

Kullanım:
    python compare_analysis.py <drawing_file_path>

Örnek:
    python compare_analysis.py test_drawing.pdf
"""

import asyncio
import requests
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import time

# API Base URL
API_BASE = "http://localhost:8001"


def print_section(title: str):
    """Bölüm başlığı yazdır"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def print_comparison(label: str, werk24_val: Any, di2d_val: Any):
    """İki değeri karşılaştır ve yazdır"""
    match = "✅" if werk24_val == di2d_val else "❌"
    print(f"\n{label}:")
    print(f"  Werk24:  {werk24_val}")
    print(f"  DI-2D:   {di2d_val}")
    print(f"  Match:   {match}")


def analyze_with_api(file_path: str, model: str) -> Dict[str, Any]:
    """
    API üzerinden analiz yap
    
    Args:
        file_path: Analiz edilecek dosya yolu
        model: AI modeli (werk24-professional, gpt-4-vision-preview, vb.)
    
    Returns:
        Analiz sonucu dict
    """
    print(f"\n🔄 {model} ile analiz yapılıyor...")
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'model': model,
            'reasoning_level': 'high',
            'enhance_mode': 'balanced'
        }
        
        start_time = time.time()
        response = requests.post(
            f"{API_BASE}/api/v1/analyze",
            files=files,
            data=data,
            timeout=300  # 5 dakika timeout
        )
        elapsed_time = time.time() - start_time
    
    if response.status_code == 200:
        result = response.json()
        result['_api_time'] = elapsed_time
        print(f"✅ Analiz tamamlandı ({elapsed_time:.2f}s)")
        return result
    else:
        print(f"❌ Hata: {response.status_code} - {response.text}")
        return None


def compare_results(werk24_result: Dict, di2d_result: Dict, output_file: str = None):
    """
    İki analiz sonucunu karşılaştır
    
    Args:
        werk24_result: Werk24 analiz sonucu
        di2d_result: DI-2D (GPT-4) analiz sonucu
        output_file: Sonuçların kaydedileceği JSON dosyası (opsiyonel)
    """
    print_section("KARŞILAŞTIRMA SONUÇLARI")
    
    # Temel Bilgiler
    print_section("1. TEMEL BİLGİLER")
    print_comparison("Başlık/Parça Adı", 
                    werk24_result.get('title', 'N/A'),
                    di2d_result.get('title', 'N/A'))
    
    print_comparison("Çizim Numarası",
                    werk24_result.get('drawing_number', 'N/A'),
                    di2d_result.get('drawing_number', 'N/A'))
    
    print_comparison("Revizyon",
                    werk24_result.get('revision', 'N/A'),
                    di2d_result.get('revision', 'N/A'))
    
    # Malzeme
    print_section("2. MALZEME BİLGİSİ")
    werk24_material = werk24_result.get('material', {})
    di2d_material = di2d_result.get('material', {})
    
    if werk24_material and di2d_material:
        print_comparison("Malzeme Adı",
                        werk24_material.get('name', 'N/A'),
                        di2d_material.get('name', 'N/A'))
        print_comparison("Standart",
                        werk24_material.get('standard', 'N/A'),
                        di2d_material.get('standard', 'N/A'))
    else:
        print("⚠️  Malzeme bilgisi eksik")
    
    # Geometri
    print_section("3. GEOMETRİ ANALİZİ")
    werk24_geo = werk24_result.get('geometry', {})
    di2d_geo = di2d_result.get('geometry', {})
    
    print_comparison("Parça Tipi",
                    werk24_geo.get('part_type', 'N/A'),
                    di2d_geo.get('part_type', 'N/A'))
    
    print_comparison("Şekil Tipi",
                    werk24_geo.get('shape_type', 'N/A'),
                    di2d_geo.get('shape_type', 'N/A'))
    
    print_comparison("Karmaşıklık Skoru",
                    f"{werk24_geo.get('complexity_score', 0):.1f}/10",
                    f"{di2d_geo.get('complexity_score', 0):.1f}/10")
    
    # Boyutlar
    werk24_dims = werk24_geo.get('overall_dimensions', {})
    di2d_dims = di2d_geo.get('overall_dimensions', {})
    
    print(f"\n📐 Boyut Sayısı:")
    print(f"  Werk24:  {len(werk24_dims)} boyut")
    print(f"  DI-2D:   {len(di2d_dims)} boyut")
    
    if werk24_dims or di2d_dims:
        print("\nİlk 3 Boyut Karşılaştırması:")
        all_keys = set(list(werk24_dims.keys())[:3] + list(di2d_dims.keys())[:3])
        for key in list(all_keys)[:3]:
            w24_dim = werk24_dims.get(key, {})
            di2_dim = di2d_dims.get(key, {})
            
            w24_str = f"{w24_dim.get('value', 'N/A')} {w24_dim.get('unit', '')}"
            di2_str = f"{di2_dim.get('value', 'N/A')} {di2_dim.get('unit', '')}"
            
            print(f"\n  {key}:")
            print(f"    Werk24:  {w24_str}")
            print(f"    DI-2D:   {di2_str}")
    
    # Özellikler (delik, cep, vb.)
    werk24_features = werk24_geo.get('features', [])
    di2d_features = di2d_geo.get('features', [])
    
    print(f"\n🔧 Özellik Sayısı:")
    print(f"  Werk24:  {len(werk24_features)} özellik")
    print(f"  DI-2D:   {len(di2d_features)} özellik")
    
    # Kalite Gereksinimleri
    print_section("4. KALİTE GEREKSİNİMLERİ")
    werk24_quality = werk24_result.get('quality', {})
    di2d_quality = di2d_result.get('quality', {})
    
    werk24_tols = werk24_quality.get('tolerances', [])
    di2d_tols = di2d_quality.get('tolerances', [])
    
    print(f"\n🎯 Tolerans Sayısı:")
    print(f"  Werk24:  {len(werk24_tols)} tolerans")
    print(f"  DI-2D:   {len(di2d_tols)} tolerans")
    
    werk24_surface = werk24_quality.get('surface_finishes', [])
    di2d_surface = di2d_quality.get('surface_finishes', [])
    
    print(f"\n✨ Yüzey İşlemi Sayısı:")
    print(f"  Werk24:  {len(werk24_surface)} işlem")
    print(f"  DI-2D:   {len(di2d_surface)} işlem")
    
    # İmalat
    print_section("5. İMALAT ANALİZİ")
    werk24_mfg = werk24_result.get('manufacturing', {})
    di2d_mfg = di2d_result.get('manufacturing', {})
    
    print_comparison("Ana İşlem",
                    werk24_mfg.get('primary_process', 'N/A'),
                    di2d_mfg.get('primary_process', 'N/A'))
    
    print_comparison("Zorluk Seviyesi",
                    werk24_mfg.get('difficulty_level', 'N/A'),
                    di2d_mfg.get('difficulty_level', 'N/A'))
    
    # Performans Metrikleri
    print_section("6. PERFORMANS METRİKLERİ")
    werk24_meta = werk24_result.get('metadata', {})
    di2d_meta = di2d_result.get('metadata', {})
    
    print(f"\n⏱️  İşlem Süresi:")
    print(f"  Werk24:  {werk24_meta.get('processing_time', 0):.2f}s (API: {werk24_result.get('_api_time', 0):.2f}s)")
    print(f"  DI-2D:   {di2d_meta.get('processing_time', 0):.2f}s (API: {di2d_result.get('_api_time', 0):.2f}s)")
    
    print(f"\n🎯 Güven Skoru:")
    print(f"  Werk24:  {werk24_meta.get('confidence_score', 0)*100:.0f}%")
    print(f"  DI-2D:   {di2d_meta.get('confidence_score', 0)*100:.0f}%")
    
    if 'tokens_used' in di2d_meta:
        print(f"\n💰 Token Kullanımı:")
        print(f"  Werk24:  N/A (trial lisans)")
        print(f"  DI-2D:   {di2d_meta['tokens_used']:,} token")
    
    # Uyarılar
    werk24_warnings = werk24_meta.get('warnings', [])
    di2d_warnings = di2d_meta.get('warnings', [])
    
    if werk24_warnings or di2d_warnings:
        print_section("7. UYARILAR")
        if werk24_warnings:
            print("\n⚠️  Werk24 Uyarıları:")
            for w in werk24_warnings:
                print(f"  - {w}")
        if di2d_warnings:
            print("\n⚠️  DI-2D Uyarıları:")
            for w in di2d_warnings:
                print(f"  - {w}")
    
    # Sonuçları kaydet
    if output_file:
        comparison_data = {
            'timestamp': datetime.now().isoformat(),
            'werk24': werk24_result,
            'di2d': di2d_result,
            'summary': {
                'dimensions': {
                    'werk24_count': len(werk24_dims),
                    'di2d_count': len(di2d_dims)
                },
                'tolerances': {
                    'werk24_count': len(werk24_tols),
                    'di2d_count': len(di2d_tols)
                },
                'features': {
                    'werk24_count': len(werk24_features),
                    'di2d_count': len(di2d_features)
                },
                'performance': {
                    'werk24_time': werk24_meta.get('processing_time', 0),
                    'di2d_time': di2d_meta.get('processing_time', 0),
                    'werk24_confidence': werk24_meta.get('confidence_score', 0),
                    'di2d_confidence': di2d_meta.get('confidence_score', 0)
                }
            }
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comparison_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Sonuçlar kaydedildi: {output_file}")


def main():
    """Ana fonksiyon"""
    if len(sys.argv) < 2:
        print("❌ Hata: Dosya yolu belirtilmedi")
        print(f"\nKullanım: python {sys.argv[0]} <drawing_file_path>")
        print(f"Örnek: python {sys.argv[0]} test_drawing.pdf")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not Path(file_path).exists():
        print(f"❌ Hata: Dosya bulunamadı: {file_path}")
        sys.exit(1)
    
    print_section("DI-2D vs WERK24 KARŞILAŞTIRMA TESTİ")
    print(f"📄 Dosya: {file_path}")
    print(f"🕐 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Backend kontrolü
    print("\n🔍 Backend bağlantısı kontrol ediliyor...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend çalışıyor")
        else:
            print("❌ Backend yanıt vermiyor")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Backend'e bağlanılamadı: {e}")
        print("\n💡 Backend'i başlatmak için:")
        print("   cd backend")
        print("   python -m uvicorn main:app --reload --port 8001")
        sys.exit(1)
    
    # Werk24 ile analiz
    print_section("WERK24 PROFESSIONAL ANALİZİ")
    werk24_result = analyze_with_api(file_path, "werk24-professional")
    
    if not werk24_result:
        print("❌ Werk24 analizi başarısız")
        sys.exit(1)
    
    # DI-2D (GPT-4) ile analiz
    print_section("DI-2D (GPT-4 VISION) ANALİZİ")
    di2d_result = analyze_with_api(file_path, "gpt-4-vision-preview")
    
    if not di2d_result:
        print("❌ DI-2D analizi başarısız")
        sys.exit(1)
    
    # Karşılaştırma
    output_filename = f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    compare_results(werk24_result, di2d_result, output_filename)
    
    print_section("TEST TAMAMLANDI")
    print("\n📊 Sonraki Adımlar:")
    print("  1. Sonuç dosyasını inceleyin")
    print("  2. Boyut okuma doğruluğunu karşılaştırın")
    print("  3. GD&T tolerans tanımalarını kontrol edin")
    print("  4. Werk24'e yaklaşma stratejilerini belirleyin")
    print(f"\n💾 Detaylı sonuçlar: {output_filename}")


if __name__ == "__main__":
    main()

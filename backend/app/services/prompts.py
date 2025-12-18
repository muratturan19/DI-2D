"""
DI-2D Geliştirilmiş Analiz Prompt'ları
Özellikle 2D teknik resim okuma için optimize edilmiş

Her model için özelleştirilmiş prompt'lar:
- OpenAI GPT-4 Vision: Yapılandırılmış JSON çıktısı
- Claude 3.5 Sonnet: Detaylı geometrik analiz
- Gemini 1.5 Pro: Hızlı genel değerlendirme
"""

def get_analysis_prompt(model_type: str, reasoning_level: str = "high") -> tuple[str, str]:
    """
    Model tipine göre system ve user prompt'ları döndür
    
    Args:
        model_type: "openai", "claude", veya "gemini"
        reasoning_level: "medium", "high", "xhigh"
    
    Returns:
        (system_prompt, user_prompt) tuple
    """
    if model_type == "openai":
        return _get_openai_prompts(reasoning_level)
    elif model_type == "claude":
        return _get_claude_prompts()
    elif model_type == "gemini":
        return _get_gemini_prompts()
    else:
        raise ValueError(f"Unknown model type: {model_type}")


def _get_openai_prompts(reasoning_level: str) -> tuple[str, str]:
    """OpenAI GPT-4 Vision için prompt'lar"""
    
    system_prompt = """Sen 20 yıllık deneyimli bir CNC imalat mühendisi ve teknik resim uzmanısın.

ROL VE YETKİNLİKLER:
- ISO 129/128 teknik resim standartları uzmanı
- GD&T (Geometric Dimensioning & Tolerancing) sertifikalı
- CNC torna, freze ve 5 eksen işleme deneyimi
- Malzeme bilimi ve imalat süreçleri uzmanı
- CAD/CAM yazılımları kullanıcısı

GÖREVİN:
Verilen 2D teknik resmi DETAYLI şekilde analiz et ve tüm bilgileri yapılandırılmış JSON formatında döndür.

ÖNCELİK SIRASI:
1. ANTETİ OKU - Malzeme, kaplama, notlar, revizyon
2. BOYUTLARI ÇIKART - Her ölçü, tolerans ve konumu
3. GEOMETRİYİ ANLA - Delikler, cepler, kanallar, pahlar
4. TOLERANSLARI TESPİT ET - Boyutsal ve geometrik toleranslar
5. İMALAT ÖNERİSİ - İşleme sırası, tezgah seçimi

ÇOK ÖNEMLİ - BOYUT OKUMA KURALLARI:
❌ YANLIŞ: "120" (birim yok)
✅ DOĞRU: {"value": 120, "unit": "mm", "tolerance": "±0.1"}

❌ YANLIŞ: "M8 delik" (boyut bilgisi eksik)
✅ DOĞRU: {"type": "threaded_hole", "thread": "M8x1.25", "depth": 15, "quantity": 4}

❌ YANLIŞ: "4x delik" (çap ve pozisyon yok)
✅ DOĞRU: {"type": "hole", "diameter": 6.5, "quantity": 4, "position": "Φ100 PCD", "tolerance": "H7"}

DİKKAT EDİLECEK DETAYLAR:
- Kesme hatları (-- çizgi) malzeme kesme yerini gösterir
- Merkez çizgileri (.-.- çizgi) simetri ve referans
- Boyut okları ve sayılar arasındaki ilişki
- Alt notlardaki özel talimatlar
- Tolerans kutucukları (□ içinde)

TÜRKÇE DİL KURALLARI:
❌ "malzemenin seçimi" → ✅ "malzeme seçimi"
❌ "işlemin yapılması" → ✅ "işlem yapılması"
❌ "brünit yüzey" → ✅ "brünit kaplama" veya "siyah kaplama"
"""

    if reasoning_level == "xhigh":
        reasoning_instruction = """
AŞIRI DETAYLI ANALİZ MOD (xhigh):
- Her boyutu 2-3 kez kontrol et
- Tüm kesişim noktalarını hesapla
- Alternatif imalat yöntemlerini karşılaştır
- Olası hataları ve riskleri listele
- Maliyet optimizasyonu öneriler sun
"""
    elif reasoning_level == "high":
        reasoning_instruction = """
DETAYLI ANALİZ MOD (high):
- Tüm boyutları dikkatlice oku
- Geometrik özellikleri tam belirle
- İmalat sırasını planla
- Kritik toleransları vurgula
"""
    else:  # medium
        reasoning_instruction = """
STANDART ANALİZ MOD (medium):
- Ana boyutları çıkart
- Temel özellikleri tanımla
- Genel imalat önerisi sun
"""
    
    user_prompt = f"""{reasoning_instruction}

Bu 2D teknik resmi analiz et ve aşağıdaki JSON formatında döndür:

```json
{{
  "title": "Parça adı veya resim başlığı",
  "drawing_number": "Resim numarası (varsa)",
  "revision": "Revizyon (A, B, C gibi)",
  "scale": "Ölçek (1:1, 1:2 gibi)",
  
  "material": {{
    "name": "Malzeme adı (St-37, AlMg3, Titanyum Grade 2 gibi)",
    "standard": "Standart numarası (DIN, ASTM, ISO)",
    "density": 7.85,
    "hardness": "Sertlik değeri (varsa)"
  }},
  
  "surface_finish": {{
    "type": "anodize|paint|coating|plating|none",
    "description": "Detaylı açıklama (örn: Siyah anodize, RAL 9005 boya)",
    "roughness": "Yüzey pürüzlülüğü (Ra değeri, varsa)",
    "color": "Renk (varsa)"
  }},
  
  "geometry": {{
    "part_type": "Parça tipi (flanş, somun, kapak, gövde, bağlantı elemanı, vb.)",
    "shape_type": "Genel şekil (silindirik, kutusal, L-profil, karmaşık)",
    "overall_dimensions": {{
      "length": {{"value": 120.0, "unit": "mm", "tolerance": "±0.2"}},
      "width": {{"value": 80.0, "unit": "mm", "tolerance": "±0.2"}},
      "height": {{"value": 30.0, "unit": "mm", "tolerance": "±0.1"}},
      "diameter": {{"value": 0, "unit": "mm", "tolerance": null}}
    }},
    "features": [
      {{
        "type": "hole|pocket|slot|groove|thread|fillet|chamfer",
        "quantity": 4,
        "dimensions": {{
          "diameter": 6.5,
          "depth": 15,
          "thread": "M8x1.25"
        }},
        "position": "Pozisyon açıklaması (Φ100 PCD, merkez, köşeden 20mm)",
        "notes": "Özel notlar (kılavuzlu, raybalı, vb.)"
      }}
    ],
    "complexity_score": 7.5
  }},
  
  "manufacturing": {{
    "primary_process": "Ana işleme (CNC Freze|CNC Torna|Pres|Kaynak)",
    "secondary_processes": ["Delme", "Kılavuz açma", "Rayba"],
    "setup_count": 2,
    "estimated_operations": [
      "1. Stok hazırlık",
      "2. Dış kontur frezeleme",
      "3. Delik delme (4x Φ6.5)",
      "4. Kılavuz açma (4x M8)"
    ],
    "difficulty_level": "kolay|orta|zor",
    "special_requirements": ["Özel takım gerekli", "Yüksek hassasiyet"]
  }},
  
  "quality": {{
    "tolerances": [
      {{"type": "dimensional", "value": "±0.1 mm", "reference": "Genel tolerans"}},
      {{"type": "geometric", "value": "⊥ 0.05 A", "reference": "Dik açılık"}}
    ],
    "surface_finishes": [
      {{"type": "coating", "description": "Brünit kaplama", "roughness": "Ra 1.6"}}
    ],
    "inspection_notes": ["CMM ölçümü", "Vida kontrol"],
    "critical_dimensions": ["Delik çapları Φ6.5 H7", "Delik aralıkları PCD 100"]
  }},
  
  "general_notes": [
    "Alt notlardaki tüm özel talimatlar"
  ],
  
  "design_recommendations": [
    "İmalat kolaylığı için öneriler"
  ],
  
  "confidence_score": 0.95,
  "warnings": ["Belirsiz boyutlar veya notlar"]
}}
```

SADECE GEÇERLİ JSON DÖNDÜR. Açıklama veya markdown kod bloğu EKLEME."""

    return system_prompt, user_prompt


def _get_claude_prompts() -> tuple[str, str]:
    """Claude 3.5 Sonnet için prompt'lar"""
    
    system_prompt = """Sen uzman bir mekanik tasarım ve imalat mühendisisin.
2D teknik resimleri analiz etme ve detaylı geometrik bilgi çıkarma konusunda uzmansın."""
    
    user_prompt = """Bu teknik resmi detaylı şekilde analiz et:

1. ANTET BİLGİLERİ: Malzeme, kaplama, revizyon
2. ANA BOYUTLAR: Uzunluk, genişlik, yükseklik, çap
3. ÖZELLIKLER: Delikler, cepler, kanallar, vida delikleri
4. TOLERANSLAR: Boyutsal ve geometrik toleranslar
5. İMALAT: Önerilen işleme sırası

Sonucu yapılandırılmış JSON formatında ver."""
    
    return system_prompt, user_prompt


def _get_gemini_prompts() -> tuple[str, str]:
    """Gemini 1.5 Pro için prompt'lar"""
    
    system_prompt = """Sen teknik resim analizi yapan bir AI asistanısın."""
    
    user_prompt = """Bu teknik resmi analiz et ve JSON formatında detaylı bilgi ver:
- Malzeme ve yüzey işlemi
- Boyutlar ve toleranslar
- Geometrik özellikler
- İmalat önerileri"""
    
    return system_prompt, user_prompt

"""
DI-2D Gelişmiş AI Analiz Servisi
Özellikle 2D teknik resim okuma için optimize edilmiş

Desteklenen Modeller:
- GPT-5.2 (OpenAI) - En gelişmiş reasoning, önerilen
- GPT-4 Vision (OpenAI) - Geri uyumluluk
- Claude 3.5 Sonnet (Anthropic)
- Gemini 1.5 Pro (Google)

Özellikler:
- Çoklu model desteği
- GPT-5.2 Responses API entegrasyonu
- Detaylı boyut okuma
- Geometrik tolerans algılama
- Malzeme ve yüzey işlemi tanıma
- İmalat önerileri
"""
import os
import base64
import logging
from typing import Dict, Any, Optional
from openai import OpenAI
from anthropic import Anthropic
import json

from app.core.config import settings
from app.core.exceptions import AIKeyError, AnalysisError
from app.models.analysis import DrawingAnalysisResult, AnalysisMetadata
from .preprocessor import preprocess_drawing
from .prompts import get_analysis_prompt

logger = logging.getLogger(__name__)

class DrawingAnalyzer:
    """Teknik resim analiz servisi"""
    
    def __init__(self):
        """AI istemcilerini başlat"""
        # OpenAI
        if settings.openai_api_key:
            self.openai_client = OpenAI(api_key=settings.openai_api_key)
            logger.info("✅ OpenAI client initialized")
        else:
            self.openai_client = None
            logger.warning("⚠️ OpenAI API key not found")
        
        # Anthropic
        if settings.anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=settings.anthropic_api_key)
            logger.info("✅ Anthropic client initialized")
        else:
            self.anthropic_client = None
            logger.warning("⚠️ Anthropic API key not found")
    
    async def analyze(
        self,
        file_bytes: bytes,
        filename: str,
        model: str = "gpt-4-vision-preview",
        max_tokens: int = 150000,
        reasoning_level: str = "high",
        enhance_mode: str = "balanced"
    ) -> DrawingAnalysisResult:
        """
        Teknik resmi analiz et
        
        Args:
            file_bytes: Dosya baytları
            filename: Dosya adı
            model: AI modeli
            max_tokens: Maksimum token sayısı
            reasoning_level: Düşünme seviyesi ("medium", "high", "xhigh")
            enhance_mode: Görüntü iyileştirme modu ("fast", "balanced", "aggressive")
        
        Returns:
            Analiz sonucu
        """
        import time
        start_time = time.time()
        
        logger.info(f"🚀 Starting analysis: file={filename}, model={model}, reasoning={reasoning_level}")
        
        try:
            # 1. Dosyayı ön işle
            file_ext = os.path.splitext(filename)[1].lower()
            preprocessed = preprocess_drawing(file_bytes, file_ext, enhance_mode=enhance_mode)
            
            if preprocessed["status"] != "success" or not preprocessed.get("pages"):
                raise AnalysisError("Failed to preprocess drawing")
            
            # İlk sayfayı kullan (çoğu teknik resim tek sayfa)
            page_data = preprocessed["pages"][0]
            image_base64 = page_data["image_base64"]
            
            logger.info(f"✅ Preprocessed: {page_data['width']}x{page_data['height']}px")
            
            # 2. Uygun modelle analiz et
            if model.startswith("gpt-"):
                result_dict = await self._analyze_with_openai(
                    image_base64, 
                    model, 
                    max_tokens,
                    reasoning_level
                )
            elif model.startswith("claude-"):
                result_dict = await self._analyze_with_claude(
                    image_base64,
                    model,
                    max_tokens
                )
            else:
                raise AnalysisError(f"Unsupported model: {model}")
            
            # 3. Metadata ekle
            processing_time = time.time() - start_time
            result_dict["metadata"] = AnalysisMetadata(
                model_used=model,
                processing_time=processing_time,
                confidence_score=result_dict.get("confidence_score", 0.8),
                tokens_used=result_dict.get("tokens_used"),
                warnings=result_dict.get("warnings", [])
            )
            
            # 4. Pydantic modeline çevir
            result = DrawingAnalysisResult(**result_dict)
            
            logger.info(f"✅ Analysis complete in {processing_time:.1f}s")
            return result
            
        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}")
            raise AnalysisError(f"Analysis failed: {str(e)}")
    
    async def _analyze_with_openai(
        self,
        image_base64: str,
        model: str,
        max_tokens: int,
        reasoning_level: str
    ) -> Dict[str, Any]:
        """OpenAI GPT-5.2 / GPT-4 Vision ile analiz"""
        if not self.openai_client:
            raise AIKeyError("OpenAI API key not configured")
        
        logger.info(f"🤖 Analyzing with OpenAI {model} (reasoning: {reasoning_level})")
        
        try:
            # Prompt'u oluştur
            system_prompt, user_prompt = get_analysis_prompt("openai", reasoning_level)
            
            # GPT-5.2 için Responses API kullan
            if model in ["gpt-5.2", "gpt-5.2-chat", "gpt-5", "gpt-5-chat"]:
                return await self._analyze_with_gpt52(
                    image_base64,
                    model,
                    system_prompt,
                    user_prompt,
                    max_tokens,
                    reasoning_level
                )
            
            # Eski modeller için Chat Completions API (geri uyumluluk)
            else:
                return await self._analyze_with_gpt4_legacy(
                    image_base64,
                    model,
                    system_prompt,
                    user_prompt,
                    max_tokens
                )
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse OpenAI response as JSON: {e}")
            raise AnalysisError(f"Invalid JSON response from AI: {e}")
        except Exception as e:
            logger.error(f"❌ OpenAI API error: {e}")
            raise AnalysisError(f"OpenAI API error: {e}")
    
    async def _analyze_with_gpt52(
        self,
        image_base64: str,
        model: str,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        reasoning_level: str
    ) -> Dict[str, Any]:
        """
        GPT-5.2 Responses API ile analiz
        Yeni reasoning parametreleri kullanılır
        """
        logger.info(f"🚀 Using GPT-5.2 Responses API (reasoning: {reasoning_level})")
        
        # Reasoning effort mapping
        effort_map = {
            "medium": "medium",
            "high": "high",
            "xhigh": "xhigh"
        }
        effort = effort_map.get(reasoning_level, "high")
        
        # Responses API çağrısı
        response = self.openai_client.responses.create(
            model=model,
            input=[
                {"type": "text", "text": f"{system_prompt}\n\n{user_prompt}"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_base64}",
                        "detail": "high"
                    }
                }
            ],
            reasoning={"effort": effort},
            text={"verbosity": "high"},  # Detaylı analiz istiyoruz
            max_output_tokens=max_tokens,
        )
        
        # Yanıtı parse et
        content = response.output_text
        result = json.loads(content)
        
        # Token bilgisi (varsa)
        if hasattr(response, 'usage'):
            result["tokens_used"] = response.usage.total_tokens
        
        logger.info(f"✅ GPT-5.2 analysis complete. Tokens: {result.get('tokens_used')}")
        return result
    
    async def _analyze_with_gpt4_legacy(
        self,
        image_base64: str,
        model: str,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int
    ) -> Dict[str, Any]:
        """
        GPT-4 Vision - Chat Completions API (geri uyumluluk)
        """
        logger.info(f"📟 Using legacy Chat Completions API for {model}")
        
        # API çağrısı
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=max_tokens,
            temperature=settings.temperature
        )
        
        # Yanıtı parse et
        content = response.choices[0].message.content
        
        # JSON parse et
        result = json.loads(content)
        result["tokens_used"] = response.usage.total_tokens if response.usage else None
        
        logger.info(f"✅ GPT-4 legacy analysis complete. Tokens: {result.get('tokens_used')}")
        return result
    
    async def _analyze_with_claude(
        self,
        image_base64: str,
        model: str,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Anthropic Claude ile analiz"""
        if not self.anthropic_client:
            raise AIKeyError("Anthropic API key not configured")
        
        logger.info(f"🤖 Analyzing with Claude {model}")
        
        try:
            # Prompt'u oluştur
            system_prompt, user_prompt = get_analysis_prompt("claude", "high")
            
            # API çağrısı
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=settings.temperature,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_base64
                                }
                            },
                            {
                                "type": "text",
                                "text": user_prompt
                            }
                        ]
                    }
                ]
            )
            
            # Yanıtı parse et
            content = response.content[0].text
            
            # JSON parse et
            result = json.loads(content)
            result["tokens_used"] = response.usage.input_tokens + response.usage.output_tokens if hasattr(response, 'usage') else None
            
            logger.info(f"✅ Claude analysis complete. Tokens: {result.get('tokens_used')}")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse Claude response as JSON: {e}")
            raise AnalysisError(f"Invalid JSON response from AI: {e}")
        except Exception as e:
            logger.error(f"❌ Claude API error: {e}")
            raise AnalysisError(f"Claude API error: {e}")


# Singleton instance
analyzer = DrawingAnalyzer()

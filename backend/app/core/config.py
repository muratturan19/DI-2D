"""
Configuration settings for DI-2D backend
"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Environment
    environment: str = "development"
    
    # API Keys
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    gemini_api_key: str = ""
    
    # Werk24 API
    w24techread_auth_region: str = ""
    w24techread_auth_token: str = ""
    
    # AI Configuration
    default_model: str = "gpt-4-vision-preview"
    max_tokens: int = 150000
    temperature: float = 0.1
    
    # PDF Processing
    pdf_dpi: int = 400
    image_max_size: int = 4096
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:3001",  # DI-2D Frontend
        "http://localhost:5173",  # Vite default
        "http://localhost:3000"   # React default
    ]
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8001
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"  # .env'deki ekstra field'lara izin ver

settings = Settings()

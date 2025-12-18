"""
DI-2D Backend - FastAPI Main Application
2D Drawing Intelligence System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import analysis

app = FastAPI(
    title="DI-2D API",
    description="2D Drawing Intelligence - Advanced Technical Drawing Analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])

@app.get("/")
async def root():
    return {
        "service": "DI-2D API",
        "version": "1.0.0",
        "status": "active",
        "description": "2D Drawing Intelligence System"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "DI-2D"}

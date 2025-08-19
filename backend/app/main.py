from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api import api_router
from app.models.database import Base, engine
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Sistema RAG com interface web para gerenciar bases de documentos e conversar com elas usando LlamaIndex e Ollama"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_PREFIX)

# Create necessary directories
os.makedirs(settings.DOCUMENTS_PATH, exist_ok=True)
os.makedirs(settings.INDEX_STORAGE_PATH, exist_ok=True)

@app.get("/")
def read_root():
    """Root endpoint with system information"""
    return {
        "message": "DocuChat API - Sistema RAG Web",
        "version": settings.VERSION,
        "docs": "/docs",
        "api_prefix": settings.API_PREFIX
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

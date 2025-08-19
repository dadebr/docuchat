"""Configuration settings for DocuChat RAG application."""

import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "DocuChat RAG API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database
    database_url: Optional[str] = "sqlite:///./docuchat.db"
    
    # LlamaIndex / LLM Settings
    llm_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    default_model: str = "llama2"
    
    # Vector Store
    vector_store_path: str = "./data/vector_store"
    chunk_size: int = 1024
    chunk_overlap: int = 20
    
    # API Settings
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8080"]
    max_upload_size: int = 50 * 1024 * 1024  # 50MB
    
    # Storage
    upload_path: str = "./data/uploads"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()

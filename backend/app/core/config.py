"""Application configuration using Pydantic Settings"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Quran Hub"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENV: str = "development"
    
    # MongoDB
    MONGO_URL: str = "mongodb://localhost:27017/quran-hub"
    
    # JWT
    JWT_SECRET: str = "your-super-secret-jwt-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    JWT_REFRESH_EXPIRATION_DAYS: int = 7
    
    # LLM
    LLM_PROVIDER: str = "openai"  # openai, gemini, claude
    LLM_API_KEY: str = ""
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Rate Limiting
    RATE_LIMIT_LOGIN: str = "5/minute"
    RATE_LIMIT_AI: str = "10/minute"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

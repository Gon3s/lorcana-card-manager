"""Application configuration and settings."""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be overridden by environment variables.
    For example, DATABASE_URL can be set in a .env file or as an environment variable.
    """
    
    # Application
    app_name: str = "Lorcana Card Manager"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # Database
    database_url: str = "sqlite:///./lorcana_cards.db"
    
    # File Upload
    upload_folder: str = "./uploads"
    max_upload_size: int = 10 * 1024 * 1024  # 10 MB
    allowed_extensions: list[str] = ["jpg", "jpeg", "png"]
    
    # OCR / Groq API
    groq_api_key: Optional[str] = None
    groq_model: str = "llama-3.2-90b-vision-preview"
    groq_timeout: int = 30
    
    # CORS
    cors_origins: str = "http://localhost:4200"
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Convert comma-separated CORS origins to list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

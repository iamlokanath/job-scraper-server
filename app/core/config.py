from typing import List, Optional, Any, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator, ConfigDict
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Job Scraper"
    APP_ENV: str = "development"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-jwt-secret-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:password@localhost:5432/job_scraper"
    )
    
    # CORS
    BACKEND_CORS_ORIGINS: Any = []
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


# Create settings instance
settings = Settings()

"""Application configuration settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # JWT Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Password Reset Token Settings
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 24
    
    # Email Settings
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@packagetracker.com"
    SMTP_FROM_NAME: str = "Package Tracker"
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./packagetracker.db"
    
    # Application Settings
    APP_NAME: str = "Package Tracker"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()

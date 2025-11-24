from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Database
    DATABASE_URL: str = "postgresql://packagetracker:packagetracker@db:5432/packagetracker"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # SMTP
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""
    
    # Application
    APP_NAME: str = "Package Tracker"
    FRONTEND_URL: str = "http://localhost:3000"
    
    # KeyDelivery
    KEYDELIVERY_API_KEY: str = ""
    KD100_APIKEY: str = ""
    KD100_SECRET: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()

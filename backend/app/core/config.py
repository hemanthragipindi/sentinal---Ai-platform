from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentinel AI Security Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str
    
    # JWT Authentication
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # External Providers
    LLM_PROVIDER: str = "huggingface"
    LLM_MODEL_NAME: str = ""
    EMBEDDING_MODEL_NAME: str = ""
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    HF_TOKEN: str = ""
    HF_ROUTER_URL: str = ""
    GOOGLE_CLIENT_ID: str = "773120015026-28ctooofrpnt6gngi9sl7j9ofd8g0bu6.apps.googleusercontent.com"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

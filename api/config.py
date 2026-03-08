from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "PowerBI Response Analytics API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "REST API for PowerBI event registration analytics"
    
    # CORS Settings
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "https://powerbi-analytics-dashboard.vercel.app",  # stable production URL
        "https://powerbi-analytics-vercel-oe13qci0a-my19813s-projects.vercel.app",  # ← add your real Vercel URL here once you know it
    ]
    
    # Data paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "outputs" / "processed_data"
    CHARTS_DIR: Path = BASE_DIR / "outputs" / "charts"
    
    # Cache settings
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

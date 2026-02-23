from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "VanAdhikar Drishti"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "fra_admin"
    POSTGRES_PASSWORD: str = "fra_secure_pass"
    POSTGRES_DB: str = "fra_atlas_db"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ML Models
    DSS_MODEL_PATH: str = "./models/dss_model.pkl"
    OCR_LANGUAGE: str = "eng+hin+mar+guj+ory"
    
    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # MinIO/S3
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "fra-documents"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

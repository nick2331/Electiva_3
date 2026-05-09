from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "sqlite+aiosqlite:///./vehicleye.db"
    model_path: str = "ml/checkpoints/efficientnet_b0_vehicleye.pth"
    admin_key: str = "vehicleye-admin-2026"

    max_image_mb: int = 10
    max_video_seconds: int = 30
    confidence_threshold: float = 0.15
    history_limit: int = 10

    upload_dir: str = "uploads"
    reports_dir: str = "reports"
    gradcam_dir: str = "gradcam_cache"

    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:4173"]
    model_download_url: str = ""

    @field_validator("database_url", mode="before")
    @classmethod
    def fix_db_url(cls, v: str) -> str:
        # Render entrega postgresql:// pero SQLAlchemy async necesita postgresql+asyncpg://
        if isinstance(v, str) and v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        # También manejar postgres:// (alias antiguo de Render)
        if isinstance(v, str) and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        return v

    def model_post_init(self, __context):
        for d in (self.upload_dir, self.reports_dir, self.gradcam_dir):
            try:
                Path(d).mkdir(parents=True, exist_ok=True)
            except OSError:
                pass  # En entornos de solo lectura no bloqueamos el arranque


settings = Settings()

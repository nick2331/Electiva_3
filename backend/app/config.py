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

    cors_origins: list[str] = ["*"]
    model_download_url: str = ""

    # Groq API para clasificación de vehículos por visión (principal)
    groq_api_key: str = ""
    groq_vision_model: str = "llama-3.2-90b-vision-preview"
    groq_text_model: str = "llama-3.3-70b-versatile"
    groq_confidence_fallback: float = 0.50  # Si ONNX < 50%, confirma con Groq

    # API externa para clasificar vehículos sin entrenar modelo propio.
    #   external_api_provider: "huggingface" | "imagenet" | ""  (vacío = desactivado)
    #   huggingface_token:     token gratuito de huggingface.co (opcional para imagenet)
    #   huggingface_model:     modelo a usar (default: car_models_image_detection)
    external_api_provider: str = ""
    huggingface_token: str = ""
    huggingface_model: str = "dima806/car_models_image_detection"

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

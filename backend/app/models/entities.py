from sqlalchemy import String, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.models.database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    input_type: Mapped[str] = mapped_column(String(10))         # "image" | "video"
    predictions: Mapped[dict] = mapped_column(JSON)             # list of PredictionItem dicts
    description_es: Mapped[str] = mapped_column(Text)
    no_vehicle: Mapped[bool] = mapped_column(Boolean, default=False)
    suggestions: Mapped[list] = mapped_column(JSON, default=list)
    thumbnail_b64: Mapped[str | None] = mapped_column(Text, nullable=True)
    gradcam_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    report_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

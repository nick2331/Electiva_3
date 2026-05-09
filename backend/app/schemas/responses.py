from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PredictionItem(BaseModel):
    rank: int
    brand: str
    model: str
    confidence: float = Field(ge=0.0, le=1.0)


class AnalysisOut(BaseModel):
    analysis_id: str
    input_type: str
    predictions: list[PredictionItem]
    description_es: str
    no_vehicle: bool
    suggestions: list[str]
    gradcam_url: Optional[str] = None
    report_url: str
    created_at: datetime


class HistoryItem(BaseModel):
    analysis_id: str
    input_type: str
    top_brand: Optional[str] = None
    top_model: Optional[str] = None
    top_confidence: Optional[float] = None
    no_vehicle: bool
    thumbnail_b64: Optional[str] = None
    created_at: datetime


class HistoryListOut(BaseModel):
    items: list[HistoryItem]
    total: int


class DailyCount(BaseModel):
    date: str
    count: int


class TopModel(BaseModel):
    brand: str
    model: str
    count: int
    percentage: float


class StatsOut(BaseModel):
    daily_counts: list[DailyCount]
    top_models: list[TopModel]
    total_analyses: int
    total_images: int
    total_videos: int


class ErrorOut(BaseModel):
    detail: str
    suggestions: list[str] = []

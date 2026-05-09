from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import require_admin
from app.models.database import get_session
from app.models.entities import Analysis
from app.schemas.responses import DailyCount, StatsOut, TopModel

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.get("/stats", response_model=StatsOut)
async def get_stats(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Analysis).order_by(Analysis.created_at.desc()))
    analyses = result.scalars().all()

    # Análisis por día — últimos 30 días
    today = datetime.now(timezone.utc).date()
    day_counter: Counter = Counter()
    img_count = 0
    vid_count = 0
    model_counter: Counter = Counter()

    for a in analyses:
        d = a.created_at.date() if hasattr(a.created_at, "date") else today
        day_counter[d] += 1
        if a.input_type == "image":
            img_count += 1
        else:
            vid_count += 1
        if a.predictions and not a.no_vehicle:
            top = a.predictions[0]
            model_counter[(top["brand"], top["model"])] += 1

    daily_counts = []
    for i in range(29, -1, -1):
        d = today - timedelta(days=i)
        daily_counts.append(DailyCount(date=d.isoformat(), count=day_counter.get(d, 0)))

    total = len(analyses)
    top_models = []
    for (brand, model_name), count in model_counter.most_common(10):
        top_models.append(TopModel(
            brand=brand,
            model=model_name,
            count=count,
            percentage=round(count / total * 100, 1) if total else 0.0,
        ))

    return StatsOut(
        daily_counts=daily_counts,
        top_models=top_models,
        total_analyses=total,
        total_images=img_count,
        total_videos=vid_count,
    )


@router.get("/metrics")
async def download_metrics():
    """
    Descarga el PDF de métricas del modelo (matriz de confusión, P/R/F1, curvas).
    El archivo se genera en el script ml/evaluate.py y se ubica en reports/.
    """
    metrics_path = Path("reports/model_metrics.pdf")
    if not metrics_path.exists():
        metrics_path = Path("reports/model_metrics.txt")
    if not metrics_path.exists():
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Reporte de métricas no disponible. Ejecute ml/evaluate.py primero.",
        )
    media = "application/pdf" if metrics_path.suffix == ".pdf" else "text/plain"
    return FileResponse(str(metrics_path), media_type=media, filename="vehicleye_metrics.pdf")

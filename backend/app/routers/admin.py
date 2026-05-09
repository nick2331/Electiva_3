from __future__ import annotations

import re
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

import psutil
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import require_admin
from app.models.database import get_session, engine
from app.models.entities import Analysis
from app.schemas.responses import DailyCount, StatsOut, TopModel

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])

_START_TIME = time.time()


# ─── Stats ───────────────────────────────────────────────────────────────────

@router.get("/stats", response_model=StatsOut)
async def get_stats(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Analysis).order_by(Analysis.created_at.desc()))
    analyses = result.scalars().all()

    today = datetime.now(timezone.utc).date()
    day_counter: Counter = Counter()
    img_count = vid_count = 0
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

    daily_counts = [
        DailyCount(date=(today - timedelta(days=i)).isoformat(),
                   count=day_counter.get(today - timedelta(days=i), 0))
        for i in range(29, -1, -1)
    ]

    total = len(analyses)
    top_models = [
        TopModel(brand=b, model=m, count=c,
                 percentage=round(c / total * 100, 1) if total else 0.0)
        for (b, m), c in model_counter.most_common(10)
    ]

    return StatsOut(daily_counts=daily_counts, top_models=top_models,
                    total_analyses=total, total_images=img_count, total_videos=vid_count)


# ─── System Health ────────────────────────────────────────────────────────────

class ServiceStatus(BaseModel):
    status: str          # "ok" | "warning" | "error"
    message: str


class HealthOut(BaseModel):
    uptime_seconds: int
    database: ServiceStatus
    model: ServiceStatus
    memory: ServiceStatus
    memory_used_mb: float
    memory_total_mb: float
    memory_percent: float
    cpu_percent: float
    disk_used_mb: float
    disk_total_mb: float
    disk_percent: float


@router.get("/health", response_model=HealthOut)
async def system_health(db: AsyncSession = Depends(get_session)):
    uptime = int(time.time() - _START_TIME)

    # DB
    try:
        await db.execute(text("SELECT 1"))
        db_status = ServiceStatus(status="ok", message="Conexión activa")
    except Exception as e:
        db_status = ServiceStatus(status="error", message=str(e))

    # Modelo
    from app.services.classifier import _session as onnx_session
    if onnx_session is not None:
        model_status = ServiceStatus(status="ok", message="Modelo ONNX cargado en memoria")
    else:
        from pathlib import Path as _P
        from app.config import settings
        if _P(settings.model_path).with_suffix(".onnx").exists():
            model_status = ServiceStatus(status="warning", message="Modelo ONNX disponible (se cargará en primer análisis)")
        else:
            model_status = ServiceStatus(status="warning", message="Sin modelo entrenado — usando predicciones demo")

    # Memoria
    mem = psutil.virtual_memory()
    mem_used = mem.used / 1024 / 1024
    mem_total = mem.total / 1024 / 1024
    if mem.percent > 90:
        mem_status = ServiceStatus(status="error", message=f"Memoria crítica: {mem.percent:.0f}%")
    elif mem.percent > 75:
        mem_status = ServiceStatus(status="warning", message=f"Memoria elevada: {mem.percent:.0f}%")
    else:
        mem_status = ServiceStatus(status="ok", message=f"Memoria normal: {mem.percent:.0f}%")

    # Disco
    disk = psutil.disk_usage("/")
    disk_used = disk.used / 1024 / 1024
    disk_total = disk.total / 1024 / 1024

    return HealthOut(
        uptime_seconds=uptime,
        database=db_status,
        model=model_status,
        memory=mem_status,
        memory_used_mb=round(mem_used, 1),
        memory_total_mb=round(mem_total, 1),
        memory_percent=round(mem.percent, 1),
        cpu_percent=round(psutil.cpu_percent(interval=0.1), 1),
        disk_used_mb=round(disk_used, 1),
        disk_total_mb=round(disk_total, 1),
        disk_percent=round(disk.percent, 1),
    )


# ─── DB Query Executor ────────────────────────────────────────────────────────

_ALLOWED_STMT = re.compile(r"^\s*(SELECT|PRAGMA|EXPLAIN|WITH)\b", re.IGNORECASE)
_DANGEROUS    = re.compile(r"\b(DROP|DELETE|UPDATE|INSERT|ALTER|TRUNCATE|CREATE|GRANT|REVOKE)\b",
                            re.IGNORECASE)


class QueryIn(BaseModel):
    sql: str


class QueryOut(BaseModel):
    columns: list[str]
    rows: list[list]
    row_count: int
    message: str


@router.post("/db/query", response_model=QueryOut)
async def run_query(body: QueryIn, db: AsyncSession = Depends(get_session)):
    sql = body.sql.strip()

    if not _ALLOWED_STMT.match(sql):
        raise HTTPException(400, "Solo se permiten consultas SELECT / PRAGMA / EXPLAIN / WITH.")
    if _DANGEROUS.search(sql):
        raise HTTPException(400, "La consulta contiene operaciones no permitidas.")
    if len(sql) > 2000:
        raise HTTPException(400, "La consulta es demasiado larga (máx 2000 caracteres).")

    try:
        result = await db.execute(text(sql))
        rows = result.fetchmany(200)          # máximo 200 filas
        cols = list(result.keys()) if result.keys() else []
        return QueryOut(
            columns=cols,
            rows=[list(r) for r in rows],
            row_count=len(rows),
            message=f"{len(rows)} filas devueltas." + (" (limitado a 200)" if len(rows) == 200 else ""),
        )
    except Exception as e:
        raise HTTPException(400, f"Error en la consulta: {e}")


# ─── Metrics PDF ─────────────────────────────────────────────────────────────

@router.get("/metrics")
async def download_metrics():
    for ext in (".pdf", ".txt"):
        p = Path(f"reports/model_metrics{ext}")
        if p.exists():
            media = "application/pdf" if ext == ".pdf" else "text/plain"
            return FileResponse(str(p), media_type=media, filename=f"vehicleye_metrics{ext}")
    raise HTTPException(404, "Reporte de métricas no disponible. Ejecute ml/evaluate.py primero.")

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
from app.models.database import get_session
from app.models.entities import Analysis
from app.schemas.responses import DailyCount, StatsOut, TopModel

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])

_START_TIME = time.time()


# ─── Stats ────────────────────────────────────────────────────────────────────

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
        DailyCount(
            date=(today - timedelta(days=i)).isoformat(),
            count=day_counter.get(today - timedelta(days=i), 0),
        )
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


# ─── Health ───────────────────────────────────────────────────────────────────

class ServiceStatus(BaseModel):
    status: str
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


def _model_status() -> ServiceStatus:
    from app.config import settings as _s
    from app.services.classifier import _session, _onnx_path
    if _session is not None:
        return ServiceStatus(status="ok", message="Modelo ONNX cargado en memoria")
    if _onnx_path().exists():
        return ServiceStatus(status="warning",
                             message="Modelo ONNX disponible — se carga en el primer análisis")
    provider = (getattr(_s, "external_api_provider", "") or "").lower()
    if provider == "huggingface":
        model = getattr(_s, "huggingface_model", "")
        token = "✓" if getattr(_s, "huggingface_token", "") else "✗ (sin token)"
        return ServiceStatus(status="ok",
                             message=f"API externa Hugging Face: {model} · token {token}")
    if provider == "imagenet":
        return ServiceStatus(status="ok",
                             message="API externa ImageNet (microsoft/resnet-50) activa")
    return ServiceStatus(status="warning",
                         message="Sin modelo entrenado — predicciones demo activas")


@router.get("/health", response_model=HealthOut)
async def system_health(db: AsyncSession = Depends(get_session)):
    uptime = int(time.time() - _START_TIME)

    # DB
    try:
        await db.execute(text("SELECT 1"))
        db_status = ServiceStatus(status="ok", message="Conexión activa")
    except Exception as exc:
        db_status = ServiceStatus(status="error", message=str(exc)[:120])

    # Modelo
    model_status = _model_status()

    # Recursos — cpu_percent con interval=None no bloquea el event loop
    mem = psutil.virtual_memory()
    mem_used = mem.used / 1024 / 1024
    mem_total = mem.total / 1024 / 1024

    if mem.percent > 90:
        mem_status = ServiceStatus(status="error",   message=f"Crítica: {mem.percent:.0f} %")
    elif mem.percent > 75:
        mem_status = ServiceStatus(status="warning", message=f"Elevada: {mem.percent:.0f} %")
    else:
        mem_status = ServiceStatus(status="ok",      message=f"Normal: {mem.percent:.0f} %")

    disk = psutil.disk_usage("/")

    return HealthOut(
        uptime_seconds=uptime,
        database=db_status,
        model=model_status,
        memory=mem_status,
        memory_used_mb=round(mem_used, 1),
        memory_total_mb=round(mem_total, 1),
        memory_percent=round(float(mem.percent), 1),
        cpu_percent=round(float(psutil.cpu_percent(interval=None)), 1),
        disk_used_mb=round(disk.used / 1024 / 1024, 1),
        disk_total_mb=round(disk.total / 1024 / 1024, 1),
        disk_percent=round(float(disk.percent), 1),
    )


# ─── DB Query Executor ────────────────────────────────────────────────────────

_ALLOWED = re.compile(r"^\s*(SELECT|PRAGMA|EXPLAIN|WITH)\b", re.IGNORECASE)
_BLOCKED  = re.compile(
    r"\b(DROP|DELETE|UPDATE|INSERT|ALTER|TRUNCATE|CREATE|GRANT|REVOKE)\b",
    re.IGNORECASE,
)


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

    if not _ALLOWED.match(sql):
        raise HTTPException(400, "Solo se permiten SELECT / PRAGMA / EXPLAIN / WITH.")
    if _BLOCKED.search(sql):
        raise HTTPException(400, "La consulta contiene operaciones no permitidas.")
    if len(sql) > 2000:
        raise HTTPException(400, "Consulta demasiado larga (máx 2000 caracteres).")

    try:
        cursor = await db.execute(text(sql))
        # keys() debe llamarse antes de fetchmany() en algunos drivers
        cols = list(cursor.keys())
        rows = cursor.fetchmany(200)
        n = len(rows)
        return QueryOut(
            columns=cols,
            rows=[list(r) for r in rows],
            row_count=n,
            message=f"{n} fila(s) devuelta(s)." + (" Limitado a 200." if n == 200 else ""),
        )
    except Exception as exc:
        raise HTTPException(400, f"Error en la consulta: {exc}")


# ─── Metrics ─────────────────────────────────────────────────────────────────

@router.get("/metrics")
async def download_metrics():
    for ext in (".pdf", ".txt"):
        p = Path(f"reports/model_metrics{ext}")
        if p.exists():
            media = "application/pdf" if ext == ".pdf" else "text/plain"
            return FileResponse(str(p), media_type=media, filename=f"vehicleye_metrics{ext}")
    raise HTTPException(404, "Ejecute ml/evaluate.py para generar el reporte.")


# ─── Groq Diagnostics ────────────────────────────────────────────────────────

@router.get("/groq-test")
async def groq_test(_: str = Depends(require_admin)):
    """Prueba la conexión con Groq y devuelve el estado detallado."""
    from app.config import settings as _s
    import urllib.request, urllib.error, json

    key = getattr(_s, "groq_api_key", "")
    if not key:
        return {"configured": False, "error": "GROQ_API_KEY no configurada en Render"}

    model = getattr(_s, "groq_vision_model", "llama-3.2-11b-vision-preview")

    # Prueba con un prompt de texto simple (sin imagen) para verificar conectividad
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Responde solo: ok"}],
        "max_tokens": 5,
    }
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            reply = data["choices"][0]["message"]["content"]
            return {
                "configured": True,
                "model": model,
                "key_prefix": key[:8] + "...",
                "response": reply,
                "status": "OK - Groq conectado y funcionando",
            }
    except urllib.error.HTTPError as exc:
        body_err = exc.read().decode(errors="ignore")
        return {"configured": True, "model": model, "http_error": exc.code, "detail": body_err[:400]}
    except Exception as exc:
        return {"configured": True, "model": model, "error": str(exc)}

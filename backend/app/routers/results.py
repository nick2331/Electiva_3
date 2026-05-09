from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.database import get_session
from app.models.entities import Analysis
from app.schemas.responses import AnalysisOut, PredictionItem

router = APIRouter(prefix="/results", tags=["results"])


def _to_out(analysis: Analysis) -> AnalysisOut:
    preds = [PredictionItem(**p) for p in analysis.predictions]
    base = "http://localhost:8000/api/v1"
    return AnalysisOut(
        analysis_id=analysis.id,
        input_type=analysis.input_type,
        predictions=preds,
        description_es=analysis.description_es,
        no_vehicle=analysis.no_vehicle,
        suggestions=analysis.suggestions,
        gradcam_url=f"{base}/results/{analysis.id}/gradcam" if analysis.gradcam_filename else None,
        report_url=f"{base}/results/{analysis.id}/report",
        created_at=analysis.created_at,
    )


async def _get_or_404(analysis_id: str, db: AsyncSession) -> Analysis:
    result = await db.execute(select(Analysis).where(Analysis.id == analysis_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="Análisis no encontrado.")
    return obj


@router.get("/{analysis_id}", response_model=AnalysisOut)
async def get_result(analysis_id: str, db: AsyncSession = Depends(get_session)):
    return _to_out(await _get_or_404(analysis_id, db))


@router.get("/{analysis_id}/report")
async def download_report(analysis_id: str, db: AsyncSession = Depends(get_session)):
    analysis = await _get_or_404(analysis_id, db)
    if not analysis.report_filename:
        raise HTTPException(status_code=404, detail="Reporte no generado aún.")
    path = Path(settings.reports_dir) / analysis.report_filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Archivo de reporte no encontrado en disco.")
    media = "application/pdf" if path.suffix == ".pdf" else "text/plain"
    return FileResponse(str(path), media_type=media, filename=f"vehicleye_{analysis_id[:8]}.pdf")


@router.get("/{analysis_id}/gradcam")
async def get_gradcam(analysis_id: str, db: AsyncSession = Depends(get_session)):
    analysis = await _get_or_404(analysis_id, db)
    if not analysis.gradcam_filename:
        raise HTTPException(status_code=404, detail="Mapa Grad-CAM no disponible para este análisis.")
    path = Path(settings.gradcam_dir) / analysis.gradcam_filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Archivo Grad-CAM no encontrado en disco.")
    return FileResponse(str(path), media_type="image/png")

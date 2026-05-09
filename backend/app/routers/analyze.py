from __future__ import annotations

import base64
import io
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, Request, UploadFile, status
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.config import settings
from app.models.database import get_session
from app.models.entities import Analysis
from app.schemas.responses import AnalysisOut, PredictionItem
from app.services.classifier import predict_bytes, VEHICLE_CLASSES
from app.services.description import build_description, build_suggestions
from app.services.gradcam import generate_gradcam
from app.services.pdf_gen import generate_pdf
from app.services.video import process_video

router = APIRouter(prefix="/analyze", tags=["analyze"])

_ALLOWED_IMAGE = {"image/jpeg", "image/png"}
_ALLOWED_VIDEO = {"video/mp4", "video/mpeg", "video/quicktime"}


def _pil_to_b64(img: Image.Image, size: tuple[int, int] = (128, 80)) -> str:
    thumb = img.copy()
    thumb.thumbnail(size)
    buf = io.BytesIO()
    thumb.save(buf, format="JPEG", quality=70)
    return base64.b64encode(buf.getvalue()).decode()


def _build_analysis_out(analysis: Analysis, base_url: str) -> AnalysisOut:
    preds = [PredictionItem(**p) for p in analysis.predictions]
    base = base_url.rstrip("/")
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


@router.post("/image", response_model=AnalysisOut, status_code=status.HTTP_201_CREATED)
async def analyze_image(
    request: Request,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
):
    if file.content_type not in _ALLOWED_IMAGE:
        raise HTTPException(
            status_code=400,
            detail="Formato no soportado. Use JPG o PNG.",
        )

    content = await file.read()
    if len(content) > settings.max_image_mb * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"El archivo supera el límite de {settings.max_image_mb} MB.",
        )

    predictions_raw = predict_bytes(content)
    no_vehicle = (not predictions_raw) or (predictions_raw[0].confidence < settings.confidence_threshold)

    preds_dicts = [p._asdict() for p in predictions_raw]
    description = build_description(predictions_raw, "image")
    suggestions = build_suggestions(predictions_raw)

    pil_img = Image.open(io.BytesIO(content)).convert("RGB")
    thumbnail_b64 = _pil_to_b64(pil_img)

    analysis_id = str(uuid.uuid4())

    gradcam_filename: str | None = None
    if not no_vehicle and predictions_raw:
        top_idx = next(
            i for i, (b, m) in enumerate(VEHICLE_CLASSES)
            if b == predictions_raw[0].brand and m == predictions_raw[0].model
        )
        try:
            gradcam_filename = generate_gradcam(content, top_idx)
        except Exception:
            gradcam_filename = None

    preds_items = [PredictionItem(**p) for p in preds_dicts]
    try:
        report_filename = generate_pdf(
            analysis_id=analysis_id,
            input_type="image",
            predictions=preds_items,
            description_es=description,
            no_vehicle=no_vehicle,
            thumbnail_b64=thumbnail_b64,
        )
    except Exception:
        report_filename = None

    analysis = Analysis(
        id=analysis_id,
        input_type="image",
        predictions=preds_dicts,
        description_es=description,
        no_vehicle=no_vehicle,
        suggestions=suggestions,
        thumbnail_b64=thumbnail_b64,
        gradcam_filename=gradcam_filename,
        report_filename=report_filename,
    )
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)

    base_url = str(request.base_url).rstrip("/") + "/api/v1"
    return _build_analysis_out(analysis, base_url)


@router.post("/video", response_model=AnalysisOut, status_code=status.HTTP_201_CREATED)
async def analyze_video(
    request: Request,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
):
    if file.content_type not in _ALLOWED_VIDEO:
        raise HTTPException(
            status_code=400,
            detail="Formato no soportado. Use MP4.",
        )

    content = await file.read()

    predictions_raw, thumbnail_pil = process_video(content)
    no_vehicle = (not predictions_raw) or (predictions_raw[0].confidence < settings.confidence_threshold)

    preds_dicts = [p._asdict() for p in predictions_raw]
    description = build_description(predictions_raw, "video")
    suggestions = build_suggestions(predictions_raw)

    thumbnail_b64 = _pil_to_b64(thumbnail_pil) if thumbnail_pil else None
    analysis_id = str(uuid.uuid4())

    preds_items = [PredictionItem(**p) for p in preds_dicts]
    try:
        report_filename = generate_pdf(
            analysis_id=analysis_id,
            input_type="video",
            predictions=preds_items,
            description_es=description,
            no_vehicle=no_vehicle,
            thumbnail_b64=thumbnail_b64,
        )
    except Exception:
        report_filename = None

    analysis = Analysis(
        id=analysis_id,
        input_type="video",
        predictions=preds_dicts,
        description_es=description,
        no_vehicle=no_vehicle,
        suggestions=suggestions,
        thumbnail_b64=thumbnail_b64,
        gradcam_filename=None,
        report_filename=report_filename,
    )
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)

    base_url = str(request.base_url).rstrip("/") + "/api/v1"
    return _build_analysis_out(analysis, base_url)

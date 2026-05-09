from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import get_session
from app.models.entities import Analysis
from app.schemas.responses import HistoryItem, HistoryListOut

router = APIRouter(prefix="/history", tags=["history"])


def _to_item(a: Analysis) -> HistoryItem:
    top = a.predictions[0] if a.predictions else None
    return HistoryItem(
        analysis_id=a.id,
        input_type=a.input_type,
        top_brand=top["brand"] if top else None,
        top_model=top["model"] if top else None,
        top_confidence=top["confidence"] if top else None,
        no_vehicle=a.no_vehicle,
        thumbnail_b64=a.thumbnail_b64,
        created_at=a.created_at,
    )


@router.get("", response_model=HistoryListOut)
async def list_history(
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_session),
):
    q = select(Analysis).order_by(Analysis.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(q)
    analyses = result.scalars().all()

    count_q = select(func.count()).select_from(Analysis)
    total = (await db.execute(count_q)).scalar_one()

    return HistoryListOut(items=[_to_item(a) for a in analyses], total=total)


@router.delete("/{analysis_id}", status_code=204)
async def delete_history_entry(analysis_id: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Analysis).where(Analysis.id == analysis_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="Entrada no encontrada.")
    await db.execute(delete(Analysis).where(Analysis.id == analysis_id))
    await db.commit()

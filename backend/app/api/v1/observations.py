from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.observation import Observation
from app.models.series import Series
from app.schemas.common import ResponseMetadata
from app.schemas.observation import ObservationListResponse, ObservationPoint
from app.services.series_registry import resolve_series_code

router = APIRouter(tags=["observations"])


@router.get("/series/{code}/observations", response_model=ObservationListResponse)
async def get_observations(
    code: str,
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    limit: int = Query(default=1000, ge=1, le=5000),
    session: AsyncSession = Depends(get_session),
) -> ObservationListResponse:
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date cannot be after end_date.")

    series = await session.scalar(select(Series).where(Series.code == resolve_series_code(code)))
    if series is None:
        raise HTTPException(status_code=404, detail=f"Series not found: {code}")

    statement = select(Observation).where(Observation.series_id == series.id)
    if start_date:
        statement = statement.where(Observation.date >= start_date)
    if end_date:
        statement = statement.where(Observation.date <= end_date)

    rows = (
        await session.execute(statement.order_by(Observation.date.desc()).limit(limit))
    ).scalars().all()
    rows.reverse()
    points = [
        ObservationPoint(date=observation.date, value=float(observation.value))
        for observation in rows
    ]
    return ObservationListResponse(
        series_code=series.code,
        count=len(points),
        observations=points,
        data=points,
        metadata=ResponseMetadata(
            source=series.source,
            last_updated=series.last_updated,
            demo_mode=series.fetch_status == "demo_seed",
            warnings=[] if points else ["No observations matched the request."],
        ),
        source=series.source,
        last_updated=points[-1].date if points else None,
        warnings=[] if points else ["No observations matched the request."],
    )

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.observation import Observation
from app.models.series import Series
from app.schemas.common import ResponseMetadata
from app.schemas.dashboard import CompareResponse, CompareSeriesItem
from app.schemas.observation import ObservationPoint
from app.schemas.series import SeriesResponse
from app.services.data_cleaner import normalize_points
from app.services.series_registry import resolve_series_code

router = APIRouter(tags=["compare"])


@router.get("/compare", response_model=CompareResponse)
async def compare_series(
    series: str = Query(..., description="Comma separated codes, e.g. USDTRY,CPI"),
    normalize: bool = Query(default=True),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> CompareResponse:
    codes = [resolve_series_code(item) for item in series.split(",") if item.strip()]
    if len(codes) < 2:
        raise HTTPException(status_code=400, detail="At least two series codes are required.")
    if len(codes) > 6:
        raise HTTPException(status_code=400, detail="Compare supports up to 6 series.")

    response_items: list[CompareSeriesItem] = []
    for code in codes:
        series_row = await session.scalar(select(Series).where(Series.code == code))
        if series_row is None:
            raise HTTPException(status_code=404, detail=f"Series not found: {code}")

        statement = select(Observation).where(Observation.series_id == series_row.id)
        if start_date:
            statement = statement.where(Observation.date >= start_date)
        if end_date:
            statement = statement.where(Observation.date <= end_date)

        rows = (
            await session.execute(statement.order_by(Observation.date).limit(2000))
        ).scalars().all()
        points = [{"date": item.date, "value": float(item.value)} for item in rows]
        if normalize:
            points = normalize_points(points)

        response_items.append(
            CompareSeriesItem(
                series=SeriesResponse.model_validate(series_row),
                observations=[
                    ObservationPoint(date=point["date"], value=point["value"])
                    for point in points
                ],
            )
        )

    last_updated = await session.scalar(select(func.max(Series.last_updated)))
    warnings = [
        f"{item.series.code}: no observations matched the request"
        for item in response_items
        if not item.observations
    ]
    demo_mode = any(item.series.fetch_status == "demo_seed" for item in response_items)
    if demo_mode:
        warnings.append("Demo seed data is active.")
    return CompareResponse(
        normalized=normalize,
        series=response_items,
        data=response_items,
        metadata=ResponseMetadata(
            source="postgresql",
            last_updated=last_updated,
            demo_mode=demo_mode,
            warnings=warnings,
        ),
        last_updated=last_updated,
        warnings=warnings,
    )

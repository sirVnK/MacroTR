from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_session
from app.models.observation import Observation
from app.models.series import Series
from app.schemas.common import ResponseMetadata
from app.schemas.observation import LatestObservationResponse, ObservationPoint
from app.schemas.series import SeriesDetailResponse, SeriesListResponse, SeriesResponse
from app.services.series_registry import resolve_series_code

router = APIRouter(prefix="/series", tags=["series"])


@router.get("", response_model=SeriesListResponse)
async def list_series(
    category: str | None = Query(default=None),
    search: str | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> SeriesListResponse:
    statement = select(Series).where(Series.is_active.is_(True))
    if category:
        statement = statement.where(Series.category == category)
    if search:
        pattern = f"%{search}%"
        statement = statement.where(
            or_(
                Series.code.ilike(pattern),
                Series.name.ilike(pattern),
                Series.description.ilike(pattern),
            )
        )

    rows = (
        await session.execute(statement.order_by(Series.category, Series.name))
    ).scalars().all()
    items = [SeriesResponse.model_validate(row) for row in rows]
    last_updated = await session.scalar(select(func.max(Series.last_updated)))
    demo_mode = any(row.fetch_status == "demo_seed" for row in rows)
    metadata = ResponseMetadata(
        source="postgresql",
        last_updated=last_updated,
        demo_mode=demo_mode,
        warnings=["Demo seed data is active."] if demo_mode else [],
    )
    return SeriesListResponse(
        count=len(items),
        items=items,
        data=items,
        metadata=metadata,
        last_updated=last_updated,
        warnings=metadata.warnings,
    )


@router.get("/{code}", response_model=SeriesDetailResponse)
async def get_series(
    code: str,
    limit: int = Query(default=120, ge=1, le=2000),
    session: AsyncSession = Depends(get_session),
) -> SeriesDetailResponse:
    series = await _get_series_or_404(session, code)
    latest = await _latest_observation(session, series)
    observations = await _observations(session, series, limit)
    return SeriesDetailResponse(
        **SeriesResponse.model_validate(series).model_dump(),
        latest=latest,
        observations=observations,
        data={"latest": latest, "observations": observations},
        metadata=ResponseMetadata(
            source=series.source,
            last_updated=series.last_updated,
            demo_mode=series.fetch_status == "demo_seed",
            warnings=[] if observations else ["No observations are stored for this series."],
        ),
        warnings=[] if observations else ["No observations are stored for this series."],
    )


@router.get("/{code}/latest", response_model=LatestObservationResponse)
async def get_latest(
    code: str,
    session: AsyncSession = Depends(get_session),
) -> LatestObservationResponse:
    series = await _get_series_or_404(session, code)
    return await _latest_observation(session, series)


async def _get_series_or_404(session: AsyncSession, code: str) -> Series:
    series = await session.scalar(
        select(Series)
        .options(selectinload(Series.observations))
        .where(Series.code == resolve_series_code(code))
    )
    if series is None:
        raise HTTPException(status_code=404, detail=f"Series not found: {code}")
    return series


async def _latest_observation(
    session: AsyncSession,
    series: Series,
) -> LatestObservationResponse:
    observation = await session.scalar(
        select(Observation)
        .where(Observation.series_id == series.id)
        .order_by(Observation.date.desc())
        .limit(1)
    )
    if observation is None:
        return LatestObservationResponse(
            series_code=series.code,
            date=None,
            value=None,
            metadata=ResponseMetadata(
                source=series.source,
                last_updated=series.last_updated,
                demo_mode=series.fetch_status == "demo_seed",
                warnings=["No latest observation is available."],
            ),
            warnings=["No latest observation is available."],
        )
    point = ObservationPoint(date=observation.date, value=float(observation.value))
    return LatestObservationResponse(
        series_code=series.code,
        date=observation.date,
        value=float(observation.value),
        source=observation.source,
        data=point,
        metadata=ResponseMetadata(
            source=observation.source,
            last_updated=series.last_updated,
            demo_mode=series.fetch_status == "demo_seed",
        ),
        last_updated=observation.date,
    )


async def _observations(
    session: AsyncSession,
    series: Series,
    limit: int,
) -> list[ObservationPoint]:
    rows = (
        await session.execute(
            select(Observation)
            .where(Observation.series_id == series.id)
            .order_by(Observation.date.desc())
            .limit(limit)
        )
    ).scalars().all()
    rows.reverse()
    return [
        ObservationPoint(date=observation.date, value=float(observation.value))
        for observation in rows
    ]

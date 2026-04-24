from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.observation import Observation
from app.models.series import Series
from app.schemas.common import ResponseMetadata
from app.schemas.dashboard import DashboardSummaryResponse, IndicatorSummary
from app.schemas.observation import ObservationPoint
from app.schemas.series import SeriesResponse
from app.services.series_registry import DISCLAIMER_TEXT

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse)
async def dashboard_summary(
    session: AsyncSession = Depends(get_session),
) -> DashboardSummaryResponse:
    series_rows = (
        await session.execute(
            select(Series)
            .where(Series.is_active.is_(True))
            .order_by(Series.category, Series.name)
        )
    ).scalars().all()

    indicators: list[IndicatorSummary] = []
    for series in series_rows:
        observations = (
            await session.execute(
                select(Observation)
                .where(Observation.series_id == series.id)
                .order_by(Observation.date.desc())
                .limit(48)
            )
        ).scalars().all()
        observations.reverse()

        latest = observations[-1] if observations else None
        previous = observations[-2] if len(observations) >= 2 else None
        latest_value = float(latest.value) if latest else None
        previous_value = float(previous.value) if previous else None
        change_percent = _change_percent(latest_value, previous_value)
        sparkline = [
            ObservationPoint(date=item.date, value=float(item.value))
            for item in observations
        ]

        indicators.append(
            IndicatorSummary(
                series=SeriesResponse.model_validate(series),
                latest_date=latest.date.isoformat() if latest else None,
                latest_value=latest_value,
                previous_value=previous_value,
                change_percent=change_percent,
                sparkline=sparkline,
            )
        )

    last_updated = await session.scalar(select(func.max(Series.last_updated)))
    demo_mode = any(series.fetch_status == "demo_seed" for series in series_rows)
    return DashboardSummaryResponse(
        generated_at=datetime.now(UTC),
        disclaimer=DISCLAIMER_TEXT,
        indicators=indicators,
        data=indicators,
        metadata=ResponseMetadata(
            source="postgresql",
            last_updated=last_updated,
            demo_mode=demo_mode,
            warnings=["Demo seed data is active."] if demo_mode else [],
        ),
        last_updated=last_updated,
        warnings=["Demo seed data is active."] if demo_mode else [],
    )


def _change_percent(latest: float | None, previous: float | None) -> float | None:
    if latest is None or previous in (None, 0):
        return None
    return round(((latest - previous) / previous) * 100, 4)

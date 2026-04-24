from __future__ import annotations

from datetime import UTC, date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_session
from app.schemas.common import ResponseMetadata
from app.schemas.dashboard import FetchDataResponse
from app.services.evds_service import EVDSConfigurationError, evds_service
from app.services.series_registry import (
    resolve_series_code,
    seed_sample_observations,
    seed_series,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/fetch-data", response_model=FetchDataResponse)
async def fetch_data(
    series: str | None = Query(default=None, description="Comma separated MacroTR codes"),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> FetchDataResponse:
    settings = get_settings()
    if settings.is_production:
        raise HTTPException(
            status_code=403,
            detail="Local/dev fetch endpoint is disabled in production.",
        )

    await seed_series(session)
    codes = [resolve_series_code(item) for item in series.split(",")] if series else None

    try:
        result = await evds_service.fetch_and_store(
            session=session,
            series_codes=codes,
            start_date=start_date,
            end_date=end_date,
        )
        return FetchDataResponse(
            mode="evds",
            fetched_series=result.fetched_series,
            inserted_observations=result.upserted_observations,
            detail="EVDS data fetched and stored.",
            data={
                "empty_series": result.empty_series,
                "failed_series": result.failed_series,
            },
            metadata=ResponseMetadata(
                source="TCMB EVDS",
                last_updated=datetime.now(UTC),
                demo_mode=False,
                warnings=result.warnings,
                errors=result.errors,
            ),
            last_updated=datetime.now(UTC),
            warnings=result.warnings,
            errors=result.errors,
        )
    except EVDSConfigurationError:
        inserted = await seed_sample_observations(session, settings.sample_years)
        return FetchDataResponse(
            mode="demo-seed",
            fetched_series=0,
            inserted_observations=inserted,
            detail="EVDS_API_KEY is missing; local demo observations are available.",
            data={"fallback": "demo-seed"},
            metadata=ResponseMetadata(
                source="local-demo",
                last_updated=datetime.now(UTC),
                demo_mode=True,
                warnings=["EVDS_API_KEY is not configured."],
            ),
            source="local-demo",
            last_updated=datetime.now(UTC),
            warnings=["EVDS_API_KEY is not configured."],
        )

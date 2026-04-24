from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.observation import Observation
from app.models.series import Series
from app.services.data_cleaner import clean_observations

logger = logging.getLogger(__name__)


class EVDSConfigurationError(RuntimeError):
    pass


@dataclass
class FetchResult:
    fetched_series: int = 0
    upserted_observations: int = 0
    empty_series: list[str] = field(default_factory=list)
    failed_series: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class EVDSService:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def fetch_series(
        self,
        evds_code: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[tuple[date, Decimal]]:
        if not self.settings.evds_api_key:
            raise EVDSConfigurationError("EVDS_API_KEY is not configured.")

        end = end_date or date.today()
        start = start_date or (end - timedelta(days=365 * 5))
        url = self._build_series_url(evds_code, start, end)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            payload = response.json()

        rows = payload.get("items", [])
        if not isinstance(rows, list):
            logger.warning("Unexpected EVDS response for %s", evds_code)
            return []

        return clean_observations(rows, evds_code)

    async def fetch_and_store(
        self,
        session: AsyncSession,
        series_codes: list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> FetchResult:
        if not self.settings.evds_api_key:
            raise EVDSConfigurationError("EVDS_API_KEY is not configured.")

        statement = select(Series).where(Series.is_active.is_(True))
        if series_codes:
            statement = statement.where(Series.code.in_(series_codes))

        series_rows = (await session.execute(statement)).scalars().all()
        result = FetchResult()

        for series in series_rows:
            now = datetime.now(UTC)
            series.last_fetch_attempt = now
            series.fetch_status = "fetching"
            series.fetch_error = None
            await session.flush()

            try:
                observations = await self.fetch_series(series.evds_code, start_date, end_date)
            except httpx.HTTPStatusError as exc:
                series.fetch_status = "error"
                series.fetch_error = f"EVDS HTTP {exc.response.status_code}"
                result.failed_series.append(series.code)
                result.errors.append(f"{series.code}: {series.fetch_error}")
                logger.warning("EVDS fetch failed for %s: %s", series.code, exc)
                continue
            except Exception as exc:
                series.fetch_status = "error"
                series.fetch_error = str(exc)
                result.failed_series.append(series.code)
                result.errors.append(f"{series.code}: {exc}")
                logger.warning("EVDS fetch failed for %s: %s", series.code, exc)
                continue

            if not observations:
                series.fetch_status = "empty"
                series.fetch_error = "EVDS returned no observations for the selected range."
                result.empty_series.append(series.code)
                result.warnings.append(f"{series.code}: empty EVDS response")
                continue

            result.fetched_series += 1
            for observed_at, value in observations:
                existing = await session.scalar(
                    select(Observation).where(
                        Observation.series_id == series.id,
                        Observation.date == observed_at,
                    )
                )
                if existing:
                    existing.value = value
                    existing.source = "TCMB EVDS"
                else:
                    session.add(
                        Observation(
                            series_id=series.id,
                            date=observed_at,
                            value=value,
                            source="TCMB EVDS",
                        )
                    )
                result.upserted_observations += 1

            series.last_updated = datetime.now(UTC)
            series.last_successful_fetch = series.last_updated
            series.fetch_status = "success"
            series.fetch_error = None

        await session.commit()
        return result

    def _build_series_url(self, evds_code: str, start_date: date, end_date: date) -> str:
        base = self.settings.evds_base_url.rstrip("/")
        start = start_date.strftime("%d-%m-%Y")
        end = end_date.strftime("%d-%m-%Y")
        return (
            f"{base}/series={evds_code}"
            f"&startDate={start}"
            f"&endDate={end}"
            f"&type=json"
            f"&key={self.settings.evds_api_key}"
        )


evds_service = EVDSService()

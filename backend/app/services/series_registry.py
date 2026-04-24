from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.observation import Observation
from app.models.series import Series


@dataclass(frozen=True)
class RegistrySeries:
    code: str
    evds_code: str
    name: str
    description: str
    source: str
    frequency: str
    unit: str
    category: str
    base_value: float
    slope: float
    amplitude: float


DEFAULT_SERIES: tuple[RegistrySeries, ...] = (
    RegistrySeries(
        code="USDTRY",
        evds_code="TP.DK.USD.A.YTL",
        name="USD/TRY",
        description="TCMB EVDS ABD doları döviz alış kuru.",
        source="TCMB EVDS",
        frequency="daily",
        unit="TRY",
        category="exchange_rate",
        base_value=13.5,
        slope=0.022,
        amplitude=0.55,
    ),
    RegistrySeries(
        code="EURTRY",
        evds_code="TP.DK.EUR.A.YTL",
        name="EUR/TRY",
        description="TCMB EVDS euro döviz alış kuru.",
        source="TCMB EVDS",
        frequency="daily",
        unit="TRY",
        category="exchange_rate",
        base_value=15.2,
        slope=0.025,
        amplitude=0.65,
    ),
    RegistrySeries(
        code="POLICY_RATE",
        evds_code="TP.TRF.YIL.P14",
        name="Politika faizi",
        description="TCMB politika faizi göstergesi için EVDS seri tanımı.",
        source="TCMB EVDS",
        frequency="monthly",
        unit="%",
        category="interest_rate",
        base_value=14.0,
        slope=0.022,
        amplitude=4.0,
    ),
    RegistrySeries(
        code="CPI",
        evds_code="TP.TUFE1YI.T1",
        name="TÜFE yıllık değişim",
        description="Tüketici fiyat endeksi yıllık yüzde değişim serisi.",
        source="TCMB EVDS",
        frequency="monthly",
        unit="%",
        category="inflation",
        base_value=36.0,
        slope=-0.005,
        amplitude=8.5,
    ),
    RegistrySeries(
        code="PPI",
        evds_code="TP.TFYI01",
        name="Yİ-ÜFE yıllık değişim",
        description="Yurt içi üretici fiyat endeksi yıllık yüzde değişim serisi.",
        source="TCMB EVDS",
        frequency="monthly",
        unit="%",
        category="inflation",
        base_value=45.0,
        slope=-0.012,
        amplitude=10.0,
    ),
    RegistrySeries(
        code="UNEMPLOYMENT",
        evds_code="TP.TG2.Y01",
        name="İşsizlik oranı",
        description="İşgücü piyasası için EVDS üzerinden takip edilen gösterge.",
        source="TCMB EVDS",
        frequency="monthly",
        unit="%",
        category="labor",
        base_value=10.8,
        slope=-0.001,
        amplitude=0.8,
    ),
    RegistrySeries(
        code="INDUSTRIAL_PRODUCTION",
        evds_code="TP.SANAYREV4.Y1",
        name="Sanayi üretim endeksi",
        description="Toplam sanayi üretim endeksi göstergesi.",
        source="TCMB EVDS",
        frequency="monthly",
        unit="Index",
        category="production",
        base_value=118.0,
        slope=0.045,
        amplitude=5.5,
    ),
    RegistrySeries(
        code="CURRENT_ACCOUNT",
        evds_code="TP.ODEAYRSUNUM6.Q1",
        name="Cari denge",
        description="Ödemeler dengesi cari işlemler hesabı göstergesi.",
        source="TCMB EVDS",
        frequency="monthly",
        unit="Million USD",
        category="external_balance",
        base_value=-2500.0,
        slope=-0.9,
        amplitude=2100.0,
    ),
    RegistrySeries(
        code="GROSS_RESERVES",
        evds_code="TP.AB.A02",
        name="TCMB brüt rezervleri",
        description="TCMB rezerv göstergesi için EVDS uyumlu seri.",
        source="TCMB EVDS",
        frequency="weekly",
        unit="Million USD",
        category="reserves",
        base_value=82000.0,
        slope=24.0,
        amplitude=4500.0,
    ),
    RegistrySeries(
        code="BIST100",
        evds_code="TP.MK.F.BILESIK",
        name="BIST 100",
        description="BIST 100 fiyat endeksi kapanış değeri.",
        source="TCMB EVDS",
        frequency="daily",
        unit="Index",
        category="market",
        base_value=2100.0,
        slope=4.8,
        amplitude=260.0,
    ),
)

SERIES_ALIASES = {
    "INFLATION": "CPI",
    "POLICY-RATE": "POLICY_RATE",
    "POLICY_RATE": "POLICY_RATE",
    "USD-TRY": "USDTRY",
    "EUR-TRY": "EURTRY",
}


DISCLAIMER_TEXT = (
    "Bu proje yalnızca eğitim ve bilgilendirme amacıyla geliştirilmiştir. "
    "Yatırım tavsiyesi, alım-satım önerisi veya finansal danışmanlık hizmeti sunmaz. "
    "Veriler halka açık veya üçüncü taraf kaynaklardan alınır ve doğruluğu garanti edilmez."
)


async def seed_series(session: AsyncSession) -> int:
    inserted = 0
    for item in DEFAULT_SERIES:
        existing = await session.scalar(select(Series).where(Series.code == item.code))
        if existing is None:
            session.add(
                Series(
                    code=item.code,
                    evds_code=item.evds_code,
                    name=item.name,
                    description=item.description,
                    source=item.source,
                    frequency=item.frequency,
                    unit=item.unit,
                    category=item.category,
                    fetch_status="not_fetched",
                )
            )
            inserted += 1
        else:
            existing.evds_code = item.evds_code
            existing.name = item.name
            existing.description = item.description
            existing.source = item.source
            existing.frequency = item.frequency
            existing.unit = item.unit
            existing.category = item.category
            if existing.fetch_status != "invalid_code":
                existing.is_active = True

    await session.commit()
    return inserted


async def seed_sample_observations(session: AsyncSession, years: int = 4) -> int:
    existing_count = await session.scalar(select(func.count(Observation.id)))
    if existing_count:
        series_rows = (await session.execute(select(Series))).scalars().all()
        for series in series_rows:
            if series.fetch_status == "not_fetched" and series.last_updated is not None:
                series.last_successful_fetch = series.last_updated
                series.last_fetch_attempt = series.last_updated
                series.fetch_status = "demo_seed"
                series.fetch_error = None
        await session.commit()
        return 0

    registry_by_code = {item.code: item for item in DEFAULT_SERIES}
    series_rows = (await session.execute(select(Series))).scalars().all()
    today = date.today()
    start = today - timedelta(days=365 * years)
    inserted = 0

    for series in series_rows:
        registry = registry_by_code.get(series.code)
        if registry is None:
            continue

        dates = _date_range(start, today, registry.frequency)
        for index, observed_at in enumerate(dates):
            value = _sample_value(registry, index)
            session.add(
                Observation(
                    series_id=series.id,
                    date=observed_at,
                    value=Decimal(str(round(value, 6))),
                    source="TCMB EVDS demo seed",
                )
            )
            inserted += 1

        series.last_updated = datetime.now(UTC)
        series.last_successful_fetch = series.last_updated
        series.last_fetch_attempt = series.last_updated
        series.fetch_status = "demo_seed"
        series.fetch_error = None

    await session.commit()
    return inserted


def _date_range(start: date, end: date, frequency: str) -> list[date]:
    step = {
        "daily": 1,
        "weekly": 7,
        "monthly": 30,
        "quarterly": 91,
    }.get(frequency, 30)

    points: list[date] = []
    cursor = start
    while cursor <= end:
        if frequency != "daily" or cursor.weekday() < 5:
            points.append(cursor)
        cursor += timedelta(days=step)
    return points


def _sample_value(series: RegistrySeries, index: int) -> float:
    seasonal = math.sin(index / 5.5) * series.amplitude
    slower_cycle = math.sin(index / 19.0) * series.amplitude * 0.35
    value = series.base_value + (index * series.slope) + seasonal + slower_cycle
    if series.unit == "%" and value < 0:
        return abs(value) * 0.4
    return value


def resolve_series_code(code: str) -> str:
    normalized = code.strip().upper()
    return SERIES_ALIASES.get(normalized, normalized)

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.config import get_settings  # noqa: E402
from app.database import AsyncSessionLocal, init_db  # noqa: E402
from app.services.evds_service import EVDSConfigurationError, evds_service  # noqa: E402
from app.services.series_registry import seed_sample_observations, seed_series  # noqa: E402


async def main() -> None:
    settings = get_settings()
    await init_db()
    async with AsyncSessionLocal() as session:
        await seed_series(session)
        try:
            fetched, observations = await evds_service.fetch_and_store(session)
            print(f"Fetched EVDS series={fetched}, observations={observations}")
        except EVDSConfigurationError:
            observations = await seed_sample_observations(session, settings.sample_years)
            print(f"EVDS_API_KEY missing; seeded demo observations={observations}")


if __name__ == "__main__":
    asyncio.run(main())


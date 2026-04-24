from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session

router = APIRouter(tags=["health"])


@router.get("/health")
async def healthcheck(session: AsyncSession = Depends(get_session)) -> dict[str, object]:
    await session.execute(text("SELECT 1"))
    return {
        "status": "ok",
        "service": "macrotr-api",
        "timestamp": datetime.now(UTC).isoformat(),
        "data": {"database": "ok"},
        "metadata": {
            "source": "postgresql",
            "last_updated": datetime.now(UTC).isoformat(),
            "cache_status": "bypass",
            "demo_mode": False,
            "warnings": [],
            "errors": [],
        },
        "source": "postgresql",
        "cache_status": "bypass",
        "warnings": [],
        "errors": [],
    }

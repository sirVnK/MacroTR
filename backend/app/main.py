from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_router
from app.config import get_settings
from app.core.errors import macrotr_exception_handler
from app.core.logging import setup_logging
from app.database import AsyncSessionLocal, init_db
from app.services.cache_service import cache_service
from app.services.series_registry import seed_sample_observations, seed_series


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    setup_logging()
    await init_db()
    await cache_service.connect(settings.redis_url)

    async with AsyncSessionLocal() as session:
        await seed_series(session)
        if settings.seed_sample_data:
            await seed_sample_observations(session, settings.sample_years)

    yield
    await cache_service.close()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="MacroTR API",
        description="Open-source Turkish macroeconomic dashboard API powered by TCMB EVDS.",
        version="0.1.0",
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )
    app.add_exception_handler(Exception, macrotr_exception_handler)
    app.include_router(api_router)
    return app


app = create_app()


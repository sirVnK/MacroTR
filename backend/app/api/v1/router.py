from fastapi import APIRouter

from app.api.v1 import admin, compare, dashboard, health, observations, series

router = APIRouter(prefix="/api/v1")

router.include_router(health.router)
router.include_router(series.router)
router.include_router(observations.router)
router.include_router(dashboard.router)
router.include_router(compare.router)
router.include_router(admin.router)


from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import MetadataDict, ResponseMetadata
from app.schemas.observation import ObservationPoint
from app.schemas.series import SeriesResponse


class IndicatorSummary(BaseModel):
    series: SeriesResponse
    latest_date: str | None
    latest_value: float | None
    previous_value: float | None = None
    change_percent: float | None = None
    sparkline: list[ObservationPoint] = Field(default_factory=list)


class DashboardSummaryResponse(BaseModel):
    generated_at: datetime
    disclaimer: str
    indicators: list[IndicatorSummary]
    data: list[IndicatorSummary] = Field(default_factory=list)
    metadata: ResponseMetadata | None = None
    source: str = "postgresql"
    last_updated: datetime | None = None
    cache_status: str = "bypass"
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class CompareSeriesItem(BaseModel):
    series: SeriesResponse
    observations: list[ObservationPoint]


class CompareResponse(BaseModel):
    normalized: bool
    series: list[CompareSeriesItem]
    data: list[CompareSeriesItem] = Field(default_factory=list)
    metadata: ResponseMetadata | None = None
    source: str = "postgresql"
    last_updated: datetime | None = None
    cache_status: str = "bypass"
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class FetchDataResponse(BaseModel):
    mode: str
    fetched_series: int
    inserted_observations: int
    detail: str
    data: MetadataDict = Field(default_factory=dict)
    metadata: ResponseMetadata | None = None
    source: str = "TCMB EVDS"
    last_updated: datetime | None = None
    cache_status: str = "bypass"
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)

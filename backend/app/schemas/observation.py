from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import ResponseMetadata


class ObservationPoint(BaseModel):
    date: date
    value: float

    model_config = ConfigDict(from_attributes=True)


class ObservationResponse(ObservationPoint):
    series_code: str
    source: str


class ObservationListResponse(BaseModel):
    series_code: str
    count: int
    observations: list[ObservationPoint]
    data: list[ObservationPoint] = Field(default_factory=list)
    metadata: ResponseMetadata | None = None
    source: str = "postgresql"
    last_updated: date | None = None
    cache_status: str = "bypass"
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class LatestObservationResponse(BaseModel):
    series_code: str
    date: date | None
    value: float | None
    source: str | None = None
    data: ObservationPoint | None = None
    metadata: ResponseMetadata | None = None
    last_updated: date | None = None
    cache_status: str = "bypass"
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)

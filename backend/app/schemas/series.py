from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import MetadataDict, ResponseMetadata
from app.schemas.observation import LatestObservationResponse, ObservationPoint


class SeriesBase(BaseModel):
    code: str
    evds_code: str
    name: str
    description: str
    source: str
    frequency: str
    unit: str
    category: str
    is_active: bool = True
    last_updated: datetime | None = None
    last_successful_fetch: datetime | None = None
    last_fetch_attempt: datetime | None = None
    fetch_status: str = "not_fetched"
    fetch_error: str | None = None

    model_config = ConfigDict(from_attributes=True)


class SeriesResponse(SeriesBase):
    pass


class SeriesDetailResponse(SeriesBase):
    latest: LatestObservationResponse | None = None
    observations: list[ObservationPoint] = Field(default_factory=list)
    data: dict[str, object] | None = None
    metadata: ResponseMetadata | None = None
    source: str = "postgresql"
    cache_status: str = "bypass"
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class SeriesListResponse(BaseModel):
    count: int
    items: list[SeriesResponse]
    data: list[SeriesResponse] = Field(default_factory=list)
    metadata: ResponseMetadata | None = None
    source: str = "postgresql"
    last_updated: datetime | None = None
    cache_status: str = "bypass"
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class SeriesFetchStatus(BaseModel):
    code: str
    evds_code: str
    is_active: bool
    last_successful_fetch: datetime | None = None
    fetch_status: str
    fetch_error: str | None = None
    metadata: MetadataDict = Field(default_factory=dict)

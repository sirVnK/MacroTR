from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ResponseMetadata(BaseModel):
    source: str = "postgresql"
    last_updated: datetime | None = None
    cache_status: str = "bypass"
    demo_mode: bool = False
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


MetadataDict = dict[str, Any]

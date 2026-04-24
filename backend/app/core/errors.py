from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse


class MacroTRError(RuntimeError):
    status_code = 400
    detail = "MacroTR request failed."


class NotFoundError(MacroTRError):
    status_code = 404
    detail = "Resource not found."


class ExternalDataError(MacroTRError):
    status_code = 502
    detail = "External data source failed."


async def macrotr_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, MacroTRError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": str(exc) or exc.detail},
        )

    return JSONResponse(
        status_code=500,
        content={"detail": "Unexpected server error."},
    )


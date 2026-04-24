# Architecture

MacroTR keeps the system deliberately small: one API, one frontend, one database and an optional cache.

```text
React/Vite frontend
        |
        | /api/v1
        v
FastAPI backend
        |
        +-- PostgreSQL: series and observations
        +-- Redis: optional cache
        +-- TCMB EVDS: official macro data source
```

## Backend

Location: `backend/app`

- `api/v1`: health, series, observations, dashboard, compare and local admin routes
- `models`: SQLAlchemy `Series` and `Observation`
- `schemas`: Pydantic response contracts
- `services`: EVDS client, cache, data cleaning and series registry
- `core`: logging and error helpers

Startup behavior:

1. Create missing tables for local development.
2. Add runtime-safe fetch status columns if an older local database exists.
3. Seed the default series registry.
4. Insert deterministic demo observations when `SEED_SAMPLE_DATA=true` and no observations exist.

## Frontend

Location: `frontend/src`

- `api`: typed API functions
- `hooks`: TanStack Query hooks
- `components`: reusable chart, selector and card components
- `pages`: dashboard, detail, compare, about and data-source pages
- `types`: shared response types

## Response Shape

Phase 1 fields are preserved. Phase 2 adds metadata where useful:

- `data`
- `metadata`
- `source`
- `last_updated`
- `cache_status`
- `warnings`
- `errors`

This keeps existing clients working while giving contributors clearer diagnostics.


# API Reference

Base URL: `/api/v1`

## Common Response Metadata

Most responses include Phase 1 fields and a Phase 2 metadata envelope:

```json
{
  "data": {},
  "metadata": {
    "source": "postgresql",
    "last_updated": "2026-04-24T21:17:09Z",
    "cache_status": "bypass",
    "demo_mode": true,
    "warnings": []
  }
}
```

Error responses use FastAPI's standard `detail` field.

## Health

`GET /health`

Example:

```json
{
  "status": "ok",
  "service": "macrotr-api",
  "data": { "database": "ok" }
}
```

## Series

`GET /series`

Query parameters:

- `category`
- `search`

`GET /series/{code}`

Supported aliases include:

- `/series/usdtry`
- `/series/eurtry`
- `/series/inflation`
- `/series/policy-rate`

`GET /series/{code}/observations`

Query parameters:

- `start_date`
- `end_date`
- `limit`

`GET /series/{code}/latest`

Returns the latest stored observation.

## Dashboard

`GET /dashboard/summary`

Returns indicator cards, latest values and sparkline data.

## Compare

`GET /compare?series=USDTRY,CPI&normalize=true`

Query parameters:

- `series`: comma-separated MacroTR codes
- `normalize`: `true` or `false`
- `start_date`
- `end_date`

Example response excerpt:

```json
{
  "normalized": true,
  "series": [
    {
      "series": { "code": "USDTRY", "source": "TCMB EVDS" },
      "observations": [{ "date": "2026-04-24", "value": 100 }]
    }
  ]
}
```

## Local Admin

`POST /admin/fetch-data`

Fetches EVDS data in local/dev. If `EVDS_API_KEY` is missing, it returns:

```json
{
  "mode": "demo-seed",
  "detail": "EVDS_API_KEY is missing; local demo observations are available.",
  "metadata": {
    "source": "local-demo",
    "demo_mode": true,
    "warnings": ["EVDS_API_KEY is not configured."]
  }
}
```

Disabled when `APP_ENV=production`.


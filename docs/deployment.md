# Deployment

## Local Docker

```bash
cp .env.example .env
docker compose up --build -d
```

Default host ports:

- Frontend: `5173`
- Backend: `8010`

Stop:

```bash
docker compose down
```

PostgreSQL and Redis are internal-only by default to avoid local port collisions.

## Seed And Fetch

Demo seed mode works automatically when `EVDS_API_KEY` is empty.

For real EVDS data:

```bash
curl -X POST "http://localhost:8010/api/v1/admin/fetch-data"
```

## Frontend: Vercel

Project root:

```text
frontend
```

Build command:

```bash
npm run build
```

Output directory:

```text
dist
```

Environment:

```text
VITE_API_BASE_URL=https://your-backend.example.com/api/v1
```

## Backend: Railway, Render Or Fly.io

Use `backend/Dockerfile`.

Required environment:

```text
APP_ENV=production
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=redis://...
EVDS_API_KEY=...
ALLOWED_ORIGINS=https://your-frontend.example.com
SEED_SAMPLE_DATA=false
MACROTR_DEBUG=false
```

## PostgreSQL: Neon, Supabase Or Railway

Use a managed PostgreSQL database and set `DATABASE_URL` with the async SQLAlchemy driver:

```text
postgresql+asyncpg://user:password@host:5432/database
```

The app can create tables for local development, but production should use Alembic migrations.

## Redis

Redis is optional in Phase 2. If `REDIS_URL` is unavailable, the API keeps working with `cache_status=bypass`.

## Production Ingestion

`/api/v1/admin/fetch-data` is local/dev only. Production ingestion should use a scheduled job or one-off worker with controlled credentials.


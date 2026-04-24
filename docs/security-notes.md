# Security Notes

## npm audit

Current result (as of 2026-04-25):

```text
5 moderate severity vulnerabilities
```

All 5 vulnerabilities originate from `esbuild ≤ 0.24.2` and its dependents in the **development** toolchain:

| Package | Severity | Classification |
| --- | --- | --- |
| `esbuild` | moderate | dev dependency (via `vite`) |
| `vite` | moderate | dev dependency |
| `@vitest/mocker` | moderate | dev dependency (test runner) |
| `vitest` | moderate | dev dependency (test runner) |
| `vite-node` | moderate | dev dependency (test runner) |

**Impact:** These vulnerabilities allow a website to send requests to the Vite development server and read responses. They only affect the **local development server** (`npm run dev`) and do not affect the production build or deployed artifacts.

**Why `npm audit fix --force` was not run:** The automated fix would upgrade Vite to v8 (a breaking change), which is incompatible with the current React/Vitest configuration. A safe migration requires a dedicated upgrade branch with full regression testing.

**Action:** Track the upstream Vite v6 patch release. When a non-breaking fix is available, apply it in a PR. Until then, do not expose `npm run dev` to untrusted networks.

## Dependency Classification

- Production dependencies include React, TanStack Query, Recharts and routing libraries.
- Development dependencies include Vite, Vitest, Testing Library, TypeScript, Tailwind and build tooling.
- The 5 moderate audit findings are all in dev dependencies and do not affect the production build.

## Secrets

Never commit:

- `.env`
- `EVDS_API_KEY`
- production database URLs
- Redis credentials

`.gitignore` excludes `.env`, `node_modules`, `dist`, `build`, `.venv`, `.pytest_cache`, coverage outputs and local database files.

## Admin Fetch Endpoint

`POST /api/v1/admin/fetch-data` is disabled when `APP_ENV=production`. Production ingestion should use a controlled scheduled job or worker.

## Rate Limit Recommendation

Before a public hosted backend is launched, add a simple rate limit to public API endpoints and a stricter policy around ingestion jobs.


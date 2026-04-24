# Open Source Guide

MacroTR should stay small, readable and useful.

## Maintainer Principles

- Never add investment advice, al/sat signals or portfolio recommendations.
- Keep source attribution visible.
- Preserve demo seed mode for contributors without EVDS keys.
- Prefer small pull requests.
- Update docs when API, deployment or data source behavior changes.

## Labels

- `good first issue`
- `bug`
- `documentation`
- `frontend`
- `backend`
- `data-source`
- `help wanted`

## Good First Issues

1. Add a new TCMB macro series.
2. Improve mobile chart layout.
3. Add English explanations for indicators.
4. Add PNG export for charts.
5. Add skeleton loading components.
6. Add more compare presets.
7. Add API response examples.
8. Add tests for CSV export.

## Screenshot Capture

1. Run `docker compose up --build -d`.
2. Open http://localhost:5173.
3. Capture:
   - Dashboard screenshot
   - Series detail screenshot
   - Compare page screenshot
   - Mobile responsive screenshot
4. Save files into `docs/assets/`:
   - `dashboard.png`
   - `series-detail.png`
   - `compare-page.png`
   - `mobile-view.png`

## Pull Request Checklist

- No investment advice added.
- Tests or build run locally.
- Docs updated when needed.
- `EVDS_API_KEY` not committed.
- Screenshots included for visible UI changes.


# Contributing

Thanks for considering a contribution to MacroTR.

## Workflow

1. Fork the repository.
2. Create a branch:

```bash
git checkout -b feature/your-change
```

3. Make a small, focused change.
4. Run the relevant tests.
5. Commit with a clear message.
6. Open a pull request with context, screenshots for UI changes and test results.

## Local Setup

```bash
cp .env.example .env
docker compose up --build -d
```

MacroTR works without `EVDS_API_KEY` by using demo seed data.

## Code Style

- Keep backend code typed and small.
- Keep frontend components focused and reusable.
- Do not add investment advice, al/sat signals or portfolio recommendations.
- Keep source attribution visible.
- Preserve demo seed mode.

## Run Checks

Backend:

```bash
pip install -r backend/requirements.txt
ruff check backend/app backend/tests scripts
pytest
```

Frontend:

```bash
cd frontend
npm install
npm run test
npm run build
```

## Good First Issues

- Add a new TCMB macro series.
- Improve mobile chart layout.
- Add English explanations for indicators.
- Add PNG export for charts.
- Add skeleton loading components.
- Add more compare presets.
- Add API response examples.
- Add tests for CSV export.


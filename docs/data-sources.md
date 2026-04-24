# Data Sources

MacroTR MVP focuses on TCMB EVDS.

Official resources:

- TCMB EVDS: https://evds2.tcmb.gov.tr
- EVDS web service guide: https://evds2.tcmb.gov.tr/help/videos/EVDS_Web_Service_Usage_Guide.pdf

## What Is TCMB EVDS?

EVDS is the Electronic Data Delivery System of the Central Bank of the Republic of Türkiye. It provides public economic and financial time series through the web interface and web service endpoints.

## API Key Setup

1. Create an account and API key at https://evds2.tcmb.gov.tr.
2. Add the key to `.env`:

```env
EVDS_API_KEY=your-key
SEED_SAMPLE_DATA=false
```

3. Restart MacroTR:

```bash
docker compose up --build -d
```

4. Fetch data in local/dev:

```bash
curl -X POST "http://localhost:8010/api/v1/admin/fetch-data"
```

## Demo Seed Mode

If `EVDS_API_KEY` is empty, the backend seeds deterministic local demo observations. Demo data keeps the dashboard usable for development and CI, but it is not official TCMB data.

## Series Registry

The current workspace has no `.env` file and no `EVDS_API_KEY`, so live EVDS validation was not executed locally. The registry remains active with demo seed data. When a key is available, use `/api/v1/admin/fetch-data` and inspect `fetch_status`, `last_successful_fetch`, `last_updated` and `fetch_error`.

| MacroTR code | Display name | EVDS code | Category | Frequency | Unit | Status | Warning |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `USDTRY` | USD/TRY | `TP.DK.USD.A.YTL` | exchange_rate | daily | TRY | pending live metadata check | verify with EVDS metadata |
| `EURTRY` | EUR/TRY | `TP.DK.EUR.A.YTL` | exchange_rate | daily | TRY | pending live metadata check | verify with EVDS metadata |
| `POLICY_RATE` | Policy rate | `TP.TRF.YIL.P14` | interest_rate | monthly | % | pending live metadata check | verify with EVDS metadata |
| `CPI` | CPI annual change | `TP.TUFE1YI.T1` | inflation | monthly | % | pending live metadata check | verify with EVDS metadata |
| `PPI` | Domestic PPI annual change | `TP.TFYI01` | inflation | monthly | % | pending live metadata check | verify with EVDS metadata |
| `UNEMPLOYMENT` | Unemployment rate | `TP.TG2.Y01` | labor | monthly | % | pending live metadata check | verify with EVDS metadata |
| `INDUSTRIAL_PRODUCTION` | Industrial production index | `TP.SANAYREV4.Y1` | production | monthly | Index | pending live metadata check | verify with EVDS metadata |
| `CURRENT_ACCOUNT` | Current account balance | `TP.ODEAYRSUNUM6.Q1` | external_balance | monthly | Million USD | pending live metadata check | verify with EVDS metadata |
| `GROSS_RESERVES` | CBRT gross reserves | `TP.AB.A02` | reserves | weekly | Million USD | pending live metadata check | verify with EVDS metadata |
| `BIST100` | BIST 100 | `TP.MK.F.BILESIK` | market | daily | Index | pending live metadata check | verify with EVDS metadata |

## How To Validate Series Codes

Use the EVDS metadata endpoints and web interface to confirm:

- Series code exists
- Frequency matches the registry
- Unit is correct
- Data is returned for a recent date range
- Source attribution remains visible

If a code repeatedly returns `empty` or `error`, do not delete it immediately. Mark it inactive, document the failure here and propose an alternative EVDS code in a pull request.

## Data Accuracy And Usage

MacroTR does not guarantee data accuracy. Data is provided as-is from public or third-party sources. For commercial use, check TCMB EVDS and any future data provider terms before publishing, redistributing or monetizing derived datasets.


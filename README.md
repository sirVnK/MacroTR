# MacroTR — Turkish Macroeconomic Dashboard

An open-source dashboard for Turkish macroeconomic indicators, built on TCMB EVDS data with a FastAPI backend, a React frontend and a PostgreSQL database. This project connects my economics background with software engineering.

## Overview

MacroTR pulls macroeconomic data from the TCMB EVDS (Electronic Data Delivery System) and presents Turkish economic indicators through a clean web dashboard. It's a full-stack project covering data ingestion, API design, storage and visualization.

## Motivation

My background is in both engineering and economics. MacroTR is where those two meet: it lets me work with real open economic data while practicing full-stack engineering — API design, a relational database, and a modern frontend.

## Features

- Ingestion of TCMB EVDS macroeconomic data
- FastAPI backend exposing a clean data API
- React frontend dashboard
- PostgreSQL storage
- Open data, open source

## Architecture

```
TCMB EVDS API
      |
 FastAPI Backend (ingest + serve)
      |
 PostgreSQL (storage)
      |
 React Frontend (dashboard)
```

## Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** React
- **Database:** PostgreSQL
- **Data Source:** TCMB EVDS
- **Domain:** Turkish macroeconomics / open data

## Installation

> Adapt to the actual setup in this repository.

```bash
git clone https://github.com/Logshi/MacroTR.git
cd MacroTR

# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

You will need a TCMB EVDS API key (kept in environment variables, **never committed**) and a running PostgreSQL instance.

## Usage

```bash
# Backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

## Demo

> Placeholders — replace with real screenshots.

- `docs/screenshots/dashboard.png`

## Results

A working full-stack dashboard over TCMB EVDS data. Specific indicator coverage and refresh behavior are documented in the app.

## Roadmap

- [ ] Expand indicator coverage
- [ ] Add caching / scheduled data refresh
- [ ] Charts and comparison views
- [ ] Containerized deployment (Docker)
- [ ] Tests and CI

## What I Learned

- Building a full-stack application end to end
- Designing a FastAPI service and PostgreSQL schema
- Working with a real external data API (TCMB EVDS)
- Connecting economics domain knowledge to a software product

## Security & Privacy

API keys and database credentials are kept in environment variables and **never committed**. No personal or sensitive data is stored in the repository.

## License

MIT — see [LICENSE](LICENSE).

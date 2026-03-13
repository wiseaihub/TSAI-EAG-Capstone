# Docker deployment

## Build and run locally

```bash
docker compose up -d
```

Builds backend and frontend from source and runs them.

## Run from GitHub Container Registry (GHCR)

To use pre-built images from GHCR, set your GitHub org or username and run:

```bash
# In project root, add to .env (or export):
# GITHUB_OWNER=your-github-org-or-username

cd deployment/docker
docker compose -f docker-compose.ghcr.yml up -d
```

Or inline:

```bash
GITHUB_OWNER=your-github-org docker compose -f docker-compose.ghcr.yml up -d
```

Images used: `ghcr.io/<GITHUB_OWNER>/tsiag-capstone-backend:latest`, `ghcr.io/<GITHUB_OWNER>/tsiag-capstone-frontend:latest` (built by `.github/workflows/docker-publish.yml`).

## Full stack (wise-ai + S18Share)

To run wise-ai with S18 (EHR Data Miner integration) in one command:

```bash
cd deployment/docker
docker compose -f docker-compose.full.yml up -d
```

**Prerequisite:** S18Share must be a sibling of wise-ai (e.g. `Downloads/wise-ai` and `Downloads/S18Share`). If your layout differs, set `S18_PATH`:

```bash
S18_PATH=/path/to/S18Share/S18Share docker compose -f docker-compose.full.yml up -d
```

This starts:
- **wise-ai backend** (port 8000) and **frontend** (port 3000)
- **S18 s18share-api** (port 8001) with EHRDataMinerAgent and mockehr MCP
- **ollama** for S18 (port 11434)

S18's mockehr uses `WISE_MOCKEHR_BASE_URL=http://backend:8000` to fetch patient data and labs from wise-ai's Mock EHR API.

---

## S18 integration (optional env overrides)

| Variable | Default | Purpose |
| --- | --- | --- |
| `S18_BASE_URL` | `http://s18share-api:8000` | S18 API base URL |
| `RUN_POLL_TIMEOUT_SECONDS` | `300` | Total wait timeout for polling GET /runs/{id}; exposed in GET /health so clients/gateways can set their timeout (e.g. 300 or higher so ~2 min runs are not cut off). |
| `S18_POLL_TIMEOUT_SEC` | (fallback) | Legacy env; used if RUN_POLL_TIMEOUT_SECONDS not set. |
| `S18_POLL_INTERVAL_SEC` | `2.0` | Seconds between poll requests |
| `WISE_TIMEOUT_SEC` | `920` | Max seconds for /analyze to wait for WISE (must exceed poll timeout) |
| `WISE_MOCKEHR_BASE_URL` | (S18 env) | Points to wise-ai backend base URL when running integrated stack |

Optional override via backend `settings.json`: set `"run_poll_timeout_seconds": 300` (or higher). Path via `SETTINGS_PATH` or default `backend/settings.json`. See `backend/settings.json.example`.

**Testing POST /analyze with curl:** S18 runs can take 1–3 minutes. Use a client timeout at least as long as `poll_timeout_seconds` (e.g. 300s), otherwise you'll see "Request timed out" even though the backend and S18 complete. Example: `curl --max-time 400 -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_JWT" -d '{"hemoglobin":13.5,"wbc":7000,"rbc":4.5,"platelets":250000}'`

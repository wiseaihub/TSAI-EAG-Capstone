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

## S18 integration (optional env overrides)

| Variable | Default | Purpose |
| --- | --- | --- |
| `S18_BASE_URL` | `http://s18share-api:8000` | S18 API base URL |
| `S18_POLL_TIMEOUT_SEC` | `900` | Max seconds to poll S18 run before soft fallback |
| `S18_POLL_INTERVAL_SEC` | `2.0` | Seconds between poll requests |
| `WISE_TIMEOUT_SEC` | `920` | Max seconds for /analyze to wait for WISE (must exceed S18 poll timeout) |

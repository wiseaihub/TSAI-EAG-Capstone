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

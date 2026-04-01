# GitHub issue traceability (TSAI-EAG-Capstone)

This file maps [wiseaihub/TSAI-EAG-Capstone](https://github.com/wiseaihub/TSAI-EAG-Capstone) issues to artefacts in this repository and records triage status. Regenerate the open-issue snapshot with:

`gh issue list --repo wiseaihub/TSAI-EAG-Capstone --state open --limit 250 --json number,title,labels,milestone > issues-open.json` (optional local export).

## Repository access (verified)

| Check | Result |
|--------|--------|
| Local `origin` | `https://github.com/wiseaihub/TSAI-EAG-Capstone.git` (not a fork; same canonical repo) |
| `gh repo view … --json viewerPermission` | **WRITE** (authenticated user can close issues and comment) |
| Default branch | `main` |

## Explicit doc links in this repo

| Issue | Title | Wise-ai evidence | Triage |
|-------|--------|------------------|--------|
| [5](https://github.com/wiseaihub/TSAI-EAG-Capstone/issues/5) | Repository Setup and Data Models | [`docs/api-specs.md`](api-specs.md) (Pydantic CBC/vitals/patient/encounter; repo structure section); implementations under `backend/app/schemas/`, `backend/app/db/models.py` | **Closed** on GitHub (no action needed) |

## Infra / execution (sample mapping from open list)

| Issue | Title | Wise-ai evidence | Triage |
|-------|--------|------------------|--------|
| [112](https://github.com/wiseaihub/TSAI-EAG-Capstone/issues/112) | GitHub Repo Initialisation & Project Board Setup | Repo populated: `backend/`, `frontend/`, `docs/`, `deployment/`, `.github/workflows/` | **Closed** (evidence comment posted 2026-03-31) |
| [118](https://github.com/wiseaihub/TSAI-EAG-Capstone/issues/118) | Docker Dev Environment & CI/CD Pipeline Setup | [`deployment/docker/README.md`](../deployment/docker/README.md), [`deployment/docker/docker-compose.yml`](../deployment/docker/docker-compose.yml), [`.github/workflows/capstone.yml`](../.github/workflows/capstone.yml), `backend-ci.yml`, `docker-publish.yml` | **Closed** (evidence comment posted 2026-03-31) |
| [198](https://github.com/wiseaihub/TSAI-EAG-Capstone/issues/198) | Distributed Agent Execution Layer (Celery + Redis) | [`backend/app/core/celery_app.py`](../backend/app/core/celery_app.py), [`backend/app/tasks/cbc_tasks.py`](../backend/app/tasks/cbc_tasks.py); branch `feature/celery-redis` also noted on issue | **Open** — progress comment 2026-03-31 (Celery scaffold in repo; compose/worker/task API/polling still vs acceptance criteria) |

## Governance / BODH / SAHI (#200–#211)

| Issue range | Notes |
|-------------|--------|
| #200–#211 | Primarily documentation and external BODH/SAHI deliverables. No `docs/compliance/` tree in this repo at last update. Map each issue to MoHFW/arXiv/packaged evidence elsewhere before closing; do not close from code presence alone. |

## How to update this matrix

1. Pick an open issue and confirm acceptance criteria from the issue body.
2. Link merged PRs or paths under `wise-ai/` (or sibling repos).
3. **Done:** comment with evidence → `gh issue close N --repo wiseaihub/TSAI-EAG-Capstone --comment "..."` or close in UI.
4. **Partial:** comment only; optional labels/milestone on GitHub.

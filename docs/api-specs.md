# API & Schema Specs

Pydantic models and API contract for the WISE AI CDSS backend (aligned with [Issue #5](https://github.com/wiseaihub/TSAI-EAG-Capstone/issues/5)).

---

## 1. CBC (Complete Blood Count)

**Location:** `backend/app/schemas/cbc.py`

### CBCInput

| Field        | Type                | Required | Description              |
|-------------|---------------------|----------|--------------------------|
| hemoglobin  | float               | Yes      | Hb (g/dL)                |
| wbc         | float               | Yes      | WBC (per µL)             |
| rbc         | float               | Yes      | RBC (million/µL)         |
| platelets   | float               | Yes      | Platelets (per µL)       |
| differential| DifferentialCounts | No       | WBC differential counts  |

### DifferentialCounts (optional)

| Field        | Type  | Description                    |
|-------------|-------|--------------------------------|
| neutrophils | float | Neutrophils (10^9/L or %)      |
| lymphocytes | float | Lymphocytes                   |
| monocytes   | float | Monocytes                     |
| eosinophils | float | Eosinophils                   |
| basophils   | float | Basophils                     |

### CBCOutput

| Field      | Type   | Description        |
|------------|--------|--------------------|
| risk_level | string | Low / Moderate / High |
| flags      | list[str] | Clinical flags |
| confidence | float  | 0–1                |

**API:** `POST /cbc/analyze` — body: `CBCInput`, response: agent result (risk_level, flags, confidence, session_id, etc.).

---

## 2. Vitals

**Location:** `backend/app/schemas/vitals.py`

### VitalsInput

| Field       | Type  | Required | Description           |
|------------|-------|----------|-----------------------|
| systolic_bp  | int   | Yes      | Systolic BP (mmHg)    |
| diastolic_bp | int   | Yes      | Diastolic BP (mmHg)  |
| temp_c    | float | Yes      | Temperature (°C)     |
| pulse     | int   | Yes      | Heart rate (bpm)     |
| spo2      | float | Yes      | SpO2 (%)             |

### VitalsOutput

| Field      | Type     | Description |
|------------|----------|-------------|
| risk_level | string   | Low / Moderate / High |
| flags      | list[str]| Clinical flags |
| confidence | float    | 0–1         |

---

## 3. Patient & Encounter (data models)

**Location (DB):** `backend/app/db/models.py`  
**Location (schemas):** `backend/app/schemas/patient.py`

### Patient (SQLAlchemy)

| Column     | Type   | Description                    |
|------------|--------|--------------------------------|
| id         | string | PK                             |
| external_id| string | Unique external identifier     |
| created_at | datetime |                               |
| updated_at | datetime |                               |

### Encounter (SQLAlchemy)

| Column        | Type   | Description     |
|---------------|--------|-----------------|
| id            | string | PK              |
| patient_id    | string | FK → patients.id |
| encounter_type| string | Optional        |
| started_at    | datetime |               |
| ended_at      | datetime | Optional       |
| metadata      | JSON   | Optional        |

### Pydantic schemas

- **PatientCreate** / **PatientRead**: create payload and API response for Patient.
- **EncounterCreate** / **EncounterRead**: create payload and API response for Encounter.

---

## 4. Agent session (existing)

**Location:** `backend/app/db/models.py` — `AgentSession`

Stores per-run agent results: `session_id`, `patient_id`, `agent_name`, `agent_version`, `risk_level`, `confidence`, `flags`, `timestamp`.

---

## Repo structure (Issue #5)

- **backend** — FastAPI app, schemas, DB models, agents, API routes.
- **frontend** — Vite/React app.
- **data** — Placeholder for datasets / artifacts.
- **docs** — Architecture and this API spec (`docs/api-specs.md`).
- **tests** — Top-level tests placeholder; backend unit tests in `backend/tests/`.
- **deployment** — Docker Compose and GHCR publish workflow.

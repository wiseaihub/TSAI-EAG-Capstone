# WISE AI – Agentic Clinical Decision & Continued‑Care System (CDSS)

This repository contains the **Capstone Project** for the course  
**Extensive AI for Generative Systems** (TSAI – The School of AI).

The project implements an **Agentic Clinical Decision Support System (CDSS)** that integrates with an existing EHR (WISE Doctor) to assist **patients and doctors** across the healthcare journey — from triage and diagnostics to continued care and follow‑ups.

---

## 🎯 Capstone Objective

Design and demonstrate a **production‑thinking AI system** that:

- Uses **agentic architecture** (multiple cooperating AI agents)
- Is **clinically responsible** (decision support, not automation)
- Shows clear **system design, reasoning, and UX**
- Aligns with TSAI capstone dos & don’ts

Primary demo audience: **Rohan Shravan (TSAI)**

---

## 🧠 What This System Is

**WISE AI** is an overlay CDSS that works *alongside* an EHR.

- **EHR (WISE Doctor)** remains the system of record
- **WISE AI** is user‑invoked, consent‑based, and explainable
- No silent background processing
- No automated clinical actions

---

## 🧩 Core Components

### 1. WISE AI Plugin
- User‑triggered (patient or doctor)
- Consent‑based data capture from EHR screens
- Research + signal extraction
- Feeds the shared knowledge bank

### 2. WISE AI CDSS Web App
- Standalone web application
- Rich UI for:
  - Recommendations
  - Clinical summaries
  - Confidence scores
  - Missing‑signal feedback
- Hosts the agentic reasoning loop

### 3. Shared Knowledge Bank
- Research corpus (WWW + platform‑level)
- Anonymised contextual signals
- Doctor & patient workspaces (conceptual)

---

## 🤖 Agentic Architecture (High Level)

The CDSS uses multiple cooperating agents, including:

- Symptom Agent
- CBC / Lab Agent
- Trend / History Agent
- Research Agent
- Action / Recommendation Agent

📐 **Architecture diagram (Mermaid source & rendered image)**  
See: `docs/architecture.md`

---

## 📁 Repository Structure

```text
/
├── docs/
│   ├── architecture.md        # Mermaid + rendered architecture
│   ├── north-star.md          # Vision, principles, MVP freeze
│
├── plugin/                    # WISE AI browser plugin (if applicable)
├── cdss-app/                  # WISE AI CDSS web application
├── demo/                      # Demo scripts, screenshots, videos
├── paper/                     # Capstone paper outline / drafts
│
└── README.md
```

### CI / Automation
Basic GitHub Actions workflow is defined in `.github/workflows/capstone.yml`

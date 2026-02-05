# WISE AI  
### Agentic Clinical Decision & Continued‑Care System (CDSS)

![Capstone](https://img.shields.io/badge/TSAI-Capstone-blue)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange)
![Domain](https://img.shields.io/badge/Domain-Healthcare-informational)
[![Capstone CI](https://github.com/wiseaihub/TSAI-EAG-Capstone/actions/workflows/capstone.yml/badge.svg)](
https://github.com/wiseaihub/TSAI-EAG-Capstone/actions/workflows/capstone.yml
)

---

## 📌 Overview

WISE AI is an **Agentic Clinical Decision Support System (CDSS)** designed as part of the  
**TSAI – Extensive AI for Generative Systems Capstone Project**.

It supports **continued care** across patients and doctors through
consent‑based data capture, multi‑agent reasoning, and explainable outputs.
It is designed to work *alongside* an existing EHR (WISE Doctor), assisting both **patients and doctors** across the end‑to‑end healthcare journey — from triage and diagnostics to treatment guidance and continued care.

> ⚠️ This system provides **decision support, not medical automation**.  
> All clinical decisions remain with licensed practitioners.

## 🎯 Vision

To build a **responsible, explainable, agentic healthcare assistant**
that supports — but never replaces — licensed clinicians.

WISE AI focuses on:
- Clinical decision support (not diagnosis)
- Patient‑centric continued care
- Human‑in‑the‑loop safety
- Transparent reasoning and confidence feedback

---

## 🎯 Capstone Objective

Design and demonstrate a **production‑thinking AI system** that:

- Uses **agentic architecture** (multiple cooperating AI agents)
- Is **clinically responsible** (decision support, not automation)
- Shows clear **system design, reasoning, and UX**
- Aligns with TSAI capstone dos & don’ts

Primary demo audience: **Rohan Shravan (TSAI)**

---

## 🧠 What This System Is (and Is Not)

### ✅ What It Is
- A **user‑invoked**, consent‑based CDSS
- An **overlay** on top of an EHR (not a replacement)
- Agentic reasoning with confidence & feedback loops
- Designed for both **patients and doctors**

### ❌ What It Is Not
- Not an autonomous medical system
- Not silently monitoring users
- Not writing back to EHR automatically (future only)

---

## 🧩 Core System Components

### 1️⃣ WISE AI Plugin
- Browser‑based, user‑triggered
- Consent‑based data extraction from EHR views
- Research & signal capture
- Feeds the shared knowledge bank

### 2️⃣ WISE AI CDSS Web App
- Standalone web application
- Rich UI for:
  - Recommendations & guidance
  - Clinical summaries
  - Confidence scores
  - Missing‑signal feedback
- Hosts the **agentic reasoning loop**

### 3️⃣ Shared Knowledge Bank
- World‑wide research sources (RAG)
- Platform‑level anonymised context
- Doctor & patient workspaces (conceptual)
- Supports feedback loops

---

### 1. **WISE AI Plugin**
- User‑triggered (no background scraping)
- Consent‑based data extraction from EHR screens
- Research adapter (WWW + curated sources)
- Pushes structured signals into the shared knowledge bank

### 2. **WISE AI CDSS Web App**
- Standalone, rich UI (opened in a separate tab)
- Orchestrates multiple reasoning agents
- Displays:
  - Clinical summaries
  - Diagnostic guidance
  - Treatment considerations
  - Confidence scores & missing signals
- Clearly labels **“future / simulated” actions**

### 3. **Shared Knowledge Bank**
- Stores:
  - Patient‑context (session‑scoped)
  - Doctor workspace knowledge
  - Anonymised platform knowledge
- Enables feedback loops and iterative reasoning

---

## 🤖 Agentic Architecture (High Level)

WISE AI follows a **multi‑agent pattern**, where each agent specializes in a specific reasoning task:

- Symptom Agent
- Lab / CBC Agent
- Trend & History Agent
- Research Agent
- Action / Recommendation Agent

All outputs are synthesized, scored for confidence, and presented for **human approval**.

> 📌 **No agent directly writes to the EHR in MVP** — all actions are advisory.

📐 **Architecture diagram (Mermaid source & rendered image)**  
See: `docs/architecture.md`

---

🚦MVP Feature Freeze (Capstone Scope)
✅ Included
- Manual invocation via “WISE AI” button in EHR
- Plugin‑based data capture (on demand)
- Multi‑agent reasoning
- CDSS UI with explainable outputs
- Confidence feedback loop
- Simulated future actions (clearly labelled)

❌ Explicitly Out of Scope (These are shown as *future / disabled* features where relevant)
- Automatic EHR write‑back
- Silent background monitoring
- Autonomous actions (lab booking, Rx ordering)
- Production compliance certifications
---

🧪 Demo Philosophy (for TSAI Evaluation)
- Real UI, real flows
- No mock screenshots passed as real
- Clear separation between:
  - Working MVP logic
  - Future extensibility
- Emphasis on **agentic reasoning quality**, not UI polish alone

---

🛠️ Technology Posture (Indicative)
- Frontend: Web UI (framework‑agnostic)
- AI Layer: LLM‑driven agent orchestration
- Local Dev: Cursor IDE, Ollama (multi‑LLM switching)
- Demo LLM: Gemini (mentor‑preferred)
- Hosting (stretch): AWS (credits‑based)
  
---


## 🗓 Project Constraints

- ⏱ 30‑day hard deadline
- 🎓 Academic capstone (design clarity > production scale)
- 🧪 PoC first, extensible architecture second
- 🧑‍⚕️ Clinical responsibility & explainability are non‑negotiable

---

## 👥 Team & Roles

- **Sreedhar Byreeka** — Product Manager & Healthcare IT SME  
- **Ritesh Verma** — Agentic AI & Technical Lead  
- **Mentor:** Rohan Shravan (TSAI)

---

## 📌 Status

🔄 Active development  
📌 MVP feature set frozen  
📐 Architecture finalised  
🧪 Demo & evaluation in progress

---

## 📁 Repository Structure

```text
/
├── docs/
│   ├── architecture.md        # Mermaid + rendered architecture diagrams
│   ├── north-star.md          # Vision, principles, MVP feature freeze
│
├── plugin/                    # WISE AI browser plugin (data capture & research)
│
├── cdss-app/                  # WISE AI CDSS web application (UI + agents)
│
├── demo/
│   ├── scripts/               # Demo narration & walkthroughs
│   ├── screenshots/
│   └── videos/
│
├── paper/                     # Capstone paper (outline & drafts)
│
├── .github/
│   └── workflows/
│       └── capstone.yml       # Basic CI / automation
│
└── README.md
```

---
## ⚙️ CI / Automation

Basic GitHub Actions workflow is defined in:

.github/workflows/capstone.yml

---
## ⚠️ Disclaimer
WISE AI is a **clinical decision‑support system**.

It does **not** diagnose, prescribe, or replace licensed medical professionals.  
All outputs are advisory and require human clinical judgment.

---

📚 References

- TSAI – The School of AI: https://theschoolof.ai/
- Course: Extensive AI for Generative Systems
- Capstone Guidelines: See `/docs` and uploaded PDFs

---

# WISE AI-CDSS – Product Vision Document (T17)

**Task:** T17 · **Issue:** #123 · **Week:** 1  
**Owners:** Sreedhar (wiseaihub), Ritesh (riteshverma)  
**SAHI Reference:** SAHI Lifecycle Step 1 – Problem Formulation  
**Depends on:** T01, T04  

---

## Product Name & Brand

| Element | Detail |
|---------|--------|
| Full name | WISE AI Clinical Decision Support System (WISE AI-CDSS) |
| Acronym expansion | **W**orkflow-**I**ntegrated **S**mart **E**vidence – CDSS |
| Tagline | "Clinician-first AI for India's primary care" |
| Brand principles | Trustworthy, Transparent, India-context, SAHI-aligned |
| Visual identity | Clean clinical blue/white palette; no-clutter GP workflow UI |

---

## Vision Statement

To empower every Indian General Practitioner with AI-augmented clinical decision support
that is evidence-based, explainable, and safe — reducing diagnostic error and improving
patient outcomes across India's primary care settings, regardless of infrastructure
constraints or EHR availability.

---

## Problem We Solve

| Pain Point | Current Reality | WISE AI-CDSS Response |
|------------|----------------|----------------------|
| High patient load | 40–80 patients/day per GP | AI triage reduces cognitive burden |
| Diagnostic uncertainty | Limited specialist access in Tier 2/3 | Evidence-backed differential suggestions |
| No CDSS for Indian context | Existing tools built for Western EHR systems | Designed for paper-based Indian GP workflow |
| Regulatory vacuum | No SAHI/CDSCO-aligned AI product exists | Built compliance-first from day one |
| Data privacy risk | DPDP Act 2023 obligations | Consent-first architecture (T11) |

---

## Target Users (Personas)

| Persona | Role | Context | Primary Need |
|---------|------|---------|--------------|
| Dr. Priya | Urban GP | Private clinic, 50 patients/day | Fast differential diagnosis at point of care |
| Dr. Anand | PHC Physician | Rural/semi-urban PHC | Guideline-based triage with no internet dependency |
| Nurse Meena | Triage Nurse | OPD, clinic | Pre-consultation vitals & CBC flag support |
| Dr. Kavitha | Specialist (Haematology) | Referral recipient | Structured referral notes from CDSS output |

---

## Core Value Propositions

1. **India-first design** — built around ICMR, IAP, and API clinical guidelines, not NICE or CMS
2. **No EHR required** — operates as a standalone tool; structured input via simple form/voice
3. **Explainable AI** — every recommendation includes a reasoning trace (LangGraph agent chain)
4. **SAHI-aligned governance** — all 7 Sutras embedded in design, not bolted on post-launch
5. **BODH-ready** — architecture supports independent benchmarking via BODH platform
6. **DPDP Act 2023 compliant** — patient consent captured at every data collection touchpoint

---

## Confirmed v1 Use Cases

| UC | Clinical Scenario | Acceptance Criteria |
|----|-------------------|---------------------|
| UC-01 | CBC-based anaemia / infection / thrombocytopenia triage | Accuracy ≥ 85% on labelled dataset |
| UC-02 | Medication safety – drug interaction checks | Zero missed critical interactions in test set |
| UC-03 | Chronic disease (DM/HTN) follow-up support | Clinician override rate < 20% |

**Out of scope (v1):** Imaging, surgical planning, paediatric haematology, mental health.

---

## Product Principles

- **Augment, not replace** — WISE AI-CDSS supports the GP decision; final call always with clinician
- **Explainability by default** — no black-box outputs; every suggestion shows evidence source
- **Fail safe** — when confidence is low, system defers to clinician rather than guessing
- **Minimum viable data** — collects only what is clinically necessary; no surplus data retention
- **Offline-first consideration** — core triage logic designed to function with minimal connectivity

---

## SAHI Alignment Summary

| SAHI Sutra | Product Manifestation |
|------------|-----------------------|
| Sutra 1 – Trustworthy AI | Responsible AI principles (T15); governance model (T91) |
| Sutra 2 – Reliability | RAG pipeline grounded in curated Indian guidelines (T08) |
| Sutra 3 – Explainability | LangGraph reasoning traces visible to GP at every step |
| Sutra 4 – Fairness | Bias framework across demographic subgroups (T10) |
| Sutra 5 – Privacy & Security | DPDP consent framework; threat model (T11, T18) |
| Sutra 6 – Accountability | Accountability model; audit trail (T91) |
| Sutra 7 – Continuous Improvement | BODH evaluation pipeline; sprint retrospectives (T20) |

---

## Success Metrics (v1)

| Metric | Target |
|--------|--------|
| Diagnostic accuracy (UC-01 CBC triage) | ≥ 85% |
| Drug interaction recall (UC-02) | 100% (zero missed critical) |
| Clinician acceptance rate (UC-03) | > 80% |
| SAHI compliance score (BODH) | Pass all 7 Sutras |
| DPDP consent capture rate | 100% of data collection events |
| Time to recommendation (GP workflow) | < 30 seconds per case |

---

## Roadmap (High Level)

| Phase | Sprint | Milestone |
|-------|--------|-----------|
| Foundation | Sprint 1 (Week 1) | Governance, compliance, scope, architecture baselined |
| Build | Sprint 2–3 (Weeks 2–4) | CBC triage agent, RAG pipeline, drug interaction module |
| Validate | Sprint 4 (Week 5) | Clinical validation, GP user testing, BODH submission |
| Paper & Submit | Sprint 5 (Week 6) | arXiv preprint submitted; capstone evaluation |

---

*Document owner: Sreedhar (wiseaihub) · Co-owner: Ritesh (riteshverma) · Last updated: Feb 2026*

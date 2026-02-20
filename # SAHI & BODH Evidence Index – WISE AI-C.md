# SAHI & BODH Evidence Index – WISE AI-CDSS

**Owner:** Sreedhar Byreeka (wiseaihub)  
**Scope:** All evidence artefacts for SAHI (7 Sutras + 8-step lifecycle + 32 recommendations) and BODH readiness/validation  
**Last updated:** TODO

---

## 1. How to Use This Index

- This file is the **canonical map** of SAHI/BODH evidence for WISE AI-CDSS.  
- Each table row links: **SAHI/BODH requirement → Project task(s) → Evidence file(s) → GitHub issue(s)**.  
- Keep this file updated whenever you add/rename evidence documents.

---

## 2. High-Level Evidence Map

| Area | Description | Key Tasks | Evidence Folder / File |
|------|-------------|-----------|------------------------|
| SAHI Framework Overview | Core SAHI pillar/sutra/lifecycle mapping | T02, T72, T86 | `docs/compliance/T02-SAHI-BODH-Compliance-Mapping.md` |
| SAHI Lifecycle Evidence Packs | Steps 3–8 detailed evidence | T35, T58, T65, T72, T86 | `docs/compliance/sahi-lifecycle/` |
| BODH Readiness & Alignment | BODH framework, criteria, plan | T98 | `docs/compliance/T98-BODH-Readiness-Alignment-Plan.md` |
| Testing & Validation | Performance, fairness, safety, UAT | T32, T50–T52, T55–T57, T60, T69, T87 | `docs/testing/` |
| Governance & Risk | Governance, risk, accountability | T01, T03, T31, T37, T54, T74, T77 | `docs/governance/` |
| Security & Privacy | DPDP, security, anonymisation | T11, T18, T27, T53, T76 | `docs/security/` |

---

## 3. SAHI 7 Sutras – Evidence Index

### 3.1 Sutra 1 – Trustworthy AI

| Item | SAHI Ref | Project Task(s) | Evidence File(s) | GitHub Issue(s) |
|------|----------|-----------------|------------------|------------------|
| S1-1 | Sutra 1 overview & principles | T03, T15, T38, T73 | `docs/compliance/T02-SAHI-BODH-Compliance-Mapping.md`, `docs/governance/responsible-ai-principles.md`, `docs/compliance/model-card.md` | `#T03`, `#T15`, `#T38`, `#T73` |
| S1-2 | SAHI-aligned MoHFW guidelines mapping | T38 | `docs/compliance/mohfw-alignment-report.md` | `#T38` |

> Repeat a small table like this for Sutra 2–7; each row = one evidence “unit”.

---

## 4. SAHI 8-Step Lifecycle – Evidence Index

| Step | Description | Primary Tasks | Evidence File(s) | Notes |
|------|-------------|---------------|------------------|-------|
| Step 1 | Problem formulation | T04, T13, T17 | `docs/product/use-case-definition.md`, `docs/product/clinical-workflow-mapping.md`, `docs/product/product-vision.md` | – |
| Step 2 | Data strategy | T09, T24 | `docs/data/data-governance-plan.md`, `docs/data/knowledge-base-plan.md` | – |
| Step 3 | Model development | T21, T33, T34, T63 | `docs/architecture/multi-agent-architecture.md`, `docs/ai/llm-selection-benchmark.md`, `docs/ai/prompt-library.md`, `docs/ai/experiment-tracking.md` | – |
| Step 4 | Model evaluation | T35 | `docs/compliance/sahi-step3-4-evidence.md` | – |
| Step 5 | Risk assessment | T31, T37, T54, T65 | `docs/risk/samd-risk-assessment.md`, `docs/risk/risk-register.md`, `docs/compliance/sahi-steps5-6-evidence.md` | – |
| Step 6 | Testing & validation | T32, T50–T52, T55–T57, T60, T68, T69, T87 | `docs/testing/*` | – |
| Step 7 | Deployment | T70, T72, T77, T86 | `docs/compliance/sahi-step7-8-evidence.md`, `docs/regulatory/samd-technical-file/` | – |
| Step 8 | Monitoring | T74, T80, T86 | `docs/ops/post-market-surveillance-plan.md`, `docs/ops/monitoring-dashboards.md` | – |

---

## 5. SAHI 32 Recommendations – Evidence Index (By Pillar)

> You can keep this section tight by only listing **evidence document(s)** per rec, since the T02 mapping doc already shows task-level detail.

### 5.1 Governance, Regulation, and Trust (Recs 1–8)

| Rec | Thematic Area | Evidence File(s) |
|-----|---------------|------------------|
| 1 | Risk-based classification & obligations | `docs/risk/samd-risk-assessment.md` |
| 2 | Accountability & liability | `docs/governance/governance-accountability-model-T91.md` |
| 3 | Safety-by-design metrics | `docs/testing/performance-and-safety-metrics.md` |
| 4–5 | Fairness & equity | `docs/testing/bias-fairness-report-T52-T75.md` |
| 6 | Transparency & limitations | `docs/compliance/model-card.md`, `docs/ui/explainability-design.md` |
| 7 | Post-deployment monitoring | `docs/ops/post-market-surveillance-plan.md` |
| 8 | Cross-sector governance | `docs/governance/institutional-governance-note-T92.md` |

> Repeat a compact table for Pillars 2–5.

---

## 6. BODH Alignment – Evidence Index

| BODH Criterion | Evidence File(s) | Linked Tasks |
|----------------|------------------|-------------|
| Performance metrics | `docs/testing/performance-benchmark-report-T55.md` | T55, T56, T57 |
| Robustness & generalizability | `docs/testing/robustness-generalizability-report.md` | T51, T52 |
| Bias & fairness | `docs/testing/bias-fairness-report-T52-T75.md` | T10, T52, T75 |
| Safety & clinical risk | `docs/risk/samd-risk-assessment.md`, `docs/testing/hallucination-safety-testing-T57.md` | T31, T37, T54, T57 |
| Interoperability | `docs/compliance/fhir-abdm-gap-analysis-T14.md`, `docs/compliance/abdm-integration-roadmap-T59.md` | T14, T59 |
| Data governance & privacy | `docs/data/data-governance-plan.md`, `docs/security/dpdp-framework-T11.md`, `docs/security/anonymisation-methodology-T27.md`, `docs/security/security-audit-T53-T76.md` | T09, T11, T27, T30, T53, T76 |
| Overall BODH plan | `docs/compliance/T98-BODH-Readiness-Alignment-Plan.md`, `docs/compliance/bodh-readiness-checklist-T99.md` | T98, T99, T100 |

---

## 7. File & Folder Conventions

- All compliance docs: `docs/compliance/…`
- Governance & risk: `docs/governance/…`
- Data & security: `docs/data/…`, `docs/security/…`
- Testing & validation: `docs/testing/…`
- Ops & monitoring: `docs/ops/…`
- Product & UX: `docs/product/…`, `docs/ui/…`

---

## 8. Maintenance Checklist (for T97)

- [ ] All new evidence docs linked here with file paths  
- [ ] All SAHI recs 1–32 have at least one evidence row  
- [ ] All BODH criteria have at least one evidence row  
- [ ] All links checked after any repo restructuring  
- [ ] Index reviewed at end of each sprint

# Role-based AI Competency & Training Plan (T93)

**Document ID:** T93  
**Owner:** Sreedhar Byreeka (wiseaihub)  
**Project:** WISE AI-CDSS – SAHI-Compliant Capstone  
**Related Issues:** T02, T16, T29, T49, T60, T69  

---

## 1. Purpose

This document defines a **role-based AI competency framework and training plan** for safe and effective use of WISE-CDSS.  
It operationalises **SAHI Recommendation 16** on role-based AI competencies across clinical, administrative, frontline, and leadership roles.[file:4]

---

## 2. Roles & Required Competencies

### 2.1 Competency Dimensions

For each role, we define:

- **AI Understanding:** What they need to know about AI and WISE-CDSS.  
- **WISE-CDSS Skills:** What they must be able to do in practice.  
- **Risks & Responsibilities:** Key boundaries and obligations.  
- **Training Format & Timing:** How and when we train them.

### 2.2 Competency Matrix

| Role | AI Understanding | WISE-CDSS Skills | Risks & Responsibilities | Training Format & Timing |
|------|------------------|------------------|--------------------------|--------------------------|
| **Consultant / Attending Physician** | Basic AI concepts; limitations of LLMs and CDSS; SAHI principles. | Enter or verify inputs; interpret recommendations & explanations; use override controls; document decisions. | Maintain clinical judgement; not rely solely on AI; report unsafe behaviour; respect consent and privacy. | 1–2 hour interactive workshop; quick reference guide; before UAT and go-live. |
| **Junior Doctor / Resident** | Awareness of how WISE-CDSS is used in the team. | Run scenarios under supervision; interpret outputs; escalate uncertainties. | Must not make unsupervised decisions beyond scope; escalate edge cases. | 1-hour briefing + supervised usage during pilot. |
| **Nurse / Frontline Staff** | Awareness-level understanding; basic idea of CDSS support. | Input triage data; view outputs relevant to nursing workflows; escalate to physicians. | Not to interpret or act beyond defined protocols; ensure accurate data entry. | Short briefing (30–45 min) + workflow posters; before deployment in their unit. |
| **Clinical Administrator / OPD Manager** | Understanding of WISE-CDSS role in service delivery and throughput. | Ensure correct routing; manage schedules; monitor non-clinical KPIs. | Ensure tool does not introduce bottlenecks or burden; escalate operational issues. | 45–60 min session; part of operational readiness workshops. |
| **IT / DevOps / Security** | Solid understanding of architecture, data flows, logging, and security controls. | Maintain infra; ensure logging, monitoring, backups; manage access control integrations. | Protect patient data (DPDP); ensure uptime; respond to incidents; avoid misconfigurations. | Technical deep dive (2–3 hours) plus runbooks; early in project and at each major release. |
| **Clinical Leadership (CMO, Medical Director)** | High-level understanding of SAHI, BODH, and WISE-CDSS capabilities/limitations. | Approve scope of use; review governance and risk reports; champion safe adoption. | Own clinical governance decisions; ensure policies are followed; approve escalation processes. | 45–60 min executive briefing; before pilot approval and again before scale-up. |
| **Hospital Management / CIO / CEO** | Strategic understanding of AI in health, SAHI/BODH, and institutional responsibilities. | Align WISE-CDSS with strategy; support AI governance unit; allocate resources. | Ensure sustainable, ethical deployment; avoid “shadow AI”. | Executive summary deck + Q&A; early in project. |
| **Regulatory / Quality Officer (if present)** | Knowledge of SAHI, CDSCO SaMD, DPDP, ABDM basics. | Read model card, risk assessments, SAHI lifecycle evidence; participate in audits. | Ensure compliance; escalate deviations; interface with external regulators. | 1–2 hour compliance session; prior to regulatory interactions. |

---

## 3. Training Plan

### 3.1 Training Artefacts

WISE-CDSS training will reuse and link to existing project artefacts:

- **Use case & workflow docs:** T04, T13 (for clinical context and workflows).[file:1]  
- **HITL design & clinician dashboard:** T29, T49.[file:1]  
- **Test strategy & UAT plan:** T32, T60, T69.[file:1]  
- **Model card & Responsible AI statement:** T73.[file:1]  
- **Post-market surveillance plan:** T74, T80.[file:1]

These artefacts serve as source material for role-based training content.

### 3.2 Training Sessions

| Session | Audience | Content | Duration | When |
|---------|----------|---------|----------|------|
| Clinician Introduction to WISE-CDSS | Consultants, Residents | Overview of system, SAHI principles, demo of use cases, limitations & overrides. | 60–90 min | Before UAT. |
| Workflow & Change Management | Clinicians, Nurses, Admins | Mapping of WISE-CDSS into existing workflows, roles & responsibilities, escalation paths. | 60–90 min | Before pilot. |
| Technical & Security Deep Dive | IT/DevOps/Security | Architecture, logging, monitoring, incident response, DPDP controls. | 120–180 min | Early in implementation. |
| Leadership Briefing | CMO, CIO, management | SAHI/BODH context, risk and governance model (T91), roadmap and KPIs. | 45–60 min | Early; revisited before scale-up. |

---

## 4. Competency Validation

Competency is validated via:

- **Scenario-based exercises** during UAT (T60, T69) where clinicians must:  
  - Correctly interpret outputs and explanations.  
  - Recognise when to override or escalate.  
- **Short quizzes or checklists** at the end of training sessions.  
- **Feedback loop (T64)** collecting qualitative feedback from clinicians.[file:1]

---

## 5. Maintenance

- Update this document whenever:
  - New features or agents significantly change workflows.  
  - New roles are added (e.g., telemedicine staff, external auditors).  
- Ensure this plan is referenced in:
  - Change management guidelines (T94).  
  - SAHI governance audit (T72).  

**T93 Definition of Done:**  
This document is published at `docs/governance/ai-competency-matrix-T93.md` and linked from UAT and change-management artefacts.

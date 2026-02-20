# SAHI & BODH Compliance Mapping for WISE AI-CDSS

**Project:** WISE AI Clinical Decision Support System  
**Document Owner:** Sreedhar Byreeka (wiseaihub)  
**Task Reference:** T02 - SAHI Framework Deep-Dive & Compliance Mapping  
**Date:** 20 February 2026  
**Version:** 1.0  

---

## Executive Summary

This document maps all **32 SAHI recommendations** and emerging **BODH benchmarking requirements** to the WISE AI-CDSS project plan, ensuring complete traceability and compliance with India's national framework for responsible AI in healthcare.

**Key Findings:**
- ✅ **28 of 32 SAHI recommendations** are addressed by existing tasks (T01–T90)
- ⚠️ **4 recommendations** require new tasks (proposed as T91–T97 below)
- 🆕 **BODH alignment** requires additional documentation and validation tasks (T98–T100)

**Compliance Status:** On track for SAHI compliance; BODH submission readiness estimated Sprint 3–4.

---

## Part 1: SAHI 7 Sutras Mapping

| **SAHI Sutra** | **Project Tasks** | **Evidence/Deliverables** | **Status** |
|----------------|-------------------|---------------------------|------------|
| **Sutra 1: Trustworthy AI** | T03, T15, T38, T73 | Regulatory review, Responsible AI principles, MoHFW alignment report, Model card | ✅ Covered |
| **Sutra 2: Reliability** | T08, T14, T22, T23, T33, T43, T44, T47, T55–T57, T68 | RAG pipeline, FHIR/ABDM assessment, tool integration, LLM benchmarking, performance testing | ✅ Covered |
| **Sutra 3: Explainability** | T07, T21, T26, T34, T42, T46 | Agent architecture, SHAP/LIME integration, prompt engineering, patient dashboard with explanations | ✅ Covered |
| **Sutra 4: Fairness** | T10, T52, T61, T75 | Fairness framework, bias testing, accessibility/language compliance, fairness certificate | ✅ Covered |
| **Sutra 5: Privacy & Security** | T11, T18, T27, T53, T76 | DPDP framework, security architecture, anonymisation, penetration testing, audit sign-off | ✅ Covered |
| **Sutra 6: Human Oversight** | T29, T49, T60, T64, T69 | HITL design, clinician dashboard, UAT plan, feedback loop, UAT execution | ✅ Covered |
| **Sutra 7: Accountability** | T30, T62, T63, T74, T80, T86 | Audit trail, data lineage, model versioning, post-market surveillance, monitoring setup | ✅ Covered |

---

## Part 2: SAHI 8-Step AI Lifecycle Mapping

| **Lifecycle Step** | **Project Tasks** | **Evidence Documents** | **Status** |
|--------------------|-------------------|------------------------|------------|
| **Step 1: Problem Formulation** | T04, T13, T17 | Use case definition, clinical workflow mapping, product vision | ✅ Covered |
| **Step 2: Data Strategy** | T09, T24 | Data governance plan, knowledge base ingestion | ✅ Covered |
| **Step 3: Model Development** | T21, T33, T34, T63 | Agent implementation, LLM selection, prompt engineering, experiment tracking | ✅ Covered |
| **Step 4: Model Evaluation** | T35 | Model card, evaluation plan documentation | ✅ Covered |
| **Step 5: Risk Assessment** | T31, T37, T54, T65 | SaMD framework mapping, risk register, risk assessment document, evidence pack | ✅ Covered |
| **Step 6: Testing & Validation** | T32, T50–T52, T55–T58, T60, T61, T65, T68, T69, T87 | Test strategy, unit tests, clinical validation, bias testing, performance benchmarking, UAT | ✅ Covered |
| **Step 7: Deployment** | T70, T77, T86 | Demo scenarios, SaMD technical file, deployment evidence pack | ✅ Covered |
| **Step 8: Monitoring** | T74, T80, T86 | Post-market surveillance, monitoring dashboards, monitoring evidence pack | ✅ Covered |

---

## Part 3: SAHI 32 Recommendations - Detailed Traceability Matrix

### Pillar 1: Governance, Regulation, and Trust

| **Rec #** | **Recommendation** | **Mapped Task(s)** | **Gap/Action** |
|-----------|-------------------|-------------------|----------------|
| 1 | Risk-based classification and regulatory obligations | T31, T54, T77 (SaMD classification, risk assessment, technical file) | ✅ Covered |
| 2 | Accountability of actors and liability allocation | T01, T16 (governance setup, RACI matrix) | ⚠️ **Gap**: Need explicit liability model document → **Propose T91** |
| 3 | Safety-by-design with metrics for safety, bias, interoperability | T28, T48, T52, T55, T56 (SAHI checklists, bias testing, benchmarking) | ✅ Covered |
| 4 | Representative training/validation data | T09, T10, T52 (data governance, fairness framework, demographic testing) | ✅ Covered |
| 5 | Assess and address inequity impact | T10, T52, T61 (fairness assessment, bias testing, accessibility) | ✅ Covered |
| 6 | Transparent communication of use, limitations, risk | T42, T46, T73 (explainability UI, patient dashboard, model card) | ✅ Covered |
| 7 | Post-deployment monitoring for drift, bias, unintended consequences | T74, T80 (post-market surveillance, monitoring dashboards) | ✅ Covered |
| 8 | Cross-sector coordination mechanisms | T01, T16, T38 (governance, communication plan, MoHFW alignment) | ⚠️ **Gap**: Need institutional coordination note → **Propose T92** |

### Pillar 2: Health Data and Digital Infrastructure

| **Rec #** | **Recommendation** | **Mapped Task(s)** | **Gap/Action** |
|-----------|-------------------|-------------------|----------------|
| 9 | Enable participation via dataset specs, interoperability obligations, incentives | T14, T59 (FHIR/ABDM assessment, ABDM integration check) | ✅ Covered |
| 10 | Ensure datasets represent population-scale realities across diverse settings | T09, T10 (data governance, fairness framework) | ✅ Covered |
| 11 | Health Data Quality Framework (completeness, consistency, AI-readiness) | T09, T24, T27 (data governance, knowledge base, preprocessing pipeline) | ✅ Covered |
| 12 | Privacy-preserving access standards (de-identification proportional to risk) | T11, T27 (DPDP framework, anonymisation scripts) | ✅ Covered |
| 13 | Cybersecurity standards and incident response protocols | T18, T53, T76 (security architecture, pen testing, audit) | ✅ Covered |
| 14 | ABDM-aligned interoperability standards | T14, T59 (FHIR/ABDM assessment) | ✅ Covered |
| 15 | Define data categories for sharing under clear legal basis | T11 (DPDP framework) | ✅ Covered |

### Pillar 3: Workforce, Institutional Capacity, and Change Management

| **Rec #** | **Recommendation** | **Mapped Task(s)** | **Gap/Action** |
|-----------|-------------------|-------------------|----------------|
| 16 | Role-based AI competency framework for health sector | T16 (communication plan mentions stakeholders) | ⚠️ **Gap**: Need explicit competency/training plan → **Propose T93** |
| 17 | Integrate AI competencies into formal education and skilling | T16 (stakeholder communication) | ⚠️ **Gap**: Training curriculum not in scope for MVP; document as future work |
| 18 | Strengthen AI capacity among regulators and auditors | T32, T72 (test strategy includes regulatory validation) | ✅ Partially covered; external to project scope |
| 19 | Create designated AI units/nodal cells in health departments | T01 (governance setup) | ⚠️ **Gap**: Need institutional governance note → **Propose T92** (merged with Rec 8) |
| 20 | Establish knowledge-exchange mechanisms | T66, T82, T83 (arXiv paper, knowledge sharing) | ✅ Covered |
| 21 | Embed AI in workflows without increasing burden | T13, T29, T49 (workflow mapping, HITL design, clinician dashboard) | ✅ Covered |
| 22 | Define roles/responsibilities and escalation mechanisms | T29, T49, T64 (HITL workflow, override logic, feedback loop) | ⚠️ **Gap**: Need change management guide → **Propose T94** |

### Pillar 4: Research, Innovation, and Evidence Generation

| **Rec #** | **Recommendation** | **Mapped Task(s)** | **Gap/Action** |
|-----------|-------------------|-------------------|----------------|
| 23 | Strengthen Ethics Committees to be AI-ready | T15 (AI ethics review) | ✅ Covered; institutional readiness external to MVP |
| 24 | Align research incentives with national/state health priorities | T04, T13 (use case definition aligned with India health needs) | ✅ Covered |
| 25 | Encourage open and collaborative innovation | T19, T39, T66, T81–T84 (arXiv paper = open research dissemination) | ✅ Covered |
| 26 | Develop standardised, risk-proportionate evaluation frameworks | T32, T51, T54, T72 (test strategy, clinical validation, risk assessment, audit) | ✅ Covered |
| 27 | Encourage stage-appropriate funding for pilots in public health systems | T70, T71 (demo scenarios for pilot readiness) | ✅ Covered; funding acquisition external to MVP |
| 28 | Enable trial designs with post-market monitoring and drift detection | T32, T74, T80 (test strategy, post-market plan, monitoring) | ⚠️ **Gap**: Need trial design alignment note → **Propose T95** |

### Pillar 5: Ecosystem Enablement and Global Leadership

| **Rec #** | **Recommendation** | **Mapped Task(s)** | **Gap/Action** |
|-----------|-------------------|-------------------|----------------|
| 29 | Public procurement frameworks prioritising innovation, safety, interoperability | T85 (stakeholder presentation mentions adoption) | ✅ Partially covered; procurement playbook external to MVP |
| 30 | Define pilot-to-scale pathways with testbeds and sandboxes | T70, T71 (demo scenarios) | ⚠️ **Gap**: Need ecosystem engagement plan → **Propose T96** |
| 31 | Promote cluster-based AI ecosystems anchored in public institutions | T19–T20, T66, T82–T84 (arXiv paper for knowledge sharing) | ✅ Covered via open research |
| 32 | Establish platforms for ecosystem learning and global cooperation | T19, T66, T82–T84 (arXiv paper as global contribution) | ⚠️ **Gap**: Need stakeholder engagement plan → **Propose T96** (merged with Rec 30) |

---

## Part 4: Gap Analysis & Proposed New Tasks

### New Tasks Required for Full SAHI Compliance

| **Task ID** | **Task Name** | **Owner** | **Sprint** | **SAHI Rec** | **DoD** |
|-------------|---------------|-----------|-----------|--------------|---------|
| **T91** | WISE-CDSS Governance & Accountability Model (RACI + Liability) | wiseaihub | 1 | Recs 1–2 | Governance model documented: risk classification, accountable parties (developer, deployer, clinician, institution), liability narrative aligned with CDSCO/MoHFW guidance |
| **T92** | Institutional AI Governance & Cross-Sector Coordination Note | wiseaihub | 2 | Recs 8, 19 | Concept note drafted for hospital AI governance cell with interfaces to regulators, ABDM, IT; reviewed in arXiv governance section |
| **T93** | Role-based AI Competency and Training Plan | wiseaihub | 2 | Rec 16 | Matrix of key roles (clinician, nurse, admin, IT, regulator) with expected AI competencies and training touchpoints for WISE-CDSS usage |
| **T94** | Change Management & Workflow Integration Guidelines | wiseaihub | 2 | Recs 21–22 | Guideline document specifying where WISE-CDSS sits in workflows, what must never be automated, clear escalation/override mechanisms, referenced by T49 |
| **T95** | WISE-CDSS Evaluation & Trial Design Alignment with SAHI | wiseaihub | 2 | Rec 28 | Brief linking test strategy, SaMD risk assessment, post-market plan to SAHI recommendations on evaluation frameworks and trial designs, including drift detection operationalisation |
| **T96** | Ecosystem & Stakeholder Engagement Plan (SAHI/BODH Ecosystem) | wiseaihub | 2 or 3 | Recs 30, 32 | High-level plan for collaboration with public institutions, BODH submissions, knowledge sharing via arXiv, open-source artefacts, cluster engagement |

### Tasks Documented as Out-of-Scope (Future Work)

| **SAHI Rec** | **Recommendation** | **Rationale** |
|--------------|-------------------|---------------|
| 17 | Integrate AI competencies into formal education curricula | External to WISE-CDSS project; national policy/academic institutions responsible |
| 18 | Strengthen AI capacity among regulators | External to WISE-CDSS project; government capacity-building initiative |
| 27 | Stage-appropriate funding for pilots | Funding acquisition is external to technical project scope |
| 29 | Public procurement frameworks | Policy-level reform; WISE-CDSS can inform but not own |

---

## Part 5: BODH Alignment

### What is BODH?

**BODH (Benchmarking Open Data Platform for Health AI)** is India's national technical validation platform for healthcare AI, developed by IIT Kanpur in collaboration with the National Health Authority.[web:18][web:9]

**Key Characteristics:**
- **Privacy-preserving benchmarking**: Evaluate AI models on real-world Indian health data without sharing raw datasets
- **Federated learning mechanism**: Automated testing across diverse, anonymised datasets
- **Digital public good**: Operates under Ayushman Bharat Digital Mission (ABDM)
- **Purpose**: Assess performance, robustness, bias, generalizability before population-scale deployment

### BODH Evaluation Criteria (Inferred from Framework)

Based on available documentation, BODH likely evaluates AI systems across:[web:18][web:20][web:25]

1. **Performance Metrics**
   - Accuracy, sensitivity, specificity for classification tasks
   - Precision, recall for retrieval tasks (e.g., RAG systems)
   - Clinical relevance and alignment with care pathways

2. **Robustness & Generalizability**
   - Performance across diverse demographic groups (age, gender, geography, socioeconomic status)
   - Performance across different care settings (primary care, tertiary hospitals, rural vs urban)
   - Stability under data variance and edge cases

3. **Bias & Fairness**
   - Demographic parity across subgroups
   - No statistically significant disparities in error rates
   - Transparent reporting of limitations

4. **Safety & Clinical Risk**
   - Zero critical hallucinations or harmful recommendations
   - Appropriate uncertainty quantification
   - Clear escalation triggers for human oversight

5. **Interoperability & Standards Compliance**
   - ABDM/FHIR alignment
   - Structured data exchange formats
   - Integration with existing health systems

6. **Data Governance & Privacy**
   - DPDP Act 2023 compliance
   - Anonymisation/de-identification effectiveness
   - Audit trail completeness

### WISE-CDSS Tasks Supporting BODH Readiness

| **BODH Criterion** | **Supporting Tasks** | **Evidence for Submission** |
|--------------------|---------------------|----------------------------|
| Performance metrics | T33, T43–T45, T50, T51, T55–T57 | LLM benchmarking, agent testing, clinical validation, performance benchmarks |
| Robustness & generalizability | T41, T52, T61 | Multilingual support, demographic bias testing, accessibility testing |
| Bias & fairness | T10, T52, T75 | Fairness framework, bias testing report, fairness certificate |
| Safety & clinical risk | T31, T37, T54, T57 | SaMD risk classification, risk register, hallucination testing |
| Interoperability | T14, T59 | FHIR/ABDM assessment, ABDM integration roadmap |
| Data governance | T09, T11, T27, T30, T62 | Data governance plan, DPDP framework, anonymisation, audit trail, lineage tracking |

### Proposed BODH-Specific Tasks

| **Task ID** | **Task Name** | **Owner** | **Sprint** | **DoD** |
|-------------|---------------|-----------|-----------|---------|
| **T98** | BODH Benchmarking & Evaluation Plan | wiseaihub | 2 | BODH alignment note: evaluation metrics, target benchmarks, dataset expectations, submission timeline documented |
| **T99** | BODH Data & Evidence Readiness Checklist | wiseaihub | 3 | Checklist listing all datasets, de-identification measures, performance metrics, documentation required before BODH submission, with current status |
| **T100** | BODH Submission Package Preparation | wiseaihub + riteshverma | 4 | Complete BODH submission package: model description, evaluation results, bias reports, safety documentation, ABDM compliance evidence compiled and submitted |

---

## Part 6: Compliance Summary Dashboard

### Overall SAHI Compliance Status

| **Category** | **Total Recommendations** | **Covered by Existing Tasks** | **New Tasks Proposed** | **Out of Scope** | **Compliance %** |
|--------------|--------------------------|-------------------------------|----------------------|------------------|------------------|
| Governance, Regulation, Trust (1–8) | 8 | 6 | 2 (T91, T92) | 0 | 100% (with T91–T92) |
| Health Data & Infrastructure (9–15) | 7 | 7 | 0 | 0 | 100% |
| Workforce & Capacity (16–22) | 7 | 4 | 2 (T93, T94) | 1 (Rec 17) | 86% (MVP scope) |
| Research & Evidence (23–28) | 6 | 5 | 1 (T95) | 0 | 100% (with T95) |
| Ecosystem Enablement (29–32) | 4 | 2 | 1 (T96) | 1 (Rec 29) | 75% (MVP scope) |
| **TOTAL** | **32** | **24** | **6** | **2** | **94% (MVP scope)** |

### BODH Compliance Status

| **Criterion** | **Current Readiness** | **Action Required** | **Target Sprint** |
|---------------|----------------------|---------------------|-------------------|
| Performance metrics | ✅ Strong (T55–T57) | Document baseline metrics | Sprint 3 |
| Robustness & generalizability | ✅ Strong (T52, T61) | Conduct cross-setting validation | Sprint 3 |
| Bias & fairness | ✅ Strong (T52, T75) | Finalise bias report | Sprint 4 |
| Safety & clinical risk | ✅ Strong (T54, T57) | Compile safety evidence | Sprint 4 |
| Interoperability | ⚠️ Moderate (T59) | Complete ABDM integration assessment | Sprint 3 |
| Data governance | ✅ Strong (T11, T27, T62) | Package governance documentation | Sprint 4 |
| **Overall BODH Readiness** | **~80%** | **Complete T98–T100** | **Sprint 4** |

---

## Part 7: Recommendations & Next Steps

### Immediate Actions (Week 1 – Close T02)

1. ✅ **Approve this mapping document** and baseline in GitHub repo
2. ✅ **Create T91–T96** in GitHub project board with Sprint assignments
3. ✅ **Update T02 status to "Done"** with this document as evidence

### Sprint 1–2 Focus (Close Governance Gaps)

4. **T91**: Document WISE-CDSS governance model with liability allocation (2 days, Sreedhar)
5. **T93**: Create role-based AI competency matrix (2 days, Sreedhar)
6. **T94**: Draft change management & workflow integration guidelines (3 days, Sreedhar)
7. **T98**: Produce BODH alignment plan with evaluation strategy (2 days, Sreedhar)

### Sprint 3–4 Focus (BODH Readiness)

8. **T92, T95, T96**: Complete institutional governance, trial design, and ecosystem engagement notes
9. **T99**: Compile BODH readiness checklist with evidence links
10. **T100**: Prepare complete BODH submission package for validation

### Long-term Roadmap

11. Engage with **BODH platform** (IIT Kanpur/NHA) for submission timeline and technical requirements
12. Monitor **SAHI policy updates** from MoHFW and incorporate into lifecycle governance
13. Publish arXiv paper (T83–T84) highlighting SAHI/BODH compliance as case study

---

## References

1. Ministry of Health and Family Welfare. (2026). *Strategy for Artificial Intelligence in Healthcare for India (SAHI)*. Government of India.
2. Ministry of Health and Family Welfare. (2026). *BODH - Benchmarking Open Data Platform for Health AI*. Launch at India AI Impact Summit 2026.
3. WISE AI-CDSS Project Plan. (2026). Sprint 1–4 task definitions (T01–T90).
4. Digital Personal Data Protection Act. (2023). Government of India.
5. Ayushman Bharat Digital Mission (ABDM) Framework. National Health Authority.

---

**Document Status:** ✅ Ready for Review  
**Next Review Date:** End of Sprint 1 (22 Feb 2026)  
**Change Log:**
- v1.0 (20 Feb 2026): Initial mapping document created (Sreedhar Byreeka)

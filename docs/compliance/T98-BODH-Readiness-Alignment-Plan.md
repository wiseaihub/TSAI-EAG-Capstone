# BODH Readiness & Alignment Plan for WISE AI-CDSS

**BODH Platform for Health AI Benchmarking & Validation**

---

**Project:** WISE AI Clinical Decision Support System  
**Document Owner:** Sreedhar Byreeka (wiseaihub)  
**Task Reference:** T98 - BODH Benchmarking & Evaluation Plan  
**Date:** 20 February 2026  
**Version:** 1.0  

---

## Executive Summary

This document outlines the **BODH (Benchmarking Open Data Platform for Health AI)** framework and details how the WISE AI-CDSS project will prepare for validation and submission to BODH during Sprint 3–4.

**BODH** is India's national technical validation platform for healthcare AI, developed by IIT Kanpur in collaboration with the National Health Authority (NHA), launched February 2026 at the India AI Impact Summit[web:18][web:9].

**Key Objectives:**
1. Understand BODH evaluation criteria and submission requirements
2. Map WISE-CDSS capabilities to BODH benchmarking dimensions
3. Identify gaps and prepare evidence packages for validation
4. Plan phased BODH submission strategy aligned with project milestones

**Target Submission:** End of Sprint 4 (March 2026) for initial benchmarking evaluation

---

## Part 1: Understanding BODH

### 1.1 What is BODH?

**BODH** stands for **Benchmarking Open Data Platform for Health AI**[web:18][web:25]

**Developed by:** Indian Institute of Technology (IIT) Kanpur in collaboration with National Health Authority (NHA)  
**Launched:** February 2026 at India AI Impact Summit, New Delhi  
**Operates under:** Ayushman Bharat Digital Mission (ABDM) as a Digital Public Good

### 1.2 Core Purpose & Functions

BODH enables **systematic, privacy-preserving evaluation** of healthcare AI models before population-scale deployment:[web:18][web:9][web:25]

| **Function** | **Description** |
|--------------|-----------------|
| **Privacy-Preserving Benchmarking** | Evaluate AI models on real-world Indian health data without sharing raw datasets; protects patient privacy while ensuring scientific rigor |
| **Federated Learning Mechanism** | Automated testing across diverse, anonymised datasets from multiple sources (public hospitals, medical colleges, research institutions) |
| **Performance Validation** | Assess accuracy, sensitivity, specificity, clinical relevance across different populations and care settings |
| **Bias & Fairness Testing** | Detect demographic disparities, ensure equitable performance across age, gender, geography, socioeconomic groups |
| **Robustness Evaluation** | Test generalizability, stability under variance, edge case handling |
| **Standards Alignment** | Verify ABDM/FHIR interoperability, DPDP compliance, clinical safety protocols |
| **Knowledge Hub** | Promote best practices in health AI development, governance, and implementation |

### 1.3 Why BODH Matters for WISE-CDSS

1. **Regulatory Credibility**: BODH validation strengthens CDSCO SaMD submission (T77) and demonstrates real-world readiness
2. **Trust Building**: Independent benchmarking by IIT Kanpur/NHA increases stakeholder confidence (clinicians, hospitals, regulators)
3. **National Integration**: Aligns WISE-CDSS with India's digital health infrastructure (ABDM, NDHM)
4. **Continuous Improvement**: Identifies performance gaps across diverse Indian populations and care settings
5. **Ecosystem Participation**: Positions WISE-CDSS as a validated solution in India's responsible AI healthcare ecosystem

---

## Part 2: BODH Evaluation Criteria (Framework Analysis)

Based on BODH launch documentation and SAHI alignment, the platform likely evaluates AI systems across **6 key dimensions**:[web:18][web:20][web:25]

### 2.1 Performance Metrics

**What BODH Evaluates:**
- **Classification tasks**: Accuracy, sensitivity (recall), specificity, positive/negative predictive value, F1-score, AUC-ROC
- **Retrieval tasks** (RAG systems): Precision, recall, F1-score, NDCG (normalized discounted cumulative gain)
- **Regression tasks**: Mean absolute error (MAE), root mean squared error (RMSE), R² score
- **Clinical relevance**: Alignment with standard care pathways, actionability of recommendations

**WISE-CDSS Evidence:**
| **WISE Component** | **Performance Metrics** | **Evidence Task** | **Current Status** |
|--------------------|------------------------|-------------------|-------------------|
| Diagnosis Support Agent (T43) | Triage accuracy >80% on symptom sets | T51, T55 | Sprint 3 testing |
| Medication Safety Agent (T44) | Drug interaction detection: zero false negatives on test pairs | T50, T51 | Sprint 3 testing |
| Chronic Disease Agent (T45) | Management plan quality reviewed by SME | T51, T55 | Sprint 3 testing |
| RAG Pipeline (T23) | Precision >0.75, Recall >0.70 on clinical queries | T56 | Sprint 3 testing |
| LLM Hallucination Rate (T57) | Zero critical hallucinations in 50 test prompts | T57 | Sprint 3 testing |
| End-to-End Latency (T55) | Response time <5 seconds | T55 | Sprint 3 testing |

### 2.2 Robustness & Generalizability

**What BODH Evaluates:**
- Performance consistency across **demographic groups**: age, gender, urban/rural, income levels
- Performance across **care settings**: primary health centres, district hospitals, tertiary medical colleges
- **Edge case handling**: rare conditions, ambiguous inputs, missing data scenarios
- **Distribution shift**: Model stability when tested on datasets from different regions/institutions

**WISE-CDSS Evidence:**
| **Robustness Dimension** | **WISE Approach** | **Evidence Task** | **Gap Analysis** |
|-------------------------|-------------------|-------------------|------------------|
| Demographic fairness | Bias testing across 4+ demographic subgroups (T52) | T52 | ✅ Covered |
| Geographic diversity | Multilingual support (Hindi, Telugu) for diverse populations (T41) | T41, T61 | ✅ Covered |
| Care setting adaptability | Clinical workflow mapping includes primary to tertiary settings (T13) | T13, T49 | ⚠️ Need explicit multi-setting validation data |
| Edge cases | Unit testing with mocks, hallucination testing (T50, T57) | T50, T57 | ✅ Covered |

**Action Required:** Document WISE-CDSS testing across at least 2 care setting types (e.g., urban tertiary hospital + rural primary health centre scenarios) in T99 checklist.

### 2.3 Bias & Fairness

**What BODH Evaluates:**
- **Demographic parity**: Similar accuracy/error rates across protected groups (gender, age, caste, religion, geography)
- **Equitable false positive/negative rates**: No subgroup suffers disproportionately higher clinical risk
- **Accessibility**: Language, literacy, disability accommodations
- **Transparency**: Clear documentation of model limitations and known biases

**WISE-CDSS Evidence:**
| **Fairness Criterion** | **WISE Approach** | **Evidence Task** | **Status** |
|-----------------------|-------------------|-------------------|-----------|
| Demographic subgroup analysis | Statistical testing for disparities across 4 groups (T52) | T52 | Sprint 3 |
| Language equity | Hindi + Telugu + English support (T41) | T41, T61 | Sprint 3 |
| Accessibility compliance | WCAG 2.1 AA testing (T61) | T61 | Sprint 3 |
| Bias documentation | Fairness framework (T10), fairness certificate (T75) | T10, T75 | Sprint 1 & 4 |

**BODH Submission Package:** Bias testing report (T52) + Fairness certificate (T75) + Accessibility audit (T61)

### 2.4 Safety & Clinical Risk

**What BODH Evaluates:**
- **SaMD risk classification**: Alignment with CDSCO Medical Device Rules 2017
- **Clinical safety incidents**: Rate of harmful recommendations, contraindication violations
- **Uncertainty quantification**: Model confidence scores, "I don't know" triggers
- **Human oversight mechanisms**: Clear escalation paths, clinician override capabilities
- **Failure modes**: System behavior under degraded conditions (network loss, data corruption)

**WISE-CDSS Evidence:**
| **Safety Dimension** | **WISE Approach** | **Evidence Task** | **Status** |
|---------------------|-------------------|-------------------|-----------|
| SaMD risk class | Risk assessment document (T54), CDSCO technical file (T77) | T54, T77 | Sprint 3–4 |
| Clinical safety testing | 10 clinical scenarios validated by SME (T51) | T51 | Sprint 3 |
| Hallucination prevention | Zero critical hallucinations in 50 prompts (T57) | T57 | Sprint 3 |
| HITL workflow | Clinician dashboard with override logging (T49) | T29, T49 | Sprint 2–3 |
| Risk register | 10+ clinical AI risks documented with mitigations (T37) | T37 | Sprint 2 |

**BODH Submission Package:** SaMD risk assessment (T54) + Clinical validation report (T51) + Safety testing results (T57) + HITL workflow spec (T29, T49)

### 2.5 Interoperability & Standards Compliance

**What BODH Evaluates:**
- **ABDM alignment**: Health ID integration, consent framework, data exchange protocols
- **HL7 FHIR compatibility**: Structured data formats, resource definitions (Patient, Observation, DiagnosticReport, MedicationRequest)
- **Ayushman Bharat integration**: Health facility registry, health professional registry linkage
- **Data standards**: LOINC (lab codes), SNOMED CT (clinical terms), ICD-10 (diagnosis codes)
- **API interoperability**: RESTful interfaces, authentication/authorization (OAuth 2.0)

**WISE-CDSS Evidence:**
| **Interoperability Dimension** | **WISE Approach** | **Evidence Task** | **Gap Analysis** |
|-------------------------------|-------------------|-------------------|------------------|
| FHIR assessment | Gap analysis complete (T14) | T14 | ✅ Sprint 1 |
| ABDM compliance check | Integration roadmap documented (T59) | T59 | ⚠️ Sprint 3 (in progress) |
| API gateway design | Backend integration layer (T47) | T47 | ✅ Sprint 3 |
| Clinical terminology standards | Not explicitly scoped | — | ⚠️ **Gap**: Document LOINC/SNOMED usage in T99 |

**Action Required:** 
1. Complete T59 (ABDM integration assessment) with concrete compliance evidence
2. Document clinical terminology standards (LOINC, SNOMED, ICD-10) usage in knowledge base (T24) and agent outputs (T43–T45)

### 2.6 Data Governance & Privacy

**What BODH Evaluates:**
- **DPDP Act 2023 compliance**: Consent mechanisms, purpose limitation, data minimization, retention policies
- **Anonymisation effectiveness**: PII removal, re-identification risk assessment
- **Audit trail completeness**: All AI actions logged with timestamps, user IDs, input/output data
- **Data lineage**: Provenance tracking from source to model output
- **Cybersecurity posture**: Encryption (at rest, in transit), access controls, incident response plans

**WISE-CDSS Evidence:**
| **Governance Dimension** | **WISE Approach** | **Evidence Task** | **Status** |
|-------------------------|-------------------|-------------------|-----------|
| DPDP framework | Consent framework document (T11) | T11 | Sprint 1 |
| Anonymisation | Anonymisation scripts tested, PII removal verified (T27) | T27 | Sprint 2 |
| Audit trail | Logging architecture design, agent action coverage (T30) | T30, T62 | Sprint 2–3 |
| Data lineage | Provenance tracking implemented (T62) | T62 | Sprint 3 |
| Security audit | Pen testing, DPDP compliance sign-off (T53, T76) | T53, T76 | Sprint 3–4 |
| Data governance plan | Dataset inventory, governance plan approved (T09) | T09 | Sprint 1 |

**BODH Submission Package:** DPDP compliance documentation (T11, T76) + Anonymisation validation (T27) + Audit trail spec (T30) + Data lineage map (T62) + Security audit report (T53, T76)

---

## Part 3: WISE-CDSS BODH Readiness Assessment

### 3.1 Current Readiness Score (Sprint 1 Baseline)

| **BODH Criterion** | **Weight** | **Readiness** | **Score** | **Evidence** | **Gap** |
|--------------------|-----------|---------------|-----------|--------------|---------|
| Performance Metrics | 20% | 60% | 12/20 | Tasks planned (T55–T57) but not yet executed | Execute testing in Sprint 3 |
| Robustness & Generalizability | 15% | 50% | 7.5/15 | Bias testing planned (T52), multilingual (T41), but no multi-setting validation | Add care setting diversity validation |
| Bias & Fairness | 20% | 70% | 14/20 | Framework defined (T10), testing planned (T52, T61, T75) | Execute testing in Sprint 3 |
| Safety & Clinical Risk | 20% | 65% | 13/20 | Risk assessment (T54), HITL design (T29), testing planned (T51, T57) | Execute clinical validation |
| Interoperability | 10% | 40% | 4/10 | FHIR/ABDM assessment (T14, T59) in progress, no concrete compliance evidence yet | Complete T59, document standards |
| Data Governance | 15% | 80% | 12/15 | Strong coverage (T09, T11, T27, T30, T62) with Sprint 1–2 deliverables | Finalise security audit (T53, T76) |
| **Overall BODH Readiness** | **100%** | **62%** | **62.5/100** | **Sprint 1 baseline** | **Target 85%+ by Sprint 4** |

### 3.2 Readiness Trajectory

| **Sprint** | **Target Readiness** | **Key Deliverables** | **Milestone** |
|-----------|---------------------|---------------------|---------------|
| **Sprint 1** (Current) | 62% | Governance frameworks, data plans, architecture design (T01–T20) | ✅ Foundation established |
| **Sprint 2** | 70% | SAHI compliance checklists (T28), HITL design (T29), audit architecture (T30), risk assessment (T31) | Governance + design complete |
| **Sprint 3** | 82% | Performance testing (T55–T57), bias testing (T52), clinical validation (T51), ABDM assessment (T59) | Validation + testing complete |
| **Sprint 4** | 90%+ | Final audits (T72, T76), fairness certificate (T75), SaMD technical file (T77), BODH submission (T100) | **BODH submission ready** |

---

## Part 4: BODH Submission Strategy

### 4.1 Phased Submission Approach

Given BODH's novelty (launched Feb 2026) and limited public documentation, we propose a **3-phase engagement strategy**:

#### Phase 1: Early Engagement & Requirements Clarification (Sprint 2)
**Objective:** Understand BODH submission process, technical requirements, dataset expectations

**Actions:**
1. **Contact IIT Kanpur BODH team** via NHA channels or ABDM developer portal
2. Request:
   - Submission guidelines and technical documentation
   - Dataset characteristics (size, format, anonymisation standards)
   - Evaluation timeline and feedback cycle
   - Example submission packages or case studies
3. **Document findings** in T98 (BODH Benchmarking & Evaluation Plan)

**Deliverable:** BODH submission requirements document (Week 2)

#### Phase 2: Evidence Package Preparation (Sprint 3)
**Objective:** Compile comprehensive documentation and test results aligned with BODH criteria

**Actions:**
1. Complete all testing tasks (T50–T57, T60–T61)
2. Generate evaluation reports:
   - Performance metrics report (T55)
   - RAG evaluation report (T56)
   - Hallucination & safety testing report (T57)
   - Bias & fairness report (T52)
   - Clinical validation report (T51)
   - Accessibility audit report (T61)
3. Compile governance evidence:
   - DPDP compliance documentation (T11, T27, T76)
   - SaMD risk assessment (T54)
   - Audit trail specification (T30)
   - Data lineage map (T62)
4. Package ABDM alignment evidence (T59)
5. Create **BODH Readiness Checklist** (T99) mapping all evidence to BODH criteria

**Deliverable:** Complete evidence package (End of Sprint 3)

#### Phase 3: Submission & Iterative Validation (Sprint 4)
**Objective:** Submit WISE-CDSS to BODH platform and address feedback

**Actions:**
1. Prepare formal submission package (T100):
   - Model architecture documentation
   - Training data description (anonymised)
   - Evaluation methodology and results
   - Bias and fairness analysis
   - Safety and clinical risk assessment
   - Interoperability evidence
   - Governance and compliance documentation
2. Submit to BODH platform via official channels
3. Participate in benchmarking evaluation process
4. Address any feedback or additional testing requirements
5. Obtain BODH validation certificate (if available) or benchmarking report

**Deliverable:** BODH validation report / certificate (Sprint 4 or post-MVP)

### 4.2 Submission Package Structure (Template)

Based on standard AI model validation frameworks and SAHI/BODH alignment:[web:24][web:27]

```
WISE-CDSS BODH Submission Package/
│
├── 1_Executive_Summary.pdf
│   ├── System overview (1 page)
│   ├── Clinical use cases (diagnosis, medication, chronic disease)
│   ├── Key performance metrics summary
│   └── SAHI/ABDM compliance statement
│
├── 2_Model_Architecture/
│   ├── 2.1_System_Architecture_Diagram.pdf (from T07, T08)
│   ├── 2.2_Multi-Agent_Design.pdf (LangGraph orchestration, T21)
│   ├── 2.3_RAG_Pipeline_Specification.pdf (T23, T24)
│   └── 2.4_LLM_Selection_Rationale.pdf (T33)
│
├── 3_Data_Strategy/
│   ├── 3.1_Data_Governance_Plan.pdf (T09)
│   ├── 3.2_Knowledge_Base_Sources.pdf (PubMed, MoHFW guidelines, T24)
│   ├── 3.3_Anonymisation_Methodology.pdf (T27)
│   └── 3.4_Data_Quality_Framework.pdf (completeness, consistency)
│
├── 4_Performance_Evaluation/
│   ├── 4.1_Performance_Benchmarking_Report.pdf (T55)
│   │   └── Latency, accuracy, end-to-end metrics
│   ├── 4.2_RAG_Evaluation_Report.pdf (T56)
│   │   └── Precision, recall, retrieval quality
│   ├── 4.3_Clinical_Validation_Report.pdf (T51)
│   │   └── 10 clinical scenarios, SME review
│   └── 4.4_Agent_Performance_by_Task.pdf (T43–T45)
│       └── Diagnosis accuracy, drug interaction detection, chronic disease management
│
├── 5_Bias_and_Fairness/
│   ├── 5.1_Fairness_Framework.pdf (T10)
│   ├── 5.2_Demographic_Bias_Testing_Report.pdf (T52)
│   │   └── Statistical analysis across age, gender, geography, SES
│   ├── 5.3_Accessibility_Audit.pdf (T61)
│   │   └── WCAG 2.1 AA compliance, multilingual testing
│   └── 5.4_Fairness_Certificate.pdf (T75)
│
├── 6_Safety_and_Clinical_Risk/
│   ├── 6.1_SaMD_Risk_Classification.pdf (T31, T54)
│   │   └── CDSCO risk class, rationale
│   ├── 6.2_Clinical_Risk_Register.pdf (T37)
│   │   └── 10+ risks with mitigations
│   ├── 6.3_Hallucination_Safety_Testing.pdf (T57)
│   │   └── Zero critical hallucinations evidence
│   └── 6.4_HITL_Workflow_Specification.pdf (T29, T49)
│       └── Clinician override, escalation paths
│
├── 7_Interoperability/
│   ├── 7.1_FHIR_ABDM_Gap_Analysis.pdf (T14)
│   ├── 7.2_ABDM_Integration_Roadmap.pdf (T59)
│   ├── 7.3_API_Gateway_Specification.pdf (T47)
│   └── 7.4_Clinical_Terminology_Standards.pdf (LOINC, SNOMED, ICD-10)
│
├── 8_Governance_and_Privacy/
│   ├── 8.1_DPDP_Compliance_Framework.pdf (T11)
│   ├── 8.2_Security_Architecture.pdf (T18)
│   ├── 8.3_Audit_Trail_Specification.pdf (T30)
│   ├── 8.4_Data_Lineage_Map.pdf (T62)
│   ├── 8.5_Penetration_Testing_Report.pdf (T53)
│   └── 8.6_DPDP_Audit_Sign-Off.pdf (T76)
│
├── 9_SAHI_Compliance/
│   ├── 9.1_SAHI_Traceability_Matrix.pdf (T02 – this document)
│   ├── 9.2_SAHI_Lifecycle_Evidence_Packs.pdf (T35, T58, T65, T86)
│   └── 9.3_SAHI_Full_Audit_Report.pdf (T72)
│
├── 10_Post_Market_Surveillance/
│   ├── 10.1_Post_Market_Surveillance_Plan.pdf (T74)
│   ├── 10.2_Monitoring_Dashboard_Specification.pdf (T80)
│   └── 10.3_Model_Drift_Detection_Protocol.pdf
│
└── 11_Supporting_Materials/
    ├── 11.1_Demo_Video.mp4 (T71)
    ├── 11.2_ArXiv_Paper_Draft.pdf (T83)
    └── 11.3_Model_Card.pdf (T73)
```

### 4.3 Expected BODH Evaluation Process

Based on federated learning architecture mentioned in BODH launch:[web:22]

1. **Submission Review** (1–2 weeks)
   - IIT Kanpur/NHA team reviews documentation completeness
   - Requests clarifications or additional evidence

2. **Model Upload** (1 week)
   - WISE-CDSS model (or API endpoint) provided to BODH platform
   - Containerised deployment (Docker image, T79) may be required

3. **Automated Benchmarking** (2–4 weeks)
   - BODH runs model against diverse anonymised datasets via federated learning
   - Tests performance, robustness, bias across multiple Indian healthcare settings
   - No raw data shared; only aggregated metrics returned

4. **Human Expert Review** (2–3 weeks)
   - Clinical SMEs review outputs for clinical relevance and safety
   - Regulatory experts assess governance and compliance documentation

5. **Validation Report** (1 week)
   - BODH issues benchmarking report with:
     - Performance scores across evaluation criteria
     - Identified strengths and limitations
     - Recommendations for improvement
     - Validation certificate (if passed)

**Total Timeline:** 7–10 weeks from submission to validation report

**WISE-CDSS Target:** Submit end of Sprint 4 (mid-March 2026), receive report by May 2026

---

## Part 5: Gap Analysis & Action Plan

### 5.1 Critical Gaps for BODH Readiness

| **Gap ID** | **Description** | **Impact** | **Remediation** | **Task** | **Sprint** |
|-----------|----------------|-----------|----------------|---------|-----------|
| **G1** | No multi-care-setting validation data | High | Extend clinical validation (T51) to include primary care and tertiary hospital scenarios | T51 extension | Sprint 3 |
| **G2** | Clinical terminology standards (LOINC, SNOMED, ICD-10) not documented | Medium | Document standards usage in knowledge base (T24) and agent outputs (T43–T45) | T99 checklist | Sprint 3 |
| **G3** | ABDM integration assessment incomplete | High | Complete T59 with concrete compliance evidence and integration roadmap | T59 | Sprint 3 |
| **G4** | BODH submission requirements unknown | High | Contact IIT Kanpur/NHA, obtain official guidelines | T98 | Sprint 2 |
| **G5** | No contact established with BODH team | Medium | Reach out via ABDM developer portal, NHA channels, or MoHFW coordination | T98 | Sprint 2 |

### 5.2 Action Plan by Sprint

#### Sprint 2 Actions (Week 2–3)

1. **T98: BODH Benchmarking & Evaluation Plan** (Owner: wiseaihub, Duration: 2 days)
   - **Action 1.1:** Contact IIT Kanpur BODH team via:
     - ABDM developer portal (https://sandbox.abdm.gov.in)
     - NHA partnership channels
     - LinkedIn outreach to IIT Kanpur faculty (CS/AI/Healthcare)
   - **Action 1.2:** Request submission guidelines, technical requirements, dataset specs
   - **Action 1.3:** Document BODH evaluation criteria and timeline
   - **Deliverable:** BODH alignment note with evaluation strategy

2. **T91: WISE-CDSS Governance & Accountability Model** (Owner: wiseaihub, Duration: 2 days)
   - Document risk classification, accountable parties, liability narrative
   - Aligns with BODH governance evaluation

3. **T93: Role-based AI Competency and Training Plan** (Owner: wiseaihub, Duration: 2 days)
   - Create competency matrix for clinician/admin/IT roles
   - Supports BODH change management and workforce capacity criteria

#### Sprint 3 Actions (Week 4–6)

4. **Complete All Testing Tasks**
   - T50: Unit testing (agents & tool-calling)
   - T51: Clinical validation (10 scenarios) — **Extend to 2 care settings**
   - T52: Bias & fairness testing (demographic subgroups)
   - T55: Performance benchmarking (latency, accuracy)
   - T56: RAG evaluation (precision, recall)
   - T57: Hallucination & safety testing
   - T61: Accessibility & vernacular language testing

5. **T59: ABDM Integration Assessment** (Owner: wiseaihub, Duration: 3 days)
   - Complete compliance gap analysis
   - Document ABDM-aligned interoperability evidence
   - Produce integration roadmap

6. **T99: BODH Data & Evidence Readiness Checklist** (Owner: wiseaihub, Duration: 2 days)
   - Map all evidence documents to BODH criteria
   - Identify missing documentation
   - Track completion status (Y/N/In Progress)
   - **Deliverable:** Comprehensive readiness checklist

#### Sprint 4 Actions (Week 7–8)

7. **T100: BODH Submission Package Preparation** (Owner: wiseaihub + riteshverma, Duration: 3 days)
   - Compile all documentation per submission package structure (Section 4.2)
   - Package Docker image (T79) for model deployment
   - Write executive summary and cover letter
   - **Deliverable:** Complete BODH submission package

8. **Submit to BODH Platform**
   - Upload submission package via official channels
   - Provide model access (API endpoint or containerised deployment)
   - Await benchmarking evaluation

---

## Part 6: Benefits & Expected Outcomes

### 6.1 Benefits of BODH Validation for WISE-CDSS

| **Benefit** | **Description** | **Stakeholder Impact** |
|------------|----------------|----------------------|
| **Regulatory Credibility** | Independent validation by IIT Kanpur/NHA strengthens CDSCO SaMD submission | Regulators, hospital procurement committees |
| **Trust Building** | Third-party benchmarking increases clinician and patient confidence in AI recommendations | End-users (doctors, patients) |
| **Performance Assurance** | Rigorous testing across diverse Indian datasets ensures real-world robustness | Healthcare institutions |
| **Bias Detection** | BODH identifies hidden demographic disparities that internal testing may miss | Equity-focused stakeholders, public health authorities |
| **Market Differentiation** | "BODH-validated" becomes a quality seal in India's health AI marketplace | Investors, partners, customers |
| **Continuous Improvement** | Benchmarking feedback informs model refinement and future versions | Development team |
| **Ecosystem Integration** | Aligns WISE-CDSS with ABDM, enabling seamless integration with national digital health infrastructure | National Health Authority, state health departments |
| **Global Leadership** | Positions WISE-CDSS as case study in responsible AI for healthcare in emerging markets | Research community (arXiv paper, T83) |

### 6.2 Expected BODH Validation Outcomes

Based on current WISE-CDSS design and planned testing:

| **BODH Criterion** | **Expected Outcome** | **Confidence Level** | **Rationale** |
|--------------------|---------------------|---------------------|---------------|
| Performance Metrics | **Strong Pass** (>80% accuracy targets) | High | Robust testing plan (T55–T57), LLM selection process (T33), agent design (T21–T23) |
| Robustness & Generalizability | **Pass** (some limitations acknowledged) | Medium | Multilingual support (T41), bias testing (T52), but limited care setting diversity |
| Bias & Fairness | **Strong Pass** (no significant disparities) | High | Comprehensive fairness framework (T10), demographic testing (T52), accessibility (T61) |
| Safety & Clinical Risk | **Pass** (appropriate risk class, good HITL design) | High | SaMD risk assessment (T54), clinical validation (T51), HITL workflow (T29, T49) |
| Interoperability | **Pass with Recommendations** | Medium | FHIR/ABDM assessment complete (T14, T59), but implementation depth may be limited in MVP |
| Data Governance | **Strong Pass** (excellent privacy/security posture) | High | DPDP compliance (T11, T76), anonymisation (T27), audit trail (T30), security testing (T53) |

**Overall Expected BODH Rating:** **85–90% (Strong Pass with Minor Recommendations)**

### 6.3 Post-BODH Roadmap

After receiving BODH validation report (estimated May 2026):

1. **Address Recommendations** (Sprint 5, if applicable)
   - Implement any improvement suggestions from BODH feedback
   - Re-test and resubmit if major gaps identified

2. **Leverage Validation for Market Entry**
   - Include "BODH-validated" badge in marketing materials
   - Cite validation report in hospital pitches and procurement bids
   - Reference in CDSCO SaMD technical file (T77)

3. **Publish Case Study**
   - Add BODH validation results to arXiv paper (T83)
   - Write blog post/white paper on lessons learned from BODH process
   - Share at health AI conferences and ABDM developer forums

4. **Continuous Re-Validation**
   - Plan annual BODH re-validation as model evolves
   - Integrate BODH benchmarking into post-market surveillance (T74, T80)

---

## Part 7: Risk Assessment & Mitigation

### 7.1 BODH Submission Risks

| **Risk ID** | **Risk Description** | **Probability** | **Impact** | **Mitigation Strategy** |
|------------|---------------------|----------------|-----------|------------------------|
| **R1** | BODH platform not yet fully operational for submissions (new initiative) | Medium | High | Early engagement (T98) to understand timeline; prepare submission package regardless for internal use |
| **R2** | Submission requirements more stringent than anticipated | Medium | Medium | Over-prepare documentation; conduct internal pre-review against SAHI 32 recommendations |
| **R3** | Performance below BODH benchmarks on unfamiliar datasets | Low-Medium | High | Conduct internal stress testing (T50–T57); acknowledge limitations transparently in submission |
| **R4** | ABDM integration gaps identified during validation | Medium | Medium | Complete T59 thoroughly; document integration roadmap even if full implementation deferred to v2.0 |
| **R5** | Bias detected in subpopulations not tested internally | Low | High | Expand demographic testing (T52) beyond 4 groups; test on edge cases |
| **R6** | Validation timeline extends beyond project scope (7–10 weeks) | High | Low | Submit by Sprint 4 regardless; validation can continue post-MVP as continuous improvement |
| **R7** | No response from BODH team to outreach | Medium | Medium | Use multiple channels (ABDM portal, NHA, LinkedIn, MoHFW); proceed with submission package preparation even without direct contact |

### 7.2 Contingency Plans

**If BODH submission not feasible by Sprint 4:**
- Position submission package as **internal validation evidence** for CDSCO SaMD technical file (T77)
- Use package for **hospital pilot discussions** and procurement conversations
- **Publish arXiv paper** (T83) highlighting "BODH-ready" system design aligned with national framework
- **Resubmit in post-MVP phase** once BODH platform fully operational

**If BODH validation reveals major gaps:**
- Treat as **MVP v1.0 baseline** and plan v2.0 improvements
- **Transparently acknowledge** limitations in model card (T73) and post-market plan (T74)
- Use feedback to prioritize Sprint 5+ backlog items

---

## Part 8: Success Metrics & KPIs

### 8.1 BODH Readiness KPIs

| **KPI** | **Baseline (Sprint 1)** | **Target (Sprint 4)** | **Measurement** |
|---------|------------------------|---------------------|----------------|
| Overall BODH Readiness Score | 62% | 90%+ | Weighted average across 6 criteria (Section 3.1) |
| Documentation Completeness | 50% | 95% | % of submission package sections complete |
| Testing Coverage | 40% | 100% | % of planned testing tasks (T50–T57, T60–T61) executed |
| Evidence Package Artifacts | 15 | 35+ | Number of completed evidence documents |
| BODH Team Engagement | 0 contacts | 3+ touchpoints | Outreach, meetings, guideline requests |
| ABDM Compliance Score | 40% | 80% | Completion of T59 assessment |

### 8.2 Post-Submission Success Metrics

| **Metric** | **Target** | **Timeline** | **Source** |
|-----------|-----------|--------------|-----------|
| BODH Validation Report Received | Yes | May 2026 | BODH platform |
| Overall BODH Score | 85%+ | May 2026 | Validation report |
| Criteria with "Strong Pass" Rating | 4+ of 6 | May 2026 | Validation report |
| Critical Issues Identified | 0 | May 2026 | Validation report |
| Recommendations for Improvement | <5 | May 2026 | Validation report |
| Re-submission Required | No | May 2026 | Validation report |

---

## Part 9: Conclusion & Recommendations

### 9.1 Summary

BODH represents a **transformative validation mechanism** for healthcare AI in India, aligning with SAHI's governance framework to ensure responsible, evidence-based deployment at population scale.

**WISE AI-CDSS is well-positioned for BODH validation** with:
- ✅ Strong governance foundations (SAHI compliance, DPDP framework)
- ✅ Comprehensive testing strategy (bias, fairness, safety, performance)
- ✅ Transparent explainability and human oversight mechanisms
- ⚠️ Some gaps in interoperability evidence and multi-setting validation

**With focused effort in Sprints 2–4, WISE-CDSS can achieve 90%+ BODH readiness and submit for validation by end of Sprint 4.**

### 9.2 Key Recommendations

1. **Prioritize BODH Engagement (Sprint 2)**
   - Contact IIT Kanpur/NHA immediately to understand submission requirements
   - Do not wait for complete system implementation; engage early

2. **Enhance Multi-Setting Validation (Sprint 3)**
   - Extend clinical testing (T51) to cover primary care and tertiary hospital scenarios
   - Document diversity in care settings explicitly in T99 checklist

3. **Complete ABDM Integration Assessment (Sprint 3)**
   - T59 is critical for interoperability score; allocate sufficient time
   - Document concrete compliance evidence, not just gap analysis

4. **Treat BODH Submission as Milestone, Not Blocker**
   - Prepare submission package by Sprint 4 regardless of BODH platform readiness
   - Package serves multiple purposes: CDSCO SaMD filing, hospital pitches, investor credibility

5. **Leverage BODH for Continuous Improvement**
   - View validation as beginning of feedback loop, not one-time assessment
   - Plan annual re-validation as model evolves

---

## Appendices

### Appendix A: BODH Key Contacts (To Be Updated)

| **Organization** | **Contact** | **Purpose** |
|-----------------|-----------|-----------|
| IIT Kanpur (BODH Development Lead) | TBD | Submission guidelines, technical requirements |
| National Health Authority (NHA) | TBD | ABDM integration, BODH coordination |
| Ministry of Health and Family Welfare (MoHFW) | TBD | SAHI/BODH policy guidance |
| ABDM Developer Portal | https://sandbox.abdm.gov.in | Interoperability specs, sandbox testing |

### Appendix B: BODH-Related Resources

1. **BODH Launch Announcement**  
   PIB Press Release (Feb 2026): https://www.pib.gov.in/PressReleseDetail.aspx?PRID=2229226

2. **SAHI Strategy Document**  
   Ministry of Health and Family Welfare (2026)

3. **ABDM Framework**  
   National Health Authority: https://abdm.gov.in

4. **Digital Personal Data Protection Act 2023**  
   Ministry of Electronics and IT

5. **AI Model Validation Best Practices**  
   - PMID: 35158399 (Validation strategies: LOOCV, k-fold, hold-out)
   - PMID: 39219648 (Clinical chatbot validation frameworks)

### Appendix C: Glossary

| **Term** | **Definition** |
|---------|---------------|
| **ABDM** | Ayushman Bharat Digital Mission – India's national digital health infrastructure |
| **BODH** | Benchmarking Open Data Platform for Health AI – National validation platform by IIT Kanpur/NHA |
| **DPDP Act** | Digital Personal Data Protection Act 2023 – India's data privacy legislation |
| **FHIR** | Fast Healthcare Interoperability Resources – HL7 standard for health data exchange |
| **LOOCV** | Leave-One-Out Cross-Validation – Model validation technique |
| **NHA** | National Health Authority – Implements ABDM |
| **SAHI** | Strategy for Artificial Intelligence in Healthcare for India – National governance framework |
| **SaMD** | Software as a Medical Device – Regulatory classification under CDSCO Medical Device Rules 2017 |

---

**Document Status:** ✅ Ready for Review  
**Next Actions:**
1. Contact IIT Kanpur/NHA for BODH guidelines (Week 2)
2. Complete BODH readiness checklist (T99, Sprint 3)
3. Prepare submission package (T100, Sprint 4)

**Change Log:**
- v1.0 (20 Feb 2026): Initial BODH alignment document created (Sreedhar Byreeka)
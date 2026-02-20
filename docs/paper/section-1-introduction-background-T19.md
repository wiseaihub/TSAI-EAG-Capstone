# Section 1: Introduction & Background (T19)

**Paper:** WISE AI CDSS – A SAHI-Aligned Clinical Decision Support System for Indian Primary Care  
**Authors:** Sreedhar (wiseaihub), Ritesh Verma (riteshverma)  
**Target:** arXiv preprint · TSAI EAG Capstone 2026  
**Status:** Sprint 1 Draft · Week 1

---

## 1.1 Problem Statement

India faces a severe primary care diagnostic gap. With a physician-to-population ratio of approximately 1:1,457 — well below the WHO recommended 1:1,000 — General Practitioners (GPs) manage high patient volumes with limited decision support, limited access to specialist consultation, and time-constrained clinical encounters. Misdiagnosis, delayed referral, and over-reliance on symptomatic treatment are systemic outcomes of this resource constraint, particularly in Tier 2 and Tier 3 cities and rural settings.

Clinical Decision Support Systems (CDSS) have demonstrated effectiveness in high-resource healthcare environments (US, UK, EU) in reducing diagnostic error and improving guideline adherence. However, existing CDSS solutions are not designed for the Indian GP context: they assume EHR integration (rare in Indian primary care), English-language interfaces, Western clinical guideline corpora, and high-bandwidth infrastructure — none of which can be assumed in the target deployment environment.

---

## 1.2 Indian Healthcare Context

| Dimension | Indian Reality | Implication for CDSS |
|-----------|---------------|----------------------|
| Physician density | ~1.4 per 1,000 population | High caseload; AI must reduce cognitive burden |
| Primary care infrastructure | Mostly unstructured, paper-based | CDSS must operate without EHR dependency |
| Regulatory landscape | CDSCO SaMD, DPDP Act 2023, ABDM | Compliance-first design required |
| Language diversity | 22 scheduled languages | Multilingual interface consideration |
| Data availability | Limited labelled clinical datasets | RAG + curated knowledge base approach |
| Digital health maturity | ABDM/NDHM in early rollout | FHIR-readiness required for future integration |

---

## 1.3 Gap in Existing Literature

Existing CDSS research and products (Isabel DDx, UpToDate, DXplain) share four limitations that disqualify direct adoption in the Indian GP context:

1. **EHR dependency** – Assume structured EMR data as input; Indian primary care is predominantly paper-based.
2. **Western guideline corpora** – Clinical evidence bases (UpToDate, NICE, CMS) do not reflect Indian disease prevalence, drug formularies, or clinical pathways.
3. **No AI ethics framework for LMICs** – Existing systems lack explicit fairness, explainability, and accountability mechanisms calibrated for Low and Middle Income Country (LMIC) populations.
4. **No India regulatory alignment** – None address CDSCO SaMD classification, DPDP Act 2023 consent obligations, or ABDM interoperability requirements.

The WISE AI CDSS is designed to close each of these gaps explicitly.

---

## 1.4 The SAHI Framework as Ethical Backbone

The WISE AI CDSS is built in full alignment with the **SAHI (Safe AI for Healthcare in India) Framework** published February 2026. SAHI provides:

| SAHI Component | Application to WISE AI CDSS |
|----------------|----------------------------|
| Sutra 1 – Trustworthy AI | Governance structure, responsible AI principles (T15) |
| Sutra 2 – Reliability | RAG pipeline design, FHIR standards alignment (T08, T14) |
| Sutra 3 – Explainability | LangGraph agent reasoning traces, audit logs |
| Sutra 4 – Fairness | Bias & fairness assessment framework (T10) |
| Sutra 5 – Privacy & Security | DPDP consent framework, threat modelling (T11, T18) |
| Sutra 6 – Accountability | Governance & accountability model (T91) |
| Sutra 7 – Continuous Improvement | Sprint review cadence, BODH evaluation pipeline (T20) |
| 8-Step Lifecycle | End-to-end project task mapping (T02) |

SAHI is not treated as a compliance overlay but as the primary design driver — every architectural and product decision is evaluated against the 7 Sutras before implementation.

---

## 1.5 Project Overview & Contribution

**WISE AI CDSS** (Workflow-Integrated Smart Evidence – Clinical Decision Support System) is a multi-agent AI system designed to assist Indian GPs in clinical triage, differential diagnosis, and evidence-based treatment recommendation for high-prevalence conditions in the Indian primary care setting.

Key contributions of this work:

- First CDSS architecture explicitly designed for the Indian GP workflow and regulatory environment
- SAHI-aligned multi-agent architecture using LangGraph/CrewAI with explainable reasoning chains
- RAG pipeline grounded in curated Indian medical guidelines (ICMR, IAP, API) and CBC triage logic
- Full DPDP Act 2023 and CDSCO SaMD compliance framework
- BODH platform evaluation plan for independent AI benchmarking

This paper documents the design rationale, architecture decisions, compliance mapping, and evaluation approach for the WISE AI CDSS capstone project.

---

## References (Section 1)

- SAHI Framework – Safe AI for Healthcare in India, February 2026
- CDSCO – Medical Devices Rules 2017, SaMD Guidance
- DPDP Act – Digital Personal Data Protection Act, India, 2023
- ABDM – Ayushman Bharat Digital Mission, NHA India
- WHO – Global Health Workforce Statistics, 2023
- BODH – Benchmark for Observational and Diagnostic Health AI, February 2026

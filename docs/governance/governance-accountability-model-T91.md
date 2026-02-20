# WISE-CDSS Governance & Accountability Model (T91)

**Document ID:** T91  
**Owner:** Sreedhar Byreeka (wiseaihub)  
**Project:** WISE AI-CDSS – SAHI-Compliant Capstone  
**Related Issues:** T02, T16, T31, T37, T54, T72, T77  

---

## 1. Purpose & Scope

This document defines the **governance and accountability model** for WISE-CDSS as an AI-enabled Clinical Decision Support System (CDSS) intended for use in the Indian healthcare context.  
It aligns with **SAHI recommendations 1–3** on risk-based classification, accountability of actors, and safety-by-design across the AI lifecycle.[file:4]

Scope includes:

- Governance of WISE-CDSS as **Software as a Medical Device (SaMD)**.  
- Roles and responsibilities of key actors (developer, deployer, clinician, patient, regulator).  
- Allocation of accountability and liability for harms or failures.  
- Links to risk management, monitoring, and post-market processes defined elsewhere in the project (T31, T37, T54, T74, T80).[file:1]

---

## 2. Risk Classification & Regulatory Context

WISE-CDSS is treated as an **AI-enabled SaMD** under the CDSCO Medical Device Rules 2017.  
The exact risk class (e.g., Class B/C) is determined in T31/T54 based on:

- Intended use: *clinical decision support* (triage, medication safety, chronic disease management), not autonomous diagnosis.  
- Risk of harm: tool provides **recommendations**, final decisions remain with clinicians.  
- Integration context: deployed within regulated healthcare facilities (hospitals/clinics).

Regulatory alignment:

- **CDSCO SaMD Framework** – mapped in T31 and documented in the SaMD risk assessment (T54).[file:1]  
- **MoHFW / SAHI Framework** – WISE-CDSS adopts SAHI’s 8-step lifecycle and 7 Sutras as its governance spine.[file:4]  
- **DPDP Act 2023** – data protection and privacy governance handled via T11, T27, T53, T76.[file:1]

---

## 3. Governance Structure

WISE-CDSS governance is organised along three layers:

1. **Product Governance (Vendor / Development Team)**  
   - Owns architecture, model development, testing, documentation, and updates.  
   - Ensures SAHI-aligned lifecycle evidence is maintained (T02, T35, T58, T65, T72, T86).[file:1]

2. **Operational Governance (Deploying Institution – Hospital / Health System)**  
   - Owns deployment decisions, configuration, user access, and local policies.  
   - Establishes an internal AI governance unit / nodal cell (to be detailed in T92).

3. **Clinical Governance (Clinicians & Clinical Leadership)**  
   - Own safe and appropriate clinical use of WISE-CDSS.  
   - Ensure adherence to clinical protocols and override AI where necessary.

These layers are underpinned by:

- **RACI matrix** defined in T16 (Project Kick-off & Governance Setup).[file:1]  
- **Audit trail and logging** (T30, T62).  
- **Post-market surveillance and monitoring** (T74, T80, T86).

---

## 4. Roles & Responsibilities

### 4.1 Key Actors

| Actor | Role | Key Responsibilities |
|------|------|----------------------|
| **Developer / Vendor (WISE-CDSS team)** | Builds and maintains the AI CDSS | Design & implement models and agents; ensure adherence to SAHI lifecycle; perform testing (technical, safety, fairness); maintain documentation (model card, SaMD file); respond to field issues; manage releases. |
| **Deploying Institution (Hospital / Health System)** | Deploys and operates WISE-CDSS in real care settings | Decide where/how WISE-CDSS is used; ensure infrastructure, access controls, and integration; approve policies; ensure staff are trained; run local monitoring and incident management. |
| **Clinician User (Doctor, Nurse Practitioner)** | Uses recommendations in patient care | Provide accurate inputs; interpret outputs; apply clinical judgement; override AI when necessary; report issues or unexpected behaviours. |
| **Patient / Caregiver** | Receives care influenced by WISE-CDSS | Provide consent to data use; understand that WISE-CDSS supports clinicians, not replaces them; raise concerns if they perceive issues. |
| **Regulators (CDSCO, MoHFW / NHA)** | Provide external oversight | Approve SaMD where required; issue guidance; audit compliance; oversee BODH participation. |

### 4.2 RACI Overview (Summary)

This is a high-level view; detailed RACI remains in the T16 artefact.[file:1]

| Activity | Developer | Institution | Clinician | Regulator |
|----------|-----------|------------|-----------|-----------|
| Model design & training | R | C | I | I |
| Clinical workflow design | C | C | R | I |
| Deployment decision | C | R | C | I |
| Day-to-day system use | I | C | R | I |
| Monitoring & incident reporting | R | R | C | I |
| Regulatory submissions (SaMD, BODH) | R | C | I | A/R |

- R = Responsible, A = Accountable, C = Consulted, I = Informed.

---

## 5. Accountability & Liability Model

### 5.1 Principles

- **Shared accountability:** No single actor bears all risk; accountability is distributed across design, deployment, and use.  
- **Proximate cause:** Liability is linked to the party whose action/inaction most directly caused or failed to prevent harm.  
- **SAHI-aligned safety-by-design:** Governance must show that reasonable steps were taken across the lifecycle to prevent foreseeable harms.[file:4]

### 5.2 Developer / Vendor Accountability

The WISE-CDSS team is accountable for:

- Systemic errors in design or implementation (e.g., known unsafe logic not fixed).  
- Failure to address documented model weaknesses when aware of them.  
- Inadequate testing relative to stated claims (e.g., no fairness testing where risk is high).  
- Misleading documentation about intended use or limitations.

To mitigate:

- Maintain thorough lifecycle documentation (T35, T58, T65, T72).[file:1]  
- Maintain model card & Responsible AI statement (T73).[file:1]  
- Actively respond to incident reports from institutions.

### 5.3 Deploying Institution Accountability

The institution is accountable for:

- Using WISE-CDSS in clinical contexts where it is **not** suitable (e.g., outside intended indications).  
- Failure to provide adequate training (T93) and workflow integration (T94).[file:1]  
- Misconfiguration (e.g., integration errors, incomplete data leading to systematically wrong outputs).  
- Ignoring known system limitations documented by the vendor.

Mitigations:

- Internal AI governance / nodal cell to oversee deployments (to be detailed in T92).  
- Local policies specifying where WISE-CDSS is allowed / disallowed.  
- Internal incident management and escalation process.

### 5.4 Clinician Accountability

Clinicians remain the final decision-makers.

They are accountable for:

- Using WISE-CDSS within their scope of practice.  
- Applying clinical judgement and not blindly following recommendations.  
- Reviewing warnings, contraindications, and explanations.  
- Reporting unexpected or unsafe system behaviour.

They are **not** accountable for:

- Hidden model-level defects unknown to them.  
- Infrastructure or integration failures under institutional control.

### 5.5 Regulator & Ecosystem Accountability

Regulators and ecosystem platforms (e.g., BODH) are accountable for:

- Providing clear, up-to-date guidelines and evaluation frameworks.  
- Running fair and robust benchmarking where applicable.  
- Communicating expectations to developers and institutions.

WISE-CDSS’s role is to:

- Participate in such frameworks (e.g., BODH – T98–T100).  
- Align SaMD documentation with regulatory expectations (T77).[file:1]

---

## 6. Governance Mechanisms & Controls

WISE-CDSS governance relies on the following concrete mechanisms:

- **Risk assessment & classification:** T31, T54, T65 produce a SaMD risk assessment and SAHI Step 5–6 evidence packs.[file:1]  
- **Audit trail & logging:** T30, T62 define and implement logging of agent actions, data provenance, and overrides.  
- **Safety & performance testing:** T32, T50–T57, T68, T87 define and run validation suites.[file:1]  
- **Fairness & accessibility:** T10, T52, T61, T75 handle fairness frameworks, bias testing, and accessibility compliance.[file:1]  
- **Post-market surveillance:** T74, T80 define KPIs, monitoring dashboards, and drift detection.  
- **Governance audits:** T72, T86 aggregate lifecycle evidence and run full SAHI compliance audits.[file:1]

These controls must be kept up to date as the system evolves.

---

## 7. Review & Maintenance

- **Owner:** Sreedhar Byreeka (wiseaihub).  
- **Initial Version:** v1.0 – February 2026.  
- **Review Frequency:** At least once per major release or annually, whichever is earlier.  
- **Change Log:**  

  - v1.0 – Initial governance and accountability model drafted for SAHI compliance (T91 DoD).

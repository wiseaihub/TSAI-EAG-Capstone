# Change Management & Workflow Integration Guidelines (T94)

**Document ID:** T94  
**Owner:** Sreedhar Byreeka (wiseaihub)  
**Project:** WISE AI-CDSS – SAHI-Compliant Capstone  
**Related Issues:** T02, T04, T13, T16, T29, T49, T60, T69, T72  

---

## 1. Purpose

These guidelines describe how to **embed WISE-CDSS into clinical workflows** in a way that supports clinicians without increasing burden or fragmenting care.  
They address **SAHI Recommendations 21–22** on change management, workflow integration, and clarity of human vs AI roles.[file:4]

---

## 2. Guiding Principles

1. **Clinician-in-the-loop:** WISE-CDSS assists; it never replaces clinical judgement.  
2. **Minimum friction:** Integrations should reduce, not increase, workflow burden.  
3. **Clarity of responsibility:** It must always be clear who is responsible for each decision.  
4. **Safety first:** In doubt or system degradation, default to standard manual workflows.  
5. **Transparency:** Users must understand what WISE-CDSS is doing, with clear explanations and limitations.

These principles are reflected in HITL design (T29, T49) and post-market surveillance (T74).[file:1]

---

## 3. Workflow Integration Scenarios

WISE-CDSS initially targets three core use-case clusters (T04, T13):[file:1]

- **Diagnosis / Triage Support**  
- **Medication Safety**  
- **Chronic Disease Management**

### 3.1 Diagnosis / Triage Support

**Where it fits:**

- After initial patient intake and history taking.  
- Before final diagnosis and ordering investigations.

**Typical flow:**

1. Clinician or trained staff enters key symptoms, vitals, and history into WISE-CDSS.  
2. System proposes differential diagnoses and recommended next steps (e.g., investigations, referrals).  
3. Clinician reviews recommendations and explanations.  
4. Clinician accepts, modifies, or rejects recommendations and documents rationale.

**Key change management points:**

- Ensure no step removes the clinician’s ability to **override or ignore** recommendations.  
- Use WISE-CDSS triage suggestions to **support existing triage protocols**, not replace them.  
- During early deployment, restrict to **advisory** mode and avoid hard gating access to care.

### 3.2 Medication Safety

**Where it fits:**

- At the point of prescribing or reconciling medications.

**Flow:**

1. Clinician enters or confirms medication orders.  
2. WISE-CDSS checks for drug–drug, drug–disease, and drug–allergy interactions.  
3. Alerts and explanations are displayed; clinician can adjust orders.  
4. Critical alerts require explicit acknowledgement in the UI.

**Key points:**

- Avoid over-alerting; configure sensible severity thresholds.  
- Always present **clear explanations** for alerts so clinicians can quickly assess relevance.  
- Log overrides with reasons (T49, T62) for future safety review.[file:1]

### 3.3 Chronic Disease Management

**Where it fits:**

- In outpatient follow-up for conditions like diabetes and hypertension.

**Flow:**

1. Clinician or nurse enters updated vitals, lab values, and complaints.  
2. WISE-CDSS suggests plan adjustments (e.g., lifestyle advice, medication titration suggestions) based on guidelines.  
3. Clinician reviews, tailors, and communicates plan to patient.  
4. Education materials may be generated for patients.

**Key points:**

- Recommendations must be aligned with accepted guidelines and MoHFW guidance (T38).[file:1]  
- Patients should be made aware that the tool supports, rather than replaces, clinician judgement.

---

## 4. Roles & Responsibilities in Change Management

### 4.1 Clinical Leadership

- Approve the **scope of use** for WISE-CDSS (which departments, which scenarios).  
- Own decision to move from pilot to scale.  
- Champion safe usage culture and encourage feedback and reporting.

### 4.2 Project / Product Team

- Provide clear documentation and training materials (T02, T91, T93).  
- Configure WISE-CDSS to align with local workflows.  
- Support monitoring, incident triage, and updates.

### 4.3 Frontline Clinicians

- Participate in UAT and pilot testing (T60, T69).  
- Provide feedback on usability, alerting, and workflow fit (T64).  
- Use override and escalation paths appropriately.

### 4.4 IT / Operations

- Ensure integration with existing HIS/EMR systems where applicable.  
- Monitor performance and uptime.  
- Coordinate with vendors for upgrades and fixes.

---

## 5. Adoption & Rollout Strategy

### 5.1 Phased Rollout

1. **Sandbox / Demo Stage**  
   - Use synthetic or anonymised data.  
   - Focus on familiarisation and feedback.

2. **Pilot in a Single Unit**  
   - Limited number of clinicians and patients.  
   - Close monitoring of usage and incidents.

3. **Controlled Expansion**  
   - Gradually add more units once KPIs are stable.  
   - Adjust based on incident reports and feedback.

4. **Scale-Up**  
   - Integrate into standard operating procedures.  
   - Use metrics from T74/T80 to monitor long-term performance.

### 5.2 Communication Plan

- Align with stakeholder communication plan and RACI (T16).[file:1]  
- Key messages:
  - Why WISE-CDSS is being introduced.  
  - What it will and will not do.  
  - How to get help or report an issue.

---

## 6. Oversight, Escalation & Feedback

### 6.1 Escalation Pathways

- **Clinical escalation:** from frontline clinicians → senior consultant → institutional AI governance cell.  
- **Technical escalation:** from users → IT helpdesk → vendor support.  
- **Safety escalation:** from incident log → risk committee → regulator if required.

### 6.2 Feedback Loop

- T64 defines a feedback loop where clinician ratings and comments are captured and aggregated.[file:1]  
- Feedback should be regularly reviewed by:
  - Product team (for UX/model changes).  
  - Clinical leadership (for practice changes).  
  - Governance unit (for policy updates).

---

## 7. When NOT to Use WISE-CDSS

Change management must explicitly state **contraindications**, for example:

- Situations where **time-critical decisions** cannot tolerate any delay (e.g., immediate resuscitation).  
- Clinical scenarios **outside the validated scope** documented in T04/T51.[file:1]  
- When system status indicates degraded performance (e.g., partial outage, known bug impacting results).  
- Where local policy or regulator guidance explicitly prohibits use.

In such cases, staff must revert to standard manual processes.

---

## 8. Maintenance

- These guidelines should be updated when:
  - New use cases are added.  
  - Post-market surveillance (T74) reveals workflow-related risks.  
  - Feedback (T64) identifies persistent friction points.

**T94 Definition of Done:**  
This document is published at `docs/governance/change-management-guidelines-T94.md` and referenced by HITL dashboard (T49), UAT plan (T60), and SAHI lifecycle audit (T72).

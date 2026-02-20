# CBC Triage Use Cases – Indian GP Context

## 1. Target Setting
- Indian General Practice / Primary Health Centre (PHC) / urban clinic
- Resource-constrained; GP sees 50–100 patients/day
- CBC (Complete Blood Count) is most common ordered test

## 2. Use Cases

### UC-01: Anaemia Detection & Severity Classification
- Trigger: Hb < 12 (F) / < 13 (M) g/dL
- WISE-CDSS output: Severity (mild/moderate/severe), likely type (iron-deficiency, B12, haemolytic), next steps
- Clinical action: Dietary advice, supplementation, or referral

### UC-02: Infection / Sepsis Flag
- Trigger: WBC > 11,000 or < 4,000; neutrophilia / lymphocytosis patterns
- WISE-CDSS output: Likely bacterial vs viral, urgency flag, antibiotic guidance
- Clinical action: Empirical treatment or culture-and-wait

### UC-03: Thrombocytopenia Alert (Dengue / ITP / Drug-induced)
- Trigger: Platelets < 1,50,000
- WISE-CDSS output: Pattern match (dengue fever profile, drug list, ITP likelihood), urgency
- Clinical action: Admit / monitor / review medications

### UC-04: Polycythaemia / Leukaemia Suspicion Flag
- Trigger: RBC/WBC out of range + morphology flags
- WISE-CDSS output: Haematology referral recommendation
- Clinical action: Refer to secondary/tertiary care

### UC-05: Routine Follow-up for Chronic Conditions (DM, Hypertension)
- Trigger: Periodic CBC in DM/HTN follow-up
- WISE-CDSS output: Trend analysis vs last result, flag deviations
- Clinical action: Adjust management plan

## 3. Out of Scope (v1)
- Bone marrow biopsy decisions
- Paediatric haematology (deferred to v2)
- Oncology treatment planning

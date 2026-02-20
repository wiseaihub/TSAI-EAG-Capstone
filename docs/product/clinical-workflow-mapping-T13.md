# Clinical Workflow Mapping – 3 Use Cases (T13)

## UC-01: Triage / Diagnosis (CBC)
Patient → Nurse intake → GP consult → CBC ordered →
Lab result → WISE-CDSS recommendation → GP accepts/overrides →
Document → Prescribe/refer → Follow-up

## UC-02: Medication Safety
GP prescribes → WISE-CDSS checks interactions →
Alert shown (if any) → GP reviews → Adjusts/acknowledges →
Override logged

## UC-03: Chronic Disease Follow-up (DM/HTN)
Patient attends follow-up → Nurse enters vitals/labs →
WISE-CDSS compares vs last visit → Flags deviations →
GP reviews trend + suggestion → Adjusts plan →
Patient education material generated

## Clinician Touchpoints (all 3 use cases)
- Input: vitals, CBC, medication list, history
- Output: recommendations, alerts, education content
- Override: available at all times with mandatory reason logging

"""Write clinical notes for a patient. S18-compatible: execute(params, context) + DESCRIPTOR."""

DESCRIPTOR = {
    "name": "note_writer",
    "description": "Write or append a clinical note for the patient.",
    "parameters": {
        "type": "object",
        "properties": {
            "note_type": {"type": "string", "description": "Type of note (e.g. progress, discharge)."},
            "content": {"type": "string", "description": "Note text content."},
            "encounter_id": {"type": "string", "description": "Optional encounter id to attach note to."},
        },
        "required": ["note_type", "content"],
    },
}


def execute(params: dict, context: dict) -> dict:
    """Write a note. Uses context['patient_id'] for the patient."""
    patient_id = context.get("patient_id", "")
    note_type = params.get("note_type", "")
    content = params.get("content", "")
    encounter_id = params.get("encounter_id")

    # Stub: in production would call EHR notes API
    return {
        "success": True,
        "patient_id": patient_id,
        "note_type": note_type,
        "encounter_id": encounter_id,
        "message": f"Note ({note_type}) written for patient {patient_id} (stub).",
    }

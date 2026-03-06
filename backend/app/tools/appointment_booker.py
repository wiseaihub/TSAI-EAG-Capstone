"""Book appointments for a patient. S18-compatible: execute(params, context) + DESCRIPTOR."""

DESCRIPTOR = {
    "name": "appointment_booker",
    "description": "Book a clinical appointment for the patient (date, type, provider).",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {"type": "string", "description": "Appointment date (ISO or YYYY-MM-DD)."},
            "appointment_type": {"type": "string", "description": "Type of appointment (e.g. follow-up, checkup)."},
            "provider_id": {"type": "string", "description": "Optional provider identifier."},
        },
        "required": ["date", "appointment_type"],
    },
}


def execute(params: dict, context: dict) -> dict:
    """Book an appointment. Uses context['patient_id'] for the patient."""
    patient_id = context.get("patient_id", "")
    date = params.get("date", "")
    appointment_type = params.get("appointment_type", "")
    provider_id = params.get("provider_id")

    # Stub: in production would call scheduling/EHR API
    return {
        "success": True,
        "patient_id": patient_id,
        "appointment": {
            "date": date,
            "type": appointment_type,
            "provider_id": provider_id,
        },
        "message": f"Appointment booked for patient {patient_id} on {date} ({appointment_type}).",
    }

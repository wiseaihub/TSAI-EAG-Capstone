"""EHR client: read/write patient data. S18-compatible: execute(params, context) + DESCRIPTOR."""

DESCRIPTOR = {
    "name": "ehr_client",
    "description": "Read or write patient data from the EHR (vitals, labs, demographics).",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["read", "write"], "description": "Read or write."},
            "resource": {"type": "string", "description": "Resource type (e.g. vitals, labs, demographics)."},
            "data": {"type": "object", "description": "Payload for write; ignored for read."},
        },
        "required": ["action", "resource"],
    },
}


def execute(params: dict, context: dict) -> dict:
    """Execute EHR action. Uses context['patient_id'] for the patient."""
    patient_id = context.get("patient_id", "")
    action = params.get("action", "read")
    resource = params.get("resource", "")
    data = params.get("data") or {}

    # Stub: in production would call EHR API
    if action == "read":
        return {
            "success": True,
            "patient_id": patient_id,
            "resource": resource,
            "data": {},
            "message": f"Read {resource} for patient {patient_id} (stub).",
        }
    return {
        "success": True,
        "patient_id": patient_id,
        "resource": resource,
        "written": data,
        "message": f"Wrote {resource} for patient {patient_id} (stub).",
    }

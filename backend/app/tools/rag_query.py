"""RAG query over knowledge base. S18-compatible: execute(params, context) + DESCRIPTOR."""

DESCRIPTOR = {
    "name": "rag_query",
    "description": "Query the RAG knowledge base (guidelines, research) with optional patient context.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Natural language or keyword query."},
            "top_k": {"type": "integer", "description": "Max number of results (default 5).", "default": 5},
        },
        "required": ["query"],
    },
}


def execute(params: dict, context: dict) -> dict:
    """Run RAG query. May use context['patient_id'] to scope or rank results."""
    patient_id = context.get("patient_id", "")
    query = params.get("query", "")
    top_k = params.get("top_k", 5)

    # Stub: in production would call RAG/search service
    return {
        "success": True,
        "patient_id": patient_id,
        "query": query,
        "results": [],
        "message": f"RAG query for patient {patient_id} (stub).",
    }

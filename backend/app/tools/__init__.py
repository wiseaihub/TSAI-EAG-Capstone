"""WISE tools for S18-compatible adapter: execute + DESCRIPTOR per tool."""

from app.tools.appointment_booker import execute as appointment_booker, DESCRIPTOR as APPOINTMENT_BOOKER
from app.tools.ehr_client import execute as ehr_client, DESCRIPTOR as EHR_CLIENT
from app.tools.note_writer import execute as note_writer, DESCRIPTOR as NOTE_WRITER
from app.tools.rag_query import execute as rag_query, DESCRIPTOR as RAG_QUERY

WISE_TOOLS = [APPOINTMENT_BOOKER, EHR_CLIENT, NOTE_WRITER, RAG_QUERY]

__all__ = [
    "appointment_booker",
    "ehr_client",
    "note_writer",
    "rag_query",
    "APPOINTMENT_BOOKER",
    "EHR_CLIENT",
    "NOTE_WRITER",
    "RAG_QUERY",
    "WISE_TOOLS",
]

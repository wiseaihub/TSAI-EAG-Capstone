from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Float,
    ForeignKey,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True)
    external_id = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id = Column(String, primary_key=True)
    role = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class Encounter(Base):
    __tablename__ = "encounters"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.id"), index=True, nullable=False)
    encounter_type = Column(String)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime)
    metadata_ = Column("metadata", JSON)


class AgentSession(Base):
    __tablename__ = "agent_sessions"

    session_id = Column(String, primary_key=True)
    patient_id = Column(String, index=True, nullable=False)
    agent_name = Column(String)
    agent_version = Column(String)
    risk_level = Column(String)
    confidence = Column(Float)
    flags = Column(JSON)
    timestamp = Column(DateTime, nullable=False)


class Case(Base):
    __tablename__ = "cases"

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True, nullable=False)
    status = Column(String, nullable=False)
    title = Column(String, nullable=True)
    input_payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(String, primary_key=True)
    case_id = Column(String, ForeignKey("cases.id"), index=True, nullable=False)
    session_id = Column(String, index=True, nullable=True)
    s18_run_id = Column(String, unique=True, index=True, nullable=True)
    agent_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    error_text = Column(Text, nullable=True)
    metrics = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)


class AgentMessage(Base):
    __tablename__ = "agent_messages"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    case_id = Column(String, ForeignKey("cases.id"), index=True, nullable=False)
    run_id = Column(String, ForeignKey("agent_runs.id"), index=True, nullable=True)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    meta = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)


class RunArtifact(Base):
    __tablename__ = "run_artifacts"

    id = Column(String, primary_key=True)
    run_id = Column(String, ForeignKey("agent_runs.id"), index=True, nullable=False)
    artifact_type = Column(String, nullable=False)
    storage_path = Column(String, nullable=True)
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True, nullable=True)
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    event_payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)

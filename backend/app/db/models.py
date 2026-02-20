from sqlalchemy import Column, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True)
    external_id = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


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

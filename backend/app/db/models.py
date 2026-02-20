from sqlalchemy import Column, String, Float, JSON, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AgentSession(Base):
    __tablename__ = "agent_sessions"

    session_id = Column(String, primary_key=True)
    patient_id = Column(String, index=True)
    agent_name = Column(String)
    agent_version = Column(String)
    risk_level = Column(String)
    confidence = Column(Float)
    flags = Column(JSON)
    timestamp = Column(DateTime)

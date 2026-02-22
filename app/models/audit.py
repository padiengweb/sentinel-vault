# app/models/audit.py
import uuid
from sqlalchemy import Column, String, DateTime, func
from app.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    event_type = Column(String, index=True) # e.g., "JIT_ACCESS_GRANTED"
    actor_id = Column(String)               # e.g., "ENG-9981"
    target_resource = Column(String)        # e.g., "PROD-DB-CLUSTER-01"
    reason = Column(String)                 # e.g., "ECDSA signature verification failed."
    status = Column(String)                 # e.g., "SUCCESS" or "CRITICAL_ALERT"
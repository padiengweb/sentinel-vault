# app/core/audit.py
from datetime import datetime
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditLog

async def emit_audit_log(
    db: AsyncSession, 
    event_type: str, 
    actor_id: str, 
    target_resource: str, 
    reason: str, 
    status: str
):
    """Prints to terminal AND saves to the PostgreSQL database."""
    
    
    log_payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "actor_id": actor_id,
        "target_resource": target_resource,
        "status": status,
        "pipeline_destination": "https://nifi-internal.enterprise.com/api/webhook/audit"
    }
    print("\n" + "="*65)
    print("🚀 [NIFI WEBHOOK EMITTER] -> Streaming to Cribl/Snowflake...")
    print(json.dumps(log_payload, indent=2))
    print("="*65 + "\n")

    
    new_log = AuditLog(
        event_type=event_type,
        actor_id=actor_id,
        target_resource=target_resource,
        reason=reason,
        status=status
    )
    db.add(new_log)
    await db.commit()
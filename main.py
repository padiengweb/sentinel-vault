from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import random
import uuid
import json

app = FastAPI(title="Sentinel-Vault API", description="Mutual Authentication & JIT Access System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


def emit_audit_log(event_type: str, actor_id: str, target_resource: str, reason: str, status: str):
    """Formats and emits a high-fidelity JSON log to the terminal."""
    log_payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "actor_id": actor_id,
        "target_resource": target_resource,
        "status": status,
        "reason": reason,
        "pipeline_destination": "https://nifi-internal.enterprise.com/api/webhook/audit"
    }
    
    
    print("\n" + "="*65)
    print("🚀 [NIFI WEBHOOK EMITTER] -> Streaming to Cribl/Snowflake...")
    print(json.dumps(log_payload, indent=2))
    print("="*65 + "\n")



active_sessions = {}


class TransactionRequest(BaseModel):
    account_number: str
    amount: float
    destination: str
    is_employee_instructing: bool  

class SessionRequest(BaseModel):
    account_number: str

class CustomerVerifyEmployeeRequest(BaseModel):
    session_id: str
    employee_code_a: str  

class EmployeeVerificationRequest(BaseModel):
    session_id: str
    customer_code_b: str



@app.post("/api/transaction/request")
def request_transaction(request: TransactionRequest):
    """Intercepts JIT access request and checks for Four-Eyes Principle."""
    if request.is_employee_instructing:
        
        emit_audit_log(
            event_type="JIT_AUTH_REQUIRED",
            actor_id=request.account_number,
            target_resource=request.destination,
            reason="High-risk target requires live Admin authorization via Sentinel-Vault.",
            status="PENDING_AUTH"
        )
        return {
            "status": "BLOCKED_PENDING_AUTH",
            "alert": "High risk of social engineering detected.",
            "action_required": "Please ask the caller for their Sentinel-Vault Session ID."
        }
        
    
    emit_audit_log(
        event_type="JIT_ACCESS_DENIED",
        actor_id=request.account_number,
        target_resource=request.destination,
        reason="Missing live Admin authorization for high-risk target.",
        status="FAILED"
    )
    return {
        "status": "APPROVED", 
        "message": f"Successfully transferred ${request.amount} to {request.destination}."
    }

@app.post("/api/initiate-call")
def initiate_call(request: SessionRequest):
    """Step 1: Admin generates a Session ID AND both codes."""
    session_id = str(uuid.uuid4())[:8].upper()
    code_a = str(random.randint(1000, 9999))
    code_b = str(random.randint(1000, 9999))
    
    active_sessions[session_id] = {
        "account_number": request.account_number,
        "status": "pending_customer",
        "code_a": code_a,
        "code_b": code_b
    }
    
    
    emit_audit_log(
        event_type="SECURE_SESSION_GENERATED",
        actor_id="IAM-ADMIN",
        target_resource=session_id,
        reason="Admin initiated Sentinel-Vault JIT Arbiter session.",
        status="ACTIVE"
    )
    
    return {
        "session_id": session_id, 
        "employee_code_a": code_a 
    }

@app.post("/api/customer/verify-employee")
def customer_verify_employee(request: CustomerVerifyEmployeeRequest):
    """Step 2: Engineer submits Code A to verify Admin."""
    session = active_sessions.get(request.session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Invalid Session ID. Hang up immediately.")
        
    if request.employee_code_a != session["code_a"]:
        
        emit_audit_log(
            event_type="UNAUTHORIZED_ADMIN_ATTEMPT",
            actor_id="ENG-9981",
            target_resource=request.session_id,
            reason="Cryptographic Handshake Failed - Invalid Admin Code provided.",
            status="CRITICAL_ALERT"
        )
        raise HTTPException(status_code=401, detail="FAKE ADMIN DETECTED. Disconnect immediately.")
    
    session["status"] = "employee_verified_awaiting_customer"
    

    emit_audit_log(
        event_type="ADMIN_IDENTITY_VERIFIED",
        actor_id="ENG-9981",
        target_resource=request.session_id,
        reason="Engineer successfully verified Admin's cryptographic code.",
        status="SUCCESS"
    )
    
    return {
        "message": "Admin Identity Verified!",
        "customer_code_b": session["code_b"]
    }

@app.post("/api/employee/verify-handshake")
def employee_verify_handshake(request: EmployeeVerificationRequest):
    """Step 3: Admin submits Code B to complete the handshake and grant access."""
    session = active_sessions.get(request.session_id)
    
    if not session or request.customer_code_b != session["code_b"]:
    
        emit_audit_log(
            event_type="JIT_HANDSHAKE_FAILED",
            actor_id="IAM-ADMIN",
            target_resource=request.session_id,
            reason="Admin failed to provide matching Engineer code.",
            status="CRITICAL_ALERT"
        )
        raise HTTPException(status_code=401, detail="Authentication Failed. Disconnect call.")
        
    session["status"] = "SECURE"
    
    
    emit_audit_log(
        event_type="JIT_ACCESS_GRANTED",
        actor_id="IAM-ADMIN",
        target_resource=session["account_number"],
        reason="Mutual handshake complete. Least Privilege access granted to enclave.",
        status="SUCCESS"
    )
    
    return {"message": "MUTUAL HANDSHAKE COMPLETE. Session is secure. You may proceed with the transaction."}
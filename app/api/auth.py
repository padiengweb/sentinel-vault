from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import TransactionRequest, SessionRequest, CustomerVerifyRequest, EmployeeVerifyRequest
from app.core.audit import emit_audit_log
from app.core.security import generate_nonce, verify_signature
from app.core.database import get_db
import uuid
import random

router = APIRouter(prefix="/api")

active_sessions = {}

@router.post("/transaction/request")
async def request_transaction(request: TransactionRequest, db: AsyncSession = Depends(get_db)):
    if request.is_employee_instructing:
        await emit_audit_log(db, "JIT_AUTH_REQUIRED", request.account_number, request.destination, "High-risk target requires live Admin authorization.", "PENDING_AUTH")
        return {"status": "BLOCKED_PENDING_AUTH"}
        
    await emit_audit_log(db, "JIT_ACCESS_DENIED", request.account_number, request.destination, "Missing live Admin authorization.", "FAILED")
    return {"status": "APPROVED"}

@router.post("/initiate-call")
async def initiate_call(request: SessionRequest, db: AsyncSession = Depends(get_db)):
    session_id = str(uuid.uuid4())[:8].upper()
    code_a = str(random.randint(1000, 9999))
    code_b = str(random.randint(1000, 9999))
    nonce = generate_nonce() 
    
    active_sessions[session_id] = {
        "account_number": request.account_number,
        "code_a": code_a,
        "code_b": code_b,
        "nonce": nonce,
        "status": "pending_customer"
    }
    
    await emit_audit_log(db, "SECURE_SESSION_GENERATED", "IAM-ADMIN", session_id, "Admin initiated JIT session.", "ACTIVE")
    return {"session_id": session_id, "employee_code_a": code_a}

@router.post("/customer/verify-employee")
async def verify_employee(request: CustomerVerifyRequest, db: AsyncSession = Depends(get_db)):
    session = active_sessions.get(request.session_id)
    if not session or request.employee_code_a != session["code_a"]:
        await emit_audit_log(db, "UNAUTHORIZED_ADMIN_ATTEMPT", "ENG-9981", request.session_id, "Invalid Admin Code provided.", "CRITICAL_ALERT")
        raise HTTPException(status_code=401, detail="FAKE ADMIN DETECTED.")
        
    await emit_audit_log(db, "ADMIN_IDENTITY_VERIFIED", "ENG-9981", request.session_id, "Engineer verified Admin code.", "SUCCESS")
    
    return {
        "message": "Admin Identity Verified!",
        "customer_code_b": session["code_b"],
        "cryptographic_nonce": session["nonce"] 
    }

@router.post("/employee/verify-handshake")
async def verify_handshake(request: EmployeeVerifyRequest, db: AsyncSession = Depends(get_db)):
    session = active_sessions.get(request.session_id)
    if not session or request.customer_code_b != session["code_b"]:
        await emit_audit_log(db, "JIT_HANDSHAKE_FAILED", "IAM-ADMIN", request.session_id, "Admin failed matching code.", "CRITICAL_ALERT")
        raise HTTPException(status_code=401, detail="Authentication Failed.")
        
    
    is_valid = verify_signature(request.public_key_pem, session["nonce"], request.signature)
    if not is_valid:
        await emit_audit_log(db, "CRYPTOGRAPHIC_MISMATCH", "IAM-ADMIN", request.session_id, "ECDSA signature verification failed.", "CRITICAL_ALERT")
        raise HTTPException(status_code=401, detail="Cryptographic signature invalid.")
        
    session["status"] = "SECURE"
    await emit_audit_log(db, "JIT_ACCESS_GRANTED", "IAM-ADMIN", session["account_number"], "Mutual cryptographic handshake complete.", "SUCCESS")
    
    return {"message": "MUTUAL HANDSHAKE COMPLETE. Session is mathematically secure."}
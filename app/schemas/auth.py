from pydantic import BaseModel

class TransactionRequest(BaseModel):
    account_number: str
    amount: float
    destination: str
    is_employee_instructing: bool  

class SessionRequest(BaseModel):
    account_number: str

class CustomerVerifyRequest(BaseModel):
    session_id: str
    employee_code_a: str  

class EmployeeVerifyRequest(BaseModel):
    session_id: str
    customer_code_b: str
    public_key_pem: str  
    signature: str       
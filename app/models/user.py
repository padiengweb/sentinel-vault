import enum
import uuid
from sqlalchemy import Column, String, DateTime, Enum, Boolean, func
from app.core.database import Base

class RoleEnum(str, enum.Enum):
    employee = "employee"
    admin = "admin"
    auditor = "auditor"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    public_key_pem = Column(String, nullable=False) 
    role = Column(Enum(RoleEnum), default=RoleEnum.employee, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
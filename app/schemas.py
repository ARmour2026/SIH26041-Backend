from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import uuid


class WorkerCreate(BaseModel):
    name: str
    mobile_number: str
    sector: str
    language_pref: Optional[str] = "hi"


class WorkerResponse(WorkerCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ModuleResponse(BaseModel):
    id: int
    title: str
    safety_domain: str
    created_at: datetime

    class Config:
        from_attributes = True


class AssessmentCreate(BaseModel):
    worker_id: int
    module_id: int
    score: int
    passed: bool
    answers_payload: Optional[Dict[str, Any]] = None


class AssessmentResponse(AssessmentCreate):
    id: int
    completed_at: datetime

    class Config:
        from_attributes = True


class CertificateResponse(BaseModel):
    certificate_code: uuid.UUID
    worker_id: int
    module_id: int
    qr_payload: str
    issued_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True


class SyncBatchPayload(BaseModel):
    worker_id: int
    offline_assessments: list[AssessmentCreate] = []


# =========================
# Authentication Schemas
# =========================

class RegisterRequest(BaseModel):
    name: str
    mobile_number: str
    password: str
    sector: str
    language_pref: Optional[str] = "hi"


class LoginRequest(BaseModel):
    mobile_number: str
    password: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


# =========================
# Forgot Password Schemas
# =========================

class ForgotPasswordRequest(BaseModel):
    mobile_number: str


class VerifyOTPRequest(BaseModel):
    mobile_number: str
    otp: str


class ResetPasswordRequest(BaseModel):
    mobile_number: str
    new_password: str
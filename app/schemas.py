from pydantic import BaseModel, Field
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
    title_hi: str
    title_sat: str
    safety_domain: str
    version: str
    content_payload: Dict[str, Any]
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

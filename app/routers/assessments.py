from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
from ..database import get_db
from ..models import Assessment, Certification, Worker, Module
from ..schemas import AssessmentCreate, AssessmentResponse, CertificateResponse, SyncBatchPayload

router = APIRouter(prefix="/assessments", tags=["Assessments & Certification"])

@router.post("/", response_model=AssessmentResponse)
def submit_assessment(payload: AssessmentCreate, db: Session = Depends(get_db)):
    assessment = Assessment(**payload.dict())
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    if payload.passed:
        cert_code = uuid.uuid4()
        qr_data = f"VERIFIED_CERT:{cert_code}:W{payload.worker_id}:M{payload.module_id}"
        expires = datetime.utcnow() + timedelta(days=365)
        
        existing_cert = db.query(Certification).filter(
            Certification.worker_id == payload.worker_id,
            Certification.module_id == payload.module_id
        ).first()

        if not existing_cert:
            cert = Certification(
                certificate_code=cert_code,
                worker_id=payload.worker_id,
                module_id=payload.module_id,
                qr_payload=qr_data,
                expires_at=expires
            )
            db.add(cert)
            db.commit()

    return assessment

@router.post("/sync-offline")
def sync_offline_data(batch: SyncBatchPayload, db: Session = Depends(get_db)):
    results = []
    for item in batch.offline_assessments:
        assessment = Assessment(**item.dict())
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        results.append(assessment.id)
    return {"status": "success", "synced_assessments": len(results)}

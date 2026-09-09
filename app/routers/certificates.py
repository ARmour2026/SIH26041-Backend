from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from ..database import get_db
from ..models import Certification, Worker, Module
from ..schemas import CertificateResponse

router = APIRouter(prefix="/certificates", tags=["Certificate Verification"])

@router.get("/verify/{certificate_code}", response_model=CertificateResponse)
def verify_certificate(certificate_code: uuid.UUID, db: Session = Depends(get_db)):
    cert = db.query(Certification).filter(Certification.certificate_code == certificate_code).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Invalid or non-existent certificate code.")
    return cert

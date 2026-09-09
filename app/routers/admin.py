from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import Worker, Assessment, Certification

router = APIRouter(prefix="/admin", tags=["Web Admin Compliance Dashboard"])

@router.get("/compliance-stats")
def get_compliance_stats(db: Session = Depends(get_db)):
    total_workers = db.query(func.count(Worker.id)).scalar()
    total_assessments = db.query(func.count(Assessment.id)).scalar()
    total_passed = db.query(func.count(Assessment.id)).filter(Assessment.passed == True).scalar()
    total_certificates = db.query(func.count(Certification.id)).scalar()

    sector_breakdown = db.query(
        Worker.sector, func.count(Worker.id)
    ).group_by(Worker.sector).all()

    return {
        "total_workers": total_workers,
        "total_assessments": total_assessments,
        "total_passed": total_passed,
        "total_certificates_issued": total_certificates,
        "sector_breakdown": {sector: count for sector, count in sector_breakdown}
    }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Worker
from ..schemas import WorkerCreate, WorkerResponse

router = APIRouter(prefix="/workers", tags=["Workers"])

@router.post("/", response_model=WorkerResponse)
def register_worker(worker: WorkerCreate, db: Session = Depends(get_db)):
    existing = db.query(Worker).filter(Worker.mobile_number == worker.mobile_number).first()
    if existing:
        return existing
    db_worker = Worker(**worker.dict())
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker

@router.get("/{worker_id}", response_model=WorkerResponse)
def get_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

@router.get("/", response_model=list[WorkerResponse])
def get_worker(db: Session = Depends(get_db)):
    workers = db.query(Worker).all()
    if not workers:
        raise HTTPException(status_code=404, detail="Worker not found")
    return workers

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Module
from ..schemas import ModuleResponse

router = APIRouter(prefix="/modules", tags=["AR Training Modules"])

@router.get("/", response_model=List[ModuleResponse])
def list_modules(db: Session = Depends(get_db)):
    return db.query(Module).all()

@router.get("/{module_id}", response_model=ModuleResponse)
def get_module(module_id: int, db: Session = Depends(get_db)):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module

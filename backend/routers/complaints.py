from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter(
    prefix="/api/complaints",
    tags=["Complaints"]
)

@router.post("/", response_model=schemas.ComplaintResponse)
def create_complaint(complaint: schemas.ComplaintCreate, db: Session = Depends(get_db)):
    db_complaint = models.Complaint(**complaint.model_dump())
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

@router.get("/", response_model=List[schemas.ComplaintResponse])
def get_complaints(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    complaints = db.query(models.Complaint).offset(skip).limit(limit).all()
    return complaints

@router.get("/{complaint_id}", response_model=schemas.ComplaintResponse)
def get_complaint(complaint_id: str, db: Session = Depends(get_db)):
    db_complaint = db.query(models.Complaint).filter(models.Complaint.id == complaint_id).first()
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return db_complaint

@router.put("/{complaint_id}", response_model=schemas.ComplaintResponse)
def update_complaint(complaint_id: str, complaint: schemas.ComplaintUpdate, db: Session = Depends(get_db)):
    db_complaint = db.query(models.Complaint).filter(models.Complaint.id == complaint_id).first()
    if db_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    update_data = complaint.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_complaint, key, value)
        
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

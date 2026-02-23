from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import date

from app.core.database import get_db
from app.models.fra_models import Grievance
from app.schemas.fra_schemas import (
    Grievance as GrievanceSchema,
    GrievanceCreate,
    GrievanceUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[GrievanceSchema])
async def get_grievances(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=300),
    status: Optional[str] = None,
    priority: Optional[str] = None,
    state: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get all grievances with optional filters"""
    query = db.query(Grievance)
    
    if status:
        query = query.filter(Grievance.status == status)
    if priority:
        query = query.filter(Grievance.priority == priority)
    if state:
        query = query.filter(Grievance.state == state)
    
    # Order by priority and filed date
    grievances = query.order_by(Grievance.filed_date.desc()).offset(skip).limit(limit).all()
    return grievances


@router.get("/{grievance_id}", response_model=GrievanceSchema)
async def get_grievance(grievance_id: str, db: Session = Depends(get_db)):
    """Get a specific grievance by ID"""
    grievance = db.query(Grievance).filter(Grievance.grievance_id == grievance_id).first()
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")
    return grievance


@router.post("/", response_model=GrievanceSchema, status_code=201)
async def create_grievance(grievance: GrievanceCreate, db: Session = Depends(get_db)):
    """File a new grievance"""
    db_grievance = Grievance(**grievance.model_dump(), filed_date=date.today())
    db.add(db_grievance)
    db.commit()
    db.refresh(db_grievance)
    return db_grievance


@router.patch("/{grievance_id}", response_model=GrievanceSchema)
async def update_grievance(
    grievance_id: str,
    grievance_update: GrievanceUpdate,
    db: Session = Depends(get_db),
):
    """Update a grievance status or response"""
    db_grievance = db.query(Grievance).filter(Grievance.grievance_id == grievance_id).first()
    if not db_grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")
    
    update_data = grievance_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_grievance, field, value)
    
    db.commit()
    db.refresh(db_grievance)
    return db_grievance


@router.get("/stats/summary")
async def get_grievance_stats(
    state: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get grievance statistics"""
    query = db.query(Grievance)
    
    if state:
        query = query.filter(Grievance.state == state)
    
    total = query.count()
    open_count = query.filter(Grievance.status == "open").count()
    in_progress = query.filter(Grievance.status == "in-progress").count()
    resolved = query.filter(Grievance.status == "resolved").count()
    
    return {
        "total_grievances": total,
        "open": open_count,
        "in_progress": in_progress,
        "resolved": resolved,
        "resolution_rate": round((resolved / total * 100) if total > 0 else 0, 2),
    }

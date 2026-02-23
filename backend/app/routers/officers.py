from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.fra_models import Officer
from app.schemas.fra_schemas import Officer as OfficerSchema, OfficerCreate

router = APIRouter()


@router.get("/", response_model=List[OfficerSchema])
async def get_officers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=200),
    state: Optional[str] = None,
    role: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get all officers with optional filters"""
    query = db.query(Officer)
    
    if state:
        query = query.filter(Officer.state == state)
    if role:
        query = query.filter(Officer.role == role)
    
    officers = query.offset(skip).limit(limit).all()
    return officers


@router.get("/{officer_code}", response_model=OfficerSchema)
async def get_officer(officer_code: str, db: Session = Depends(get_db)):
    """Get a specific officer by code"""
    officer = db.query(Officer).filter(Officer.code == officer_code).first()
    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")
    return officer


@router.post("/", response_model=OfficerSchema, status_code=201)
async def create_officer(officer: OfficerCreate, db: Session = Depends(get_db)):
    """Create a new officer"""
    existing = db.query(Officer).filter(Officer.code == officer.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Officer code already exists")
    
    db_officer = Officer(**officer.model_dump())
    db.add(db_officer)
    db.commit()
    db.refresh(db_officer)
    return db_officer

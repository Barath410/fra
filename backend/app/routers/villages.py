from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.core.database import get_db
from app.models.fra_models import Village
from app.schemas.fra_schemas import Village as VillageSchema, VillageCreate

router = APIRouter()


@router.get("/", response_model=List[VillageSchema])
async def get_villages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    state: Optional[str] = None,
    district: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get all villages with optional filters"""
    query = db.query(Village)
    
    if state:
        query = query.filter(Village.state == state)
    if district:
        query = query.filter(Village.district == district)
    
    villages = query.offset(skip).limit(limit).all()
    return villages


@router.get("/{village_code}", response_model=VillageSchema)
async def get_village(village_code: str, db: Session = Depends(get_db)):
    """Get a specific village by code"""
    village = db.query(Village).filter(Village.code == village_code).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    return village


@router.post("/", response_model=VillageSchema, status_code=201)
async def create_village(village: VillageCreate, db: Session = Depends(get_db)):
    """Create a new village"""
    existing = db.query(Village).filter(Village.code == village.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Village code already exists")
    
    db_village = Village(**village.model_dump())
    db.add(db_village)
    db.commit()
    db.refresh(db_village)
    return db_village


@router.get("/stats/summary")
async def get_village_stats(
    state: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get village statistics"""
    query = db.query(Village)
    
    if state:
        query = query.filter(Village.state == state)
    
    total_villages = query.count()
    total_claims = query.with_entities(func.sum(Village.total_claims)).scalar() or 0
    total_granted = query.with_entities(func.sum(Village.granted_claims)).scalar() or 0
    total_patta_holders = query.with_entities(func.sum(Village.patta_holder_count)).scalar() or 0
    
    return {
        "total_villages": total_villages,
        "total_claims": total_claims,
        "total_granted": total_granted,
        "total_patta_holders": total_patta_holders,
    }

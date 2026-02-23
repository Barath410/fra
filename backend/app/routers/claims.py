from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import date

from app.core.database import get_db
from app.models.fra_models import FRAClaim, ClaimStatus, ClaimType
from app.schemas.fra_schemas import (
    FRAClaim as FRAClaimSchema,
    FRAClaimCreate,
    FRAClaimUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[FRAClaimSchema])
async def get_claims(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    state: Optional[str] = None,
    district: Optional[str] = None,
    status: Optional[str] = None,
    claim_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get all claims with optional filters"""
    query = db.query(FRAClaim)
    
    if state:
        query = query.filter(FRAClaim.state == state)
    if district:
        query = query.filter(FRAClaim.district == district)
    if status:
        query = query.filter(FRAClaim.status == status)
    if claim_type:
        query = query.filter(FRAClaim.claim_type == claim_type)
    
    claims = query.offset(skip).limit(limit).all()
    return claims


@router.get("/{claim_id}", response_model=FRAClaimSchema)
async def get_claim(claim_id: str, db: Session = Depends(get_db)):
    """Get a specific claim by ID"""
    claim = db.query(FRAClaim).filter(FRAClaim.claim_id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim


@router.post("/", response_model=FRAClaimSchema, status_code=201)
async def create_claim(claim: FRAClaimCreate, db: Session = Depends(get_db)):
    """Create a new FRA claim"""
    # Check if claim_id already exists
    existing = db.query(FRAClaim).filter(FRAClaim.claim_id == claim.claim_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Claim ID already exists")
    
    db_claim = FRAClaim(**claim.model_dump())
    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)
    return db_claim


@router.patch("/{claim_id}", response_model=FRAClaimSchema)
async def update_claim(
    claim_id: str,
    claim_update: FRAClaimUpdate,
    db: Session = Depends(get_db),
):
    """Update a claim's status or verification"""
    db_claim = db.query(FRAClaim).filter(FRAClaim.claim_id == claim_id).first()
    if not db_claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    update_data = claim_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_claim, field, value)
    
    db.commit()
    db.refresh(db_claim)
    return db_claim


@router.get("/stats/summary")
async def get_claim_stats(
    state: Optional[str] = None,
    district: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get claim statistics"""
    query = db.query(FRAClaim)
    
    if state:
        query = query.filter(FRAClaim.state == state)
    if district:
        query = query.filter(FRAClaim.district == district)
    
    total = query.count()
    granted = query.filter(FRAClaim.status == ClaimStatus.granted).count()
    pending = query.filter(FRAClaim.status == ClaimStatus.pending).count()
    rejected = query.filter(FRAClaim.status == ClaimStatus.rejected).count()
    
    total_area = query.with_entities(func.sum(FRAClaim.area_verified_ha)).scalar() or 0
    
    return {
        "total_claims": total,
        "granted": granted,
        "pending": pending,
        "rejected": rejected,
        "grant_rate": round((granted / total * 100) if total > 0 else 0, 2),
        "total_area_granted_ha": round(total_area, 2),
    }


@router.get("/stats/by-state")
async def get_claims_by_state(db: Session = Depends(get_db)):
    """Get claim statistics grouped by state"""
    results = (
        db.query(
            FRAClaim.state,
            func.count(FRAClaim.id).label("total"),
            func.sum(func.case((FRAClaim.status == ClaimStatus.granted, 1), else_=0)).label("granted"),
            func.sum(func.case((FRAClaim.status == ClaimStatus.pending, 1), else_=0)).label("pending"),
            func.sum(func.case((FRAClaim.status == ClaimStatus.rejected, 1), else_=0)).label("rejected"),
        )
        .group_by(FRAClaim.state)
        .all()
    )
    
    return [
        {
            "state": row.state,
            "total_claims": row.total,
            "granted": row.granted or 0,
            "pending": row.pending or 0,
            "rejected": row.rejected or 0,
            "grant_rate": round((row.granted / row.total * 100) if row.total > 0 else 0, 2),
        }
        for row in results
    ]

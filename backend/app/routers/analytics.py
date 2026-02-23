from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from app.core.database import get_db
from app.models.fra_models import FRAClaim, Village, Officer, Grievance, ClaimStatus

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_analytics(
    state: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get comprehensive dashboard analytics"""
    claim_query = db.query(FRAClaim)
    village_query = db.query(Village)
    
    if state:
        claim_query = claim_query.filter(FRAClaim.state == state)
        village_query = village_query.filter(Village.state == state)
    
    total_claims = claim_query.count()
    granted = claim_query.filter(FRAClaim.status == ClaimStatus.granted).count()
    pending = claim_query.filter(FRAClaim.status == ClaimStatus.pending).count()
    rejected = claim_query.filter(FRAClaim.status == ClaimStatus.rejected).count()
    
    total_villages = village_query.count()
    total_area = claim_query.with_entities(func.sum(FRAClaim.area_verified_ha)).scalar() or 0
    
    states = claim_query.distinct(FRAClaim.state).count()
    districts = claim_query.distinct(FRAClaim.district).count()
    
    return {
        "total_claims": total_claims,
        "granted_claims": granted,
        "pending_claims": pending,
        "rejected_claims": rejected,
        "grant_rate": round((granted / total_claims * 100) if total_claims > 0 else 0, 2),
        "total_villages": total_villages,
        "total_area_granted_ha": round(total_area, 2),
        "states_covered": states,
        "districts_covered": districts,
    }


@router.get("/claims-trend")
async def get_claims_trend(
    state: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get monthly claims trend"""
    query = db.query(FRAClaim)
    
    if state:
        query = query.filter(FRAClaim.state == state)
    
    # Group by month (simplified - would need proper date_trunc in production)
    results = (
        query
        .with_entities(
            func.date_trunc('month', FRAClaim.filed_date).label('month'),
            func.count(FRAClaim.id).label('count')
        )
        .group_by('month')
        .order_by('month')
        .limit(12)
        .all()
    )
    
    return [
        {
            "month": row.month.strftime("%b %Y"),
            "count": row.count,
        }
        for row in results
    ]


@router.get("/state-comparison")
async def get_state_comparison(db: Session = Depends(get_db)):
    """Get state-wise comparison"""
    results = (
        db.query(
            FRAClaim.state,
            func.count(FRAClaim.id).label("total"),
            func.sum(func.case((FRAClaim.status == ClaimStatus.granted, 1), else_=0)).label("granted"),
            func.sum(FRAClaim.area_verified_ha).label("total_area"),
        )
        .group_by(FRAClaim.state)
        .all()
    )
    
    return [
        {
            "state": row.state,
            "total_claims": row.total,
            "granted": row.granted or 0,
            "grant_rate": round((row.granted / row.total * 100) if row.total > 0 else 0, 2),
            "total_area_ha": round(row.total_area or 0, 2),
        }
        for row in results
    ]

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.core.database import get_db
from app.models.fra_models import DSSRecommendation
from app.schemas.fra_schemas import (
    DSSRecommendation as DSSRecommendationSchema,
    DSSRecommendationCreate,
)

router = APIRouter()


@router.get("/recommendations", response_model=List[DSSRecommendationSchema])
async def get_recommendations(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=200),
    state: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get DSS recommendations with optional filters"""
    query = db.query(DSSRecommendation)
    
    if state:
        query = query.filter(DSSRecommendation.state == state)
    if priority:
        query = query.filter(DSSRecommendation.priority == priority)
    
    # Order by AI score (highest first)
    recommendations = query.order_by(DSSRecommendation.ai_score.desc()).offset(skip).limit(limit).all()
    return recommendations


@router.post("/recommendations", response_model=DSSRecommendationSchema, status_code=201)
async def create_recommendation(
    recommendation: DSSRecommendationCreate,
    db: Session = Depends(get_db),
):
    """Create a new DSS recommendation"""
    db_rec = DSSRecommendation(**recommendation.model_dump())
    db_rec.gap = db_rec.eligible_beneficiaries - db_rec.currently_enrolled
    db.add(db_rec)
    db.commit()
    db.refresh(db_rec)
    return db_rec


@router.get("/recommendations/stats")
async def get_recommendation_stats(
    state: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get DSS recommendation statistics"""
    query = db.query(DSSRecommendation)
    
    if state:
        query = query.filter(DSSRecommendation.state == state)
    
    total = query.count()
    critical = query.filter(DSSRecommendation.priority == "critical").count()
    high = query.filter(DSSRecommendation.priority == "high").count()
    medium = query.filter(DSSRecommendation.priority == "medium").count()
    
    return {
        "total_recommendations": total,
        "critical": critical,
        "high": high,
        "medium": medium,
        "avg_ai_score": round(query.with_entities(func.avg(DSSRecommendation.ai_score)).scalar() or 0, 2),
    }

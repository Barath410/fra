from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.fra_models import SchemeEnrollment
from app.schemas.fra_schemas import (
    SchemeEnrollment as SchemeEnrollmentSchema,
    SchemeEnrollmentCreate,
)

router = APIRouter()


@router.get("/", response_model=List[SchemeEnrollmentSchema])
async def get_scheme_enrollments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=200),
    village_code: Optional[str] = None,
    scheme_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get scheme enrollments with optional filters"""
    query = db.query(SchemeEnrollment)
    
    if village_code:
        query = query.filter(SchemeEnrollment.village_code == village_code)
    if scheme_id:
        query = query.filter(SchemeEnrollment.scheme_id == scheme_id)
    
    enrollments = query.offset(skip).limit(limit).all()
    return enrollments


@router.post("/", response_model=SchemeEnrollmentSchema, status_code=201)
async def create_enrollment(enrollment: SchemeEnrollmentCreate, db: Session = Depends(get_db)):
    """Create a new scheme enrollment"""
    db_enrollment = SchemeEnrollment(**enrollment.model_dump())
    
    # Calculate saturation percentage
    if db_enrollment.target_beneficiaries > 0:
        db_enrollment.saturation_pct = (
            db_enrollment.enrolled_beneficiaries / db_enrollment.target_beneficiaries * 100
        )
    
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


@router.get("/stats/saturation")
async def get_scheme_saturation(scheme_id: Optional[str] = None, db: Session = Depends(get_db)):
    """Get scheme saturation statistics"""
    query = db.query(SchemeEnrollment)
    
    if scheme_id:
        query = query.filter(SchemeEnrollment.scheme_id == scheme_id)
    
    enrollments = query.all()
    
    total_target = sum(e.target_beneficiaries for e in enrollments)
    total_enrolled = sum(e.enrolled_beneficiaries for e in enrollments)
    avg_saturation = sum(e.saturation_pct for e in enrollments) / len(enrollments) if enrollments else 0
    
    return {
        "total_target_beneficiaries": total_target,
        "total_enrolled": total_enrolled,
        "overall_saturation_pct": round((total_enrolled / total_target * 100) if total_target > 0 else 0, 2),
        "avg_village_saturation_pct": round(avg_saturation, 2),
    }

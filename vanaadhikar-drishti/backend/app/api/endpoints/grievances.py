from __future__ import annotations

from typing import Annotated
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.grievance import Grievance
from app.schemas.domain import GrievanceCreate, GrievanceRead
from app.schemas.pagination import GrievancesPaginatedResponse
from app.services.data_service import list_grievances


router = APIRouter(prefix="/grievances", tags=["grievances"])


@router.get("", response_model=GrievancesPaginatedResponse)
def get_grievances(
    state: Annotated[str | None, Query(description="Filter by state")] = None,
    district: Annotated[str | None, Query(description="Filter by district")] = None,
    status_filter: Annotated[str | None, Query(alias="status", description="Filter by status")] = None,
    priority: Annotated[str | None, Query(description="Filter by priority (LOW, MEDIUM, HIGH, CRITICAL)")] = None,
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    limit: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 20,
    db: Session = Depends(get_db),
):
    """Get all grievances with pagination and filtering.
    
    Query Parameters:
    - state: Filter by state code (e.g., 'MP', 'CG', 'MH')
    - district: Filter by district name
    - status: Filter by status (OPEN, PENDING, RESOLVED)
    - priority: Filter by priority (LOW, MEDIUM, HIGH, CRITICAL)
    - page: Page number (default 1)
    - limit: Items per page (default 20, max 100)
    
    Returns paginated list of grievances with metadata.
    """
    return list_grievances(
        db,
        state=state,
        status=status_filter,
        district=district,
        priority=priority,
        page=page,
        limit=limit,
    )


@router.get("/{grievance_id}", response_model=GrievanceRead)
def get_grievance(grievance_id: str, db: Session = Depends(get_db)):
    """Get a specific grievance by ID."""
    grievance = db.query(Grievance).filter(Grievance.grievance_id == grievance_id).first()
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")
    return GrievanceRead.model_validate(grievance)


@router.post("", response_model=GrievanceRead, status_code=status.HTTP_201_CREATED)
def create_grievance(payload: GrievanceCreate, db: Session = Depends(get_db)):
    """Create a new grievance.
    
    A grievance is a complaint filed against a claim or officer action.
    """
    # Check if grievance ID already exists
    existing = db.query(Grievance).filter(Grievance.grievance_id == payload.grievance_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Grievance with this ID already exists")

    grievance = Grievance(
        grievance_id=payload.grievance_id,
        claimant_name=payload.claimant_name,
        claim_id=payload.claim_id,
        village_name=payload.village_name,
        block=payload.block,
        district=payload.district,
        state=payload.state,
        category=payload.category,
        status=payload.status,
        priority=payload.priority,
        description=payload.description,
        channel=payload.channel,
        mobile=payload.mobile,
        source=payload.source,
        assigned_officer_id=payload.assigned_officer_id,
        filed_date=payload.filed_date,
    )
    db.add(grievance)
    db.commit()
    db.refresh(grievance)
    return GrievanceRead.model_validate(grievance)


@router.patch("/{grievance_id}", response_model=GrievanceRead)
def update_grievance(
    grievance_id: str,
    payload: dict,
    db: Session = Depends(get_db),
):
    """Update a grievance status or details."""
    grievance = db.query(Grievance).filter(Grievance.grievance_id == grievance_id).first()
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")

    # Update allowed fields
    allowed_fields = {"status", "priority", "resolution", "assigned_officer_id", "assigned_to"}
    for field, value in payload.items():
        if field in allowed_fields and value is not None:
            setattr(grievance, field, value)

    db.commit()
    db.refresh(grievance)
    return GrievanceRead.model_validate(grievance)
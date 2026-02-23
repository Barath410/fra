from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.officer import Officer
from app.schemas.domain import OfficerRead
from app.schemas.pagination import OfficersPaginatedResponse
from app.services.data_service import list_officers


router = APIRouter(prefix="/officers", tags=["officers"])


@router.get("", response_model=OfficersPaginatedResponse)
def get_officers(
    state: Annotated[str | None, Query(description="Filter by state")] = None,
    district: Annotated[str | None, Query(description="Filter by district")] = None,
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    limit: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 20,
    db: Session = Depends(get_db),
):
    """Get all officers with pagination and filtering.
    
    Query Parameters:
    - state: Filter by state code (e.g., 'MP', 'CG', 'MH')
    - district: Filter by district name
    - page: Page number (default 1)
    - limit: Items per page (default 20, max 100)
    
    Returns paginated list of officers with metadata.
    """
    return list_officers(db, state=state, district=district, page=page, limit=limit)


@router.get("/{officer_id}", response_model=OfficerRead)
def get_officer(officer_id: str, db: Session = Depends(get_db)):
    """Get a specific officer by ID."""
    officer = db.query(Officer).filter(Officer.officer_id == officer_id).first()
    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")
    return OfficerRead.model_validate(officer)
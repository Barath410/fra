from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.village import Village
from app.schemas.domain import VillageRead
from app.schemas.pagination import VillagesPaginatedResponse
from app.services.data_service import list_villages


router = APIRouter(prefix="/villages", tags=["villages"])


@router.get("", response_model=VillagesPaginatedResponse)
def get_villages(
    state: Annotated[str | None, Query(description="Filter by state")] = None,
    district: Annotated[str | None, Query(description="Filter by district")] = None,
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    limit: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 20,
    db: Session = Depends(get_db),
):
    """Get all villages with pagination and filtering.
    
    Query Parameters:
    - state: Filter by state code (e.g., 'MP', 'CG', 'MH')
    - district: Filter by district name
    - page: Page number (default 1)
    - limit: Items per page (default 20, max 100)
    
    Returns paginated list of villages with metadata.
    """
    return list_villages(db, state=state, district=district, page=page, limit=limit)


@router.get("/{code}", response_model=VillageRead)
def get_village(code: str, db: Session = Depends(get_db)):
    """Get a specific village by code."""
    village = db.query(Village).filter(Village.code == code).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    return VillageRead.model_validate(village)
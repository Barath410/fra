from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies import CurrentUser
from app.db.session import get_db
from app.models.claim import Claim
from app.schemas.domain import ClaimRead
from app.schemas.pagination import ClaimsPaginatedResponse
from app.services.data_service import search_claims


router = APIRouter(prefix="/claims", tags=["claims"])


@router.get("", response_model=ClaimsPaginatedResponse)
def list_claims(
    state: Annotated[str | None, Query(description="Filter by state")] = None,
    district: Annotated[str | None, Query(description="Filter by district")] = None,
    status: Annotated[str | None, Query(description="Filter by status")] = None,
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    limit: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 20,
    db: Session = Depends(get_db),
):
    """Get all claims with pagination and filtering.
    
    Query Parameters:
    - state: Filter by state code (e.g., 'MP', 'CG')
    - district: Filter by district name
    - status: Filter by claim status (PENDING, APPROVED, REJECTED)
    - page: Page number (default 1)
    - limit: Items per page (default 20, max 100)
    
    Returns paginated list of claims with metadata.
    """
    return search_claims(db, state=state, status=status, district=district, page=page, limit=limit)


@router.get("/{claim_id}", response_model=ClaimRead)
def get_claim(claim_id: str, db: Session = Depends(get_db)):
    """Get a specific claim by ID."""
    claim = db.query(Claim).filter(Claim.claim_id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return ClaimRead.model_validate(claim)


@router.post("", response_model=ClaimRead)
def create_claim(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
    claim_data: dict,
) -> ClaimRead:
    """Create new claim (requires authentication)."""
    # Only authenticated users can create claims
    claim = Claim(**claim_data)
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return ClaimRead.model_validate(claim)

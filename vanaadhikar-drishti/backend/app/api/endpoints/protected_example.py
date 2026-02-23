from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import CurrentUser
from app.db.session import get_db
from app.schemas.auth import UserResponse

router = APIRouter(prefix="/protected-example", tags=["protected example"])


@router.get("/user-claims", response_model=list[dict])
def get_user_claims(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> list[dict]:
    """Protected endpoint example - requires valid JWT token.
    
    Access token can be provided via:
    1. Authorization header: Authorization: Bearer <token>
    2. Cookie: auth_token=<token>
    
    Returns claims associated with current user.
    """
    # current_user is automatically validated and injected
    # Use it to query data or filter by user
    return [
        {
            "claim_id": "FRA-2026-MP-00001",
            "user_id": current_user.id,
            "user_email": current_user.email,
            "status": "APPROVED",
        }
    ]


@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: CurrentUser) -> UserResponse:
    """Protected endpoint - get current user's full profile."""
    return current_user


@router.post("/update-profile")
def update_profile(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    """Protected endpoint - update user profile data.
    
    Only authenticated users can modify their own profile.
    """
    return {
        "message": "Profile updated successfully",
        "user_id": current_user.id,
        "email": current_user.email,
    }

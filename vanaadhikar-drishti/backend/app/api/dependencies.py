from __future__ import annotations

from typing import Annotated

from fastapi import Cookie, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import UserResponse
from app.services.auth_service import AuthService


async def get_token_from_header_or_cookie(
    authorization: Annotated[str | None, Header()] = None,
    auth_token: Annotated[str | None, Cookie()] = None,
) -> str:
    """Extract JWT token from Authorization header or auth_token cookie."""
    token = None

    # Priority: Cookie > Authorization header
    if auth_token:
        token = auth_token
    elif authorization:
        # Handle "Bearer <token>" format
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1]
        else:
            token = authorization

    if not token:
        raise HTTPException(status_code=401, detail="Missing authentication token")

    return token


async def get_current_user(
    token: Annotated[str, Depends(get_token_from_header_or_cookie)],
    db: Annotated[Session, Depends(get_db)],
) -> UserResponse:
    """Dependency to get current authenticated user."""
    try:
        user = AuthService.get_current_user(db, token)
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            picture=user.picture,
            provider=user.provider,
            last_login=user.last_login,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


CurrentUser = Annotated[UserResponse, Depends(get_current_user)]

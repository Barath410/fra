from __future__ import annotations

from typing import Annotated
from base64 import urlsafe_b64decode, urlsafe_b64encode
import json
from urllib.parse import urlencode, urljoin

import httpx
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.api.dependencies import CurrentUser
from app.core.config import settings
from app.db.session import get_db
from app.schemas.auth import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/google/login", response_model=dict)
def google_login(next: str | None = None):
    """Generate Google OAuth login URL."""
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }

    if next:
        state_payload = json.dumps({"next": next}).encode()
        params["state"] = urlsafe_b64encode(state_payload).decode()

    return {"auth_url": f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"}


@router.get("/google/callback", response_model=dict)
def google_callback(code: str, state: str | None = None, db: Session = Depends(get_db)):
    """Handle Google OAuth callback - create/update user and issue JWT token."""
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    redirect_target: str | None = None
    if state:
        try:
            decoded = urlsafe_b64decode(state.encode()).decode()
            payload = json.loads(decoded)
            next_path = payload.get("next")
            if next_path:
                candidate = urljoin(settings.frontend_base_url, next_path)
                if candidate.startswith(settings.frontend_base_url):
                    redirect_target = candidate
        except Exception:
            redirect_target = None

    token_payload = {
        "code": code,
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "redirect_uri": settings.google_redirect_uri,
        "grant_type": "authorization_code",
    }

    try:
        with httpx.Client(timeout=15) as client:
            token_resp = client.post("https://oauth2.googleapis.com/token", data=token_payload)
            if token_resp.status_code != 200:
                raise HTTPException(
                    status_code=400, detail="Failed to exchange Google auth code"
                )
            token_data = token_resp.json()
            access_token = token_data.get("access_token")
            if not access_token:
                raise HTTPException(status_code=400, detail="Missing Google access token")

            profile_resp = client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if profile_resp.status_code != 200:
                raise HTTPException(status_code=400, detail="Unable to fetch Google profile")
            profile = profile_resp.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Google API error: {str(e)}")

    email = profile.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Google profile missing email")

    # Get or create user
    user = AuthService.get_or_create_user(
        db=db,
        email=email,
        name=profile.get("name") or "Google User",
        picture=profile.get("picture"),
    )

    # Update last_login on subsequent logins
    if user.last_login is not None:  # User already existed
        user = AuthService.update_last_login(db, user)

    # Generate JWT token
    jwt_token, expires_in = AuthService.generate_access_token(user)

    # Set HttpOnly cookie for browser clients
    if redirect_target:
        resp = RedirectResponse(url=f"{redirect_target}?token={jwt_token}")
        resp.status_code = 302
    else:
        resp = JSONResponse(
            {
                "token": jwt_token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "picture": user.picture,
                },
            }
        )

    resp.set_cookie(
        key="auth_token",
        value=jwt_token,
        httponly=True,
        secure=settings.app_env == "production",
        samesite="lax",
        max_age=expires_in,
    )

    return resp


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: CurrentUser) -> UserResponse:
    """Get current authenticated user profile."""
    return current_user


@router.post("/logout")
def logout(response: Response) -> dict:
    """Logout by clearing auth token cookie."""
    response.delete_cookie(key="auth_token", samesite="lax")
    return {"message": "Logout successful"}
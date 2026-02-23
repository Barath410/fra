from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    name: str
    picture: str | None = None
    provider: str = "google"


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    last_login: datetime | None = None


class UserResponse(UserBase):
    id: int
    last_login: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenPayload(BaseModel):
    sub: str = Field(..., description="User ID")
    email: EmailStr
    name: str
    exp: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(default=43200, description="Token expiration in seconds (12 hours)")
    user: UserResponse


class GoogleUserInfo(BaseModel):
    email: str
    name: str | None = None
    picture: str | None = None


class AuthResponse(BaseModel):
    token: str
    user: dict

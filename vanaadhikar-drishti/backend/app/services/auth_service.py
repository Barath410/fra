from __future__ import annotations

from datetime import datetime, timedelta, timezone

from jose import jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.schemas.auth import UserCreate, UserResponse


class AuthService:
    @staticmethod
    def get_or_create_user(db: Session, email: str, name: str, picture: str | None = None) -> User:
        """Get existing user or create new one on first login."""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                name=name or "Google User",
                picture=picture,
                provider="google",
                last_login=datetime.now(timezone.utc),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def update_last_login(db: Session, user: User) -> User:
        """Update user's last_login timestamp on each login."""
        user.last_login = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def generate_access_token(user: User, expires_delta: timedelta | None = None) -> tuple[str, int]:
        """Generate JWT access token for user."""
        if expires_delta is None:
            expires_delta = timedelta(hours=12)

        expire = datetime.now(timezone.utc) + expires_delta
        to_encode = {
            "sub": str(user.id),
            "email": user.email,
            "name": user.name,
            "exp": expire,
        }
        encoded_jwt = jwt.encode(
            to_encode,
            settings.jwt_private_key,
            algorithm=settings.jwt_algorithm,
        )
        return encoded_jwt, int(expires_delta.total_seconds())

    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify JWT token and return payload."""
        try:
            payload = jwt.decode(
                token,
                settings.jwt_public_key,
                algorithms=[settings.jwt_algorithm],
            )
            return payload
        except Exception as e:
            raise ValueError(f"Invalid token: {str(e)}")

    @staticmethod
    def get_current_user(db: Session, token: str) -> User:
        """Get current user from valid token."""
        try:
            payload = AuthService.verify_token(token)
        except ValueError:
            raise ValueError("Invalid or expired token")

        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Invalid token payload")

        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise ValueError("User not found")

        return user

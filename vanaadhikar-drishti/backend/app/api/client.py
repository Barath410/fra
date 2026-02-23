from __future__ import annotations

from typing import Any

from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.services.auth_service import AuthService

security = HTTPBearer(auto_error=False)


def get_api_client_user(
    authorization: str | None = Header(None),
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.token if credentials else None
    if not token and authorization:
        token = authorization.removeprefix("Bearer ")

    if not token:
        raise HTTPException(status_code=401, detail="Missing authorization token")

    try:
        return AuthService.get_current_user(db, token)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc))


def add_authorization_header(headers: dict[str, str], token: str | None) -> dict[str, str]:
    result: dict[str, str] = {"Content-Type": "application/json", **headers}
    if token:
        result["Authorization"] = f"Bearer {token}"
    return result


class APIClient:
    def __init__(self, token: str | None = None):
        self.token = token

    async def get(self, path: str, **kwargs: Any) -> Any:
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> Any:
        return await self.request("POST", path, **kwargs)

    async def request(self, method: str, path: str, **kwargs: Any) -> Any:
        import httpx

        headers = add_authorization_header(kwargs.pop("headers", {}), self.token)
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.request(method, path, headers=headers, **kwargs)
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        if response.content:
            return response.json()
        return None
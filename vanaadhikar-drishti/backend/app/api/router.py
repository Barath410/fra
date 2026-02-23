from fastapi import APIRouter

from app.api.endpoints import auth, claims, dashboard, documents, grievances, officers, villages

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(documents.router, prefix="/documents")
api_router.include_router(dashboard.router)
api_router.include_router(claims.router)
api_router.include_router(villages.router)
api_router.include_router(officers.router)
api_router.include_router(grievances.router)

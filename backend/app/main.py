from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.routers import (
    claims,
    villages,
    officers,
    dss,
    grievances,
    analytics,
    ocr,
    schemes,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 Starting VanAdhikar Drishti API Server...")
    yield
    # Shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title="VanAdhikar Drishti API",
    description="Forest Rights Act (FRA) Atlas & WebGIS Decision Support System API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Health Check
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "vanaadhikar-drishti-api",
    }


# Include Routers
app.include_router(claims.router, prefix="/api/claims", tags=["Claims"])
app.include_router(villages.router, prefix="/api/villages", tags=["Villages"])
app.include_router(officers.router, prefix="/api/officers", tags=["Officers"])
app.include_router(dss.router, prefix="/api/dss", tags=["DSS Engine"])
app.include_router(grievances.router, prefix="/api/grievances", tags=["Grievances"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(ocr.router, prefix="/api/ocr", tags=["OCR Digitization"])
app.include_router(schemes.router, prefix="/api/schemes", tags=["Schemes"])


@app.get("/")
async def root():
    return {
        "message": "VanAdhikar Drishti API — Forest Rights Act Atlas & Decision Support System",
        "docs": "/api/docs",
        "version": "1.0.0",
    }

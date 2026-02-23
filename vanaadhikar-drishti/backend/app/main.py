from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.tasks.cache_refresher import CacheRefresher

app = FastAPI(title="Vanaadhikar Document Processor", version="1.0.0")

app.include_router(api_router, prefix=settings.api_v1_prefix)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
  allow_credentials=True,
)


@app.get("/health", tags=["health"])
def health_check():
  return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
  """Start background cache refresh scheduler on app startup."""
  try:
    CacheRefresher.start()
  except Exception as e:
    print(f"Warning: Failed to start cache refresher: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
  """Stop background cache refresh scheduler on app shutdown."""
  try:
    CacheRefresher.stop()
  except Exception as e:
    print(f"Warning: Failed to stop cache refresher: {str(e)}")

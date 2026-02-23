from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.models.data_blob import DataBlob


class CacheService:
    """Caching service using data_blobs table."""

    CACHE_KEYS = {
        "dashboard_summary": "dashboard_summary",
        "claims_stats": "claims_stats",
        "villages_stats": "villages_stats",
        "grievances_stats": "grievances_stats",
        "state_stats": "state_stats",
        "district_stats": "district_stats",
        "monthly_progress": "monthly_progress",
        "claim_pipeline": "claim_pipeline",
    }

    @staticmethod
    def get(db: Session, key: str) -> dict[str, Any] | None:
        """Get cached data by key."""
        try:
            blob = db.query(DataBlob).filter(DataBlob.key == key).first()
            if not blob:
                return None
            if isinstance(blob.payload, dict):
                return blob.payload
            if isinstance(blob.payload, str):
                return json.loads(blob.payload)
            return blob.payload
        except Exception:
            return None

    @staticmethod
    def set(db: Session, key: str, data: dict[str, Any] | list) -> DataBlob:
        """Set cached data, creating or updating as needed."""
        existing = db.query(DataBlob).filter(DataBlob.key == key).first()

        if existing:
            existing.payload = data
            existing.updated_at = datetime.now(timezone.utc)
        else:
            existing = DataBlob(key=key, payload=data, created_at=datetime.now(timezone.utc))
            db.add(existing)

        db.commit()
        db.refresh(existing)
        return existing

    @staticmethod
    def delete(db: Session, key: str) -> bool:
        """Delete cached data by key."""
        blob = db.query(DataBlob).filter(DataBlob.key == key).first()
        if blob:
            db.delete(blob)
            db.commit()
            return True
        return False

    @staticmethod
    def exists(db: Session, key: str) -> bool:
        """Check if key exists in cache."""
        return db.query(DataBlob).filter(DataBlob.key == key).first() is not None

    @staticmethod
    def is_expired(db: Session, key: str, ttl_minutes: int = 15) -> bool:
        """Check if cached data is expired."""
        blob = db.query(DataBlob).filter(DataBlob.key == key).first()
        if not blob:
            return True
        
        age_seconds = (datetime.now(timezone.utc) - blob.updated_at).total_seconds()
        return age_seconds > (ttl_minutes * 60)

    @staticmethod
    def get_with_ttl(
        db: Session, key: str, ttl_minutes: int = 15
    ) -> dict[str, Any] | list | None:
        """Get cached data if not expired."""
        if CacheService.is_expired(db, key, ttl_minutes):
            return None
        return CacheService.get(db, key)

    @staticmethod
    def clear_all(db: Session) -> int:
        """Clear all cache entries."""
        count = db.query(DataBlob).delete()
        db.commit()
        return count

    @staticmethod
    def get_stats(db: Session) -> dict[str, Any]:
        """Get cache statistics."""
        total = db.query(DataBlob).count()
        sizes = db.query(DataBlob).all()
        total_size = sum(len(json.dumps(b.payload)) for b in sizes)

        return {
            "total_keys": total,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "keys": [{"key": b.key, "updated_at": b.updated_at.isoformat()} for b in sizes],
        }

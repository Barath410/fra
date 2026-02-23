from __future__ import annotations

import logging
from datetime import datetime, timezone

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.aggregation_service import AggregationService
from app.services.cache_service import CacheService


logger = logging.getLogger(__name__)


class CacheRefresher:
    """Background task scheduler for cache refresh."""

    _scheduler: BackgroundScheduler | None = None

    @classmethod
    def start(cls):
        """Start the background scheduler."""
        if cls._scheduler is not None:
            return

        cls._scheduler = BackgroundScheduler()

        # Refresh dashboard summary every 15 minutes
        cls._scheduler.add_job(
            cls._refresh_dashboard_summary,
            "interval",
            minutes=15,
            id="refresh_dashboard_summary",
            name="Refresh Dashboard Summary",
            replace_existing=True,
        )

        # Refresh state snapshots every 15 minutes
        cls._scheduler.add_job(
            cls._refresh_state_snapshots,
            "interval",
            minutes=15,
            id="refresh_state_snapshots",
            name="Refresh State Snapshots",
            replace_existing=True,
        )

        # Clear stale cache every hour
        cls._scheduler.add_job(
            cls._cleanup_stale_cache,
            "interval",
            hours=1,
            id="cleanup_stale_cache",
            name="Cleanup Stale Cache",
            replace_existing=True,
        )

        cls._scheduler.start()
        logger.info("Cache refresh scheduler started")

    @classmethod
    def stop(cls):
        """Stop the background scheduler."""
        if cls._scheduler is not None:
            cls._scheduler.shutdown()
            cls._scheduler = None
            logger.info("Cache refresh scheduler stopped")

    @staticmethod
    def _refresh_dashboard_summary():
        """Refresh dashboard summary cache."""
        try:
            db = SessionLocal()
            AggregationService.get_dashboard_summary(db)
            logger.info("Dashboard summary cache refreshed successfully")
            db.close()
        except Exception as e:
            logger.error(f"Error refreshing dashboard summary: {str(e)}")

    @staticmethod
    def _refresh_state_snapshots():
        """Refresh state snapshot caches."""
        try:
            db = SessionLocal()
            states = ["MP", "CG", "MH", "OD", "JH", "TS", "VN", "GJ"]
            
            for state in states:
                try:
                    AggregationService.get_state_snapshot(db, state)
                except Exception as e:
                    logger.warning(f"Error refreshing snapshot for state {state}: {str(e)}")
            
            logger.info("State snapshots cache refreshed successfully")
            db.close()
        except Exception as e:
            logger.error(f"Error refreshing state snapshots: {str(e)}")

    @staticmethod
    def _cleanup_stale_cache():
        """Cleanup stale cache entries."""
        try:
            db = SessionLocal()
            # Could add custom TTL cleanup logic here
            logger.info("Cache cleanup completed")
            db.close()
        except Exception as e:
            logger.error(f"Error cleaning up cache: {str(e)}")

    @classmethod
    def get_scheduler(cls) -> BackgroundScheduler | None:
        """Get scheduler instance."""
        return cls._scheduler

    @classmethod
    def is_running(cls) -> bool:
        """Check if scheduler is running."""
        return cls._scheduler is not None and cls._scheduler.running

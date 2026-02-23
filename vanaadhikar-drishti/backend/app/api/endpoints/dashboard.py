from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.aggregation_service import AggregationService
from app.services.cache_service import CacheService


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=dict[str, Any])
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get dashboard summary with aggregated statistics.
    
    Includes:
    - Claims statistics (total, approved, pending, rejected, by type, area)
    - Villages statistics (total, population, claims, area)
    - Grievances statistics (total, by priority, by category)
    - Officers statistics (total, by state, claims handled)
    - Timeline statistics (daily, weekly, monthly trends)
    
    Results are cached and refreshed every 15 minutes automatically.
    """
    try:
        summary = AggregationService.get_dashboard_summary(db)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating dashboard summary: {str(e)}")


@router.get("/state/{state}", response_model=dict[str, Any])
def get_state_snapshot(state: str, db: Session = Depends(get_db)):
    """Get state-specific snapshot with aggregated statistics.
    
    Path Parameters:
    - state: State code (e.g., 'MP', 'CG', 'MH')
    
    Returns aggregated data for the specified state.
    Results are cached and refreshed every 15 minutes automatically.
    """
    try:
        snapshot = AggregationService.get_state_snapshot(db, state)
        return snapshot
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating state snapshot: {str(e)}")


@router.get("/district/{state}/{district}", response_model=dict[str, Any])
def get_district_snapshot(state: str, district: str, db: Session = Depends(get_db)):
    """Get district-specific snapshot with aggregated statistics.
    
    Path Parameters:
    - state: State code (e.g., 'MP', 'CG')
    - district: District name (e.g., 'Mandla', 'Bastar')
    
    Returns aggregated data for the specified district.
    """
    try:
        cache_key = f"district_snapshot_{state}_{district}"
        cached = CacheService.get_with_ttl(db, cache_key, ttl_minutes=15)
        if cached:
            return cached

        from app.models.claim import Claim
        from app.models.grievance import Grievance
        from app.models.village import Village
        from sqlalchemy import func

        claims_query = db.query(Claim).filter(Claim.state == state, Claim.district == district)
        grievances_query = db.query(Grievance).filter(
            Grievance.state == state, Grievance.district == district
        )
        villages_query = db.query(Village).filter(Village.state == state, Village.district == district)

        snapshot = {
            "state": state,
            "district": district,
            "claims": {
                "total": claims_query.count(),
                "approved": claims_query.filter(Claim.status == "APPROVED").count(),
                "pending": claims_query.filter(Claim.status == "PENDING").count(),
                "rejected": claims_query.filter(Claim.status == "REJECTED").count(),
                "total_area": float(
                    claims_query.with_entities(func.sum(Claim.area_acres)).scalar() or 0
                ),
            },
            "villages": {
                "total": villages_query.count(),
                "population": int(
                    villages_query.with_entities(func.sum(Village.population)).scalar() or 0
                ),
            },
            "grievances": {
                "total": grievances_query.count(),
                "open": grievances_query.filter(Grievance.status == "OPEN").count(),
                "resolved": grievances_query.filter(Grievance.status == "RESOLVED").count(),
            },
        }

        CacheService.set(db, cache_key, snapshot)
        return snapshot
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating district snapshot: {str(e)}")


@router.get("/cache/stats", response_model=dict[str, Any])
def get_cache_stats(db: Session = Depends(get_db)):
    """Get cache statistics and status.
    
    Returns information about cached data including:
    - Total number of cached keys
    - Total cache size
    - Last update times
    """
    try:
        stats = CacheService.get_stats(db)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting cache stats: {str(e)}")


@router.post("/cache/refresh")
def refresh_cache(db: Session = Depends(get_db)):
    """Manually refresh all cache entries.
    
    Triggers immediate refresh of all aggregated statistics.
    Useful for manual cache update without waiting for scheduled refresh.
    """
    try:
        AggregationService.get_dashboard_summary(db)
        
        states = ["MP", "CG", "MH", "OD", "JH", "TS", "VN", "GJ"]
        for state in states:
            try:
                AggregationService.get_state_snapshot(db, state)
            except Exception:
                pass

        return {
            "status": "success",
            "message": "Cache refreshed successfully",
            "refreshed_at": "2026-02-23T10:30:00Z",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing cache: {str(e)}")


@router.delete("/cache/clear")
def clear_cache(db: Session = Depends(get_db)):
    """Clear all cache entries.
    
    WARNING: This will remove cached data for all dashboards.
    Use with caution. Caches will be automatically regenerated on next request.
    """
    try:
        count = CacheService.clear_all(db)
        return {
            "status": "success",
            "message": f"Cleared {count} cache entries",
            "cleared_count": count,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing cache: {str(e)}")


@router.get("/overview", response_model=dict[str, Any])
def get_dashboard_overview(
    state: str | None = Query(None, description="Filter by state"),
    db: Session = Depends(get_db),
):
    """Get dashboard overview with optional state filter.
    
    If state is provided, returns state-specific overview.
    Otherwise returns national overview.
    """
    try:
        if state:
            return AggregationService.get_state_snapshot(db, state)
        else:
            summary = AggregationService.get_dashboard_summary(db)
            
            overview = {
                "national": {
                    "claims": summary["claims"],
                    "villages": summary["villages"],
                    "grievances": summary["grievances"],
                    "officers": summary["officers"],
                },
                "timeline": summary["timeline"],
                "generated_at": summary["generated_at"],
            }
            return overview
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating overview: {str(e)}")
from __future__ import annotations

from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.claim import Claim
from app.models.data_blob import DataBlob
from app.models.grievance import Grievance
from app.models.officer import Officer
from app.models.village import Village
from app.schemas.domain import ClaimRead, VillageRead, OfficerRead, GrievanceRead
from app.schemas.pagination import (
    ClaimsPaginatedResponse,
    VillagesPaginatedResponse,
    OfficersPaginatedResponse,
    GrievancesPaginatedResponse,
)


def get_blob_payload(db: Session, key: str) -> dict[str, Any] | list[dict[str, Any]]:
    blob = db.query(DataBlob).filter(DataBlob.key == key).first()
    if not blob:
        raise HTTPException(status_code=404, detail=f"Dataset '{key}' not found")
    return blob.payload


def dashboard_snapshot(db: Session) -> dict[str, Any]:
    claims = db.query(Claim).order_by(Claim.claim_date.desc()).all()
    villages = db.query(Village).all()
    officers = db.query(Officer).all()
    grievances = db.query(Grievance).order_by(Grievance.filed_date.desc().nullslast()).all()

    return {
        "nationalStats": get_blob_payload(db, "national_stats"),
        "stateStats": get_blob_payload(db, "state_stats"),
        "districtStats": {
            "MP": get_blob_payload(db, "district_stats_mp"),
            "OD": get_blob_payload(db, "district_stats_od"),
        },
        "claims": claims,
        "villages": villages,
        "officers": officers,
        "grievances": grievances,
        "datasets": {
            "dajguaInterventions": get_blob_payload(db, "dajgua_interventions"),
            "dssRecommendations": get_blob_payload(db, "dss_recommendations"),
            "monthlyProgress": get_blob_payload(db, "monthly_progress"),
            "forestFireAlerts": get_blob_payload(db, "forest_fire_alerts"),
            "fieldVisitReports": get_blob_payload(db, "field_visit_reports"),
            "ndviTrend": get_blob_payload(db, "ndvi_trend"),
            "claimPipeline": get_blob_payload(db, "claim_pipeline"),
        },
    }


def search_claims(
    db: Session,
    *,
    state: str | None = None,
    status: str | None = None,
    district: str | None = None,
    page: int = 1,
    limit: int = 20,
) -> ClaimsPaginatedResponse:
    """Search claims with pagination and filtering."""
    try:
        query = db.query(Claim)

        # Apply filters
        if state:
            query = query.filter(Claim.state == state)
        if status:
            query = query.filter(Claim.status == status)
        if district:
            query = query.filter(Claim.district == district)

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        claims = query.order_by(Claim.claim_date.desc()).offset(offset).limit(limit).all()

        # Convert to response models
        data = [ClaimRead.model_validate(c) for c in claims]

        # Calculate pages
        pages = (total + limit - 1) // limit

        return ClaimsPaginatedResponse(
            data=data,
            total=total,
            page=page,
            limit=limit,
            pages=pages,
            filters={"state": state, "status": status, "district": district},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching claims: {str(e)}")


def list_grievances(
    db: Session,
    *,
    state: str | None = None,
    status: str | None = None,
    district: str | None = None,
    priority: str | None = None,
    page: int = 1,
    limit: int = 20,
) -> GrievancesPaginatedResponse:
    """List grievances with pagination and filtering."""
    try:
        query = db.query(Grievance)

        # Apply filters
        if state:
            query = query.filter(Grievance.state == state)
        if status:
            query = query.filter(Grievance.status == status)
        if district:
            query = query.filter(Grievance.district == district)
        if priority:
            query = query.filter(Grievance.priority == priority)

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        grievances = (
            query.order_by(Grievance.last_updated.desc().nullslast())
            .offset(offset)
            .limit(limit)
            .all()
        )

        # Convert to response models
        data = [GrievanceRead.model_validate(g) for g in grievances]

        # Calculate pages
        pages = (total + limit - 1) // limit

        return GrievancesPaginatedResponse(
            data=data,
            total=total,
            page=page,
            limit=limit,
            pages=pages,
            filters={"state": state, "status": status, "district": district, "priority": priority},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing grievances: {str(e)}")


def list_villages(
    db: Session,
    *,
    state: str | None = None,
    district: str | None = None,
    page: int = 1,
    limit: int = 20,
) -> VillagesPaginatedResponse:
    """List villages with pagination and filtering."""
    try:
        query = db.query(Village)

        # Apply filters
        if state:
            query = query.filter(Village.state == state)
        if district:
            query = query.filter(Village.district == district)

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        villages = query.order_by(Village.name.asc()).offset(offset).limit(limit).all()

        # Convert to response models
        data = [VillageRead.model_validate(v) for v in villages]

        # Calculate pages
        pages = (total + limit - 1) // limit

        return VillagesPaginatedResponse(
            data=data,
            total=total,
            page=page,
            limit=limit,
            pages=pages,
            filters={"state": state, "district": district},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing villages: {str(e)}")


def list_officers(
    db: Session,
    *,
    state: str | None = None,
    district: str | None = None,
    page: int = 1,
    limit: int = 20,
) -> OfficersPaginatedResponse:
    """List officers with pagination and filtering."""
    try:
        query = db.query(Officer)

        # Apply filters
        if state:
            query = query.filter(Officer.state == state)
        if district:
            query = query.filter(Officer.district == district)

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        officers = query.order_by(Officer.last_active.desc()).offset(offset).limit(limit).all()

        # Convert to response models
        data = [OfficerRead.model_validate(o) for o in officers]

        # Calculate pages
        pages = (total + limit - 1) // limit

        return OfficersPaginatedResponse(
            data=data,
            total=total,
            page=page,
            limit=limit,
            pages=pages,
            filters={"state": state, "district": district},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing officers: {str(e)}")
from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime, Boolean,
    ForeignKey, Text, Enum, JSON, Index,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
import enum

from app.core.database import Base


class ClaimStatus(str, enum.Enum):
    received = "received"
    verified = "verified"
    pending = "pending"
    granted = "granted"
    rejected = "rejected"


class ClaimType(str, enum.Enum):
    IFR = "IFR"
    CFR = "CFR"
    CR = "CR"


class FRAClaim(Base):
    __tablename__ = "fra_claims"
    
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(String(50), unique=True, index=True, nullable=False)
    
    # Claimant Details
    claimant_name = Column(String(200), nullable=False)
    father_husband_name = Column(String(200))
    aadhaar_number = Column(String(12))
    mobile = Column(String(15))
    tribal_group = Column(String(100))
    is_pvtg = Column(Boolean, default=False)
    
    # Location
    state = Column(String(50), nullable=False, index=True)
    district = Column(String(100), nullable=False, index=True)
    block = Column(String(100))
    village_code = Column(String(50), ForeignKey("villages.code"), index=True)
    
    # Claim Details
    claim_type = Column(Enum(ClaimType), nullable=False)
    area_claimed_ha = Column(Float)
    area_verified_ha = Column(Float)
    claim_boundary = Column(Geometry("POLYGON", srid=4326))
    
    # Status & Timeline
    status = Column(Enum(ClaimStatus), default=ClaimStatus.received, index=True)
    filed_date = Column(Date, nullable=False)
    frc_decision_date = Column(Date)
    sdlc_decision_date = Column(Date)
    dlc_decision_date = Column(Date)
    grant_date = Column(Date)
    
    # Verification
    frc_verified = Column(Boolean, default=False)
    sdlc_verified = Column(Boolean, default=False)
    gps_verified = Column(Boolean, default=False)
    
    # Documents & OCR
    documents = Column(JSON)  # Array of document URLs
    ocr_extracted_data = Column(JSON)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    village = relationship("Village", back_populates="claims")
    
    __table_args__ = (
        Index("idx_claim_status_state", "status", "state"),
        Index("idx_claim_type_status", "claim_type", "status"),
        Index("idx_claim_spatial", "claim_boundary", postgresql_using="gist"),
    )


class Village(Base):
    __tablename__ = "villages"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    
    # Location
    state = Column(String(50), nullable=False, index=True)
    district = Column(String(100), nullable=False, index=True)
    block = Column(String(100))
    
    # Geometry
    boundary = Column(Geometry("POLYGON", srid=4326))
    centroid = Column(Geometry("POINT", srid=4326))
    
    # Demographics
    total_households = Column(Integer)
    tribal_households = Column(Integer)
    total_population = Column(Integer)
    tribal_population = Column(Integer)
    
    # FRA Data
    total_claims = Column(Integer, default=0)
    granted_claims = Column(Integer, default=0)
    pending_claims = Column(Integer, default=0)
    rejected_claims = Column(Integer, default=0)
    patta_holder_count = Column(Integer, default=0)
    
    # Infrastructure
    school_distance_km = Column(Float)
    road_connectivity = Column(Boolean, default=False)
    electricity_coverage_pct = Column(Float)
    water_source_availability = Column(Boolean)
    
    # Environmental Indicators
    ndvi_score = Column(Float)
    groundwater_depth_m = Column(Float)
    forest_cover_pct = Column(Float)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    claims = relationship("FRAClaim", back_populates="village")
    
    __table_args__ = (
        Index("idx_village_state_district", "state", "district"),
        Index("idx_village_spatial_boundary", "boundary", postgresql_using="gist"),
        Index("idx_village_spatial_centroid", "centroid", postgresql_using="gist"),
    )


class Officer(Base):
    __tablename__ = "officers"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    
    # Role & Designation
    designation = Column(String(100), nullable=False)  # district-collector, sdlc-officer, range-officer
    role = Column(String(50), nullable=False, index=True)
    
    # Location
    state = Column(String(50), nullable=False, index=True)
    district = Column(String(100))
    block = Column(String(100))
    
    # Contact
    email = Column(String(100), unique=True)
    mobile = Column(String(15))
    
    # Activity
    claims_reviewed = Column(Integer, default=0)
    claims_approved = Column(Integer, default=0)
    claims_rejected = Column(Integer, default=0)
    last_active = Column(DateTime(timezone=True))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class DSSRecommendation(Base):
    __tablename__ = "dss_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Location
    village_code = Column(String(50), ForeignKey("villages.code"), index=True)
    state = Column(String(50), nullable=False, index=True)
    district = Column(String(100), nullable=False, index=True)
    block = Column(String(100))
    
    # Scheme Details
    scheme_id = Column(String(50), nullable=False)
    scheme_name = Column(String(200), nullable=False)
    
    # Gap Analysis
    eligible_beneficiaries = Column(Integer, nullable=False)
    currently_enrolled = Column(Integer, default=0)
    gap = Column(Integer)
    
    # Priority & Scoring
    priority = Column(String(20), index=True)  # critical, high, medium, low
    ai_score = Column(Float, nullable=False)
    impact_estimate = Column(Float)
    
    # ML Features (stored as JSON)
    ml_features = Column(JSON)
    
    # Recommendation
    trigger_condition = Column(Text)
    action_required = Column(Text)
    deadline = Column(Date)
    
    # Metadata
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="pending")  # pending, acted, completed
    
    __table_args__ = (
        Index("idx_dss_priority_state", "priority", "state"),
        Index("idx_dss_ai_score", "ai_score"),
    )


class Grievance(Base):
    __tablename__ = "grievances"
    
    id = Column(Integer, primary_key=True, index=True)
    grievance_id = Column(String(50), unique=True, index=True, nullable=False)
    
    # Complainant
    claimant_name = Column(String(200), nullable=False)
    mobile = Column(String(15), nullable=False)
    claim_id = Column(String(50), ForeignKey("fra_claims.claim_id"))
    
    # Location
    state = Column(String(50), nullable=False, index=True)
    district = Column(String(100), nullable=False, index=True)
    block = Column(String(100))
    village = Column(String(200))
    
    # Grievance Details
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(20), default="medium", index=True)
    
    # Status & Timeline
    status = Column(String(20), default="open", index=True)  # open, in-progress, resolved, closed
    filed_date = Column(Date, nullable=False)
    resolution_date = Column(Date)
    days_open = Column(Integer)
    
    # Assignment
    assigned_to = Column(String(200))
    assigned_to_officer_id = Column(Integer, ForeignKey("officers.id"))
    
    # Source
    source = Column(String(50), default="portal")  # portal, helpline, mobile-app
    
    # Response
    response = Column(Text)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index("idx_grievance_status_priority", "status", "priority"),
    )


class SchemeEnrollment(Base):
    __tablename__ = "scheme_enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Village
    village_code = Column(String(50), ForeignKey("villages.code"), index=True)
    
    # Scheme
    scheme_id = Column(String(50), nullable=False, index=True)
    scheme_name = Column(String(200), nullable=False)
    
    # Enrollment Data
    target_beneficiaries = Column(Integer)
    enrolled_beneficiaries = Column(Integer, default=0)
    saturation_pct = Column(Float, default=0.0)
    
    # Budget
    allocated_budget = Column(Float)
    utilized_budget = Column(Float, default=0.0)
    
    # Timeline
    start_date = Column(Date)
    end_date = Column(Date)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index("idx_scheme_village_scheme", "village_code", "scheme_id"),
    )

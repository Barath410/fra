from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List
from enum import Enum


class ClaimStatusEnum(str, Enum):
    received = "received"
    verified = "verified"
    pending = "pending"
    granted = "granted"
    rejected = "rejected"


class ClaimTypeEnum(str, Enum):
    IFR = "IFR"
    CFR = "CFR"
    CR = "CR"


# FRA Claim Schemas
class FRAClaimBase(BaseModel):
    claim_id: str
    claimant_name: str
    father_husband_name: Optional[str] = None
    mobile: Optional[str] = None
    tribal_group: Optional[str] = None
    is_pvtg: bool = False
    state: str
    district: str
    block: Optional[str] = None
    village_code: Optional[str] = None
    claim_type: ClaimTypeEnum
    area_claimed_ha: Optional[float] = None
    filed_date: date


class FRAClaimCreate(FRAClaimBase):
    pass


class FRAClaimUpdate(BaseModel):
    status: Optional[ClaimStatusEnum] = None
    area_verified_ha: Optional[float] = None
    frc_verified: Optional[bool] = None
    sdlc_verified: Optional[bool] = None
    gps_verified: Optional[bool] = None


class FRAClaim(FRAClaimBase):
    id: int
    status: ClaimStatusEnum
    area_verified_ha: Optional[float] = None
    grant_date: Optional[date] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Village Schemas
class VillageBase(BaseModel):
    code: str
    name: str
    state: str
    district: str
    block: Optional[str] = None
    total_households: Optional[int] = None
    tribal_households: Optional[int] = None


class VillageCreate(VillageBase):
    pass


class Village(VillageBase):
    id: int
    total_claims: int = 0
    granted_claims: int = 0
    pending_claims: int = 0
    patta_holder_count: int = 0
    ndvi_score: Optional[float] = None
    school_distance_km: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Officer Schemas
class OfficerBase(BaseModel):
    code: str
    name: str
    designation: str
    role: str
    state: str
    district: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None


class OfficerCreate(OfficerBase):
    pass


class Officer(OfficerBase):
    id: int
    claims_reviewed: int = 0
    claims_approved: int = 0
    last_active: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# DSS Recommendation Schemas
class DSSRecommendationBase(BaseModel):
    village_code: str
    state: str
    district: str
    scheme_id: str
    scheme_name: str
    eligible_beneficiaries: int
    currently_enrolled: int = 0
    priority: str
    ai_score: float
    trigger_condition: str
    action_required: str


class DSSRecommendationCreate(DSSRecommendationBase):
    pass


class DSSRecommendation(DSSRecommendationBase):
    id: int
    gap: Optional[int] = None
    generated_at: datetime
    status: str = "pending"

    class Config:
        from_attributes = True


# Grievance Schemas
class GrievanceBase(BaseModel):
    grievance_id: str
    claimant_name: str
    mobile: str
    state: str
    district: str
    village: str
    category: str
    description: str
    priority: str = "medium"


class GrievanceCreate(GrievanceBase):
    pass


class GrievanceUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    response: Optional[str] = None


class Grievance(GrievanceBase):
    id: int
    status: str = "open"
    filed_date: date
    days_open: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Scheme Enrollment Schemas
class SchemeEnrollmentBase(BaseModel):
    village_code: str
    scheme_id: str
    scheme_name: str
    target_beneficiaries: int
    enrolled_beneficiaries: int = 0


class SchemeEnrollmentCreate(SchemeEnrollmentBase):
    pass


class SchemeEnrollment(SchemeEnrollmentBase):
    id: int
    saturation_pct: float = 0.0
    created_at: datetime

    class Config:
        from_attributes = True


# Analytics Response Schemas
class StateStats(BaseModel):
    state: str
    total_claims: int
    granted: int
    pending: int
    rejected: int
    grant_rate: float


class DistrictStats(BaseModel):
    district: str
    state: str
    total_claims: int
    granted: int
    pending: int
    villages: int


class DashboardStats(BaseModel):
    total_claims: int
    granted_claims: int
    pending_claims: int
    rejected_claims: int
    total_villages: int
    total_area_granted_ha: float
    states_covered: int
    districts_covered: int

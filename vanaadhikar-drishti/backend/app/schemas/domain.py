from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, computed_field


class ORMModel(BaseModel):
  model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ClaimRead(ORMModel):
  id: str = Field(alias="claim_id")
  claimantName: str = Field(alias="claimant_name")
  claimantAadhaar: str | None = Field(default=None, alias="claimant_aadhaar")
  villageName: str = Field(alias="village_name")
  villageCode: str = Field(alias="village_code")
  gramPanchayat: str | None = Field(default=None, alias="gram_panchayat")
  block: str | None = None
  district: str
  state: str
  claimType: str = Field(alias="claim_type")
  formNumber: str | None = Field(default=None, alias="form_number")
  areaAcres: float = Field(alias="area_acres")
  surveyKhasraNo: str | None = Field(default=None, alias="survey_khasra_no")
  claimDate: date = Field(alias="claim_date")
  verificationDate: date | None = Field(default=None, alias="verification_date")
  decisionDate: date | None = Field(default=None, alias="decision_date")
  status: str
  rejectionReason: str | None = Field(default=None, alias="rejection_reason")
  patteNumber: str | None = Field(default=None, alias="patte_number")
  patteIssuedDate: date | None = Field(default=None, alias="patte_issued_date")
  tribalGroup: str | None = Field(default=None, alias="tribal_group")
  isPVTG: bool = Field(alias="is_pvtg")
  notes: str | None = None
  gpsLat: float | None = Field(default=None, alias="gps_lat")
  gpsLng: float | None = Field(default=None, alias="gps_lng")
  boundaryGeojson: dict[str, Any] | None = Field(default=None, alias="boundary_geojson")
  scannedDocUrl: str | None = Field(default=None, alias="scanned_doc_url")
  ocrData: dict[str, Any] | None = Field(default=None, alias="ocr_data")
  assignedOfficerId: str | None = Field(default=None, alias="assigned_officer_id")
  created_at: datetime
  updated_at: datetime

  @computed_field  # type: ignore[misc]
  @property
  def gpsCoordinates(self) -> dict[str, float] | None:
    if self.gpsLat is None or self.gpsLng is None:
      return None
    return {"lat": self.gpsLat, "lng": self.gpsLng}


class VillageRead(ORMModel):
  code: str
  name: str
  gramPanchayat: str | None = Field(default=None, alias="gram_panchayat")
  block: str | None = None
  district: str
  state: str
  population: int | None = None
  stPopulation: int | None = Field(default=None, alias="st_population")
  totalHouseholds: int | None = Field(default=None, alias="total_households")
  pvtgPresent: bool = Field(alias="pvtg_present")
  tribalGroups: list[str] | None = Field(default=None, alias="tribal_groups")
  totalClaims: int = Field(alias="total_claims")
  grantedClaims: int = Field(alias="granted_claims")
  pendingClaims: int = Field(alias="pending_claims")
  rejectedClaims: int = Field(alias="rejected_claims")
  ifrGrantedArea: float = Field(alias="ifr_granted_area")
  cfrGrantedArea: float = Field(alias="cfr_granted_area")
  crGrantedArea: float = Field(alias="cr_granted_area")
  saturationScore: int = Field(alias="saturation_score")
  gpsLat: float | None = Field(default=None, alias="gps_lat")
  gpsLng: float | None = Field(default=None, alias="gps_lng")
  assets: dict[str, Any] | None = None
  schemeEnrollments: list[dict[str, Any]] | None = Field(default=None, alias="scheme_enrollments")
  lastSatelliteUpdate: str | None = Field(default=None, alias="last_satellite_update")
  created_at: datetime
  updated_at: datetime

  @computed_field  # type: ignore[misc]
  @property
  def gpsCenter(self) -> dict[str, float] | None:
    if self.gpsLat is None or self.gpsLng is None:
      return None
    return {"lat": self.gpsLat, "lng": self.gpsLng}


class OfficerRead(ORMModel):
  id: str = Field(alias="officer_id")
  name: str
  designation: str
  state: str | None = None
  district: str | None = None
  block: str | None = None
  mobile: str
  email: str
  lastActive: datetime = Field(alias="last_active")
  totalClaimsHandled: int = Field(alias="total_claims_handled")
  pendingActions: int = Field(alias="pending_actions")
  created_at: datetime
  updated_at: datetime


class GrievanceRead(ORMModel):
  id: str = Field(alias="grievance_id")
  claimantName: str = Field(alias="claimant_name")
  claimId: str | None = Field(default=None, alias="claim_id")
  villageName: str = Field(alias="village_name")
  block: str | None = None
  district: str
  state: str
  category: str
  status: str
  priority: str
  assignedOfficerId: str | None = Field(default=None, alias="assigned_officer_id")
  assignedTo: str | None = Field(default=None, alias="assigned_to")
  description: str
  filedDate: date | None = Field(default=None, alias="filed_date")
  lastUpdated: datetime | None = Field(default=None, alias="last_updated")
  daysOpen: int = Field(alias="days_open")
  resolution: str | None = None
  source: str | None = None
  channel: str | None = None
  mobile: str | None = None
  createdAt: datetime = Field(alias="created_at")
  updatedAt: datetime = Field(alias="updated_at")


class GrievanceCreate(BaseModel):
  grievance_id: str
  claimant_name: str
  claim_id: str | None = None
  village_name: str
  block: str | None = None
  district: str
  state: str
  category: str
  status: str
  priority: str
  description: str
  channel: str | None = None
  mobile: str | None = None
  source: str | None = None
  assigned_officer_id: str | None = None
  filed_date: date | None = None
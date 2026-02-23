from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.mysql import BIGINT, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class Claim(TimestampMixin, Base):
  __tablename__ = "claims"
  __table_args__ = (
    Index("idx_claim_state", "state"),
    Index("idx_claim_district", "district"),
    Index("idx_claim_village", "village_code"),
    Index("idx_claim_status", "status"),
  )

  id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
  claim_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
  claimant_name: Mapped[str] = mapped_column(String(255), nullable=False)
  claimant_aadhaar: Mapped[Optional[str]] = mapped_column(String(32))
  village_name: Mapped[str] = mapped_column(String(255), nullable=False)
  village_code: Mapped[str] = mapped_column(String(64), nullable=False)
  gram_panchayat: Mapped[Optional[str]] = mapped_column(String(255))
  block: Mapped[Optional[str]] = mapped_column(String(255))
  district: Mapped[str] = mapped_column(String(255), nullable=False)
  state: Mapped[str] = mapped_column(String(8), nullable=False)
  claim_type: Mapped[str] = mapped_column(String(8), nullable=False)
  form_number: Mapped[Optional[str]] = mapped_column(String(32))
  area_acres: Mapped[float] = mapped_column(Float, nullable=False)
  survey_khasra_no: Mapped[Optional[str]] = mapped_column(String(64))
  claim_date: Mapped[datetime] = mapped_column(Date, nullable=False)
  verification_date: Mapped[Optional[datetime]] = mapped_column(Date)
  decision_date: Mapped[Optional[datetime]] = mapped_column(Date)
  status: Mapped[str] = mapped_column(String(32), nullable=False)
  rejection_reason: Mapped[Optional[str]] = mapped_column(String(1000))
  patte_number: Mapped[Optional[str]] = mapped_column(String(128))
  patte_issued_date: Mapped[Optional[datetime]] = mapped_column(Date)
  tribal_group: Mapped[Optional[str]] = mapped_column(String(128))
  is_pvtg: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
  notes: Mapped[Optional[str]] = mapped_column(String(512))
  gps_lat: Mapped[Optional[float]] = mapped_column(Float)
  gps_lng: Mapped[Optional[float]] = mapped_column(Float)
  boundary_geojson: Mapped[Optional[dict]] = mapped_column(JSON)
  scanned_doc_url: Mapped[Optional[str]] = mapped_column(String(512))
  ocr_data: Mapped[Optional[dict]] = mapped_column(JSON)
  assigned_officer_id: Mapped[Optional[str]] = mapped_column(String(64))

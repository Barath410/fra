from __future__ import annotations

from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.dialects.mysql import BIGINT, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class Village(TimestampMixin, Base):
  __tablename__ = "villages"

  id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
  code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
  name: Mapped[str] = mapped_column(String(255), nullable=False)
  gram_panchayat: Mapped[str | None] = mapped_column(String(255))
  block: Mapped[str | None] = mapped_column(String(255))
  district: Mapped[str] = mapped_column(String(255), nullable=False)
  state: Mapped[str] = mapped_column(String(8), nullable=False, index=True)
  population: Mapped[int | None] = mapped_column(Integer)
  st_population: Mapped[int | None] = mapped_column(Integer)
  total_households: Mapped[int | None] = mapped_column(Integer)
  pvtg_present: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
  tribal_groups: Mapped[list[str] | None] = mapped_column(JSON)
  total_claims: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
  granted_claims: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
  pending_claims: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
  rejected_claims: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
  ifr_granted_area: Mapped[float] = mapped_column(Float, default=0, nullable=False)
  cfr_granted_area: Mapped[float] = mapped_column(Float, default=0, nullable=False)
  cr_granted_area: Mapped[float] = mapped_column(Float, default=0, nullable=False)
  saturation_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
  gps_lat: Mapped[float | None] = mapped_column(Float)
  gps_lng: Mapped[float | None] = mapped_column(Float)
  assets: Mapped[dict | None] = mapped_column(JSON)
  scheme_enrollments: Mapped[list[dict] | None] = mapped_column(JSON)
  last_satellite_update: Mapped[str | None] = mapped_column(String(64))

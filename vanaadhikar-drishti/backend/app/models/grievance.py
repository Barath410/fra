from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Date, DateTime, Integer, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class Grievance(TimestampMixin, Base):
  __tablename__ = "grievances"

  id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
  grievance_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
  claimant_name: Mapped[str] = mapped_column(String(255), nullable=False)
  claim_id: Mapped[Optional[str]] = mapped_column(String(64))
  village_name: Mapped[str] = mapped_column(String(255), nullable=False)
  block: Mapped[Optional[str]] = mapped_column(String(255))
  district: Mapped[str] = mapped_column(String(255), nullable=False)
  state: Mapped[str] = mapped_column(String(8), nullable=False)
  category: Mapped[str] = mapped_column(String(64), nullable=False)
  status: Mapped[str] = mapped_column(String(32), nullable=False)
  priority: Mapped[str] = mapped_column(String(16), nullable=False)
  assigned_officer_id: Mapped[Optional[str]] = mapped_column(String(64))
  assigned_to: Mapped[Optional[str]] = mapped_column(String(255))
  description: Mapped[str] = mapped_column(String(1000), nullable=False)
  filed_date: Mapped[Optional[datetime]] = mapped_column(Date)
  last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime)
  days_open: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
  resolution: Mapped[Optional[str]] = mapped_column(String(1000))
  source: Mapped[Optional[str]] = mapped_column(String(64))
  channel: Mapped[Optional[str]] = mapped_column(String(64))
  mobile: Mapped[Optional[str]] = mapped_column(String(32))

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class Officer(TimestampMixin, Base):
  __tablename__ = "officers"

  id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
  officer_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
  name: Mapped[str] = mapped_column(String(255), nullable=False)
  designation: Mapped[str] = mapped_column(String(64), nullable=False)
  state: Mapped[Optional[str]] = mapped_column(String(8))
  district: Mapped[Optional[str]] = mapped_column(String(255))
  block: Mapped[Optional[str]] = mapped_column(String(255))
  mobile: Mapped[str] = mapped_column(String(32), nullable=False)
  email: Mapped[str] = mapped_column(String(255), nullable=False)
  last_active: Mapped[datetime] = mapped_column(DateTime, nullable=False)
  total_claims_handled: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
  pending_actions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

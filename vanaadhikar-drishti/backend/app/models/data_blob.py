from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.mysql import BIGINT, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class DataBlob(Base):
  __tablename__ = "data_blobs"

  id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
  key: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
  description: Mapped[str | None] = mapped_column(String(512))
  payload: Mapped[dict] = mapped_column(JSON, nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
  updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
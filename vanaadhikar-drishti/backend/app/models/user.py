from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class User(TimestampMixin, Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
  email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
  name: Mapped[str] = mapped_column(String(255), nullable=False)
  picture: Mapped[str | None] = mapped_column(String(512))
  provider: Mapped[str] = mapped_column(String(32), nullable=False, default="google")
  last_login: Mapped[datetime | None] = mapped_column(DateTime)

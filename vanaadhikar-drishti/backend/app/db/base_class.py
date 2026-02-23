from __future__ import annotations

from typing import Any

from sqlalchemy.orm import DeclarativeBase, declared_attr


class CustomBase(DeclarativeBase):
  __abstract__ = True

  @declared_attr.directive
  def __tablename__(cls) -> str:  # type: ignore[misc]
    return cls.__name__.lower()


Base = CustomBase

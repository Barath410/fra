from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
  from app.models.master_document import MasterDocument


class DocTitleCommunityForestResources(TimestampMixin, Base):
  __tablename__ = "doc_title_community_forest_resources"
  __table_args__ = (
    Index("idx_dtcfrs_state", "state"),
    Index("idx_dtcfrs_district", "district"),
    Index("idx_dtcfrs_village", "village"),
  )

  id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
  document_id: Mapped[int] = mapped_column(
    BIGINT(unsigned=True), ForeignKey("master_documents.id", ondelete="CASCADE"), unique=True
  )
  state: Mapped[str | None] = mapped_column(String(255))
  district: Mapped[str | None] = mapped_column(String(255))
  tehsil_taluka: Mapped[str | None] = mapped_column(String(255))
  village: Mapped[str | None] = mapped_column(String(255))
  gram_panchayat: Mapped[str | None] = mapped_column(String(255))
  gram_sabha: Mapped[str | None] = mapped_column(String(255))
  community_type_scheduled_tribe: Mapped[str | None] = mapped_column(String(255))
  community_type_other_tfd: Mapped[str | None] = mapped_column(String(255))
  community_type_both: Mapped[str | None] = mapped_column(String(255))
  khasra_compartment_number: Mapped[str | None] = mapped_column(String(100))
  boundary_description: Mapped[str | None] = mapped_column(Text)
  customary_boundary: Mapped[str | None] = mapped_column(Text)

  document: Mapped["MasterDocument"] = relationship(back_populates="title_community_forest_resources")

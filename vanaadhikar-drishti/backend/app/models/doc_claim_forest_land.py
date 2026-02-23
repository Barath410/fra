from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
  from app.models.master_document import MasterDocument


class DocClaimForestLand(TimestampMixin, Base):
  __tablename__ = "doc_claim_forest_land"
  __table_args__ = (
    Index("idx_dcf_land_state", "state"),
    Index("idx_dcf_land_district", "district"),
    Index("idx_dcf_land_village", "village"),
  )

  id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
  document_id: Mapped[int] = mapped_column(
    BIGINT(unsigned=True), ForeignKey("master_documents.id", ondelete="CASCADE"), unique=True
  )
  claimant_name: Mapped[str | None] = mapped_column(String(255))
  father_mother_name: Mapped[str | None] = mapped_column(String(255))
  spouse_name: Mapped[str | None] = mapped_column(String(255))
  address_full: Mapped[str | None] = mapped_column(Text)
  state: Mapped[str | None] = mapped_column(String(255))
  district: Mapped[str | None] = mapped_column(String(255))
  tehsil_taluka: Mapped[str | None] = mapped_column(String(255))
  village: Mapped[str | None] = mapped_column(String(255))
  gram_panchayat: Mapped[str | None] = mapped_column(String(255))
  gram_sabha: Mapped[str | None] = mapped_column(String(255))
  category_scheduled_tribe: Mapped[str | None] = mapped_column(String(255))
  category_other_traditional_forest_dweller: Mapped[str | None] = mapped_column(String(255))
  family_member_name: Mapped[str | None] = mapped_column(String(255))
  family_member_age: Mapped[str | None] = mapped_column(String(100))
  dependent_name: Mapped[str | None] = mapped_column(String(255))
  land_extent_habitation: Mapped[str | None] = mapped_column(String(100))
  land_extent_self_cultivation: Mapped[str | None] = mapped_column(String(100))
  land_extent_forest_village: Mapped[str | None] = mapped_column(String(100))
  disputed_land_description: Mapped[str | None] = mapped_column(Text)
  existing_pattas_leases_grants: Mapped[str | None] = mapped_column(Text)
  rehabilitation_land: Mapped[str | None] = mapped_column(Text)
  displaced_from_land: Mapped[str | None] = mapped_column(Text)
  other_traditional_right: Mapped[str | None] = mapped_column(Text)
  evidence_item: Mapped[str | None] = mapped_column(Text)
  other_information: Mapped[str | None] = mapped_column(Text)

  document: Mapped["MasterDocument"] = relationship(back_populates="claim_forest_land")

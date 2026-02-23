from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
  from app.models.master_document import MasterDocument


class DocClaimCommunityRights(TimestampMixin, Base):
  __tablename__ = "doc_claim_community_rights"
  __table_args__ = (
    Index("idx_dccr_state", "state"),
    Index("idx_dccr_district", "district"),
    Index("idx_dccr_village", "village"),
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
  community_type_fdst: Mapped[str | None] = mapped_column(String(255))
  community_type_otfd: Mapped[str | None] = mapped_column(String(255))
  community_right_nistar: Mapped[str | None] = mapped_column(Text)
  right_minor_forest_produce: Mapped[str | None] = mapped_column(Text)
  community_right_resource_use: Mapped[str | None] = mapped_column(Text)
  community_right_grazing: Mapped[str | None] = mapped_column(Text)
  community_right_nomadic_pastoralist_access: Mapped[str | None] = mapped_column(Text)
  community_tenure_habitat: Mapped[str | None] = mapped_column(Text)
  community_right_biodiversity_ipr_tk: Mapped[str | None] = mapped_column(Text)
  other_traditional_right: Mapped[str | None] = mapped_column(Text)
  evidence_item: Mapped[str | None] = mapped_column(Text)
  other_information: Mapped[str | None] = mapped_column(Text)

  document: Mapped["MasterDocument"] = relationship(back_populates="claim_community_rights")

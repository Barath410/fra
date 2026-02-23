from __future__ import annotations

from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.mysql import BIGINT, LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
  from app.models.doc_claim_forest_land import DocClaimForestLand
  from app.models.doc_claim_community_rights import DocClaimCommunityRights
  from app.models.doc_claim_community_forest_resource import DocClaimCommunityForestResource
  from app.models.doc_title_under_occupation import DocTitleUnderOccupation
  from app.models.doc_title_community_forest_rights import DocTitleCommunityForestRights
  from app.models.doc_title_community_forest_resources import DocTitleCommunityForestResources


class MasterDocument(Base):
  __tablename__ = "master_documents"

  id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, index=True)
  file_name: Mapped[str] = mapped_column(String(255), nullable=False)
  file_path: Mapped[str] = mapped_column(Text, nullable=False)
  document_type: Mapped[str | None] = mapped_column(String(100))
  language: Mapped[str | None] = mapped_column(String(20))
  upload_timestamp: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), default=datetime.utcnow, nullable=False
  )
  processing_status: Mapped[str] = mapped_column(String(50), default="PENDING", nullable=False)
  raw_text: Mapped[str | None] = mapped_column(LONGTEXT)
  extracted_payload: Mapped[str | None] = mapped_column(LONGTEXT)

  claim_forest_land: Mapped["DocClaimForestLand"] = relationship(back_populates="document")
  claim_community_rights: Mapped["DocClaimCommunityRights"] = relationship(back_populates="document")
  claim_community_forest_resource: Mapped["DocClaimCommunityForestResource"] = relationship(back_populates="document")
  title_under_occupation: Mapped["DocTitleUnderOccupation"] = relationship(back_populates="document")
  title_community_forest_rights: Mapped["DocTitleCommunityForestRights"] = relationship(back_populates="document")
  title_community_forest_resources: Mapped["DocTitleCommunityForestResources"] = relationship(back_populates="document")

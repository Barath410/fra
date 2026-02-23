from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
  document_type: str | None = Field(default=None, description="Detected or user provided type")
  language: str | None = Field(default=None, max_length=20)


class RuleBasedPayload(BaseModel):
  template_id: str
  entities: dict[str, Any]


class DocumentUploadResponse(BaseModel):
  document_id: int
  document_type: str | None
  processing_status: str
  template_id: str | None
  created_at: datetime


class MasterDocumentRead(BaseModel):
  id: int
  file_name: str
  file_path: str
  document_type: str | None
  language: str | None
  upload_timestamp: datetime
  processing_status: str

  class Config:
    from_attributes = True

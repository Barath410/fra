from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.schemas.document import DocumentUploadResponse, DocumentMetadata
from app.services.document_service import document_ingestion_service

router = APIRouter(tags=["documents"])


@router.post("/upload-document", response_model=DocumentUploadResponse)
def upload_document(
  file: UploadFile = File(...),
  document_type: str | None = Form(default=None),
  language: str | None = Form(default=None),
  db: Session = Depends(get_db),
):
  size_limit = settings.max_upload_mb * 1024 * 1024
  if hasattr(file.file, "seek"):
    current_pos = file.file.tell()
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(current_pos)
    if file_size > size_limit:
      raise HTTPException(status_code=413, detail="File too large")

  metadata = DocumentMetadata(document_type=document_type, language=language)
  return document_ingestion_service.ingest(db=db, file=file, metadata=metadata)

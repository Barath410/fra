from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os

router = APIRouter()


@router.post("/extract")
async def extract_document(file: UploadFile = File(...)):
    """
    OCR document extraction endpoint
    Upload a document and extract text + named entities
    """
    # Verify file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are supported")
    
    # TODO: Implement actual OCR processing with Tesseract + spaCy
    # For now, return mock response
    
    return {
        "status": "completed",
        "confidence": 0.942,
        "extracted_fields": {
            "claimant_name": "Ramesh Kumar Bhil",
            "father_name": "Sohan Lal",
            "village": "Bichhiya",
            "district": "Mandla",
            "area_claimed": "2.4 ha",
            "date": "15-Jan-2024",
        },
        "ner_entities": [
            {"text": "Ramesh Kumar Bhil", "type": "PERSON", "verified": True},
            {"text": "Bichhiya", "type": "LOCATION", "verified": True},
            {"text": "Mandla", "type": "LOCATION", "verified": True},
            {"text": "2.4 ha", "type": "AREA", "verified": False},
        ],
        "flags": ["Low signature quality", "Date format inconsistent"],
    }


@router.post("/batch-extract")
async def batch_extract(files: List[UploadFile] = File(...)):
    """
    Batch OCR processing for multiple documents
    """
    results = []
    for file in files:
        if not file.content_type.startswith("image/"):
            results.append({"filename": file.filename, "status": "failed", "error": "Invalid file type"})
            continue
        
        # TODO: Process each file with OCR
        results.append({
            "filename": file.filename,
            "status": "completed",
            "confidence": 0.94,
        })
    
    return {"processed": len(results), "results": results}

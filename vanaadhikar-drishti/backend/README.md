# Vanaadhikar Drishti – Document Processing Backend

This service ingests multilingual legal documents, extracts text (OCR if required), pushes the text through the existing `rule_based_recog` pipeline, and persists structured entities into MySQL. It is designed for production workloads with FastAPI, SQLAlchemy, and Alembic.

## Folder Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   └── documents.py       # POST /upload-document
│   │   └── router.py
│   ├── core/config.py             # Pydantic settings
│   ├── db/
│   │   ├── base.py
│   │   ├── base_class.py
│   │   └── session.py
│   ├── models/                    # Master + 6 entity tables
│   ├── schemas/document.py        # Pydantic schemas
│   └── services/document_service.py
├── alembic/                       # Migration environment
├── docs/schema.sql                # Hand-written schema (reference)
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml / requirements.txt
└── README.md
```

## Prerequisites

- Python 3.11+
- Tesseract OCR + poppler (installed automatically inside Docker image)
- Access to `rule_based_recog/` at repository root
- MySQL 8 (Docker compose sets it up automatically)

## Environment Variables

Copy `.env.example` → `.env` and adjust if needed.

```
APP_ENV=production
DATABASE_URL=mysql+pymysql://root:Lakpra849@@mysql:3306/fra_documents?charset=utf8mb4
UPLOAD_DIR=uploads
ENABLE_TRANSLATION=true
RULE_BASED_RECOG_DIR=../rule_based_recog
OCR_LANGUAGE_HINT=eng+hin
```

## Running Locally (Docker)

```bash
cd backend
cp .env.example .env
docker compose up --build
```

- API available at http://localhost:8000
- MySQL exposed on port 3306 (user `root`, password `Lakpra849@`)
- Uploads stored inside `../uploads`

## Running Locally (without Docker)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Ensure MySQL is running and update `DATABASE_URL` accordingly.

## Database Migrations

1. Autogenerate migrations after updating models:
   ```bash
   alembic revision --autogenerate -m "init"
   ```
2. Apply migrations:
   ```bash
   alembic upgrade head
   ```

## API Contract

### POST /api/v1/documents/upload-document

- Accepts multipart/form-data
  - `file`: required UploadFile (PDF, DOCX, TXT, PNG, etc.)
  - `document_type`: optional hint
  - `language`: optional BCP47 tag
- Response: `DocumentUploadResponse`

```json
{
  "document_id": 12,
  "document_type": "DOC_CLAIM_FOREST_LAND",
  "processing_status": "COMPLETED",
  "template_id": "DOC_CLAIM_FOREST_LAND",
  "created_at": "2026-02-23T09:05:31.000Z"
}
```

### Processing Flow

1. Save file in `/uploads` with slugified name.
2. Extract text:
   - PDF → `pdfplumber`, fallback to OCR
   - Images → Tesseract OCR (`pytesseract`)
   - DOC/DOCX → `python-docx`
   - TXT → read directly
3. Send text to `rule_based_recog/pipeline_ocr_extract_translate.py`
   - `--translate` flag controlled by `ENABLE_TRANSLATION`
4. Parse JSON `{template_id, entities}` output
5. Insert master row → determine template model → insert entity row in transaction
6. Commit results or mark failure

## Rule-Based Module Integration

- Configurable path via `RULE_BASED_RECOG_DIR`
- The service writes a temp `input.txt`, calls:
  - `python pipeline_ocr_extract_translate.py --input input.txt --output result.json [--translate]`
- Expects JSON output identical to `placeholders_report.txt`

## Extending / Replacing Rule Engine

- `DocumentIngestionService._invoke_rule_based` is the only integration point.
- Swap with ML or gRPC inference while keeping `RuleBasedPayload` schema.

## Testing Strategy

- Unit-test `DocumentIngestionService` with `pytest` by mocking `_invoke_rule_based`
- Use FastAPI `TestClient` for endpoint tests
- Integration tests spin up docker-compose services and assert DB contents via SQLAlchemy session

## Security & Production Notes

- Switch to signed URLs / S3 for uploads in production
- Enable authentication middleware (API keys, JWT) before exposing endpoints
- Configure S3/MinIO for durable storage
- Add observability (OpenTelemetry, Prometheus) as needed
- Keep Alembic migrations under version control for reproducible releases

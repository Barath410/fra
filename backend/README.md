# VanAdhikar Drishti API

FastAPI backend for the Forest Rights Act (FRA) Atlas & WebGIS Decision Support System.

## Features

- **RESTful API** for FRA claims, villages, officers, and schemes
- **PostgreSQL + PostGIS** for spatial data storage
- **AI/ML Decision Support System** with scikit-learn & XGBoost
- **OCR Digitization** using Tesseract + spaCy NER
- **Grievance Management** with SLA tracking
- **Analytics & Reporting** endpoints
- **GeoServer** integration for WMS/WFS services

## Tech Stack

- **FastAPI** 0.110.0
- **SQLAlchemy** 2.0.25 + **GeoAlchemy2** 0.14.3
- **PostgreSQL 15 + PostGIS** 3.3
- **Redis** for caching
- **MinIO** for object storage
- **Celery** for background tasks

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start Database

```bash
docker-compose up -d postgres redis minio
```

### 4. Run Migrations

```bash
alembic upgrade head
```

### 5. Start Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: http://localhost:8000

API Documentation: http://localhost:8000/api/docs

## API Endpoints

### Claims
- `GET /api/claims` - Get all claims (with filters)
- `GET /api/claims/{claim_id}` - Get claim by ID
- `POST /api/claims` - Create new claim
- `PATCH /api/claims/{claim_id}` - Update claim
- `GET /api/claims/stats/summary` - Get claim statistics
- `GET /api/claims/stats/by-state` - State-wise statistics

### Villages
- `GET /api/villages` - Get all villages
- `GET /api/villages/{village_code}` - Get village by code
- `POST /api/villages` - Create new village
- `GET /api/villages/stats/summary` - Village statistics

### Officers
- `GET /api/officers` - Get all officers
- `GET /api/officers/{officer_code}` - Get officer by code
- `POST /api/officers` - Create new officer

### DSS (Decision Support System)
- `GET /api/dss/recommendations` - Get AI recommendations
- `POST /api/dss/recommendations` - Create recommendation
- `GET /api/dss/recommendations/stats` - DSS statistics

### Grievances
- `GET /api/grievances` - Get all grievances
- `GET /api/grievances/{grievance_id}` - Get grievance by ID
- `POST /api/grievances` - File new grievance
- `PATCH /api/grievances/{grievance_id}` - Update grievance
- `GET /api/grievances/stats/summary` - Grievance statistics

### Analytics
- `GET /api/analytics/dashboard` - Dashboard analytics
- `GET /api/analytics/claims-trend` - Monthly claims trend
- `GET /api/analytics/state-comparison` - State-wise comparison

### OCR
- `POST /api/ocr/extract` - Extract text from document
- `POST /api/ocr/batch-extract` - Batch document processing

### Schemes
- `GET /api/schemes` - Get scheme enrollments
- `POST /api/schemes` - Create enrollment
- `GET /api/schemes/stats/saturation` - Saturation statistics

## Database Schema

### Main Tables
- `fra_claims` - FRA claim records
- `villages` - Village master with spatial data
- `officers` - Officer master
- `dss_recommendations` - AI-generated recommendations
- `grievances` - Grievance tracking
- `scheme_enrollments` - Scheme enrollment data

## Development

### Run Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
flake8 app/
```

### Create Migration
```bash
alembic revision --autogenerate -m "description"
```

## Deployment

### Using Docker Compose
```bash
docker-compose up --build -d
```

### Environment Variables (Production)
- Set strong `SECRET_KEY`
- Update database credentials
- Configure CORS origins
- Set up SSL/TLS

## License

Government of India — Ministry of Tribal Affairs

## Contact

For support: support@fra.gov.in

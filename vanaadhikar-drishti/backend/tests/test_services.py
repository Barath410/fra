"""
Production Services - API Endpoint Tests

Test paginated endpoints with filtering
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base_class import Base
from app.db.session import get_db
from app.models.claim import Claim
from app.models.village import Village
from app.models.officer import Officer
from app.models.grievance import Grievance


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_services.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    
    # Insert test data
    db = TestingSessionLocal()
    
    # Add villages
    villages = [
        Village(
            code=f"VIL-MP-{i:03d}",
            name=f"Village {i}",
            district="Mandla",
            state="MP",
            population=2000 + i * 100,
        )
        for i in range(1, 26)
    ]
    db.add_all(villages)
    
    # Add officers
    officers = [
        Officer(
            officer_id=f"OFF-MP-{i:03d}",
            name=f"Officer {i}",
            designation="Range Officer",
            state="MP",
            district="Mandla",
            mobile=f"+919876543{i:03d}",
            email=f"officer{i}@gov.in",
            last_active="2026-02-23",
        )
        for i in range(1, 6)
    ]
    db.add_all(officers)
    
    # Add claims
    claims = [
        Claim(
            claim_id=f"FRA-2026-MP-{i:05d}",
            claimant_name=f"Claimant {i}",
            village_name=f"Village {i}",
            village_code=f"VIL-MP-{i:03d}",
            district="Mandla",
            state="MP",
            claim_type="IFR" if i % 2 == 0 else "CFR",
            area_acres=2.5 + i * 0.1,
            claim_date="2025-11-15",
            status="PENDING" if i % 3 == 0 else "APPROVED",
        )
        for i in range(1, 31)
    ]
    db.add_all(claims)
    
    # Add grievances
    grievances = [
        Grievance(
            grievance_id=f"GRV-2026-MP-{i:05d}",
            claimant_name=f"Claimant {i}",
            village_name=f"Village {i}",
            district="Mandla",
            state="MP",
            category="Slow Processing",
            status="OPEN" if i % 2 == 0 else "RESOLVED",
            priority="HIGH" if i % 3 == 0 else "MEDIUM",
            description=f"Grievance description {i}",
        )
        for i in range(1, 11)
    ]
    db.add_all(grievances)
    
    db.commit()
    yield
    db.drop_all()


class TestClaimsEndpoint:
    def test_get_claims_default_pagination(self):
        response = client.get("/api/v1/claims")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "total" in data
        assert "page" in data
        assert "limit" in data
        assert "pages" in data
        assert len(data["data"]) <= 20  # Default limit

    def test_get_claims_with_custom_pagination(self):
        response = client.get("/api/v1/claims?page=2&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert data["limit"] == 10
        assert len(data["data"]) <= 10

    def test_get_claims_with_status_filter(self):
        response = client.get("/api/v1/claims?status=APPROVED")
        assert response.status_code == 200
        data = response.json()
        for claim in data["data"]:
            assert claim["status"] == "APPROVED"

    def test_get_claims_with_state_filter(self):
        response = client.get("/api/v1/claims?state=MP")
        assert response.status_code == 200
        data = response.json()
        for claim in data["data"]:
            assert claim["state"] == "MP"

    def test_get_claims_with_multiple_filters(self):
        response = client.get("/api/v1/claims?state=MP&status=PENDING&district=Mandla")
        assert response.status_code == 200
        data = response.json()
        assert data["filters"]["state"] == "MP"
        assert data["filters"]["status"] == "PENDING"
        assert data["filters"]["district"] == "Mandla"

    def test_get_single_claim(self):
        response = client.get("/api/v1/claims/FRA-2026-MP-00001")
        assert response.status_code == 200
        claim = response.json()
        assert claim["id"] == "FRA-2026-MP-00001"

    def test_get_nonexistent_claim(self):
        response = client.get("/api/v1/claims/NONEXISTENT")
        assert response.status_code == 404


class TestVillagesEndpoint:
    def test_get_villages_default_pagination(self):
        response = client.get("/api/v1/villages")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "total" in data
        assert data["total"] == 25

    def test_get_villages_with_pagination(self):
        response = client.get("/api/v1/villages?page=1&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 5
        assert data["pages"] == 5  # 25 villages / 5 per page

    def test_get_villages_with_state_filter(self):
        response = client.get("/api/v1/villages?state=MP")
        assert response.status_code == 200
        data = response.json()
        for village in data["data"]:
            assert village["state"] == "MP"

    def test_get_villages_with_district_filter(self):
        response = client.get("/api/v1/villages?district=Mandla")
        assert response.status_code == 200
        data = response.json()
        for village in data["data"]:
            assert village["district"] == "Mandla"

    def test_get_single_village(self):
        response = client.get("/api/v1/villages/VIL-MP-001")
        assert response.status_code == 200
        village = response.json()
        assert village["code"] == "VIL-MP-001"


class TestOfficersEndpoint:
    def test_get_officers_default_pagination(self):
        response = client.get("/api/v1/officers")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["total"] == 5

    def test_get_officers_with_pagination(self):
        response = client.get("/api/v1/officers?page=1&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 2
        assert data["pages"] == 3  # 5 officers / 2 per page

    def test_get_officers_with_state_filter(self):
        response = client.get("/api/v1/officers?state=MP")
        assert response.status_code == 200
        data = response.json()
        for officer in data["data"]:
            assert officer["state"] == "MP"

    def test_get_single_officer(self):
        response = client.get("/api/v1/officers/OFF-MP-001")
        assert response.status_code == 200
        officer = response.json()
        assert officer["id"] == "OFF-MP-001"


class TestGrievancesEndpoint:
    def test_get_grievances_default_pagination(self):
        response = client.get("/api/v1/grievances")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["total"] == 10

    def test_get_grievances_with_pagination(self):
        response = client.get("/api/v1/grievances?page=1&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 3
        assert data["pages"] == 4  # 10 grievances / 3 per page

    def test_get_grievances_with_status_filter(self):
        response = client.get("/api/v1/grievances?status=OPEN")
        assert response.status_code == 200
        data = response.json()
        for grievance in data["data"]:
            assert grievance["status"] == "OPEN"

    def test_get_grievances_with_priority_filter(self):
        response = client.get("/api/v1/grievances?priority=HIGH")
        assert response.status_code == 200
        data = response.json()
        for grievance in data["data"]:
            assert grievance["priority"] == "HIGH"

    def test_get_grievances_with_multiple_filters(self):
        response = client.get("/api/v1/grievances?state=MP&district=Mandla&status=OPEN")
        assert response.status_code == 200
        data = response.json()
        assert data["filters"]["state"] == "MP"

    def test_get_single_grievance(self):
        response = client.get("/api/v1/grievances/GRV-2026-MP-00001")
        assert response.status_code == 200
        grievance = response.json()
        assert grievance["id"] == "GRV-2026-MP-00001"

    def test_create_grievance(self):
        payload = {
            "grievance_id": "GRV-2026-MP-99999",
            "claimant_name": "Test Claimant",
            "village_name": "Test Village",
            "district": "Test District",
            "state": "MP",
            "category": "Test Category",
            "status": "OPEN",
            "priority": "MEDIUM",
            "description": "Test grievance",
        }
        response = client.post("/api/v1/grievances", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == "GRV-2026-MP-99999"

    def test_create_duplicate_grievance(self):
        payload = {
            "grievance_id": "GRV-2026-MP-00001",  # Already exists
            "claimant_name": "Test Claimant",
            "village_name": "Test Village",
            "district": "Test District",
            "state": "MP",
            "category": "Test Category",
            "status": "OPEN",
            "priority": "MEDIUM",
            "description": "Test grievance",
        }
        response = client.post("/api/v1/grievances", json=payload)
        assert response.status_code == 400

    def test_update_grievance(self):
        update_payload = {"status": "RESOLVED", "priority": "CRITICAL"}
        response = client.patch("/api/v1/grievances/GRV-2026-MP-00001", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "RESOLVED"
        assert data["priority"] == "CRITICAL"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

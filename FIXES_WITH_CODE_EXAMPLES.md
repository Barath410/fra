# 🔧 DETAILED FIXES WITH CODE EXAMPLES

## 1. EMERGENCY FIX: Move Database Password Out of Source Code

### Current Problem

**File:** `backend/app/core/config.py` (Line 19-20)
```python
# ❌ BAD: PASSWORD IN SOURCE CODE!
database_url: str = Field(
    default="mysql+pymysql://root:Lakpra849%40@localhost:3306/vanaadhikar?charset=utf8mb4"
)

# ❌ BAD: DEFAULT JWT SECRET IN SOURCE CODE!
jwt_secret_key: str = "change-me"
```

### Solution

**Step 1: Create `.env` file**

```bash
cd backend
cat > .env << 'EOF'
APP_ENV=development
DATABASE_URL=mysql+pymysql://root:Lakpra849@localhost:3306/vanaadhikar
JWT_SECRET_KEY=your-super-secret-key-generate-this
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
JWT_ALGORITHM=HS256
EOF
```

**Step 2: Update `backend/app/core/config.py`**

Replace lines 19-20 from:
```python
database_url: str = Field(
    default="mysql+pymysql://root:Lakpra849%40@localhost:3306/vanaadhikar?charset=utf8mb4"
)
jwt_secret_key: str = "change-me"
```

To:
```python
database_url: str = Field(
    default="mysql+pymysql://root:root@localhost:3306/vanaadhikar"
)
jwt_secret_key: str = Field(
    default="change-me"  # Will be overridden by .env
)
```

**Step 3: Add to `.gitignore`**
```bash
echo "backend/.env" >> .gitignore
```

**Verification:**
```bash
cd backend
python -c "from app.core.config import settings; print(f'DB: {settings.database_url}')"
```

---

## 2. FIX: Frontend API Not Sending Auth Token

### Current Problem

**File:** `src/lib/api.ts` (Lines 1-20)

```typescript
// ❌ WRONG: No Authorization header!
async function fetchJSON<T>(path: string, init?: RequestInit): Promise<T> {
    const res = await fetch(`${API_BASE}${path}`, {
        ...init,
        headers: {
            "Content-Type": "application/json",
            ...(init?.headers || {}),
        },
        cache: "no-store",
    });

    if (!res.ok) {
        const text = await res.text();
        throw new Error(`API ${res.status}: ${text}`);
    }
    return res.json();
}
```

### Solution

**Replace `src/lib/api.ts` with:**

```typescript
import { DashboardSummary, FRAClaim, GrievanceTicket } from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

// Helper to extract JWT token from cookies
function getAuthToken(): string | null {
    if (typeof document === 'undefined') return null;
    const token = document.cookie
        .split('; ')
        .find(row => row.startsWith('auth_token='))
        ?.split('=')[1];
    return token ?? null;
}

async function fetchJSON<T>(path: string, init?: RequestInit): Promise<T> {
    const token = getAuthToken();
    
    const res = await fetch(`${API_BASE}${path}`, {
        ...init,
        headers: {
            "Content-Type": "application/json",
            ...(token ? { "Authorization": `Bearer ${token}` } : {}),
            ...(init?.headers || {}),
        },
        cache: "no-store",
    });

    if (!res.ok) {
        const text = await res.text();
        throw new Error(`API ${res.status}: ${text}`);
    }
    return res.json();
}

// ... rest of file unchanged
```

---

## 3. FIX: Add Missing API Methods

### Current Problem

**File:** `src/lib/api-client.ts` (Incomplete)

Pages try to call `apiClient.getSchemes()` but it doesn't exist.

### Solution

**Complete `src/lib/api-client.ts`:**

```typescript
import { fetchJSON } from './api';

export const apiClient = {
    /**
     * CLAIMS ENDPOINTS
     */
    getClaims: async (page: number = 1, limit: number = 20, filters?: Record<string, any>) => {
        const query = new URLSearchParams();
        query.append('page', page.toString());
        query.append('limit', limit.toString());
        if (filters?.state) query.append('state', filters.state);
        if (filters?.district) query.append('district', filters.district);
        if (filters?.status) query.append('status', filters.status);
        
        return fetchJSON(`/api/v1/claims?${query.toString()}`);
    },

    getClaim: async (claimId: string) => {
        return fetchJSON(`/api/v1/claims/${claimId}`);
    },

    createClaim: async (data: any) => {
        return fetchJSON(`/api/v1/claims`, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    updateClaim: async (claimId: string, data: any) => {
        return fetchJSON(`/api/v1/claims/${claimId}`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    },

    assignOfficer: async (claimId: string, officerId: string) => {
        return fetchJSON(`/api/v1/claims/${claimId}/assign-officer`, {
            method: 'PATCH',
            body: JSON.stringify({ officer_id: officerId }),
        });
    },

    /**
     * VILLAGES ENDPOINTS
     */
    getVillages: async (page: number = 1, limit: number = 20) => {
        const query = new URLSearchParams();
        query.append('page', page.toString());
        query.append('limit', limit.toString());
        return fetchJSON(`/api/v1/villages?${query.toString()}`);
    },

    /**
     * OFFICERS ENDPOINTS
     */
    getOfficers: async (page: number = 1, limit: number = 20) => {
        const query = new URLSearchParams();
        query.append('page', page.toString());
        query.append('limit', limit.toString());
        return fetchJSON(`/api/v1/officers?${query.toString()}`);
    },

    /**
     * GRIEVANCES ENDPOINTS
     */
    getGrievances: async (page: number = 1, limit: number = 20) => {
        const query = new URLSearchParams();
        query.append('page', page.toString());
        query.append('limit', limit.toString());
        return fetchJSON(`/api/v1/grievances?${query.toString()}`);
    },

    createGrievance: async (data: any) => {
        return fetchJSON(`/api/v1/grievances`, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    /**
     * DASHBOARD ENDPOINTS
     */
    getDashboardSummary: async () => {
        return fetchJSON(`/api/v1/dashboard/summary`);
    },

    /**
     * NEW: SCHEMES ENDPOINTS
     */
    getSchemes: async () => {
        return fetchJSON(`/api/v1/schemes`);
    },

    /**
     * NEW: ALERTS ENDPOINTS
     */
    getAlerts: async (districtId?: string) => {
        const query = new URLSearchParams();
        if (districtId) query.append('district_id', districtId);
        return fetchJSON(`/api/v1/alerts?${query.toString()}`);
    },

    /**
     * NEW: REPORTS ENDPOINTS
     */
    getReports: async (state?: string) => {
        const query = new URLSearchParams();
        if (state) query.append('state', state);
        return fetchJSON(`/api/v1/reports?${query.toString()}`);
    },

    /**
     * NEW: DSS RECOMMENDATIONS ENDPOINTS
     */
    getDSSRecommendations: async () => {
        return fetchJSON(`/api/v1/dss-recommendations`);
    },

    /**
     * NEW: NOTIFICATIONS ENDPOINTS
     */
    getNotifications: async () => {
        return fetchJSON(`/api/v1/notifications`);
    },
};
```

---

## 4. FIX: Create Missing Backend Routes

### Create `backend/app/api/endpoints/schemes.py`

```python
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(prefix="/schemes", tags=["schemes"])


@router.get("")
def list_schemes(
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    limit: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 20,
    db: Session = Depends(get_db),
):
    """
    List all welfare schemes.
    
    Query Parameters:
    - page: Page number (default 1)
    - limit: Items per page (default 20, max 100)
    """
    # TODO: Once schemes table exists, replace with:
    # schemes = db.query(Scheme).offset((page - 1) * limit).limit(limit).all()
    
    # Placeholder response
    return {
        "data": [
            {
                "id": "scheme-1",
                "name": "Forest Rights Act Implementation Scheme",
                "description": "Scheme to support FRA implementation",
                "budget": 1000000,
                "beneficiaries": 50000,
            },
        ],
        "page": page,
        "limit": limit,
        "total": 1,
    }
```

### Create `backend/app/api/endpoints/alerts.py`

```python
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("")
def list_alerts(
    district_id: Annotated[str | None, Query(description="Filter by district ID")] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    db: Session = Depends(get_db),
):
    """
    List system alerts (forest fires, grievances, etc).
    
    Query Parameters:
    - district_id: Filter by district
    - page: Page number
    - limit: Items per page
    """
    # Placeholder
    return {
        "data": [],
        "page": page,
        "limit": limit,
        "total": 0,
    }
```

### Create `backend/app/api/endpoints/reports.py`

```python
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.session import get_db

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("")
def list_reports(
    state: Annotated[str | None, Query(description="Filter by state")] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    db: Session = Depends(get_db),
):
    """
    List monthly progress reports by state.
    
    Query Parameters:
    - state: State code (e.g., 'MP', 'OD')
    - page: Page number
    - limit: Items per page
    """
    # Placeholder
    return {
        "data": [],
        "page": page,
        "limit": limit,
        "total": 0,
    }
```

### Repeat for `dss.py` and `notifications.py`

Store in same directory: `backend/app/api/endpoints/`

### Register Routes

**File:** `backend/app/api/router.py`

Replace:
```python
from fastapi import APIRouter

from app.api.endpoints import auth, claims, dashboard, documents, grievances, officers, villages

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(documents.router, prefix="/documents")
api_router.include_router(dashboard.router)
api_router.include_router(claims.router)
api_router.include_router(villages.router)
api_router.include_router(officers.router)
api_router.include_router(grievances.router)
```

With:
```python
from fastapi import APIRouter

from app.api.endpoints import (
    auth, 
    claims, 
    dashboard, 
    documents, 
    grievances, 
    officers, 
    villages,
    schemes,        # ADD
    alerts,         # ADD
    reports,        # ADD
    dss,            # ADD
    notifications,  # ADD
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(documents.router, prefix="/documents")
api_router.include_router(dashboard.router)
api_router.include_router(claims.router)
api_router.include_router(villages.router)
api_router.include_router(officers.router)
api_router.include_router(grievances.router)
api_router.include_router(schemes.router)      # ADD
api_router.include_router(alerts.router)       # ADD
api_router.include_router(reports.router)      # ADD
api_router.include_router(dss.router)          # ADD
api_router.include_router(notifications.router) # ADD
```

---

## 5. FIX: Replace Placeholder Pages

### Example: Schemes Page

**File:** `src/app/mera-patta/schemes/page.tsx`

**Before:**
```typescript
export default function Page() {
    return <PlaceholderPage />;
}
```

**After:**
```typescript
"use client";
import React, { useState } from "react";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { useDashboardFetch } from "@/hooks/use-dashboard-fetch";
import { apiClient } from "@/lib/api-client";
import { Skeleton } from "@/components/ui/skeleton";
import { formatNumber } from "@/lib/utils";

interface Scheme {
    id: string;
    name: string;
    description: string;
    budget: number;
    beneficiaries: number;
}

export default function SchemesPage() {
    const { data, loading, error } = useDashboardFetch<Scheme[]>(apiClient, {
        endpoint: 'schemes',
        enabled: true,
    });

    if (loading) {
        return (
            <DashboardLayout title="Welfare Schemes">
                <div className="space-y-4">
                    {[...Array(5)].map((_, i) => (
                        <Skeleton key={i} className="h-32" />
                    ))}
                </div>
            </DashboardLayout>
        );
    }

    if (error) {
        return (
            <DashboardLayout title="Welfare Schemes">
                <div className="border border-red-200 bg-red-50 rounded-lg p-4">
                    <p className="text-red-800">Error loading schemes: {error}</p>
                </div>
            </DashboardLayout>
        );
    }

    const schemes = Array.isArray(data) ? data : [];

    return (
        <DashboardLayout title="Welfare Schemes" titleHi="कल्याण योजनाएं">
            <div className="space-y-4">
                {schemes.length === 0 ? (
                    <div className="border border-gray-300 rounded-lg p-8 text-center">
                        <p className="text-gray-600">No schemes found</p>
                    </div>
                ) : (
                    schemes.map((scheme) => (
                        <div
                            key={scheme.id}
                            className="border border-gray-200 rounded-lg p-6 bg-white hover:shadow-md transition"
                        >
                            <h3 className="text-lg font-bold text-gray-900">{scheme.name}</h3>
                            <p className="text-sm text-gray-600 mt-2">{scheme.description}</p>
                            <div className="grid grid-cols-2 gap-4 mt-4">
                                <div>
                                    <p className="text-xs text-gray-500">Budget</p>
                                    <p className="text-lg font-semibold">₹{formatNumber(scheme.budget)}</p>
                                </div>
                                <div>
                                    <p className="text-xs text-gray-500">Beneficiaries</p>
                                    <p className="text-lg font-semibold">{formatNumber(scheme.beneficiaries)}</p>
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </DashboardLayout>
    );
}
```

---

## 6. FIX: Connect Form Submissions

### Example: New Report Form

**File:** `src/app/field-officer/new-report/page.tsx`

**Problem:** Form has no submit handler

**Solution:** Add handler to POST endpoint

```typescript
"use client";
import React, { useState } from "react";
import { apiClient } from "@/lib/api-client";

export default function NewReportPage() {
    const [formData, setFormData] = useState({
        claimId: "",
        findings: "",
        gpsLocation: "",
        photos: [] as File[],
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            // Validate
            if (!formData.claimId) {
                throw new Error("Claim ID is required");
            }

            // Call API
            const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/v1/field-visits`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    claim_id: formData.claimId,
                    findings: formData.findings,
                    gps_location: formData.gpsLocation,
                    // photos would need separate multipart upload
                }),
            });

            if (!response.ok) {
                const error = await response.text();
                throw new Error(`Failed to create report: ${error}`);
            }

            const result = await response.json();
            setSuccess(true);
            setFormData({ claimId: "", findings: "", gpsLocation: "", photos: [] });

            // Show success message
            alert("Report created successfully!");

        } catch (err) {
            setError(err instanceof Error ? err.message : "Unknown error");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto p-6">
            <h1 className="text-2xl font-bold mb-6">Create New Field Report</h1>

            {error && (
                <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded mb-4">
                    {error}
                </div>
            )}

            {success && (
                <div className="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded mb-4">
                    Report created successfully!
                </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium mb-1">Claim ID</label>
                    <input
                        type="text"
                        placeholder="Enter claim ID"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={formData.claimId}
                        onChange={(e) => setFormData(p => ({ ...p, claimId: e.target.value }))}
                        required
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium mb-1">Findings</label>
                    <textarea
                        placeholder="Document verification findings"
                        className="w-full px-3 py-2 border rounded-lg h-24"
                        value={formData.findings}
                        onChange={(e) => setFormData(p => ({ ...p, findings: e.target.value }))}
                        required
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium mb-1">GPS Coordinates</label>
                    <input
                        type="text"
                        placeholder="Lat,Lon"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={formData.gpsLocation}
                        onChange={(e) => setFormData(p => ({ ...p, gpsLocation: e.target.value }))}
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                    {loading ? "Creating..." : "Create Report"}
                </button>
            </form>
        </div>
    );
}
```

---

## 7. DATABASE: Load Seed Data

### Check Current Status

```bash
mysql -u root -pLakpra849 << EOF
USE vanaadhikar;
SHOW TABLES;
SELECT COUNT(*) as claim_count FROM claims;
SELECT COUNT(*) as village_count FROM villages;
SELECT COUNT(*) as officer_count FROM officers;
EOF
```

### Load Data

**Option A: Using Python Script**
```bash
cd backend
python seed_database.py
```

**Option B: Using MySQL directly**
```bash
mysql -u root -pLakpra849 vanaadhikar < ../seed_data.sql
```

**Verify:**
```bash
mysql -u root -pLakpra849 << EOF
USE vanaadhikar;
SELECT 'claims' as table_name, COUNT(*) as rows FROM claims
UNION
SELECT 'villages', COUNT(*) FROM villages
UNION
SELECT 'officers', COUNT(*) FROM officers
UNION
SELECT 'grievances', COUNT(*) FROM grievances;
EOF
```

---

## TESTING: Verify Fixes

```bash
# 1. Test API without auth (public endpoints)
curl -X GET http://localhost:8000/api/v1/claims

# 2. Test database connection
curl -X GET http://localhost:8000/health

# 3. Test frontend page loads
curl http://localhost:3000/national-dashboard

# 4. Test new schemes endpoint
curl http://localhost:8000/api/v1/schemes

# 5. Check database is populated
mysql -u root -pLakpra849 -e "SELECT COUNT(*) FROM vanaadhikar.claims;"
```

---

## NEXT STEPS CHECKLIST

- [ ] Move credentials to `.env` file
- [ ] Add missing methods to API client
- [ ] Create missing backend routes (5 routers)
- [ ] Register new routes in `api/router.py`
- [ ] Replace 26 placeholder pages
- [ ] Add form submission handlers
- [ ] Update API client to send auth tokens
- [ ] Load seed data to database
- [ ] Test each page in browser
- [ ] Run curl tests for each API
- [ ] Deploy to staging

---


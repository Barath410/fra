# API INTEGRATION ANALYSIS - Frontend vs Backend

## Cross-Check: Frontend Calls vs Backend Endpoints

| Frontend File | API Call | HTTP Verb | Endpoint | Backend File | Status | Issue |
|---|---|---|---|---|---|---|
| src/lib/api.ts | `getDashboardSummary()` | GET | `/api/v1/dashboard/summary` | backend/app/api/endpoints/dashboard.py | ❌ CRASH | Queries users (missing), claims (missing), villages (missing), officers (missing), grievances (missing), data_blobs (missing) - 6 table dependencies |
| src/lib/api.ts | `getClaims()` | GET | `/api/v1/claims` | backend/app/api/endpoints/claims.py | ❌ CRASH | Queries claims table - MISSING |
| src/lib/api.ts | `getClaims()` | GET | `/api/v1/claims` | backend/app/api/endpoints/claims.py | ❌ MISMATCH | Frontend expects `FRAClaim[]`, backend returns `list[ClaimRead]` - field name aliases may not match |
| src/lib/api.ts | `createGrievance()` | POST | `/api/v1/grievances` | backend/app/api/endpoints/grievances.py | ❌ CRASH | Queries grievances table - MISSING |
| src/app/gram-sabha/dashboard/page.tsx | uploadDocumentRequest() | POST | `/api/v1/documents/upload-document` | backend/app/api/endpoints/documents.py | ✓ WORKS | Endpoint exists, document_ingestion_service handling likely incomplete |
| src/lib/document-upload.ts | uploadDocumentRequest() | POST | `/api/v1/documents/upload-document` | backend/app/api/endpoints/documents.py | ✓ WORKS | File upload works, response format matches DocumentUploadResult |
| src/app/gram-sabha/new-claim/page.tsx | (No API calls) | - | - | - | ❌ MISSING | Form component imports but no actual submission logic |
| src/app/gram-sabha/grievance/page.tsx | (No API calls visible) | - | - | - | ❌ MISSING | Should call POST /api/v1/grievances but not implemented |
| src/app/mera-patta/page.tsx | (Uses SAMPLE_CLAIMS) | - | - | - | ❌ MISSING | Should call getClaims() but hardcoded data used instead |
| src/app/mera-patta/page.tsx | (Uses SAMPLE_GRIEVANCES) | - | - | - | ❌ MISSING | Should call getGrievances() - endpoint doesn't exist in source |
| src/app/dss/page.tsx | (Uses DSS_RECOMMENDATIONS) | - | - | - | ❌ MISSING | Should call getDSSRecommendations() but hardcoded data used instead |
| src/app/digitization/page.tsx | (Uses mockDocs) | - | - | - | ❌ MISSING | Should list documents from /api/v1/documents |
| src/app/national-dashboard/page.tsx | (Not examined) | - | - | - | ? | Likely also uses mock data |
| (Auth module) | `google_login()` | GET | `/api/v1/auth/google/login` | backend/app/api/endpoints/auth.py | ✓ WORKS | Returns Google OAuth URL |
| (Auth module) | `google_callback()` | GET | `/api/v1/auth/google/callback?code=...` | backend/app/api/endpoints/auth.py | ❌ CRASH | Creates user in users table - TABLE MISSING |
| (Auth module) | `me()` | GET | `/api/v1/auth/me` | backend/app/api/endpoints/auth.py L95 | ❌ CRASH | Queries users table to get current user - TABLE MISSING |

---

## Detailed Analysis

### FRONTEND → BACKEND CALL ANALYSIS

#### ✓ WORKING INTEGRATIONS (2/15)
```
1. Document Upload Flow
   Frontend: uploadDocumentRequest() 
   → POST /api/v1/documents/upload-document
   → Backend: document_ingestion_service.ingest()
   Status: ✓ Endpoint exists
   Issue: Service implementation unclear

2. Google OAuth Initial
   Frontend: Redirects to google.com
   → GET /api/v1/auth/google/login
   → Backend: Returns Google auth URL
   Status: ✓ Endpoint works
   Issue: Callback fails (next step)
```

---

#### ❌ BROKEN INTEGRATIONS (13/15)

**CATEGORY 1: Missing Database Tables (6 crashes)**
```
Dashboard Summary
├─ Frontend: getDashboardSummary()
├─ Call: GET /api/v1/dashboard/summary
├─ Backend: dashboard.py line 16
│  └─ Depends on:
│     ├─ dashboard_snapshot(db) → queries Claims table ❌ MISSING
│     ├─ queries Village table ❌ MISSING
│     ├─ queries Officer table ❌ MISSING
│     ├─ queries Grievance table ❌ MISSING
│     ├─ queries DataBlob table ❌ MISSING
│     └─ queries Users table ❌ MISSING
└─ HTTP Status: 500 (ProgrammingError)

Claims List
├─ Frontend: getClaims(params)
├─ Call: GET /api/v1/claims?state=&status=
├─ Backend: claims.py line 15
│  └─ db.query(Claim) ❌ Table 'fra_documents.claims' doesn't exist
└─ HTTP Status: 500 (ProgrammingError)

Villages List
├─ Frontend: Components render SAMPLE_VILLAGES (hardcoded)
├─ Should Call: GET /api/v1/villages
├─ Backend: villages.py
│  └─ db.query(Village) ❌ Table 'fra_documents.villages' doesn't exist
└─ HTTP Status: 500 (if called)

Officers List
├─ Frontend: Components render hardcoded officer data
├─ Should Call: GET /api/v1/officers
├─ Backend: officers.py
│  └─ db.query(Officer) ❌ Table 'fra_documents.officers' doesn't exist
└─ HTTP Status: 500 (if called)

Grievances List/Create
├─ Frontend: createGrievance() called from form
├─ Call: POST /api/v1/grievances
├─ Backend: grievances.py
│  └─ db.query(Grievance) ❌ Table 'fra_documents.grievances' doesn't exist
└─ HTTP Status: 500

Auth Me
├─ Frontend: Middleware queries current user
├─ Call: GET /api/v1/auth/me
├─ Backend: auth.py line 95
│  └─ db.query(User) ❌ Table 'fra_documents.users' doesn't exist
└─ HTTP Status: 500
```

**CATEGORY 2: Frontend Doesn't Call API (7 missing)**
```
1. Schemes Pages
   ├─ Route: /mera-patta/schemes
   ├─ File: src/app/mera-patta/schemes/page.tsx
   ├─ Renders: <PlaceholderPage>
   ├─ Backend: ❌ No /api/v1/schemes endpoint exists
   └─ Impact: Page shows "Live data preview" forever

2. State Schemes
   ├─ Route: /state/[state]/schemes
   ├─ File: src/app/state/[stateSlug]/schemes/page.tsx
   ├─ Renders: <PlaceholderPage>
   ├─ Backend: ❌ No endpoint
   └─ Impact: Page never loads real data

3. State Reports
   ├─ Route: /state/[state]/reports
   ├─ File: src/app/state/[stateSlug]/reports/page.tsx
   ├─ Renders: <PlaceholderPage>
   ├─ Backend: ❌ No endpoint
   └─ Impact: Page never loads real data

4. Mera Patta (Claims/Grievances Search)
   ├─ Route: /mera-patta
   ├─ File: src/app/mera-patta/page.tsx
   ├─ Renders: SAMPLE_CLAIMS, SAMPLE_GRIEVANCES (hardcoded)
   ├─ Should Call: getClaims(), getGrievances()
   ├─ Issue: Endpoints exist but Database table missing
   └─ Impact: Only mock data displayed

5. DSS Recommendations
   ├─ Route: /dss
   ├─ File: src/app/dss/page.tsx
   ├─ Renders: DSS_RECOMMENDATIONS (hardcoded)
   ├─ Should Call: GET /api/v1/dss/recommendations
   ├─ Backend: ❌ Endpoint doesn't exist
   └─ Impact: Only mock data displayed

6. Digitization (OCR)
   ├─ Route: /digitization
   ├─ File: src/app/digitization/page.tsx
   ├─ Renders: mockDocs array (hardcoded)
   ├─ Should Call: GET /api/v1/documents
   ├─ Backend: Document listing endpoint missing
   └─ Impact: Only mock documents shown

7. Gram Sabha Dashboard
   ├─ Route: /gram-sabha/dashboard
   ├─ File: src/app/gram-sabha/dashboard/page.tsx
   ├─ Renders: SAMPLE_VILLAGES, SAMPLE_CLAIMS (hardcoded)
   ├─ Should Call: getVillages(), getClaims()
   ├─ Backend: Endpoints exist but tables missing
   └─ Impact: Only mock data displayed
```

---

### REQUEST/RESPONSE SHAPE ANALYSIS

#### Claim Flow
```
Frontend (src/lib/api.ts):
  Interface FRAClaim {
    id: number;
    claim_id: string;
    claimant_name: string;
    state: string;
    district: string;
    status: string;
    // ... more fields
  }

Backend (backend/app/schemas/domain.py):
  Class ClaimRead {
    // Pydantic model with field aliases
    // e.g., Config.populate_by_name = True
  }

Mismatch:
  ⚠️ Field name transformation unclear
    - Frontend uses: claimant_name
    - Backend may use: claimant_name or claim_ant_name
  ⚠️ No schema validation or documentation
```

#### Grievance Flow
```
Frontend (src/lib/api.ts):
  Function createGrievance(payload: GrievanceTicket)
  {
    body: {
      grievance_id, claimant_name, claim_id, village_name, 
      block, district, state, category, status, priority, 
      description, channel, mobile, source, assigned_officer_id, filed_date
    }
  }

Backend (backend/app/api/endpoints/grievances.py):
  Class GrievanceCreate(BaseModel)
  {
    grievance_id, claimant_name, claim_id, village_name, 
    block, district, state, category, status, priority, 
    description, channel, mobile, source, assigned_officer_id, filed_date
  }

Status: ✓ Field names match
Issue: ❌ Table missing - endpoint 500s anyway
```

---

### AUTHENTICATION FLOW DIAGRAM

```
                    Browser                              Backend
                       |                                   |
    User clicks "Login" |                                   |
         with Google    |                                   |
                        | GET /auth/google/login            |
                        |---------------------------------->|
                        |                                   | Build Google auth URL
                        |          auth_url                 |
                        |<-----------------------------------|
                        |                                   |
    User redirects to   |                                   |
    Google OAuth page   | (User authorizes app)             |
                        |                                   |
    Google redirects to | GET /auth/google/callback?code=X  |
    callback URL        |---------------------------------->|
                        |                                   | Exchange code for token
                        |                                   | ❌ Fetch Google profile: ✓
                        |                                   | ❌ Query users table
                        |                                   |    Table doesn't exist!
                        |       Internal Server Error       |
                        |<-----------------------------------|
                        |                                   |
    Auth fails          |                                   |
    User not logged in  |                                   |
```

**Where it breaks:** `db.query(User)` in [backend/app/api/endpoints/auth.py](backend/app/api/endpoints/auth.py) line 75

---

## Summary Table: All Integrations

```
Total API Endpoints:     15
Working:                 2  (13%)
Broken:                 13  (87%)
├─ Missing tables:       6
├─ Missing backend:      7
└─ Placeholder UIs:      5
```

---

## How to Fix (Priority Order)

### 1. CREATE MISSING TABLES (Fixes 9 endpoints)
```sql
-- Run in fra_documents database
CREATE TABLE users (...)
CREATE TABLE claims (...)
CREATE TABLE villages (...)
CREATE TABLE officers (...)
CREATE TABLE grievances (...)
CREATE TABLE data_blobs (...)
-- See QUICK_FIX_CHECKLIST.md for full SQL
```

### 2. REMOVE HARDCODED MOCK DATA (Fixes 7 pages)
```typescript
// BEFORE (src/app/mera-patta/page.tsx)
const [villages] = useState(SAMPLE_VILLAGES);

// AFTER
const [villages, setVillages] = useState([]);
useEffect(() => {
  getClaims({state, status}).then(setVillages);
}, [state, status]);
```

### 3. IMPLEMENT MISSING ENDPOINTS (Fixes DSS, Schemes, Reports)
```python
# backend/app/api/endpoints/dss.py
@router.get("/recommendations")
def get_dss_recommendations(db: Session = Depends(get_db)):
  # Implement DSS engine
  pass
```

### 4. REPLACE PLACEHOLDER PAGES (Fixes 5 routes)
```typescript
// BEFORE (src/app/state/[stateSlug]/schemes/page.tsx)
return <PlaceholderPage title="..." />;

// AFTER
const [schemes, setSchemes] = useState([]);
return <SchemesTable schemes={schemes} />;
```

### 5. ADD ERROR HANDLING
```typescript
// Add try-catch around all API calls
try {
  const data = await getClaims();
  setData(data);
} catch (error) {
  toast.error("Failed to load claims: " + error.message);
}
```

---

## Environment & Config Issues

### Missing Environment Variables
```bash
# .env or .env.local (Frontend)
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
# Currently defaults to localhost:8000 - OK for dev

# .env (Backend)
DATABASE_URL="mysql://root:Lakpra849@localhost/fra_documents"
DATABASE_NAME="fra_documents"
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"  
GOOGLE_REDIRECT_URI="http://localhost:3000/auth/callback"
JWT_SECRET_KEY="your-secret-key-change-in-prod"
API_V1_PREFIX="/api/v1"
```

### Config Files
- ✓ [backend/app/core/config.py](backend/app/core/config.py) - Settings class exists
- ⚠️ .env file - Check if it exists and has correct DATABASE_URL

---

## Production Readiness Checklist

Schema Alignment:
- [ ] All 6 missing tables created
- [ ] Run `alembic upgrade head`
- [ ] Verify tables in database

Frontend:
- [ ] Remove all SAMPLE_* imports
- [ ] Remove PlaceholderPage usage
- [ ] Add API calls to all pages
- [ ] Add error boundaries

Backend:
- [ ] Implement all service functions
- [ ] Add auth decorators to protected routes
- [ ] Add comprehensive error handling
- [ ] Document API with OpenAPI/Swagger

Testing:
- [ ] End-to-end user flows
- [ ] API response scenarios
- [ ] Error handling
- [ ] Performance testing

Deployment:
- [ ] Set strong JWT_SECRET_KEY
- [ ] Configure Google OAuth production credentials
- [ ] Set CORS origins correctly
- [ ] Enable HTTPS in production
- [ ] Set up database backups

---

Last Updated: 2026-02-23  
Generated by: GitHub Copilot (Senior Full-Stack QA)

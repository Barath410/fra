# PHASE 3: API Request/Response Shape Analysis
**Generated:** February 23, 2026  
**Status:** Analyzing data structure mismatches between frontend and backend

---

## Critical Shape Mismatches Found

### ❌ 1. Dashboard Summary - MAJOR MISMATCH

#### Frontend Expects (DashboardSummary)
```typescript
{
  nationalStats: NationalStats;           // With fields: totalClaims, totalGranted, totalPending, totalIFR, totalCFR, etc.
  stateStats: StateStat[];                // Array of states with grants, pending, area, saturation data
  districtStats: Record<string, DistrictStat[]>;  // Nested by state then district
  claims: FRAClaim[];                     // Full claim objects
  villages: Village[];                    // Full village objects
  officers: Officer[];                    // Full officer objects
  grievances: GrievanceTicket[];          // Full grievance objects
  datasets: {
    dajguaInterventions: DAJGUAIntervention[];
    dssRecommendations: DSSRecommendation[];
    monthlyProgress: MonthlyProgressReport[];
    forestFireAlerts: ForestFireAlert[];
    fieldVisitReports: FieldVisitReport[];
    ndviTrend: Array<Record<string, any>>;
    claimPipeline: Array<{id, label, color, count, labelHi}>;
  }
}
```

#### Backend Actually Returns (aggregation_service.py)
```python
{
  "generated_at": "2026-02-23T...",
  "claims": {
    "total": 125000,
    "approved": 92450,
    "pending": 18230,
    "rejected": 14320,
    "approval_rate": 73.96,
    "by_type": {"IFR": 85000, "CFR": 40000},
    "total_area_acres": 2456789.50,
    "approved_area_acres": 1876543.21,
    "by_state": {"MP": 45000, "CG": 30000, ...},
    "pvtg_claims": 23450,
    "pvtg_percentage": 18.75
  },
  "villages": {
    "total": 8234,
    "total_population": 28456000,
    "st_population": 12345000,
    "total_households": 4567000,
    "st_percentage": 43.3,
    "total_claims": 125000,
    "granted_claims": 92450,
    "pending_claims": 18230,
    "claims_granted_rate": 73.96,
    "ifr_granted_area": 1234567.50,
    "cfr_granted_area": 642000.00,
    "total_granted_area": 1876567.50,
    "by_state": {"MP": 3482, "CG": 2156, ...},
    "pvtg_villages": 1234,
    "pvtg_percentage": 14.98
  },
  "grievances": {
    "total": 4520,
    "open": 1230,
    "pending": 1850,
    "resolved": 1440,
    "resolution_rate": 31.86,
    "by_priority": {"CRITICAL": 450, "HIGH": 1200, "MEDIUM": 2100, "LOW": 770},
    "by_category": {"rejection-dispute": 890, ...},
    "avg_resolution_days": 21.5
  },
  "officers": {
    "total": 456,
    "by_state": {"MP": 120, "CG": 95, ...},
    "total_claims_handled": 125000,
    "avg_claims_per_officer": 274.1,
    "pending_actions": 8234,
    "recently_active": 389,
    "active_percentage": 85.3
  },
  "timeline": [
    {"month": "2026-01", "claims_received": 8500, "claims_granted": 6200, ...},
    ...
  ]
}
```

**Impact:** 🔴 **CRITICAL**
- Frontend `useDashboardData()` hook expects `data?.nationalStats` → undefined
- Pages accessing `data?.stateStats` → undefined
- Form will fail with type errors
- Must transform backend response to match frontend schema

---

### ⚠️ 2. Claims List Pagination Response - SHAPE MISMATCH

#### Frontend Expects (from api-client.getClaims())
```typescript
{
  data?: FRAClaim[];  // Array directly or wrapped
  status: number;
  error?: string;
}
```

#### Backend Returns (ClaimsPaginatedResponse)
```python
{
  "data": [
    {
      "id": "C-2026-MP-001",
      "claimantName": "...",
      ... // ClaimRead fields
    },
    ...
  ],
  "total": 125000,
  "page": 1,
  "limit": 10,
  "pages": 12500,
  "filters": {"state": "MP", "status": "APPROVED"}
}
```

**Impact:** ⚠️ **MEDIUM**
- Frontend code expects `response.data.items` or similar
- Backend wraps in pagination metadata
- Pagination info not being used by frontend components
- Type mismatch on how data is accessed

---

### ⚠️ 3. Claim Object - Field Name Transformation

#### Frontend Expects
```typescript
{
  id: string;
  claimantName: string;
  gpsCoordinates?: { lat: number; lng: number };
  status: ClaimStatus;
  // ... other snake_case fields as camelCase
}
```

#### Backend Returns (with Pydantic aliases)
```python
class ClaimRead:
  id: str = Field(alias="claim_id")  # ← Returns as "claim_id"
  claimantName: str = Field(alias="claimant_name")  # ← Already aliased
  gpsLat: float | None = Field(alias="gps_lat")
  gpsLng: float | None = Field(alias="gps_lng")
  
  @computed_field
  @property
  def gpsCoordinates(self) -> dict[str, float] | None:  # ← Computed field
    return {"lat": self.gpsLat, "lng": self.gpsLng}
```

**Impact:** ⚠️ **MEDIUM**
- Pydantic aliases should handle snake_case → camelCase transformation
- `ConfigDict(from_attributes=True, populate_by_name=True)` should work
- BUT: computed fields may not serialize properly if backend doesn't use `model_dump(by_alias=True)`
- Frontend may receive `gpsLat`/`gpsLng` directly instead of `gpsCoordinates`

---

### ✅ 4. Village Object - CORRECT (With Caveat)

#### Frontend Expects
```typescript
{
  gpsCenter: { lat: number; lng: number };
  assets: VillageAssets;
  schemeEnrollments: SchemeEnrollment[];
}
```

#### Backend Returns
```python
class VillageRead:
  @computed_field
  @property
  def gpsCenter(self) -> dict[str, float] | None:
    return {"lat": self.gpsLat, "lng": self.gpsLng}
```

**Impact:** ✅ **OK - IF backend serializes computed_field**
- Depends on whether backend calls `model_dump()` with proper config
- If not serializing computed fields, frontend gets struct without `gpsCenter`

---

### ⚠️ 5. Grievance Object - Timestamp Format Mismatch

#### Frontend Expects
```typescript
createdAt: string;      // ISO format "2026-02-23T10:30:00Z"
lastUpdated: string;    // ISO format
```

#### Backend Returns
```python
createdAt: datetime = Field(alias="created_at")  # Python datetime object
lastUpdated: datetime | None = Field(alias="last_updated")
```

**Problem:** datetime objects serialize to different formats
- Pydantic may return: `"2026-02-23T10:30:00+00:00"` (with timezone)
- Frontend may expect: `"2026-02-23T10:30:00Z"` (Zulu time)
- Components using `.toLocaleString()` may break with timezone offset

**Impact:** ⚠️ **LOW-MEDIUM** (UI formatting issue, not data loss)

---

### ❌ 6. Grievance `daysOpen` Field - Missing Calculation

#### Frontend Expects
```typescript
daysOpen: number;  // Calculated in response
```

#### Backend Model
```python
days_open: int = Field(alias="days_open")  # Stored in DB
```

**Problem:** Backend returns stored value, doesn't auto-calculate
- If DB doesn't update `days_open` regularly, frontend shows stale info
- Each request needs fresh calculation: `(now - filed_date).days`

**Impact:** ⚠️ **LOW** (UI display issue)

---

### ❌ 7. Officer Object - GPS Location Missing

#### Frontend Expects
```typescript
gpsLocation?: { lat: number; lng: number };
```

#### Backend Returns (OfficerRead)
```python
# No GPS fields at all - not in schema
```

**Impact:** ⚠️ **MEDIUM**
- Feature for field officer location tracking won't work
- Backend model doesn't have GPS fields
- Maps won't show officer positions

---

## API Response Wrapper Inconsistency

### Frontend API Client Returns
```typescript
interface ApiResponse<T> {
  data?: T;      // Actual response data
  error?: string;
  status: number;
}
```

### But Methods Like `getClaims()` Return Backend Response Directly
```typescript
// In request method:
const data = await response.json();
return { data, status: response.status };  // ← data is the full response

// So apiClient.getClaims() returns:
{
  data: {
    data: [claims...],   // ← Nested!
    total: 125000,
    ...
  },
  status: 200
}
```

**Impact:** ⚠️ **MEDIUM**
- Frontend must access `response.data.data` (double nesting)
- This is likely causing bugs in pages accessing claims

---

## Database Type Mismatches

### 1. Status Fields - Enum vs String
**Frontend:** `ClaimStatus = "received" | "frc-verified" | "granted"` (lowercase, hyphenated)  
**Backend:** May store as UPPERCASE or different format (RECEIVED, FRC_VERIFIED, GRANTED)  
**Frontend Queries:** `getClaims({ status: "approved" })` won't match DB value "APPROVED"

### 2. Dates - String vs ISO Format
**Frontend:** Passes `"2026-02-23"`  
**Backend:** Stores as datetime, may return with time component `"2026-02-23T00:00:00Z"`

### 3. Boolean Fields - True/false vs 1/0
**Frontend:** Expects boolean `true/false`  
**Backend:** May store/return as 0/1 from database

---

## Query Parameter Mismatches

| API Call | Frontend Sends | Backend Expects | Issue |
|----------|---|---|---|
| `getClaims({status})` | `status: ["frc-verified", "sdlc-approved"]` (array) | Expects `status=frc-verified` (single value) | ❌ Array not handled; backend needs status filter enhancement |
| `getClaims({village})` | `village: "Badel Khas"` | Parameter not in endpoint | ❌ Village filter missing; needs query param support |
| `getClaims({patta})` | `patta: "PAT-2026-001"` | Parameter not in endpoint | ❌ Patta search missing |
| `getVillages()` | None | Expects state/district | ✅ OK |
| `getGrievances()` | `priority: "CRITICAL"` | Expects lowercase? | ⚠️ Unclear (check DB storage) |

---

## Auth Token Header Format

### Frontend Sends
```typescript
headers['Authorization'] = `Bearer ${token}`;
```

### Backend Expects (FastAPI with depends)
```python
# If using OAuth2PasswordBearer:
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

**Status:** ✅ **OK** - Standard Bearer token format

---

## Missing Response Fields

### Pages Expecting These Fields - NOT in Backend Response

| Field | Expected By | Status |  
|-------|-----------|--------|
| `datasets.dajguaInterventions` | `/national-dashboard`, `/state/*/dajgua` | 🔴 NOT in `/dashboard/summary` |
| `datasets.dssRecommendations` | `/dss`, `/district/*/dss` | 🔴 NOT in response |
| `datasets.forestFireAlerts` | `/national-dashboard/fire-alerts` | 🔴 NOT in response |
| `datasets.monthlyProgress` | `/analytics` | 🔴 NOT in response |
| `datasets.ndviTrend` | `/analytics/ndvi` | 🔴 NOT in response |

**Impact:** 🔴 **CRITICAL** - Dashboard pages will break trying to access undefined data

---

## Fix Priority Matrix

### 🔴 CRITICAL (Breaks pages immediately)
1. ✅ Dashboard Summary schema mismatch - transform backend response in api-client layer
2. ✅ Add missing datasets fields to backend `/dashboard/summary`
3. ✅ Fix nested data wrapping (response.data.data)
4. ✅ Claims pagination response format

### ⚠️ MEDIUM (Breaks specific features)
5. GPS location in officer records
6. Village GPS coordinates serialization
7. Status field case/format consistency
8. Multiple status filters support

### 🟡 LOW (UI display issues)
9. DateTime format standardization
10. Grievance daysOpen auto-calculation
11. Timestamp timezone handling

---

## Recommended Fix Approach

### Option A: Transform in Frontend (Quick Fix)
- Create adapter functions in `api-client.ts` to transform backend responses
- Pros: No backend changes needed, quick deployment
- Cons: Maintenance burden, type safety issues

### Option B: Standardize Backend (Correct Fix)
- Create proper response DTOs in backend
- Add response validators ensuring schema compliance
- Update aggregation_service to return DashboardSummary-compatible structure
- Pros: Clean, maintainable, type-safe
- Cons: More work, requires backend restart

### Option C: Hybrid (Recommended)
- Backend provides proper schema
- Frontend layer adds error handling for malformed responses
- Api-client validates and transforms any edge cases

---

## Immediate Action Items

1. **Update backend** `/dashboard/summary` to return:
   - Properly structured `nationalStats` (not flattened `claims`)
   - Properly structured `stateStats` array
   - Include `datasets` with interventions, recommendations, etc.

2. **Update frontend** `api-client.ts`:
   - Add transformation for paginated list responses
   - Fix double-nesting issue in ApiResponse wrapper
   - Add type guards for optional fields

3. **Add query parameter support**:
   - Backend: Support `status` array parameter
   - Backend: Add `village`, `patta` filters to claims endpoint
   - Frontend: Always include filters in requests

4. **Fix serialization**:
   - Ensure computed_field values serialize in Pydantic responses
   - Ensure datetime values use ISO 8601 format with Z suffix
   - Ensure boolean values serialize as true/false, not 1/0

---

## Testing Checklist

- [ ] Request `/api/v1/dashboard/summary`, verify contains `nationalStats`, `stateStats`, `datasets`
- [ ] Request `/api/v1/claims?page=1&limit=10`, verify response format matches pagination schema
- [ ] Request `/api/v1/villages/VILLAGE-CODE`, verify `gpsCenter` computed field present
- [ ] Request `/api/v1/grievances`, verify `createdAt` is ISO format with Z
- [ ] Test filtering: `/api/v1/claims?state=MP&status=approved`
- [ ] Test Auth: Request with `Authorization: Bearer {token}`, verify 200 vs 401

---

**Status**: PHASE 3 MISMATCH ANALYSIS COMPLETE ✅  
**Recommendation**: Proceed with Option C (Hybrid fix)  
**Est. Implementation Time**: 2 hours backend + 1.5 hours frontend


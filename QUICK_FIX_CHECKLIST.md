# 🔧 QUICK FIX CHECKLIST - Critical Path to MVP

## ⛔ BLOCKER: Database Tables Missing (1 Day to Fix)

### Step 1: Create Missing Tables
Run these SQL commands in `fra_documents` database:

```sql
-- 1. USERS TABLE (required for auth)
CREATE TABLE users (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255) NOT NULL,
  picture VARCHAR(512),
  provider VARCHAR(32) NOT NULL DEFAULT 'google',
  last_login DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_email (email)
);

-- 2. VILLAGES TABLE
CREATE TABLE villages (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  code VARCHAR(64) NOT NULL UNIQUE,
  name VARCHAR(255) NOT NULL,
  gram_panchayat VARCHAR(255),
  block VARCHAR(255),
  district VARCHAR(255) NOT NULL,
  state VARCHAR(8) NOT NULL,
  population INT,
  st_population INT,
  total_households INT,
  pvtg_present BOOLEAN DEFAULT FALSE,
  tribal_groups JSON,
  total_claims INT DEFAULT 0,
  granted_claims INT DEFAULT 0,
  pending_claims INT DEFAULT 0,
  rejected_claims INT DEFAULT 0,
  ifr_granted_area FLOAT DEFAULT 0,
  cfr_granted_area FLOAT DEFAULT 0,
  cr_granted_area FLOAT DEFAULT 0,
  saturation_score INT DEFAULT 0,
  gps_lat FLOAT,
  gps_lng FLOAT,
  assets JSON,
  scheme_enrollments JSON,
  last_satellite_update VARCHAR(64),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_code (code),
  INDEX idx_state (state),
  INDEX idx_district (district)
);

-- 3. OFFICERS TABLE
CREATE TABLE officers (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  officer_id VARCHAR(64) NOT NULL UNIQUE,
  name VARCHAR(255) NOT NULL,
  designation VARCHAR(64) NOT NULL,
  state VARCHAR(8),
  district VARCHAR(255),
  block VARCHAR(255),
  mobile VARCHAR(32) NOT NULL,
  email VARCHAR(255) NOT NULL,
  last_active DATETIME NOT NULL,
  total_claims_handled INT DEFAULT 0,
  pending_actions INT DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_officer_id (officer_id),
  INDEX idx_state (state),
  INDEX idx_district (district)
);

-- 4. CLAIMS TABLE
CREATE TABLE claims (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  claim_id VARCHAR(64) NOT NULL UNIQUE,
  claimant_name VARCHAR(255) NOT NULL,
  claimant_aadhaar VARCHAR(32),
  village_name VARCHAR(255) NOT NULL,
  village_code VARCHAR(64) NOT NULL,
  gram_panchayat VARCHAR(255),
  block VARCHAR(255),
  district VARCHAR(255) NOT NULL,
  state VARCHAR(8) NOT NULL,
  claim_type VARCHAR(8) NOT NULL,
  form_number VARCHAR(32),
  area_acres FLOAT NOT NULL,
  survey_khasra_no VARCHAR(64),
  claim_date DATE NOT NULL,
  verification_date DATE,
  decision_date DATE,
  status VARCHAR(32) NOT NULL,
  rejection_reason VARCHAR(1000),
  patte_number VARCHAR(128),
  patte_issued_date DATE,
  tribal_group VARCHAR(128),
  is_pvtg BOOLEAN DEFAULT FALSE,
  notes VARCHAR(512),
  gps_lat FLOAT,
  gps_lng FLOAT,
  boundary_geojson JSON,
  scanned_doc_url VARCHAR(512),
  ocr_data JSON,
  assigned_officer_id VARCHAR(64),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_claim_id (claim_id),
  INDEX idx_claim_state (state),
  INDEX idx_claim_district (district),
  INDEX idx_claim_village (village_code),
  INDEX idx_claim_status (status),
  INDEX idx_assigned_officer (assigned_officer_id)
);

-- 5. GRIEVANCES TABLE
CREATE TABLE grievances (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  grievance_id VARCHAR(64) NOT NULL UNIQUE,
  claimant_name VARCHAR(255) NOT NULL,
  claim_id VARCHAR(64),
  village_name VARCHAR(255) NOT NULL,
  block VARCHAR(255),
  district VARCHAR(255) NOT NULL,
  state VARCHAR(8) NOT NULL,
  category VARCHAR(64) NOT NULL,
  status VARCHAR(32) NOT NULL,
  priority VARCHAR(16) NOT NULL,
  assigned_officer_id VARCHAR(64),
  assigned_to VARCHAR(255),
  description VARCHAR(1000) NOT NULL,
  filed_date DATE,
  last_updated DATETIME,
  days_open INT DEFAULT 0,
  resolution VARCHAR(1000),
  source VARCHAR(64),
  channel VARCHAR(64),
  mobile VARCHAR(32),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_grievance_id (grievance_id),
  INDEX idx_state (state),
  INDEX idx_status (status),
  INDEX idx_priority (priority)
);

-- 6. DATA_BLOBS TABLE (for cache/aggregations)
CREATE TABLE data_blobs (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  key VARCHAR(128) NOT NULL UNIQUE,
  description VARCHAR(512),
  payload JSON NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_key (key)
);

-- Verify creation
SHOW TABLES;
```

### Step 2: Verify Tables Created
```sql
use fra_documents;
SELECT table_name FROM information_schema.tables 
WHERE table_schema='fra_documents' 
ORDER BY table_name;
```

Should show:
- ✓ users
- ✓ claims
- ✓ officers
- ✓ villages
- ✓ grievances
- ✓ data_blobs
- ✓ master_documents (existing)
- ✓ doc_claim_* (existing)
- ✓ doc_title_* (existing)

---

## ❌ BROKEN ENDPOINTS (Fix After Database)

These will crash until tables exist:

| Endpoint | Status | Test Command |
|----------|--------|---|
| `POST /api/v1/auth/google/callback` | ❌ CRASHES | `curl -X GET "http://localhost:8000/api/v1/auth/google/login"` |
| `GET /api/v1/claims` | ❌ CRASHES | `curl http://localhost:8000/api/v1/claims` |
| `GET /api/v1/villages` | ❌ CRASHES | `curl http://localhost:8000/api/v1/villages` |
| `GET /api/v1/officers` | ❌ CRASHES | `curl http://localhost:8000/api/v1/officers` |
| `GET /api/v1/grievances` | ❌ CRASHES | `curl http://localhost:8000/api/v1/grievances` |
| `GET /api/v1/dashboard/summary` | ❌ CRASHES | `curl http://localhost:8000/api/v1/dashboard/summary` |

After running SQL above, these will return `[]` (empty list) instead of error.

---

## 🔴 MOCK DATA LOCATIONS (Remove These)

Files using hardcoded data instead of API:

| File | Data | Replace With |
|------|------|---|
| [src/app/gram-sabha/dashboard/page.tsx](src/app/gram-sabha/dashboard/page.tsx) | SAMPLE_VILLAGES, SAMPLE_CLAIMS | `getClaims()`, `getVillages()` |
| [src/app/mera-patta/page.tsx](src/app/mera-patta/page.tsx) | SAMPLE_CLAIMS, SAMPLE_GRIEVANCES | `getClaims()`, `getGrievances()` |
| [src/app/dss/page.tsx](src/app/dss/page.tsx) | DSS_RECOMMENDATIONS | `getDSSRecommendations()` |
| [src/app/digitization/page.tsx](src/app/digitization/page.tsx) | mockDocs | `listDocuments()` |

---

## ⚙️ PLACEHOLDER PAGES (Replace With Real UI)

| Route | File | Action |
|-------|------|--------|
| `/mera-patta/schemes` | [src/app/mera-patta/schemes/page.tsx](src/app/mera-patta/schemes/page.tsx) | Remove PlaceholderPage, build real UI |
| `/state/[state]/schemes` | [src/app/state/[stateSlug]/schemes/page.tsx](src/app/state/[stateSlug]/schemes/page.tsx) | Remove PlaceholderPage, build real UI |
| `/state/[state]/reports` | [src/app/state/[stateSlug]/reports/page.tsx](src/app/state/[stateSlug]/reports/page.tsx) | Remove PlaceholderPage, build real UI |
| `/state/[state]/claims` | [src/app/state/[stateSlug]/claims/page.tsx](src/app/state/[stateSlug]/claims/page.tsx) | Remove PlaceholderPage, build real UI |
| `/state/[state]/dajgua` | [src/app/state/[stateSlug]/dajgua/page.tsx](src/app/state/[stateSlug]/dajgua/page.tsx) | Remove PlaceholderPage, build real UI |

---

## 🔐 AUTH FLOW TEST

After database tables created, test OAuth:

```bash
# 1. Get Google login URL
curl http://localhost:8000/api/v1/auth/google/login

# 2. Visit the URL in browser, authorize
# 3. Copy the code parameter from redirect
# 4. Test callback endpoint
curl "http://localhost:8000/api/v1/auth/google/callback?code=XXXXXX"

# Should return: {"token": "...", "user": {...}}
```

---

## 🧪 BASIC ENDPOINT TESTS

After tables created, test these:

```bash
# Health check (always works)
curl http://localhost:8000/health

# Get claims (empty list initially)
curl http://localhost:8000/api/v1/claims

# Get villages (empty list initially)
curl http://localhost:8000/api/v1/villages

# Get officers (empty list initially)
curl http://localhost:8000/api/v1/officers

# Get dashboard summary (depends on data_blobs table)
curl http://localhost:8000/api/v1/dashboard/summary
```

---

## 📋 IMPLEMENTATION ORDER

### Day 1: Database (4 hours)
1. [ ] Create 6 missing tables (1 hr)
2. [ ] Verify tables with queries (30 min)
3. [ ] Seed test data (30 min)
4. [ ] Test all tables queryable (30 min)

### Day 2-3: Backend Services (16 hours)
1. [ ] Verify auth works with users table
2. [ ] Implement search_claims() service
3. [ ] Implement list_grievances() service
4. [ ] Implement dashboard_snapshot() aggregation
5. [ ] Test all endpoints return data
6. [ ] Add error handling

### Day 4-5: Frontend Integration (16 hours)
1. [ ] Remove SAMPLE_* imports
2. [ ] Add api calls to each page
3. [ ] Add loading states
4. [ ] Add error boundaries
5. [ ] Test with real backend data
6. [ ] Fix any type mismatches

### Day 6-7: Testing & Polish (16 hours)
1. [ ] End-to-end user flows
2. [ ] Error scenario testing
3. [ ] Performance testing
4. [ ] Security review
5. [ ] Documentation

---

## 🚀 MINIMUM VIABLE PRODUCT (MVP)

To launch, these must work:

- [ ] User can log in with Google OAuth
- [ ] User can see their claims (from database)
- [ ] User can see village data (from database)
- [ ] User can file a grievance (saved to DB)
- [ ] Admin can view dashboard (pulls from DB)
- [ ] Admin can assign officers to claims
- [ ] System shows real data, not mocks

---

## ✅ VERIFICATION CHECKLIST

Run these to verify status:

### Database Status
```sql
use fra_documents;
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM claims;
SELECT COUNT(*) FROM villages;
SELECT COUNT(*) FROM officers;
SELECT COUNT(*) FROM grievances;
SELECT COUNT(*) FROM data_blobs;
```

### Backend Status
```bash
# Test claims endpoint
curl http://localhost:8000/api/v1/claims | jq '.'

# Test dashboard
curl http://localhost:8000/api/v1/dashboard/summary | jq '.'

# Test auth
curl http://localhost:8000/api/v1/auth/me
```

### Frontend Status
```bash
# Should see real data (not SAMPLE_VILLAGES)
npm run dev
# Navigate to /gram-sabha/dashboard
# Should show actual villages from database
```

---

## 📞 SUPPORT

If you encounter issues:

1. **Database creation fails:** Check MySQL credentials, ensure `fra_documents` DB exists
2. **Backend endpoints still crash:** Restart backend server after creating tables
3. **Frontend still shows mock data:** Hard refresh browser, check Network tab in DevTools
4. **Auth callback 500:** Verify GOOGLE_CLIENT_ID and GOOGLE_REDIRECT_URI correct

---

Last updated: 2026-02-23

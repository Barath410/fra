# PHASE 2: Route Verification & API Mapping Report
**Generated:** February 23, 2026  
**Status:** Backend API verification against 53 frontend routes

---

## Backend Endpoints Available ✅

### Authentication Endpoints (`/auth`)
- ✅ `GET /auth/google/login` - OAuth login URL
- ✅ `GET /auth/google/callback` - OAuth callback handler
- ✅ `GET /auth/me` - Current user profile
- ✅ `POST /auth/logout` - Logout

### Dashboard Endpoints (`/dashboard`)
- ✅ `GET /dashboard/summary` - National dashboard aggregates
- ✅ `GET /dashboard/state/{state}` - State-level snapshot
- ✅ `GET /dashboard/district/{state}/{district}` - District-level snapshot
- ✅ `GET /dashboard/overview` - Dashboard overview (national or state-filtered)
- ✅ `GET /dashboard/cache/stats` - Cache statistics
- ✅ `POST /dashboard/cache/refresh` - Refresh cache
- ✅ `DELETE /dashboard/cache/clear` - Clear cache

### Claims Endpoints (`/claims`)
- ✅ `GET /claims?state=&district=&status=&page=&limit=` - List claims with filters
- ✅ `GET /claims/{claim_id}` - Get specific claim
- ✅ `POST /claims` - Create new claim (requires auth)

### Villages Endpoints (`/villages`)
- ✅ `GET /villages?state=&district=&page=&limit=` - List villages with filters
- ✅ `GET /villages/{code}` - Get specific village

### Grievances Endpoints (`/grievances`)
- ✅ `GET /grievances?state=&district=&status=&priority=&page=&limit=` - List grievances
- ✅ `GET /grievances/{grievance_id}` - Get specific grievance
- ✅ `POST /grievances` - Create new grievance
- ✅ `PATCH /grievances/{grievance_id}` - Update grievance

### Officers Endpoints (`/officers`)
- ✅ `GET /officers?state=&district=&page=&limit=` - List officers
- ✅ `GET /officers/{officer_id}` - Get specific officer

### Documents Endpoints (`/documents`)
- ✅ `POST /documents/upload-document` - Upload and ingest document

---

## Frontend Routes vs Backend API Mapping

### 🏠 Home & Authentication Routes
| Route | Purpose | Required API | Status |
|-------|---------|--------------|--------|
| `/` | Home/login page | `/auth/*` | ✅ READY |
| `/logout` | Logout | `/auth/logout` | ✅ READY |

### 📊 National Dashboard Routes (MOTA Nodal Officer)
| Route | Purpose | Required API | Status |
|-------|---------|--------------|--------|
| `/national-dashboard` | National overview | `/dashboard/summary`, `/dashboard/overview` | ✅ READY |
| `/national-dashboard/fire-alerts` | Fire alerts monitoring | ❌ MISSING | 🔴 NEEDS `GET /alerts/fire` |
| `/national-dashboard/dajgua` | DA-JGUA tracking | ❌ MISSING | 🔴 NEEDS `GET /schemes/dajgua` |
| `/national-dashboard/documents` | Document management | ✅ `/documents/upload-document` | ✅ READY |

### 🏛️ State Dashboard Routes (State Commissioner)
| Route | Purpose | Required API | Status |
|-------|---------|--------------|--------|
| `/state/[stateSlug]/dashboard` | State dashboard | `/dashboard/state/{state}` | ✅ READY |
| `/state/[stateSlug]/claims` | State claims | `/claims?state=` | ✅ READY |
| `/state/[stateSlug]/schemes` | Scheme convergence | ❌ MISSING | 🔴 NEEDS `GET /schemes?state=` |
| `/state/[stateSlug]/reports` | State reports | ❌ MISSING | 🔴 NEEDS `GET /reports?state=` |
| `/state/[stateSlug]/dajgua` | DA-JGUA state tracking | ❌ MISSING | 🔴 NEEDS `GET /schemes/dajgua?state=` |

### 🏘️ Gram Sabha Routes (Village Leader)
| Route | Purpose | Required API | Status |
|-------|---------|--------------|--------|
| `/gram-sabha/dashboard` | Village dashboard | `/dashboard/overview`, `/villages/{code}` | ✅ READY |
| `/gram-sabha/claims` | Village claims | `/claims?village=` | ⚠️ PARTIAL |
| `/gram-sabha/new-claim` | Create new claim | `/claims` (POST) | ✅ READY |
| `/gram-sabha/grievance` | File grievance | `/grievances` (POST) | ✅ READY |
| `/gram-sabha/village` | Village info | `/villages/{code}` | ✅ READY |
| `/gram-sabha/map` | Village map | `/villages/{code}` | ✅ READY |

### 👮 Field Officer Routes (BLCO/FO)
| Route | Purpose | Required API | Status |
|-------|---------|--------------|--------|
| `/field-officer/dashboard` | FO dashboard | `/dashboard/district`, `/officers` | ✅ READY |
| `/field-officer/assignments` | Field assignments | ❌ MISSING | 🔴 NEEDS `GET /assignments` |
| `/field-officer/new-report` | Field verification | ❌ MISSING | 🔴 NEEDS `POST /field-reports` |
| `/field-officer/map` | Field visit map | `/villages?district=` | ✅ READY |
| `/field-officer/notifications` | Notifications | ❌ MISSING | 🔴 NEEDS `GET /notifications` |

### ⚖️ SDLC/DLC Routes (Claim Adjudicators)
| Route | Purpose | Required API | Status |
|-------|---------|--------------|--------|
| `/sdlc/dashboard` | SDLC queue | `/claims?status=` | ✅ READY |
| `/sdlc/adjudication` | Adjudicate claims | `/claims/{id}` (PATCH) | ⚠️ PARTIAL |
| `/sdlc/approved` | Approved claims | `/claims?status=approved` | ✅ READY |
| `/sdlc/rejected` | Rejected claims | `/claims?status=rejected` | ✅ READY |
| `/sdlc/ror` | Record of Rights | ❌ MISSING | 🔴 NEEDS `GET /ror` |
| `/sdlc/documents` | Claim documents | `/documents/*` | ✅ READY |

### 📍 District Dashboard Routes
| Route | Purpose | Required API | Status |
|-------|---------|--------------|--------|
| `/district/[districtId]/dashboard` | District overview | `/dashboard/district/{state}/{district}` | ✅ READY |
| `/district/[districtId]/claims` | District claims | `/claims?district=` | ✅ READY |
| `/district/[districtId]/alerts` | District alerts | ❌ MISSING | 🔴 NEEDS `GET /alerts?district=` |
| `/district/[districtId]/dss` | DSS recommendations | ❌ MISSING | 🔴 NEEDS `GET /dss?district=` |
| `/district/[districtId]/gaps` | Scheme gaps | ❌ MISSING | 🔴 NEEDS `GET /scheme-gaps?district=` |
| `/district/[districtId]/field-tracker` | Field officer tracking | ❌ MISSING | 🔴 NEEDS `GET /field-teams?district=` |

### 🔍 Analytics & Research Routes
| Route | Purpose | Required API | Status |
|-------|---------|--------------|--------|
| `/analytics` | Analytics portal | `/dashboard/summary`, datasets | ✅ READY |
| `/analytics/atlas` | FRA atlas map | `/villages` with geojson | ⚠️ PARTIAL |
| `/analytics/ndvi` | Vegetation index trends | ❌ MISSING | 🔴 NEEDS `GET /ndvi-trends` |
| `/analytics/builder` | Custom report builder | ❌ MISSING | 🔴 NEEDS `GET /datasets` |
| `/analytics/download` | Dataset downloads | ❌ MISSING | 🔴 NEEDS `GET /datasets/download` |

### 🆘 Grievance & Support Routes
| Route | Purpose | Required API | Status |
|-------|---------|--------------|--------|
| `/grievances` | Grievance center | `/grievances?page=&limit=` | ✅ READY |
| `/notifications` | User notifications | ❌ MISSING | 🔴 NEEDS `GET /notifications` |
| `/help` | Help & FAQ | ❌ MISSING | 🟡 STATIC (no API needed) |

### 🎛️ Admin & Settings Routes
| Route | Purpose | Required API | Status |
|-------|---------|--------------|--------|
| `/profile` | User profile | `/auth/me` | ✅ READY |
| `/settings` | App settings | ❌ MISSING | 🟡 STATIC (local storage) |
| `/digitization` | Bulk document digitization | `/documents/upload-document` (batch) | ⚠️ PARTIAL |
| `/mera-patta` | Individual patta search | `/claims?patta=` | ⚠️ PARTIAL |
| `/mera-patta/status` | Patta status tracking | `/claims/{id}` | ✅ READY |
| `/mera-patta/download` | Download patta certificate | `/documents/export` | ❌ MISSING |
| `/mera-patta/schemes` | Schemes for patta holders | `/schemes?eligible=true` | ❌ MISSING |

### 🤖 Decision Support Routes
| Route | Purpose | Required API | Status |
|-------|---------|--------------|--------|
| `/dss` | DSS recommendations | ❌ MISSING | 🔴 NEEDS `GET /dss` |
| `/atlas` | Interactive FRA map | `/villages` with geospatial | ⚠️ PARTIAL |

### 📋 Navigation Routes
| Route | Purpose | Required API | Status |
|-------|---------|--------------|--------|
| `/sitemap` | Site map | N/A (static) | ✅ READY |
| `/dashboard-template` | Template/reference | N/A (static) | ✅ READY |

---

## Gap Analysis Summary

### 🔴 Missing Backend Endpoints (Must Implement)
1. **Alerts System** - `/alerts/fire`, `/alerts?district=`, `/alerts?state=`
2. **Schemes API** - `/schemes`, `/schemes/dajgua`, `/schemes?state=`
3. **Reports API** - `/reports?state=`
4. **DSS Engine** - `/dss`, `/dss?district=`, `/dss?state=`
5. **Field Management** - `/assignments`, `/field-reports`, `/field-teams`
6. **Notifications** - `/notifications`
7. **Additional Endpoints**:
   - `/ror` - Record of Rights
   - `/scheme-gaps` - Scheme saturation gaps
   - `/ndvi-trends` - Vegetation health trends
   - `/datasets` - Dynamic dataset listings
   - `/documents/export` - Document export/download

### ⚠️ Partial Implementations (Need Query Parameter Extensions)
1. **Claims filtering** - Add `village=`, `patta=` parameters
2. **Villages filtering** - Add geospatial filtering, return geojson
3. **Documents** - Batch upload, export functionality

### ✅ Ready for Integration (14 Core Endpoints)
- `/auth/*` (login, callback, profile, logout)
- `/dashboard/summary`, `/dashboard/state/{state}`, `/dashboard/district/{state}/{district}`
- `/claims` (list, get, create)
- `/villages` (list, get)
- `/grievances` (list, get, create, patch)
- `/officers` (list, get)
- `/documents` (upload)

---

## Priority Implementation Order

### Phase 2A (Critical - Required for MVP)
- [ ] `/alerts/fire`, `/alerts?*` - Fire alert system
- [ ] `/schemes?*`, `/schemes/dajgua` - Scheme convergence
- [ ] `/dss` - Decision support recommendations
- [ ] `/notifications` - User notifications

### Phase 2B (High Priority - Needed for demo)
- [ ] `/reports?state=` - State report generation
- [ ] `/assignments`, `/field-reports` - Field officer management
- [ ] `/ror` - Record of Rights generation
- [ ] `/ndvi-trends` - Environmental analytics

### Phase 2C (Medium Priority - Enhanced features)
- [ ] `/scheme-gaps` - Saturation gap analysis
- [ ] `/field-teams` - Field team tracking
- [ ] `/datasets`, `/datasets/download` - Dataset export
- [ ] `/documents/export` - Certificate generation

### Phase 2D (Lower Priority - Nice to have)
- Query parameter extensions for claims, villages
- Batch document processing
- Advanced filtering and search

---

## Database Tables Status

## Core Tables (✅ Exist)
- `users` - User accounts
- `claims` - FRA claims
- `villages` - Village data
- `grievances` - Grievance tickets
- `officers` - Government officers

## Missing Tables (Need to Create)
- `alerts` or `astrohem_fires` - Fire/natural disaster alerts
- `schemes` - Government scheme data
- `scheme_enrollment` - Beneficiary scheme enrollment
- `dss_recommendations` - DSS algorithm outputs
- `field_assignments` - FO work assignments
- `field_reports` - FO verification reports
- `notifications` - User notifications
- `ndvi_data` - Satellite vegetation indices
- `datasets` - Available data exports
- `rights_of_record` - ROR documents

---

## Next Steps

1. **PHASE 2 Completion**: Finalize endpoint mapping (this document)
2. **PHASE 3**: Implement missing 13+ endpoints in backend
3. **PHASE 4**: Add JWT authentication headers to all API calls
4. **PHASE 5**: Seed production data in database
5. **PHASE 6**: End-to-end integration testing

---

**Status**: PHASE 2 ROUTE MAPPING COMPLETE ✅
**Ready for PHASE 3**: Backend endpoint implementation


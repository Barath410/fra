"""
PRODUCTION-READY BACKEND SERVICES

Fully implemented endpoints with pagination, filtering, and error handling
"""

# =============================================================================
# ENDPOINTS
# =============================================================================

"""
1. GET /api/v1/claims
   - List all claims with pagination
   - Filters: state, district, status
   - Response: Paginated claims list

2. GET /api/v1/claims/{claim_id}
   - Get specific claim
   - Response: Single claim details

3. POST /api/v1/claims
   - Create new claim (auth required)

4. GET /api/v1/villages
   - List all villages with pagination
   - Filters: state, district
   - Response: Paginated villages list

5. GET /api/v1/villages/{code}
   - Get specific village
   - Response: Single village details

6. GET /api/v1/officers
   - List all officers with pagination
   - Filters: state, district
   - Response: Paginated officers list

7. GET /api/v1/officers/{officer_id}
   - Get specific officer
   - Response: Single officer details

8. GET /api/v1/grievances
   - List all grievances with pagination
   - Filters: state, district, status, priority
   - Response: Paginated grievances list

9. GET /api/v1/grievances/{grievance_id}
   - Get specific grievance
   - Response: Single grievance details

10. POST /api/v1/grievances
    - Create new grievance

11. PATCH /api/v1/grievances/{grievance_id}
    - Update grievance status, priority, or resolution
"""

# =============================================================================
# PAGINATION PARAMETERS
# =============================================================================

"""
All list endpoints support:
- page: int (default 1, minimum 1)
- limit: int (default 20, minimum 1, maximum 100)

Examples:
GET /api/v1/claims?page=1&limit=20
GET /api/v1/villages?page=2&limit=50
GET /api/v1/officers?page=1&limit=100
GET /api/v1/grievances?page=3&limit=15
"""

# =============================================================================
# FILTERING PARAMETERS
# =============================================================================

"""
CLAIMS:
- state: Filter by state code (e.g., 'MP', 'CG', 'MH')
- district: Filter by district name
- status: Filter by status (PENDING, APPROVED, REJECTED)

Examples:
GET /api/v1/claims?state=MP
GET /api/v1/claims?state=MP&status=APPROVED
GET /api/v1/claims?district=Mandla&status=PENDING
GET /api/v1/claims?state=MP&district=Mandla&status=APPROVED&page=2&limit=50

VILLAGES:
- state: Filter by state code
- district: Filter by district name

Examples:
GET /api/v1/villages?state=MP
GET /api/v1/villages?state=CG&district=Bastar
GET /api/v1/villages?district=Mandla&page=1&limit=25

OFFICERS:
- state: Filter by state code
- district: Filter by district name

Examples:
GET /api/v1/officers?state=MP
GET /api/v1/officers?district=Mandla
GET /api/v1/officers?state=CG&district=Bastar&page=1&limit=50

GRIEVANCES:
- state: Filter by state code
- district: Filter by district name
- status: Filter by status (OPEN, PENDING, RESOLVED)
- priority: Filter by priority (LOW, MEDIUM, HIGH, CRITICAL)

Examples:
GET /api/v1/grievances?state=MP
GET /api/v1/grievances?status=OPEN&priority=HIGH
GET /api/v1/grievances?state=MP&district=Mandla&status=OPEN&priority=CRITICAL&page=1&limit=20
"""

# =============================================================================
# RESPONSE FORMATS
# =============================================================================

"""
PAGINATED RESPONSE (List endpoints):
{
  "data": [
    { /* item 1 */ },
    { /* item 2 */ },
    ...
  ],
  "total": 150,           // Total number of items matching filters
  "page": 1,              // Current page
  "limit": 20,            // Items per page
  "pages": 8,             // Total number of pages
  "filters": {            // Applied filters
    "state": "MP",
    "status": "APPROVED",
    "district": null
  }
}

SINGLE ITEM RESPONSE (Get by ID endpoints):
{
  "id": "FRA-2026-MP-00001",
  "claimantName": "Ramesh Kumar",
  "state": "MP",
  "status": "APPROVED",
  ...
}

ERROR RESPONSE:
{
  "detail": "Claim not found"  // or specific error message
}
"""

# =============================================================================
# CURL EXAMPLES
# =============================================================================

"""
1. GET CLAIMS - First page with default limit:
   curl http://localhost:8000/api/v1/claims

2. GET CLAIMS - Second page with custom limit:
   curl http://localhost:8000/api/v1/claims?page=2&limit=50

3. GET CLAIMS - Filter by state and status:
   curl http://localhost:8000/api/v1/claims?state=MP&status=APPROVED

4. GET CLAIMS - Filter by multiple parameters:
   curl "http://localhost:8000/api/v1/claims?state=MP&district=Mandla&status=PENDING&page=1&limit=25"

5. GET CLAIM BY ID:
   curl http://localhost:8000/api/v1/claims/FRA-2026-MP-00001

6. GET VILLAGES - With pagination:
   curl http://localhost:8000/api/v1/villages?page=1&limit=20

7. GET VILLAGES - Filter by state:
   curl http://localhost:8000/api/v1/villages?state=CG

8. GET VILLAGE BY CODE:
   curl http://localhost:8000/api/v1/villages/VIL-MP-MAN-001

9. GET OFFICERS - Paginated:
   curl http://localhost:8000/api/v1/officers?page=1&limit=10

10. GET OFFICER BY ID:
    curl http://localhost:8000/api/v1/officers/OFF-MP-2024-001

11. GET GRIEVANCES - With filters:
    curl "http://localhost:8000/api/v1/grievances?state=MP&status=OPEN&priority=HIGH"

12. GET GRIEVANCE BY ID:
    curl http://localhost:8000/api/v1/grievances/GRV-2026-MP-00001

13. CREATE GRIEVANCE:
    curl -X POST http://localhost:8000/api/v1/grievances \\
      -H "Content-Type: application/json" \\
      -d '{
        "grievance_id": "GRV-2026-NEW-1",
        "claimant_name": "John Doe",
        "village_name": "Test Village",
        "district": "Mandla",
        "state": "MP",
        "category": "Delay",
        "status": "OPEN",
        "priority": "HIGH",
        "description": "Claim processing delayed"
      }'

14. UPDATE GRIEVANCE:
    curl -X PATCH http://localhost:8000/api/v1/grievances/GRV-2026-MP-00001 \\
      -H "Content-Type: application/json" \\
      -d '{
        "status": "RESOLVED",
        "priority": "CRITICAL",
        "resolution": "Issue resolved by officer"
      }'
"""

# =============================================================================
# PAGINATION LOGIC
# =============================================================================

"""
OFFSET CALCULATION:
  offset = (page - 1) * limit
  
  Page 1, Limit 20: offset = 0 (items 1-20)
  Page 2, Limit 20: offset = 20 (items 21-40)
  Page 3, Limit 20: offset = 40 (items 41-60)

TOTAL PAGES CALCULATION:
  total_pages = ceil(total_count / limit)
  total_pages = (total_count + limit - 1) // limit

  If total = 150, limit = 20: pages = (150 + 20 - 1) // 20 = 8
  If total = 100, limit = 25: pages = (100 + 25 - 1) // 25 = 4
  If total = 50, limit = 10: pages = (50 + 10 - 1) // 10 = 5
"""

# =============================================================================
# FRONTEND INTEGRATION
# =============================================================================

"""
NEXT.JS API CLIENT:

export const claimsAPI = {
  getClaims: async (state?: string, district?: string, status?: string, page = 1, limit = 20) => {
    const params = new URLSearchParams();
    if (state) params.append('state', state);
    if (district) params.append('district', district);
    if (status) params.append('status', status);
    params.append('page', page.toString());
    params.append('limit', limit.toString());
    
    const response = await fetch(`http://localhost:8000/api/v1/claims?${params}`);
    return response.json();
  },

  getClaim: async (claimId: string) => {
    const response = await fetch(`http://localhost:8000/api/v1/claims/${claimId}`);
    return response.json();
  },
};

// Usage:
const result = await claimsAPI.getClaims('MP', undefined, 'APPROVED', 1, 20);
console.log(result.data);      // Array of claims
console.log(result.total);     // Total count
console.log(result.pages);     // Total pages
console.log(result.page);      // Current page

REACT COMPONENT WITH PAGINATION:

export function ClaimsList() {
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(20);
  const [state, setState] = useState<string | undefined>();
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    claimsAPI.getClaims(state, undefined, undefined, page, limit).then(setData);
  }, [page, limit, state]);

  return (
    <div>
      <div>
        <input 
          placeholder="Filter by state" 
          onChange={(e) => { setState(e.target.value); setPage(1); }}
        />
        <select onChange={(e) => setLimit(parseInt(e.target.value))}>
          <option value={10}>10</option>
          <option value={20} selected>20</option>
          <option value={50}>50</option>
          <option value={100}>100</option>
        </select>
      </div>

      <table>
        <tbody>
          {data?.data?.map((claim: any) => (
            <tr key={claim.id}>
              <td>{claim.claimantName}</td>
              <td>{claim.state}</td>
              <td>{claim.status}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div>
        <button 
          onClick={() => setPage(p => Math.max(1, p - 1))}
          disabled={page === 1}
        >
          Previous
        </button>
        
        <span>Page {data?.page} of {data?.pages}</span>
        
        <button 
          onClick={() => setPage(p => (p < (data?.pages || 1) ? p + 1 : p))}
          disabled={page >= (data?.pages || 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
}
"""

# =============================================================================
# ERROR HANDLING
# =============================================================================

"""
ERROR CASES:

1. Invalid page number (< 1):
   → 422 Unprocessable Entity
   → Message: "ensure this value is greater than or equal to 1"

2. Invalid limit (< 1 or > 100):
   → 422 Unprocessable Entity
   → Message: "ensure this value is less than or equal to 100"

3. Item not found:
   → 404 Not Found
   → Message: "Claim not found" or "Village not found" etc.

4. Database error:
   → 500 Internal Server Error
   → Message: "Error listing claims: <error details>"

5. Duplicate item creation:
   → 400 Bad Request
   → Message: "Grievance with this ID already exists"

6. Query timeout:
   → 500 Internal Server Error
   → Message: "Error listing claims: <timeout details>"

All errors return JSON:
{
  "detail": "Error message here"
}
"""

# =============================================================================
# PERFORMANCE CONSIDERATIONS
# =============================================================================

"""
1. PAGINATION:
   - Always use pagination for list endpoints
   - Default limit of 20 items per page
   - Maximum 100 items per page to prevent abuse
   - Offset-based pagination (page number based)

2. FILTERING:
   - Filters applied before pagination
   - All filters use SQL equality (=) operator
   - Filters support null values (no filter applied if not provided)
   - Multiple filters use AND logic (all must match)

3. INDEXING:
   - Database includes indexes on:
     * state, district, status (for claims)
     * state, district (for villages, officers)
     * state, district, status, priority (for grievances)
   - Queries use indexes for fast filtering

4. SORTING:
   - Claims sorted by claim_date DESC (newest first)
   - Villages sorted by name ASC (alphabetical)
   - Officers sorted by last_active DESC (most recent first)
   - Grievances sorted by last_updated DESC (newest first)

5. RESPONSE SIZE:
   - Default limit: 20 items
   - Maximum limit: 100 items
   - Total metadata fields: 5 (data, total, page, limit, pages, filters)
   - Average response size: 5-50 KB per page

QUERY EXECUTION TIME:
   - Simple list (no filters): < 100ms
   - Filtered list: < 200ms
   - Single item fetch: < 50ms
   - Get by ID (all lists): O(1) vs O(n) for unfiltered
"""

# =============================================================================
# TESTING
# =============================================================================

"""
RUN TESTS:
  cd backend
  python -m pytest tests/test_services.py -v

SPECIFIC TEST:
  python -m pytest tests/test_services.py::TestClaimsEndpoint::test_get_claims_default_pagination -v

TEST COVERAGE:
  python -m pytest tests/test_services.py --cov=app.services --cov=app.api.endpoints

Tests include:
  ✓ Pagination with default values
  ✓ Pagination with custom values
  ✓ Filtering by state
  ✓ Filtering by district
  ✓ Filtering by status
  ✓ Filtering by multiple parameters
  ✓ Get by ID
  ✓ Get nonexistent item (404)
  ✓ Create new item
  ✓ Create duplicate item (400)
  ✓ Update item
  ✓ Response format validation
"""

# =============================================================================
# DEPLOYMENT CHECKLIST
# =============================================================================

"""
Before production deployment:

[ ] Database indexes created
    mysql> CREATE INDEX idx_state ON claims(state);
    mysql> CREATE INDEX idx_district ON claims(district);
    mysql> CREATE INDEX idx_status ON claims(status);
    ... (see seed_data.sql for all indexes)

[ ] All tests passing
    pytest tests/test_services.py -v

[ ] Pagination limits verified (min 1, max 100)

[ ] Error handling tested
    - Invalid parameters → 422
    - Not found → 404
    - Server error → 500

[ ] Performance tested with large dataset
    - 10,000+ claims
    - 5,000+ villages
    - Response time < 500ms

[ ] SQL injection tested
    - All queries use SQLAlchemy ORM (parameterized)
    - No raw SQL with string concatenation

[ ] Rate limiting configured (if needed)

[ ] CORS configured properly for frontend domain

[ ] Database connection pooling tested

[ ] Pagination works with 0 results

[ ] Response format consistent across all endpoints
"""

if __name__ == "__main__":
    print(__doc__)

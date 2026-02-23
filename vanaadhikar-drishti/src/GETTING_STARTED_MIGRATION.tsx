/**
 * 🚀 GETTING STARTED: Frontend Page Migration
 *
 * You're reading this because there are 40 pages remaining to migrate from mock data
 * to the production dashboard pattern. This guide gets you started in 2 minutes.
 *
 * TLDR:
 * 1. Pick a "quick win" page (26 available, 5 min each)
 * 2. Copy: src/app/dashboard-template/page.tsx → your-page-path
 * 3. Update: endpoint, filters, KPIs, list mapping (5 sections)
 * 4. Test: Load page, check network tab, verify data appears
 * 5. Done! Mark as complete
 *
 * Estimated total time for all 40 pages: ~5 hours
 * Recommended approach: Parallel work across team (multiple pages simultaneously)
 */

// ============================================================================
// STEP 1: UNDERSTAND THE PATTERN
// ============================================================================

/**
 * The production dashboard pattern consists of 5 files:
 *
 * ✓ src/hooks/use-dashboard-fetch.ts
 *   └─ Custom hook for data fetching with state management
 *   └─ Usage: const { data, loading, error, retry } = useDashboardFetch(...)
 *
 * ✓ src/components/dashboard-components.tsx
 *   └─ 6 reusable components: KPI, Filter, List, Container, EmptyState, etc
 *   └─ Usage: <DashboardKPIGrid />, <DashboardFilterBar />, <DashboardList />
 *
 * ✓ src/app/dashboard-template/page.tsx
 *   └─ Complete working example you can copy
 *   └─ Shows all patterns: KPIs, filters, list, error handling
 *
 * ✓ src/lib/api-client.ts
 *   └─ API client with methods: getClaims(), getVillages(), getOfficers(), etc
 *   └─ Auto-injects authentication token
 *
 * ✓ src/components/skeletons.tsx
 *   └─ Loading placeholders for better UX
 *   └─ Usage: <DataTableSkeleton />, <StatCardSkeleton />, etc
 */

// ============================================================================
// STEP 2: PICK YOUR FIRST PAGE
// ============================================================================

/**
 * QUICK WINS (26 pages, 5 minutes each):
 * All currently showing PlaceholderPage() - just replace with template!
 *
 * Easy starting pages:
 * 1. /analytics/download
 * 2. /analytics/ndvi
 * 3. /district/[districtId]/alerts
 * 4. /field-officer/assignments
 * 5. /gram-sabha/claims
 *
 * ... and 21 more (see DASHBOARD_STATUS_TRACKER.tsx for full list)
 *
 * PARTIAL PAGES (14 pages, 10-15 minutes each):
 * Already have apiClient but missing components/error UI
 * These are good for step 2 after quick wins
 */

// ============================================================================
// STEP 3: COPY THE TEMPLATE
// ============================================================================

/**
 * Copy this file:
 *   FROM: src/app/dashboard-template/page.tsx
 *   TO:   src/app/your-page-path/page.tsx
 *
 * Windows command:
 *   copy "src\app\dashboard-template\page.tsx" "src\app\your-page-path\page.tsx"
 *
 * OR: Copy manually in VS Code
 *   1. Open src/app/dashboard-template/page.tsx
 *   2. Ctrl+A to select all
 *   3. Ctrl+C to copy
 *   4. Create/open your page file
 *   5. Ctrl+V to paste
 *   6. Start editing...
 */

// ============================================================================
// STEP 4: CUSTOMIZE (5 SECTIONS TO UPDATE)
// ============================================================================

/**
 * Open your copied page and make these 5 changes:
 */

// ────────────────────────────────────────────────────────────────────────
// SECTION 1: Change the API Endpoint (Line ~34)
// ────────────────────────────────────────────────────────────────────────

/**
 * Current template:
 *   const { data, loading, error, retry, setFilters: updateFilters } = useDashboardFetch(
 *     apiClient,
 *     { endpoint: 'claims', page: 1, limit: 10, filters }
 *   );
 *
 * Change 'claims' to one of:
 *   - 'claims'        (for filing/adjudication pages)
 *   - 'villages'      (for village/gram sabha pages)
 *   - 'officers'      (for field officer pages)
 *   - 'grievances'    (for grievance pages)
 *   - 'dashboard/summary'  (for dashboard/analytics pages)
 *
 * Example for villages page:
 *   const { data, loading, error, retry } = useDashboardFetch(
 *     apiClient,
 *     { endpoint: 'villages', page: 1, limit: 10, filters }
 *   );
 */

// ────────────────────────────────────────────────────────────────────────
// SECTION 2: Update Filters State (Line ~15)
// ────────────────────────────────────────────────────────────────────────

/**
 * Current template:
 *   const [filters, setFilters] = useState({
 *     state: '',
 *     district: '',
 *     status: '',
 *   });
 *
 * Change to match your page's filter needs.
 *
 * Example for villages page:
 *   const [filters, setFilters] = useState({
 *     state: '',
 *     villageName: '',
 *     surveyStatus: '',
 *   });
 */

// ────────────────────────────────────────────────────────────────────────
// SECTION 3: Update KPI Metrics (Lines ~45-66)
// ────────────────────────────────────────────────────────────────────────

/**
 * Current template:
 *   const kpiMetrics = [
 *     { title: 'Total Claims', value: data?.items?.length || 0, ... },
 *     { title: 'Approved', value: data?.items?.filter(...).length || 0, ... },
 *     { title: 'Pending', value: ..., ... },
 *     { title: 'Rejected', value: ..., ... },
 *   ];
 *
 * Update to match your endpoint's data.
 *
 * Example for villages page:
 *   const kpiMetrics = [
 *     {
 *       title: 'Total Villages',
 *       value: data?.items?.length || 0,
 *       accentColor: '#3B82F6',
 *     },
 *     {
 *       title: 'Surveys Complete',
 *       value: data?.items?.filter(v => v.surveyStatus === 'COMPLETE').length || 0,
 *       accentColor: '#22C55E',
 *     },
 *     ...
 *   ];
 */

// ────────────────────────────────────────────────────────────────────────
// SECTION 4: Update List Item Mapping (Lines ~74-95)
// ────────────────────────────────────────────────────────────────────────

/**
 * Current template:
 *   const listItems = (data?.items || []).map((item) => ({
 *     id: item.id,
 *     title: item.claimantName || 'Unknown',
 *     subtitle: `${item.villageName} · ${item.district}`,
 *     metadata: [
 *       { label: 'ID', value: item.id },
 *       { label: 'Type', value: item.claimType },
 *       ...
 *     ],
 *     status: { label: item.status, variant: ... },
 *     ...
 *   }));
 *
 * Update to use your endpoint's actual fields.
 *
 * Example for villages page:
 *   const listItems = (data?.items || []).map((item) => ({
 *     id: item.id,
 *     title: item.villageName,
 *     subtitle: `${item.district} · ${item.state}`,
 *     metadata: [
 *       { label: 'District', value: item.district },
 *       { label: 'Gram Sabhas', value: item.gramSabhaCount || 0 },
 *       { label: 'Population', value: item.population || 'N/A' },
 *     ],
 *     status: {
 *       label: item.surveyStatus || 'Unknown',
 *       variant: item.surveyStatus === 'COMPLETE' ? 'success' : 'warning',
 *     },
 *     ...
 *   }));
 */

// ────────────────────────────────────────────────────────────────────────
// SECTION 5: Update Filter Options (Lines ~103-126)
// ────────────────────────────────────────────────────────────────────────

/**
 * Current template:
 *   const filterOptions = [
 *     {
 *       key: 'state',
 *       label: 'State',
 *       type: 'select',
 *       options: [
 *         { label: 'MP', value: 'MP' },
 *         ...
 *       ],
 *     },
 *     ...
 *   ];
 *
 * Update filter definitions to match your needs.
 * Keys must match the filter state keys!
 *
 * Example for villages page:
 *   const filterOptions = [
 *     {
 *       key: 'state',
 *       label: 'State',
 *       type: 'select',
 *       options: [
 *         { label: 'MP', value: 'MP' },
 *         { label: 'CG', value: 'CG' },
 *       ],
 *     },
 *     {
 *       key: 'villageName',
 *       label: 'Village Name',
 *       type: 'text',
 *       placeholder: 'Search by name...',
 *     },
 *   ];
 */

// ============================================================================
// STEP 5: TEST YOUR PAGE
// ============================================================================

/**
 * 1. Run the dev server:
 *    npm run dev
 *
 * 2. Navigate to your page in browser:
 *    http://localhost:3000/your-page-path
 *
 * 3. Check for these things:
 *    ✓ Page loads without TypeScript errors
 *    ✓ Loading skeleton appears briefly
 *    ✓ Data loads and displays in the list
 *    ✓ KPI metrics show correct values
 *    ✓ Filters work (change a filter, data updates)
 *    ✓ No console errors
 *
 * 4. Check Network tab:
 *    ✓ Network tab should show request to /api/v1/endpoint
 *    ✓ Response shows data (not error)
 *    ✓ Authorization header is present (Bearer token)
 *
 * 5. If something doesn't work:
 *    ✓ Check browser console for errors
 *    ✓ Check Network tab for failed requests
 *    ✓ Compare your changes to DASHBOARD_QUICK_REFERENCE.tsx
 *    ✓ Verify endpoint exists in backend (GET /api/v1/endpoint)
 */

// ============================================================================
// STEP 6: MARK AS COMPLETE
// ============================================================================

/**
 * After testing:
 *
 * 1. Update DASHBOARD_STATUS_TRACKER.tsx:
 *    Find your page and change:
 *      status: 'NOT_DONE' → status: 'DONE'
 *      lastModified: '2024-01-01' → lastModified: '2024-[TODAY]'
 *
 * 2. Commit your changes:
 *    git add src/app/your-page-path/page.tsx
 *    git add src/DASHBOARD_STATUS_TRACKER.tsx
 *    git commit -m "Migrate /your-page-path to dashboard pattern"
 *
 * 3. Push to branch:
 *    git push origin your-branch
 *
 * 4. Create Pull Request for code review
 */

// ============================================================================
// EXAMPLE: COMPLETE MIGRATION IN 5 MINUTES
// ============================================================================

/**
 * Let's migrate /analytics/download page step-by-step:
 *
 * STEP 1: Copy template
 *   cp src/app/dashboard-template/page.tsx src/app/analytics/download/page.tsx
 *
 * STEP 2: Update endpoint (assuming it's a claims list)
 *   Line 34: endpoint: 'claims'  (keep as is)
 *
 * STEP 3: Update filters for downloads page
 *   Line 15:
 *     const [filters, setFilters] = useState({
 *       state: '',
 *       documentType: '',
 *       dateFrom: '',
 *     });
 *
 * STEP 4: Update KPIs for downloads
 *   Lines 45-66:
 *     const kpiMetrics = [
 *       { title: 'Total Downloads', value: data?.items?.length || 0, ... },
 *       { title: 'Last 7 Days', value: countLast7Days(), ... },
 *       { title: 'PDF Files', value: countByType('pdf'), ... },
 *       { title: 'Excel Files', value: countByType('excel'), ... },
 *     ];
 *
 * STEP 5: Update list mapping for documents
 *   Lines 74-95:
 *     const listItems = (data?.items || []).map((item) => ({
 *       id: item.id,
 *       title: item.fileName,
 *       subtitle: `${item.documentType} · ${item.size}`,
 *       metadata: [
 *         { label: 'Type', value: item.documentType },
 *         { label: 'Size', value: item.size },
 *         { label: 'Downloaded', value: item.downloadCount || 0 },
 *       ],
 *       status: { label: 'Available', variant: 'success' },
 *       ...
 *     }));
 *
 * STEP 6: Update filter options
 *   Lines 103-126:
 *     const filterOptions = [
 *       { key: 'state', label: 'State', type: 'select', options: [...] },
 *       { key: 'documentType', label: 'Type', type: 'select',
 *         options: [
 *           { label: 'PDF', value: 'pdf' },
 *           { label: 'Excel', value: 'excel' },
 *         ]
 *       },
 *       { key: 'dateFrom', label: 'From Date', type: 'date' },
 *     ];
 *
 * STEP 7: Test
 *   npm run dev → http://localhost:3000/analytics/download
 *   Check Network tab, verify data, test filters
 *
 * STEP 8: Commit
 *   git add .
 *   git commit -m "Migrate /analytics/download to dashboard pattern"
 *
 * Total time: 5 minutes ✓
 */

// ============================================================================
// COMMON QUESTIONS
// ============================================================================

/**
 * Q: What if my page needs a different endpoint?
 * A: Looks like you're trying to use a custom endpoint. Add it to apiClient.ts
 *    Example: export const getMyData = async (filters) => { ... }
 *    Then in useDashboardFetch, handle the custom endpoint in getEndpointUrl()
 *
 * Q: My filters don't match any of the 4 main endpoints?
 * A: Some pages need custom filters. That's OK - just update filterOptions
 *    and make sure filter keys match your state object.
 *
 * Q: How do I know which fields are available in the API response?
 * A: Check backend swagger docs:
 *    http://localhost:8000/docs
 *    Goes to "Schemas" section to see response structure for each endpoint
 *
 * Q: Can I use a different API endpoint than the 4 main ones?
 * A: Yes! Edit src/lib/api-client.ts and add your custom endpoint method,
 *    then update useDashboardFetch to handle it.
 *
 * Q: How do I handle errors if the API call fails?
 * A: The template already handles this! See the ErrorDisplay component
 *    at the bottom. It automatically shows retry button on error.
 *
 * Q: What if I need more complex filtering?
 * A: Update the filterOptions array with more complex filter UI.
 *    The hook will pass all filters to the API correctly.
 *
 * Q: Can I add more KPIs than 4?
 * A: Yes! Add more objects to the kpiMetrics array. The grid will auto-layout.
 *    Adjust 'columns' prop: <DashboardKPIGrid columns={6} /> for 6 columns.
 *
 * Q: How do I add sorting/pagination?
 * A: Check src/hooks/use-dashboard-fetch.ts for pagination support.
 *    For sorting, you'd add to filters and update the endpoint query.
 */

// ============================================================================
// NEXT: REFERENCE FILES
// ============================================================================

/**
 * These files are your reference during migration:
 *
 * 📖 DASHBOARD_TEMPLATE_GUIDE.tsx
 *   └─ Complete guide with copy-paste examples for each component
 *
 * 📖 DASHBOARD_QUICK_REFERENCE.tsx
 *   └─ Quick cheat sheet - see working code examples
 *
 * 📊 DASHBOARD_STATUS_TRACKER.tsx
 *   └─ Track which pages are DONE/PARTIAL/NOT_DONE
 *
 * 📋 DASHBOARD_MIGRATION_CHECKLIST.tsx
 *   └─ Detailed checklist for each page migration
 *
 * Open any of these files while migrating for quick reference!
 */

// ============================================================================
// YOU'RE READY! 🚀
// ============================================================================

/**
 * Now you're ready to start migrating pages. Here's the recommended order:
 * 
 * SESSION 1 (30 min): Do 6 quick wins
 *   - /analytics/download
 *   - /analytics/ndvi
 *   - /district/[districtId]/alerts
 *   - /field-officer/assignments
 *   - /gram-sabha/claims
 *   - /gram-sabha/grievance
 * 
 * SESSION 2 (1 hour): Do 12 more quick wins
 *   - All remaining PlaceholderPage pages (just copy/paste!)
 * 
 * SESSION 3 (2.5 hours): Polish PARTIAL pages
 *   - Add loading skeletons where missing
 *   - Add error displays
 *   - Complete filter/KPI/list implementations
 * 
 * Total: ~5 hours for 40 pages
 * 
 * How to get started RIGHT NOW:
 * 1. Pick a page from QUICK_WINS list
 * 2. Open DASHBOARD_QUICK_REFERENCE.tsx in split view
 * 3. Copy src/app/dashboard-template/page.tsx
 * 4. Make 5 changes as described above
 * 5. Test in browser (npm run dev)
 * 6. Commit
 * 7. Next page!
 * 
 * Good luck! 💪
 */

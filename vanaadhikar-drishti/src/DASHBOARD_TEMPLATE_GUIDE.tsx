/**
 * PRODUCTION DASHBOARD TEMPLATE - USAGE GUIDE
 *
 * This file documents the reusable pattern for building production dashboards.
 * Use this as a checklist when implementing new dashboard pages.
 *
 * ============================================================================
 * FILES INCLUDED IN THIS TEMPLATE PATTERN:
 * ============================================================================
 *
 * 1. src/hooks/use-dashboard-fetch.ts
 *    - Custom hook for data fetching with loading/error/pagination
 *    - Handles API calls and state management
 *    - Supports filters and pagination
 *
 * 2. src/components/dashboard-components.tsx
 *    - Reusable dashboard components:
 *      * DashboardKPI - Individual KPI card with loading skeleton
 *      * DashboardKPIGrid - Container for KPI cards
 *      * DashboardFilterBar - Filter controls with multiple input types
 *      * DashboardList - Data list with selection, metadata, and status badges
 *      * DashboardPageContainer - Page header wrapper
 *      * DashboardEmptyState - Empty state placeholder
 *
 * 3. src/app/dashboard-template/page.tsx
 *    - Working example page showing full implementation
 *    - Demonstrates all features and patterns
 *
 * ============================================================================
 * QUICK START: Creating a New Dashboard Page
 * ============================================================================
 *
 * Step 1: Copy the Template
 * ─────────────────────────
 * cp src/app/dashboard-template/page.tsx src/app/your-dashboard/page.tsx
 *
 * Step 2: Customize the Page Component
 * ─────────────────────────────────────
 * Replace these sections:
 *
 * a) Import statement for DashboardLayout (change role)
 *    OLD: <DashboardLayout role="national-nodal" ... >
 *    NEW: <DashboardLayout role="sdlc-officer" ... >
 *
 * b) Data fetching endpoint
 *    OLD: endpoint: 'claims'
 *    NEW: endpoint: 'villages' // or 'officers', 'grievances', etc.
 *
 * c) Initial filters (if needed)
 *    OLD: { state: '', district: '', status: '' }
 *    NEW: { state: '', villageCode: '', saturation: '' }
 *
 * d) Filter options array
 *    Replace with your domain's filter fields
 *
 * e) KPI metrics calculation
 *    Customize useMemo hook to calculate your metrics
 *
 * f) List item mapping
 *    Transform API data to DashboardListItemProps format
 *
 * ============================================================================
 * COMPONENT USAGE EXAMPLES
 * ============================================================================
 *
 * 1. Use DashboardKPIGrid for metric display
 * ──────────────────────────────────────────
 *
 * <DashboardKPIGrid
 *   kpis={[
 *     {
 *       title: 'Total Villages',
 *       value: 523,
 *       accentColor: '#3B82F6',
 *       icon: <MapPin size={20} />,
 *       trend: 'up'
 *     },
 *     {
 *       title: 'Population',
 *       value: '1.2M',
 *       accentColor: '#8B5CF6',
 *       icon: <Users size={20} />
 *     }
 *   ]}
 *   loading={loading}
 *   columns={4}
 * />
 *
 * 2. Use DashboardFilterBar for filtering
 * ────────────────────────────────────────
 *
 * <DashboardFilterBar
 *   filters={filters}
 *   onFilterChange={handleFilterChange}
 *   filterOptions={[
 *     {
 *       key: 'state',
 *       label: 'State',
 *       type: 'select',
 *       options: [
 *         { label: 'Madhya Pradesh', value: 'MP' },
 *         { label: 'Chhattisgarh', value: 'CG' }
 *       ]
 *     },
 *     {
 *       key: 'search',
 *       label: 'Search',
 *       type: 'text',
 *       placeholder: 'Search by name...'
 *     }
 *   ]}
 *   onApply={handleApplyFilters}
 *   onClear={handleClearFilters}
 * />
 *
 * 3. Use DashboardList for data display
 * ──────────────────────────────────────
 *
 * <DashboardList
 *   items={listItems}
 *   loading={loading}
 *   empty={!loading && listItems.length === 0}
 *   emptyMessage=\"No data found\"
 *   error={error}
 *   onRetry={retry}
 * />
 *
 * ============================================================================
 * HOOK USAGE: useDashboardFetch
 * ============================================================================
 *
 * const { data, loading, error, retry, setFilters, setPage } = useDashboardFetch(
 *   apiClient,
 *   {
 *     endpoint: 'claims',        // API endpoint (claims, villages, officers, etc)
 *     page: 1,                   // Current page
 *     limit: 10,                 // Items per page
 *     filters: filters,          // Current filter values
 *     enabled: true              // Enable/disable fetching
 *   }
 * );
 *
 * Available return values:
 * - data: T | null              - Fetched data
 * - loading: boolean            - Is loading
 * - error: string | null        - Error message
 * - retry: () => void           - Retry failed request
 * - refetch: () => void         - Refetch data
 * - setFilters: (filters) => void  - Update filters and reset to page 1
 * - setPage: (page) => void     - Change page number
 *
 * ============================================================================
 * STATE MANAGEMENT PATTERN
 * ============================================================================
 *
 * const [filters, setFilters] = useState({
 *   state: '',
 *   district: '',
 *   status: '',
 * });
 * const [selectedItem, setSelectedItem] = useState<string | null>(null);
 *
 * const { data, loading, error, retry, setFilters: updateFilters } = useDashboardFetch(
 *   apiClient,
 *   { endpoint: 'claims', page: 1, limit: 10, filters }
 * );
 *
 * const handleFilterChange = (key: string, value: any) => {
 *   setFilters(prev => ({ ...prev, [key]: value }));
 * };
 *
 * const handleApplyFilters = () => {
 *   updateFilters(filters);  // Update hook filters and reset pagination
 * };
 *
 * ============================================================================
 * DATA TRANSFORMATION EXAMPLES
 * ============================================================================
 *
 * Transform API response to DashboardListItemProps:
 *
 * const listItems: DashboardListItemProps[] = data?.items?.map(item => ({
 *   id: item.id,
 *   title: item.name || 'Unknown',
 *   subtitle: item.district,
 *   metadata: [
 *     { label: 'Code', value: item.code },
 *     { label: 'Population', value: item.population?.toString() || 'N/A' },
 *     { label: 'Area', value: `${item.area} sq.km` }
 *   ],
 *   status: {
 *     label: item.status,
 *     variant: item.status === 'active' ? 'success' : 'warning'
 *   },
 *   onSelect: () => setSelectedItem(item.id),
 *   isSelected: selectedItem === item.id
 * })) || [];
 *
 * ============================================================================
 * ERROR HANDLING PATTERN
 * ============================================================================
 *
 * {error ? (
 *   <ErrorDisplay
 *     title=\"Failed to Load Data\"
 *     message={error}
 *     onRetry={retry}
 *     showRetry={true}
 *   />
 * ) : (
 *   <DashboardList
 *     items={listItems}
 *     loading={loading}
 *     empty={!loading && listItems.length === 0}
 *     emptyMessage=\"No data found\"
 *   />
 * )}
 *
 * ============================================================================
 * LOADING STATE PATTERN
 * ============================================================================
 *
 * // For KPI cards:
 * <DashboardKPIGrid kpis={kpiMetrics} loading={loading} />
 *
 * // For list:
 * <DashboardList
 *   items={listItems}
 *   loading={loading}
 *   empty={!loading && listItems.length === 0}
 * />
 *
 * // For filter bar (no loading state needed - appears immediately)
 * <DashboardFilterBar ... />
 *
 * ============================================================================
 * PAGINATION SUPPORT
 * ============================================================================
 *
 * const [page, setPage] = useState(1);
 *
 * const { data, loading, error, setPage } = useDashboardFetch(
 *   apiClient,
 *   { endpoint: 'claims', page, limit: 10, filters }
 * );
 *
 * <button onClick={() => setPage(page + 1)}>Next Page</button>
 * <button onClick={() => setPage(page - 1)}>Previous Page</button>
 *
 * ============================================================================
 * COMMON PAGES TO MIGRATE
 * ============================================================================
 *
 * Priority 1 - Core Data Pages (use this template directly):
 * - /district/[districtId]/claims
 * - /district/[districtId]/dashboard
 * - /state/[stateSlug]/claims
 * - /state/[stateSlug]/dashboard
 * - /national-dashboard/documents
 *
 * Priority 2 - Role-Specific Pages:
 * - /field-officer/assignments
 * - /sdlc/approved
 * - /sdlc/rejected
 * - /sdlc/adjudication
 *
 * Priority 3 - Analytical Pages:
 * - /analytics/builder
 * - /analytics/atlas
 * - /district/[districtId]/dss
 *
 * ============================================================================
 * TESTING THE TEMPLATE
 * ============================================================================
 *
 * Open http://localhost:3000/dashboard-template to see the working example.
 *
 * Features demonstrated:
 * - ✓ KPI cards with icons and trends
 * - ✓ Filter bar with persistence
 * - ✓ Data list with selection
 * - ✓ Loading and error states
 * - ✓ Empty state handling
 * - ✓ Selected item details panel
 *
 * ============================================================================
 */

// This is a documentation file. Copy the template page when creating new dashboards.

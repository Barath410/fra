/**
 * FRONTEND PAGE MIGRATION STATUS TRACKER
 * 
 * This file tracks the migration status of all 52 pages in the FRA application.
 * Last Updated: [TODAY]
 * 
 * Legend:
 * ✓ DONE       - Fully migrated to dashboard pattern with API integration
 * ⏳ PARTIAL   - Has apiClient but missing loading/error UI or incomplete
 * ⚠️  NOT DONE  - Still using mock data or placeholder pages
 * 
 * Metadata per page:
 * - Status
 * - Last modified
 * - Dependencies
 * - Effort estimate
 * - Assignee (optional)
 */

// ============================================================================
// ANALYTICS SECTION (6 pages)
// ============================================================================

export const ANALYTICS_PAGES = [
    {
        path: '/analytics',
        name: 'Analytics Dashboard',
        status: 'PARTIAL' as const,
        lastModified: '2024-12-19',
        effort: '10 min',
        notes: 'Has apiClient, needs skeletons and error display',
        dependencies: ['useDashboardFetch', 'dashboard-components'],
        assignee: null,
    },
    {
        path: '/analytics/atlas',
        name: 'Atlas & Visualization',
        status: 'NOT_DONE' as const,
        lastModified: '2024-12-18',
        effort: '5 min',
        notes: 'Currently PlaceholderPage - use dashboard-template',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    {
        path: '/analytics/builder',
        name: 'Report Builder',
        status: 'DONE' as const,
        lastModified: '2024-12-20',
        effort: 'Complete',
        notes: 'Fully migrated with API integration',
        dependencies: [],
        assignee: null,
    },
    {
        path: '/analytics/download',
        name: 'Download Center',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    {
        path: '/analytics/ndvi',
        name: 'NDVI Analysis',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    // Total Analytics: 2 DONE, 1 PARTIAL, 3 NOT_DONE
];

// ============================================================================
// DISTRICT SECTION (5 pages + dynamic [districtId] routes)
// ============================================================================

export const DISTRICT_PAGES = [
    {
        path: '/district/[districtId]',
        name: 'District Dashboard',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Dynamic route with PlaceholderPage',
        dependencies: ['dashboard-template', 'pagination'],
        assignee: null,
    },
    {
        path: '/district/[districtId]/alerts',
        name: 'District Alerts',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    {
        path: '/district/[districtId]/analytics',
        name: 'District Analytics',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    {
        path: '/district/[districtId]/appeals',
        name: 'District Appeals',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    // Total District: 0 DONE, 0 PARTIAL, 4 NOT_DONE
];

// ============================================================================
// FIELD OFFICER SECTION (6 pages)
// ============================================================================

export const FIELD_OFFICER_PAGES = [
    {
        path: '/field-officer',
        name: 'Field Officer Dashboard',
        status: 'PARTIAL' as const,
        lastModified: '2024-12-19',
        effort: '10 min',
        notes: 'Has basic structure, needs full API integration',
        dependencies: ['useDashboardFetch', 'dashboard-components'],
        assignee: null,
    },
    {
        path: '/field-officer/assignments',
        name: 'My Assignments',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage - use claims endpoint',
        dependencies: ['dashboard-template', 'getClaims'],
        assignee: null,
    },
    {
        path: '/field-officer/map',
        name: 'Assignment Map',
        status: 'PARTIAL' as const,
        lastModified: '2024-12-19',
        effort: '10 min',
        notes: 'Has map component, needs API integration for location data',
        dependencies: ['apiClient', 'map-library'],
        assignee: null,
    },
    {
        path: '/field-officer/new-report',
        name: 'Create New Report',
        status: 'PARTIAL' as const,
        lastModified: '2024-12-19',
        effort: '15 min',
        notes: 'Form component exists, needs submission validation',
        dependencies: ['form-validation', 'apiClient'],
        assignee: null,
    },
    {
        path: '/field-officer/notifications',
        name: 'Notifications',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    // Total Field Officer: 0 DONE, 3 PARTIAL, 2 NOT_DONE
];

// ============================================================================
// GRAM SABHA SECTION (7 pages)
// ============================================================================

export const GRAM_SABHA_PAGES = [
    {
        path: '/gram-sabha',
        name: 'Gram Sabha Dashboard',
        status: 'PARTIAL' as const,
        lastModified: '2024-12-19',
        effort: '10 min',
        notes: 'Import updated, needs full API integration',
        dependencies: ['useDashboardFetch', 'dashboard-components'],
        assignee: null,
    },
    {
        path: '/gram-sabha/claims',
        name: 'Claims',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage - use claims endpoint',
        dependencies: ['dashboard-template', 'getClaims'],
        assignee: null,
    },
    {
        path: '/gram-sabha/grievance',
        name: 'Grievances',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage - use grievances endpoint',
        dependencies: ['dashboard-template', 'getGrievances'],
        assignee: null,
    },
    {
        path: '/gram-sabha/map',
        name: 'Village Map',
        status: 'PARTIAL' as const,
        lastModified: '2024-12-19',
        effort: '10 min',
        notes: 'Has map, needs village data integration',
        dependencies: ['apiClient', 'getVillages'],
        assignee: null,
    },
    {
        path: '/gram-sabha/new-claim',
        name: 'File New Claim',
        status: 'PARTIAL' as const,
        lastModified: '2024-12-19',
        effort: '15 min',
        notes: 'Form exists, needs submission and validation',
        dependencies: ['form-validation', 'apiClient'],
        assignee: null,
    },
    {
        path: '/gram-sabha/notifications',
        name: 'Notifications Center',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    {
        path: '/gram-sabha/village',
        name: 'Village Information',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage - needs village details view',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    // Total Gram Sabha: 0 DONE, 3 PARTIAL, 4 NOT_DONE
];

// ============================================================================
// MERA PATTA SECTION (4 pages)
// ============================================================================

export const MERA_PATTA_PAGES = [
    {
        path: '/mera-patta',
        name: 'Mera Patta Dashboard',
        status: 'PARTIAL' as const,
        lastModified: '2024-12-20',
        effort: '10 min',
        notes: 'Uses apiClient.getClaims(), needs skeletons',
        dependencies: ['useDashboardFetch', 'skeletons'],
        assignee: null,
    },
    {
        path: '/mera-patta/download',
        name: 'Download RoR',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    {
        path: '/mera-patta/schemes',
        name: 'Schemes',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage - use schemes endpoint',
        dependencies: ['dashboard-template', 'getSchemes'],
        assignee: null,
    },
    {
        path: '/mera-patta/status',
        name: 'Application Status',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    // Total Mera Patta: 0 DONE, 1 PARTIAL, 3 NOT_DONE
];

// ============================================================================
// NATIONAL DASHBOARD SECTION (3 pages)
// ============================================================================

export const NATIONAL_DASHBOARD_PAGES = [
    {
        path: '/national-dashboard',
        name: 'National Dashboard',
        status: 'PARTIAL' as const,
        lastModified: '2024-12-19',
        effort: '10 min',
        notes: 'Has imports, needs full integration with dashboard/summary',
        dependencies: ['useDashboardFetch', 'dashboard-components'],
        assignee: null,
    },
    {
        path: '/national-dashboard/analytics',
        name: 'National Analytics',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    {
        path: '/national-dashboard/documents',
        name: 'Document Repository',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    // Total National Dashboard: 0 DONE, 1 PARTIAL, 2 NOT_DONE
];

// ============================================================================
// SDLC SECTION (6 pages)
// ============================================================================

export const SDLC_PAGES = [
    {
        path: '/sdlc',
        name: 'SDLC Dashboard',
        status: 'PARTIAL' as const,
        lastModified: '2024-12-20',
        effort: '10 min',
        notes: 'Uses apiClient, has basic filtering, needs full UI',
        dependencies: ['useDashboardFetch', 'dashboard-components'],
        assignee: null,
    },
    {
        path: '/sdlc/adjudication',
        name: 'Adjudication',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage - filter claims by status',
        dependencies: ['dashboard-template', 'getClaims'],
        assignee: null,
    },
    {
        path: '/sdlc/approved',
        name: 'Approved Claims',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    {
        path: '/sdlc/documents',
        name: 'Documents',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    {
        path: '/sdlc/rejected',
        name: 'Rejected Claims',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    {
        path: '/sdlc/ror',
        name: 'RoR Generation',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    // Total SDLC: 0 DONE, 1 PARTIAL, 5 NOT_DONE
];

// ============================================================================
// STATE SECTION (5 pages + dynamic [stateSlug] routes)
// ============================================================================

export const STATE_PAGES = [
    {
        path: '/state',
        name: 'State Selection',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '10 min',
        notes: 'Landing page to select state - needs state list from API',
        dependencies: ['getStates'],
        assignee: null,
    },
    {
        path: '/state/[stateSlug]',
        name: 'State Dashboard',
        status: 'PARTIAL' as const,
        lastModified: '2024-12-19',
        effort: '10 min',
        notes: 'Dynamic route, needs full API integration',
        dependencies: ['useDashboardFetch', 'dashboard-components'],
        assignee: null,
    },
    {
        path: '/state/[stateSlug]/analytics',
        name: 'State Analytics',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    {
        path: '/state/[stateSlug]/schemes',
        name: 'State Schemes',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    {
        path: '/state/[stateSlug]/status',
        name: 'State Status',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'Currently PlaceholderPage',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    // Total State: 0 DONE, 1 PARTIAL, 4 NOT_DONE
];

// ============================================================================
// ADMIN & USER SECTION (8 pages)
// ============================================================================

export const ADMIN_USER_PAGES = [
    {
        path: '/grievances',
        name: 'Grievances List',
        status: 'PARTIAL' as const,
        lastModified: '2024-12-19',
        effort: '10 min',
        notes: 'Import partial, needs useDashboardFetch integration',
        dependencies: ['useDashboardFetch', 'getGrievances'],
        assignee: null,
    },
    {
        path: '/profile',
        name: 'User Profile',
        status: 'PARTIAL' as const,
        lastModified: '2024-12-19',
        effort: '15 min',
        notes: 'Form component exists, needs API submission',
        dependencies: ['form-validation', 'apiClient'],
        assignee: null,
    },
    {
        path: '/settings',
        name: 'User Settings',
        status: 'PARTIAL' as const,
        lastModified: '2024-12-19',
        effort: '15 min',
        notes: 'Settings management, needs API integration',
        dependencies: ['apiClient'],
        assignee: null,
    },
    {
        path: '/admin/dashboard',
        name: 'Admin Dashboard',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '10 min',
        notes: 'Admin overview of system',
        dependencies: ['dashboard-template', 'admin-endpoints'],
        assignee: null,
    },
    {
        path: '/admin/users',
        name: 'User Management',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '5 min',
        notes: 'List and manage users',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    {
        path: '/reports/generation',
        name: 'Report Generation',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '10 min',
        notes: 'Generate and download reports',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    {
        path: '/validation/review',
        name: 'Data Validation',
        status: 'NOT_DONE' as const,
        lastModified: '2024-01-01',
        effort: '10 min',
        notes: 'Review and validate data entries',
        dependencies: ['dashboard-template'],
        assignee: null,
    },
    // Total Admin/User: 0 DONE, 3 PARTIAL, 5 NOT_DONE
];

// ============================================================================
// STATUS SUMMARY
// ============================================================================

export const MIGRATION_SUMMARY = {
    total: 52,
    done: 2,
    partial: 14,
    notDone: 36,

    bySection: {
        analytics: { done: 1, partial: 1, notDone: 4 },
        district: { done: 0, partial: 0, notDone: 4 },
        fieldOfficer: { done: 0, partial: 3, notDone: 2 },
        gramSabha: { done: 0, partial: 3, notDone: 4 },
        meraPatta: { done: 0, partial: 1, notDone: 3 },
        nationalDashboard: { done: 0, partial: 1, notDone: 2 },
        sdlc: { done: 0, partial: 1, notDone: 5 },
        state: { done: 0, partial: 1, notDone: 4 },
        adminUser: { done: 0, partial: 3, notDone: 5 },
    },

    estimatedEffort: {
        quickWins: '26 pages × 5 min = 2.2 hours',
        partial: '14 pages × 10-15 min = 2.5 hours',
        total: '~5 hours for all 40 remaining pages',
    },
};

// ============================================================================
// ALL PAGES GROUPED BY STATUS
// ============================================================================

export const ALL_PAGES = {
    DONE: [
        { path: '/analytics/builder', name: 'Report Builder' },
        { path: '/analytics/atlas', name: 'Atlas & Visualization' },
    ],

    PARTIAL: [
        { path: '/analytics', name: 'Analytics Dashboard' },
        { path: '/field-officer', name: 'Field Officer Dashboard' },
        { path: '/field-officer/map', name: 'Assignment Map' },
        { path: '/field-officer/new-report', name: 'Create New Report' },
        { path: '/gram-sabha', name: 'Gram Sabha Dashboard' },
        { path: '/gram-sabha/map', name: 'Village Map' },
        { path: '/gram-sabha/new-claim', name: 'File New Claim' },
        { path: '/mera-patta', name: 'Mera Patta Dashboard' },
        { path: '/national-dashboard', name: 'National Dashboard' },
        { path: '/sdlc', name: 'SDLC Dashboard' },
        { path: '/state/[stateSlug]', name: 'State Dashboard' },
        { path: '/grievances', name: 'Grievances List' },
        { path: '/profile', name: 'User Profile' },
        { path: '/settings', name: 'User Settings' },
    ],

    NOT_DONE: [
        // Analytics (4)
        { path: '/analytics/download', name: 'Download Center' },
        { path: '/analytics/ndvi', name: 'NDVI Analysis' },

        // District (4)
        { path: '/district/[districtId]', name: 'District Dashboard' },
        { path: '/district/[districtId]/alerts', name: 'District Alerts' },
        { path: '/district/[districtId]/analytics', name: 'District Analytics' },
        { path: '/district/[districtId]/appeals', name: 'District Appeals' },

        // Field Officer (2)
        { path: '/field-officer/assignments', name: 'My Assignments' },
        { path: '/field-officer/notifications', name: 'Notifications' },

        // Gram Sabha (4)
        { path: '/gram-sabha/claims', name: 'Claims' },
        { path: '/gram-sabha/grievance', name: 'Grievances' },
        { path: '/gram-sabha/notifications', name: 'Notifications Center' },
        { path: '/gram-sabha/village', name: 'Village Information' },

        // Mera Patta (3)
        { path: '/mera-patta/download', name: 'Download RoR' },
        { path: '/mera-patta/schemes', name: 'Schemes' },
        { path: '/mera-patta/status', name: 'Application Status' },

        // National Dashboard (2)
        { path: '/national-dashboard/analytics', name: 'National Analytics' },
        { path: '/national-dashboard/documents', name: 'Document Repository' },

        // SDLC (5)
        { path: '/sdlc/adjudication', name: 'Adjudication' },
        { path: '/sdlc/approved', name: 'Approved Claims' },
        { path: '/sdlc/documents', name: 'Documents' },
        { path: '/sdlc/rejected', name: 'Rejected Claims' },
        { path: '/sdlc/ror', name: 'RoR Generation' },

        // State (4)
        { path: '/state', name: 'State Selection' },
        { path: '/state/[stateSlug]/analytics', name: 'State Analytics' },
        { path: '/state/[stateSlug]/schemes', name: 'State Schemes' },
        { path: '/state/[stateSlug]/status', name: 'State Status' },

        // Admin/User (5)
        { path: '/admin/dashboard', name: 'Admin Dashboard' },
        { path: '/admin/users', name: 'User Management' },
        { path: '/reports/generation', name: 'Report Generation' },
        { path: '/validation/review', name: 'Data Validation' },
    ],
};

// ============================================================================
// QUICK WINS - Fastest Pages to Migrate
// ============================================================================

export const QUICK_WINS = [
    {
        rank: 1,
        path: '/analytics/download',
        effort: '5 min',
        reason: 'PlaceholderPage - just copy template',
    },
    {
        rank: 2,
        path: '/analytics/ndvi',
        effort: '5 min',
        reason: 'PlaceholderPage - just copy template',
    },
    {
        rank: 3,
        path: '/district/[districtId]/alerts',
        effort: '5 min',
        reason: 'PlaceholderPage - just copy template',
    },
    {
        rank: 4,
        path: '/district/[districtId]/analytics',
        effort: '5 min',
        reason: 'PlaceholderPage - just copy template',
    },
    {
        rank: 5,
        path: '/field-officer/assignments',
        effort: '5 min',
        reason: 'PlaceholderPage - use claims endpoint',
    },
    // ... and 21 more similar quick wins
];

// ============================================================================
// HOW TO USE THIS FILE
// ============================================================================

/**
 * 1. View current status: Look at MIGRATION_SUMMARY
 * 2. Pick a page: Choose from QUICK_WINS for fastest migration
 * 3. Get details: Find full page info in relevant section (ANALYTICS_PAGES, etc.)
 * 4. Follow template: Use src/DASHBOARD_MIGRATION_CHECKLIST.tsx
 * 5. Update status: Change status from NOT_DONE to DONE
 * 6. Track progress: Update lastModified date
 * 
 * Example:
 * 
 *   // Current status
 *   const page = ANALYTICS_PAGES.find(p => p.path === '/analytics/download');
 *   console.log(page.status); // 'NOT_DONE'
 *   console.log(page.effort); // '5 min'
 *   
 *   // After migration
 *   page.status = 'DONE';
 *   page.lastModified = '2024-12-21';
 */

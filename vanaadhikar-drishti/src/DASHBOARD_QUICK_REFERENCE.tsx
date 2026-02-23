/**
 * QUICK REFERENCE: Production Dashboard Pattern
 * 
 * Files and their purposes:
 * ├── src/hooks/use-dashboard-fetch.ts          - Data fetching hook with state management
 * ├── src/components/dashboard-components.tsx   - Reusable UI components
 * ├── src/app/dashboard-template/page.tsx       - Working example implementation
 * ├── src/DASHBOARD_TEMPLATE_GUIDE.tsx          - Full documentation
 * └── src/DASHBOARD_QUICK_REFERENCE.tsx         - This file
 */

// ============================================================================
// 1. IMPORT REQUIRED MODULES
// ============================================================================

import { useState } from 'react';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import {
    DashboardKPIGrid,
    DashboardFilterBar,
    DashboardList,
    DashboardPageContainer,
} from '@/components/dashboard-components';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { ErrorDisplay } from '@/components/error-display';

// ============================================================================
// 2. SETUP COMPONENT
// ============================================================================

// 'use client';  // Add this for any page using dashboards

export function DashboardExample() {
    // State for filters
    const [filters, setFilters] = useState({
        state: '',
        district: '',
        status: '',
    });

    // State for selection
    const [selectedItem, setSelectedItem] = useState<string | null>(null);

    // ========================================================================
    // 3. FETCH DATA WITH CUSTOM HOOK
    // ========================================================================

    const { data, loading, error, retry, setFilters: updateFilters } = useDashboardFetch(
        apiClient,
        {
            endpoint: 'claims', // Change this to: 'villages', 'officers', 'grievances'
            page: 1,
            limit: 10,
            filters,
        }
    );

    // ========================================================================
    // 4. CALCULATE KPI METRICS
    // ========================================================================

    const kpiMetrics = [
        {
            title: 'Total Claims',
            value: data?.items?.length || 0,
            accentColor: '#3B82F6',
            icon: <Users size={20} />,
        },
        {
            title: 'Approved',
            value: data?.items?.filter((c) => c.status === 'APPROVED').length || 0,
            accentColor: '#22C55E',
            icon: <CheckCircle size={20} />,
        },
        {
            title: 'Pending',
            value: data?.items?.filter((c) => c.status === 'PENDING').length || 0,
            accentColor: '#F59E0B',
            icon: <Clock size={20} />,
            trend: 'up' as const,
        },
        {
            title: 'Rejected',
            value: data?.items?.filter((c) => c.status === 'REJECTED').length || 0,
            accentColor: '#EF4444',
            icon: <AlertTriangle size={20} />,
        },
    ];

    // ========================================================================
    // 5. TRANSFORM DATA TO LIST ITEMS
    // ========================================================================

    const listItems = (data?.items || []).map((item) => ({
        id: item.id,
        title: item.claimantName || 'Unknown',
        subtitle: `${item.villageName} · ${item.district}`,
        metadata: [
            { label: 'ID', value: item.id },
            { label: 'Type', value: item.claimType || 'N/A' },
            { label: 'Area', value: `${item.areaAcres || 0} ac` },
            { label: 'Status', value: item.status || 'N/A' },
        ],
        status: {
            label: item.status || 'Unknown',
            variant:
                item.status === 'APPROVED'
                    ? ('success' as const)
                    : item.status === 'REJECTED'
                        ? ('danger' as const)
                        : item.status === 'PENDING'
                            ? ('warning' as const)
                            : ('info' as const),
        },
        onSelect: () => setSelectedItem(item.id),
        isSelected: selectedItem === item.id,
    }));

    // ========================================================================
    // 6. DEFINE FILTER OPTIONS
    // ========================================================================

    const filterOptions = [
        {
            key: 'state',
            label: 'State',
            type: 'select' as const,
            options: [
                { label: 'MP', value: 'MP' },
                { label: 'CG', value: 'CG' },
                { label: 'MH', value: 'MH' },
            ],
        },
        {
            key: 'district',
            label: 'District',
            type: 'text' as const,
            placeholder: 'Search...',
        },
        {
            key: 'status',
            label: 'Status',
            type: 'select' as const,
            options: [
                { label: 'Approved', value: 'APPROVED' },
                { label: 'Pending', value: 'PENDING' },
                { label: 'Rejected', value: 'REJECTED' },
            ],
        },
    ];

    // ========================================================================
    // 7. HANDLE FILTER CHANGES
    // ========================================================================

    const handleFilterChange = (key: string, value: any) => {
        setFilters((prev) => ({ ...prev, [key]: value }));
    };

    const handleApplyFilters = () => {
        updateFilters(filters);
    };

    const handleClearFilters = () => {
        const emptyFilters = { state: '', district: '', status: '' };
        setFilters(emptyFilters);
        updateFilters(emptyFilters);
    };

    // ========================================================================
    // 8. RENDER COMPONENT
    // ========================================================================

    return (
        <DashboardLayout role="national-nodal" title="Dashboard" titleHi="डैशबोर्ड">
            <DashboardPageContainer title="Data Dashboard">
                {/* KPI Cards */}
                <section className="mb-6">
                    <h2 className="text-lg font-bold mb-4">Metrics</h2>
                    <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
                </section>

                {/* Filter Bar */}
                <section className="mb-6">
                    <h2 className="text-lg font-bold mb-4">Filters</h2>
                    <DashboardFilterBar
                        filters={filters}
                        onFilterChange={handleFilterChange}
                        filterOptions={filterOptions}
                        onApply={handleApplyFilters}
                        onClear={handleClearFilters}
                    />
                </section>

                {/* Data List */}
                <section>
                    <h2 className="text-lg font-bold mb-4">Results</h2>
                    {error ? (
                        <ErrorDisplay
                            title="Error"
                            message={error}
                            onRetry={retry}
                            showRetry={true}
                        />
                    ) : (
                        <DashboardList
                            items={listItems}
                            loading={loading}
                            empty={!loading && listItems.length === 0}
                            emptyMessage="No data found"
                        />
                    )}
                </section>
            </DashboardPageContainer>
        </DashboardLayout>
    );
}

// ============================================================================
// COPY-PASTE SNIPPET FOR NEW PAGES
// ============================================================================

/*
'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import {
  DashboardKPIGrid,
  DashboardFilterBar,
  DashboardList,
  DashboardPageContainer,
} from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';

export default function YourDashboardPage() {
  const [filters, setFilters] = useState({
    field1: '',
    field2: '',
  });
  const [selected, setSelected] = useState<string | null>(null);

  const { data, loading, error, retry, setFilters: updateFilters } = useDashboardFetch(
    apiClient,
    { endpoint: 'claims', page: 1, limit: 10, filters }
  );

  const kpiMetrics = [
    { title: 'Total', value: data?.items?.length || 0, accentColor: '#3B82F6' },
  ];

  const listItems = (data?.items || []).map((item) => ({
    id: item.id,
    title: item.name,
    subtitle: item.location,
    metadata: [{ label: 'Status', value: item.status }],
    status: { label: item.status, variant: 'success' as const },
    onSelect: () => setSelected(item.id),
    isSelected: selected === item.id,
  }));

  return (
    <DashboardLayout role="national-nodal" title="Your Dashboard">
      <DashboardPageContainer title="Your Title">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Metrics</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} />
        </section>

        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Filters</h2>
          <DashboardFilterBar
            filters={filters}
            onFilterChange={(k, v) => setFilters(prev => ({ ...prev, [k]: v }))}
            filterOptions={[]}
            onApply={() => updateFilters(filters)}
          />
        </section>

        <section>
          <h2 className="text-lg font-bold mb-4">Data</h2>
          {error ? (
            <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry />
          ) : (
            <DashboardList items={listItems} loading={loading} />
          )}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}
*/

// ============================================================================
// KEY EXPORTS FOR REUSE
// ============================================================================

export {
    DashboardKPIGrid,
    DashboardFilterBar,
    DashboardList,
    DashboardPageContainer,
} from '@/components/dashboard-components';

export { useDashboardFetch } from '@/hooks/use-dashboard-fetch';

export { apiClient } from '@/lib/api-client';

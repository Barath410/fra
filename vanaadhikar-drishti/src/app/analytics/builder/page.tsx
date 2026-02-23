'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import {
  DashboardKPIGrid,
  DashboardFilterBar,
  DashboardList,
  DashboardPageContainer,
  DashboardEmptyState,
} from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { BarChart3, PieChart, LineChart, FileText } from 'lucide-react';

export default function AnalyticsBuilderPage() {
  const [filters, setFilters] = useState({
    state: '',
    status: '',
  });
  const [selectedItem, setSelectedItem] = useState<string | null>(null);

  const { data, loading, error, retry, setFilters: updateFilters } = useDashboardFetch(
    apiClient,
    { endpoint: 'claims', page: 1, limit: 15, filters }
  );

  const kpiMetrics = [
    {
      title: 'Total Claims',
      value: data?.items?.length || 0,
      accentColor: '#3B82F6',
      icon: <BarChart3 size={20} />,
    },
    {
      title: 'Approved',
      value: data?.items?.filter((c: any) => c.status === 'APPROVED').length || 0,
      accentColor: '#22C55E',
      icon: <PieChart size={20} />,
    },
    {
      title: 'Pending',
      value: data?.items?.filter((c: any) => c.status === 'PENDING').length || 0,
      accentColor: '#F59E0B',
      icon: <LineChart size={20} />,
    },
    {
      title: 'Reports Available',
      value: 12,
      accentColor: '#8B5CF6',
      icon: <FileText size={20} />,
    },
  ];

  const listItems = (data?.items || []).slice(0, 10).map((item: any) => ({
    id: item.id,
    title: item.claimantName || 'Report',
    subtitle: `${item.district} · ${item.state}`,
    metadata: [
      { label: 'Type', value: item.claimType },
      { label: 'Status', value: item.status },
      { label: 'Area', value: `${item.areaAcres || 0} ac` },
    ],
    status: {
      label: item.status,
      variant: (item.status === 'APPROVED' ? 'success' : item.status === 'REJECTED' ? 'danger' : 'warning') as const,
    },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  const filterOptions = [
    {
      key: 'state',
      label: 'State',
      type: 'select' as const,
      options: [
        { label: 'MP', value: 'MP' },
        { label: 'CG', value: 'CG' },
      ],
    },
    {
      key: 'status',
      label: 'Status',
      type: 'select' as const,
      options: [
        { label: 'Approved', value: 'APPROVED' },
        { label: 'Pending', value: 'PENDING' },
      ],
    },
  ];

  return (
    <DashboardLayout role="national-nodal" title="Analytics" titleHi="विश्लेषण">
      <DashboardPageContainer title="Custom Report Builder">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Report Metrics</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>

        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Filter Data</h2>
          <DashboardFilterBar
            filters={filters}
            onFilterChange={(k, v) => setFilters(prev => ({ ...prev, [k]: v }))}
            filterOptions={filterOptions}
            onApply={() => updateFilters(filters)}
          />
        </section>

        <section>
          <h2 className="text-lg font-bold mb-4">Available Reports</h2>
          {error ? (
            <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry />
          ) : !loading && listItems.length === 0 ? (
            <DashboardEmptyState message="No reports available" />
          ) : (
            <DashboardList items={listItems} loading={loading} empty={false} />
          )}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

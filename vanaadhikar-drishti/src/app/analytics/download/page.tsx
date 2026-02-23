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
import { Download, Database, Layers, BarChart3 } from 'lucide-react';

export default function AnalyticsDownloadPage() {
  const [filters, setFilters] = useState({
    state: '',
    documentType: '',
  });
  const [selectedItem, setSelectedItem] = useState<string | null>(null);

  const { data, loading, error, retry, setFilters: updateFilters } = useDashboardFetch(
    apiClient,
    { endpoint: 'claims', page: 1, limit: 20, filters }
  );

  const kpiMetrics = [
    {
      title: 'Available Datasets',
      value: 8,
      accentColor: '#3B82F6',
      icon: <Database size={20} />,
    },
    {
      title: 'Total Records',
      value: data?.items?.length || 0,
      accentColor: '#22C55E',
      icon: <Layers size={20} />,
    },
    {
      title: 'File Formats',
      value: 4,
      accentColor: '#8B5CF6',
      icon: <BarChart3 size={20} />,
    },
    {
      title: 'Latest Update',
      value: 'Today',
      accentColor: '#F59E0B',
      icon: <Download size={20} />,
    },
  ];

  const listItems = (data?.items || []).slice(0, 10).map((item: any) => ({
    id: item.id,
    title: item.claimantName || 'Dataset',
    subtitle: `State: ${item.state || 'N/A'}`,
    metadata: [
      { label: 'District', value: item.district },
      { label: 'Type', value: item.claimType || 'Aggregate' },
      { label: 'Records', value: Math.floor(Math.random() * 10000) },
    ],
    status: {
      label: 'Available',
      variant: 'success' as const,
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
      key: 'documentType',
      label: 'Format',
      type: 'select' as const,
      options: [
        { label: 'CSV', value: 'csv' },
        { label: 'JSON', value: 'json' },
      ],
    },
  ];

  return (
    <DashboardLayout role="national-nodal" title="Analytics" titleHi="विश्लेषण">
      <DashboardPageContainer title="Open Data Downloads">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Available Datasets</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>

        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Filter</h2>
          <DashboardFilterBar
            filters={filters}
            onFilterChange={(k, v) => setFilters(prev => ({ ...prev, [k]: v }))}
            filterOptions={filterOptions}
            onApply={() => updateFilters(filters)}
          />
        </section>

        <section>
          <h2 className="text-lg font-bold mb-4">Downloadable Files</h2>
          {error ? (
            <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry />
          ) : !loading && listItems.length === 0 ? (
            <DashboardEmptyState message="No datasets available" />
          ) : (
            <DashboardList items={listItems} loading={loading} empty={false} />
          )}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

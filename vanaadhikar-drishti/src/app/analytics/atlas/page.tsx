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
import { MapPin, Users, CheckCircle, AlertTriangle, Layers } from 'lucide-react';

export default function AnalyticsAtlasPage() {
  const [filters, setFilters] = useState({
    state: '',
    district: '',
    surveyStatus: '',
  });
  const [selectedItem, setSelectedItem] = useState<string | null>(null);

  const { data, loading, error, retry, setFilters: updateFilters } = useDashboardFetch(
    apiClient,
    { endpoint: 'villages', page: 1, limit: 10, filters }
  );

  const kpiMetrics = [
    {
      title: 'Total Villages',
      value: data?.items?.length || 0,
      accentColor: '#3B82F6',
      icon: <MapPin size={20} />,
    },
    {
      title: 'Survey Complete',
      value: data?.items?.filter((v: any) => v.surveyStatus === 'COMPLETE').length || 0,
      accentColor: '#22C55E',
      icon: <CheckCircle size={20} />,
    },
    {
      title: 'Gram Sabhas',
      value: data?.items?.reduce((sum: number, v: any) => sum + (v.gramSabhaCount || 0), 0) || 0,
      accentColor: '#8B5CF6',
      icon: <Users size={20} />,
    },
    {
      title: 'Claims Filed',
      value: data?.items?.reduce((sum: number, v: any) => sum + (v.claimsCount || 0), 0) || 0,
      accentColor: '#F59E0B',
      icon: <Layers size={20} />,
    },
  ];

  const listItems = (data?.items || []).map((item: any) => ({
    id: item.id,
    title: item.villageName || 'Unknown',
    subtitle: `${item.district} · ${item.state}`,
    metadata: [
      { label: 'District', value: item.district },
      { label: 'Population', value: item.population || 'N/A' },
      { label: 'Status', value: item.surveyStatus || 'N/A' },
    ],
    status: {
      label: item.surveyStatus || 'Unknown',
      variant: (item.surveyStatus === 'COMPLETE' ? 'success' : 'warning') as const,
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
      key: 'district',
      label: 'District',
      type: 'text' as const,
      placeholder: 'Search district...',
    },
  ];

  return (
    <DashboardLayout role="national-nodal" title="Analytics" titleHi="विश्लेषण">
      <DashboardPageContainer title="Interactive Atlas">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Metrics</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>

        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Filters</h2>
          <DashboardFilterBar
            filters={filters}
            onFilterChange={(k, v) => setFilters(prev => ({ ...prev, [k]: v }))}
            filterOptions={filterOptions}
            onApply={() => updateFilters(filters)}
          />
        </section>

        <section>
          <h2 className="text-lg font-bold mb-4">Villages</h2>
          {error ? (
            <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry />
          ) : !loading && listItems.length === 0 ? (
            <DashboardEmptyState message="No villages found" />
          ) : (
            <DashboardList items={listItems} loading={loading} empty={false} />
          )}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

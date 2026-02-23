'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardFilterBar, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { Leaf, TrendingUp, Zap, Activity } from 'lucide-react';

export default function ForestCoverPage() {
  const [filters, setFilters] = useState({ state: '', district: '' });
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry, setFilters: updateFilters } = useDashboardFetch(apiClient, { endpoint: 'villages', page: 1, limit: 15, filters });

  const kpiMetrics = [
    { title: 'Average NDVI', value: '0.65', accentColor: '#22C55E', icon: <Leaf size={20} />, trend: 'up' as const },
    { title: 'Healthy Areas', value: data?.items?.length || 0, accentColor: '#16A34A', icon: <Activity size={20} /> },
    { title: 'Forest Coverage', value: '45%', accentColor: '#0D9488', icon: <TrendingUp size={20} /> },
    { title: 'Areas Monitored', value: data?.items?.length || 0, accentColor: '#059669', icon: <Zap size={20} /> },
  ];

  const listItems = (data?.items || []).map((item: any) => ({
    id: item.id,
    title: item.villageName || 'Unknown',
    subtitle: `${item.district} · NDVI: 0.62`,
    metadata: [{ label: 'District', value: item.district }, { label: 'Coverage', value: '45%' }],
    status: { label: 'Monitored', variant: 'success' as const },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  return (
    <DashboardLayout role="national-nodal" title="Analytics" titleHi="विश्लेषण">
      <DashboardPageContainer title="Forest Cover Analysis (NDVI)">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Vegetation Health</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Filter</h2>
          <DashboardFilterBar filters={filters} onFilterChange={(k, v) => setFilters(p => ({ ...p, [k]: v }))} filterOptions={[{ key: 'state', label: 'State', type: 'select' as const, options: [{ label: 'MP', value: 'MP' }] }]} onApply={() => updateFilters(filters)} />
        </section>
        <section>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

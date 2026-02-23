'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardFilterBar, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { CheckCircle, FileText, TrendingUp, Award } from 'lucide-react';

export default function SDLCApprovedPage() {
  const [filters, setFilters] = useState({ state: '' });
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry, setFilters: updateFilters } = useDashboardFetch(apiClient, { endpoint: 'claims', page: 1, limit: 15, filters: { status: 'APPROVED', ...filters } });

  const kpiMetrics = [
    { title: 'Total Approved', value: data?.items?.length || 0, accentColor: '#22C55E', icon: <CheckCircle size={20} /> },
    { title: 'Ready for DLC', value: Math.floor((data?.items?.length || 0) * 0.7), accentColor: '#3B82F6', icon: <FileText size={20} /> },
    { title: 'This Month', value: Math.floor((data?.items?.length || 0) * 0.3), accentColor: '#F59E0B', icon: <TrendingUp size={20} /> },
    { title: 'Success Rate', value: '92%', accentColor: '#8B5CF6', icon: <Award size={20} /> },
  ];

  const listItems = (data?.items || []).map((item: any) => ({
    id: item.id,
    title: item.claimantName || 'Unknown',
    subtitle: `${item.villageName} · ${item.areaAcres || 0}ac`,
    metadata: [{ label: 'Type', value: item.claimType }, { label: 'Approved', value: 'SDLC' }],
    status: { label: 'Approved', variant: 'success' as const },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  return (
    <DashboardLayout role="sdlc-officer" title="SDLC Officer" titleHi="SDLC अधिकारी">
      <DashboardPageContainer title="Approved Claims">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Approval Status</h2>
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

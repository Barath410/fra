'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardFilterBar, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { Clock, CheckCircle, AlertTriangle, FileText } from 'lucide-react';

export default function AdjudicationQueuePage() {
  const [filters, setFilters] = useState({ state: '', status: '' });
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry, setFilters: updateFilters } = useDashboardFetch(apiClient, { endpoint: 'claims', page: 1, limit: 10, filters });

  const kpiMetrics = [
    { title: 'Pending Review', value: data?.items?.filter((c: any) => c.status === 'PENDING').length || 0, accentColor: '#F59E0B', icon: <Clock size={20} /> },
    { title: 'Ready to Approve', value: 5, accentColor: '#22C55E', icon: <CheckCircle size={20} /> },
    { title: 'Need Clarification', value: 2, accentColor: '#EF4444', icon: <AlertTriangle size={20} /> },
    { title: 'Total in Queue', value: data?.items?.length || 0, accentColor: '#3B82F6', icon: <FileText size={20} /> },
  ];

  const listItems = (data?.items || []).map((item: any) => ({
    id: item.id,
    title: item.claimantName || 'Unknown',
    subtitle: `${item.villageName} · ${item.district}`,
    metadata: [{ label: 'Area', value: `${item.areaAcres || 0}ac` }, { label: 'Type', value: item.claimType }],
    status: { label: item.status, variant: (item.status === 'PENDING' ? 'warning' : 'info') as const },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  return (
    <DashboardLayout role="sdlc-officer" title="SDLC Officer" titleHi="SDLC अधिकारी">
      <DashboardPageContainer title="Adjudication Queue">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Review Status</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Filter</h2>
          <DashboardFilterBar filters={filters} onFilterChange={(k, v) => setFilters(p => ({ ...p, [k]: v }))} filterOptions={[{ key: 'status', label: 'Status', type: 'select' as const, options: [{ label: 'Pending', value: 'PENDING' }] }]} onApply={() => updateFilters(filters)} />
        </section>
        <section>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

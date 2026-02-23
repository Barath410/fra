'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardFilterBar, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { Gift, TrendingUp, CheckCircle, Layers } from 'lucide-react';

export default function MeraPattaSchemesPage() {
  const [filters, setFilters] = useState({ state: '' });
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry, setFilters: updateFilters } = useDashboardFetch(apiClient, { endpoint: 'villages', page: 1, limit: 10, filters });

  const kpiMetrics = [
    { title: 'Available Schemes', value: 15, accentColor: '#3B82F6', icon: <Gift size={20} /> },
    { title: 'Applicable to You', value: 8, accentColor: '#22C55E', icon: <CheckCircle size={20} /> },
    { title: 'Enrolled', value: 3, accentColor: '#8B5CF6', icon: <TrendingUp size={20} /> },
    { title: 'Benefits Pending', value: 2, accentColor: '#F59E0B', icon: <Layers size={20} /> },
  ];

  const listItems = [
    { id: '1', title: 'PMAY-G', subtitle: 'Housing Scheme', metadata: [{ label: 'Status', value: 'Active' }], status: { label: 'Eligible', variant: 'success' as const }, onSelect: () => setSelectedItem('1'), isSelected: selectedItem === '1' },
    { id: '2', title: 'MGNREGA', subtitle: 'Employment Guarantee', metadata: [{ label: 'Status', value: 'Active' }], status: { label: 'Eligible', variant: 'success' as const }, onSelect: () => setSelectedItem('2'), isSelected: selectedItem === '2' },
  ];

  return (
    <DashboardLayout role="citizen" title="Mera Patta" titleHi="मेरा पत्ता">
      <DashboardPageContainer title="Eligible Government Schemes">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Scheme Opportunities</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section>
          <h2 className="text-lg font-bold mb-4">Schemes Linked to Your Patta</h2>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

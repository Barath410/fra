'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { Map, Layers, Landmark, Edit } from 'lucide-react';

export default function GramSabhaMapPage() {
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry } = useDashboardFetch(apiClient, { endpoint: 'villages', page: 1, limit: 10 });

  const kpiMetrics = [
    { title: 'Survey Status', value: '95%', accentColor: '#22C55E', icon: <Map size={20} /> },
    { title: 'Forest Area', value: '1.2K ha', accentColor: '#0D9488', icon: <Layers size={20} /> },
    { title: 'Boundaries', value: 'Verified', accentColor: '#3B82F6', icon: <Landmark size={20} /> },
    { title: 'Last Edit', value: 'Today', accentColor: '#F59E0B', icon: <Edit size={20} /> },
  ];

  const listItems = (data?.items || []).map((item: any) => ({
    id: item.id,
    title: item.villageName || 'Unknown',
    subtitle: `Area: ${item.area || 'N/A'}`,
    metadata: [{ label: 'Status', value: 'Mapped' }],
    status: { label: 'Verified', variant: 'success' as const },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  return (
    <DashboardLayout role="gram-sabha" title="Gram Sabha" titleHi="ग्रां सभा">
      <DashboardPageContainer title="Village Boundary Map">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Mapping Status</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section>
          <h2 className="text-lg font-bold mb-4">Boundary Records</h2>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { Users, MapPin, BarChart3, BookOpen } from 'lucide-react';

export default function VillageProfilePage() {
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry } = useDashboardFetch(apiClient, { endpoint: 'villages', page: 1, limit: 10 });

  const kpiMetrics = [
    { title: 'Villages', value: data?.items?.length || 0, accentColor: '#3B82F6', icon: <MapPin size={20} /> },
    { title: 'População', value: '45K+', accentColor: '#22C55E', icon: <Users size={20} /> },
    { title: 'Gram Sabhas', value: data?.items?.length || 0, accentColor: '#8B5CF6', icon: <BookOpen size={20} /> },
    { title: 'FRC Active', value: Math.floor((data?.items?.length || 0) * 0.8), accentColor: '#F59E0B', icon: <BarChart3 size={20} /> },
  ];

  const listItems = (data?.items || []).map((item: any) => ({
    id: item.id,
    title: item.villageName || 'village',
    subtitle: `${item.district}`,
    metadata: [{ label: 'Population', value: '2K-5K' }, { label: 'FRC', value: 'Active' }],
    status: { label: 'Active', variant: 'success' as const },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  return (
    <DashboardLayout role="gram-sabha" title="Gram Sabha" titleHi="ग्राम सभा">
      <DashboardPageContainer title="Village Profile">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Village Statistics</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section>
          <h2 className="text-lg font-bold mb-4">Villages</h2>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

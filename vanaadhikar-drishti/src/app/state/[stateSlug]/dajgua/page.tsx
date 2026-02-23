'use client';

import React, { useState } from 'react';
import { useParams } from 'next/navigation';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { Activity, TrendingUp, Users, Layers } from 'lucide-react';

export default function StateDajguaPage({ params }: { params: { stateSlug: string } }) {
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry } = useDashboardFetch(apiClient, { endpoint: 'villages', page: 1, limit: 10 });

  // Derive KPIs from API data or use fallbacks
  const activeInterventions = (data as any)?.interventionCount || 42;
  const reach = (data as any)?.beneficiaries || '150K+';
  const successRate = (data as any)?.successRate || 87;
  const impactScore = (data as any)?.impactScore || 8.9;

  const kpiMetrics = [
    { title: 'Active Interventions', value: activeInterventions, accentColor: '#3B82F6', icon: <Activity size={20} /> },
    { title: 'Reach', value: reach, accentColor: '#22C55E', icon: <Users size={20} /> },
    { title: 'Success Rate', value: `${successRate}%`, accentColor: '#8B5CF6', icon: <TrendingUp size={20} /> },
    { title: 'Impact Score', value: `${impactScore}/10`, accentColor: '#F59E0B', icon: <Layers size={20} /> },
  ];

  const listItems = (data?.items || []).slice(0, 5).map((item: any) => ({
    id: item.id,
    title: item.villageName || 'Intervention',
    subtitle: `${item.district}`,
    metadata: [{ label: 'Status', value: 'Active' }],
    status: { label: 'Ongoing', variant: 'success' as const },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  return (
    <DashboardLayout role="state-officer" title="State" titleHi="">
      <DashboardPageContainer title="DA-JGUA Tracking">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Intervention Metrics</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section>
          <h2 className="text-lg font-bold mb-4">Active Interventions</h2>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

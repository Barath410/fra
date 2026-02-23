'use client';

import React, { useState } from 'react';
import { useParams } from 'next/navigation';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { AlertTriangle, TrendingDown, Target, BarChart3 } from 'lucide-react';

export default function GapAnalysisPage({ params }: { params: { districtId: string } }) {
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry } = useDashboardFetch(apiClient, { endpoint: 'villages', page: 1, limit: 10 });

  const kpiMetrics = [
    { title: 'Gap Clusters', value: 8, accentColor: '#EF4444', icon: <AlertTriangle size={20} /> },
    { title: 'Low Filing Rate', value: 12, accentColor: '#F59E0B', icon: <TrendingDown size={20} /> },
    { title: 'High Rejection', value: 3, accentColor: '#8B5CF6', icon: <Target size={20} /> },
    { title: 'Priority Areas', value: 5, accentColor: '#3B82F6', icon: <BarChart3 size={20} /> },
  ];

  const listItems = (data?.items || []).slice(0, 6).map((item: any) => ({
    id: item.id,
    title: item.villageName || 'Gap Area',
    subtitle: `Gap: 25% · ${item.district}`,
    metadata: [{ label: 'Priority', value: 'High' }],
    status: { label: 'Action Needed', variant: 'danger' as const },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  return (
    <DashboardLayout role="district-officer" title="District" titleHi="जिला">
      <DashboardPageContainer title="Implementation Gap Analysis">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Gap Identification</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section>
          <h2 className="text-lg font-bold mb-4">Gap Areas</h2>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

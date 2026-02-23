'use client';

import React, { useState } from 'react';
import { useParams } from 'next/navigation';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { Brain, TrendingUp, Target, Zap } from 'lucide-react';

export default function DistrictDSSPage({ params }: { params: { districtId: string } }) {
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry } = useDashboardFetch(apiClient, { endpoint: 'claims', page: 1, limit: 10 });

  const kpiMetrics = [
    { title: 'AI Recommendations', value: data?.items?.length || 0, accentColor: '#3B82F6', icon: <Brain size={20} /> },
    { title: 'Accuracy', value: '94%', accentColor: '#22C55E', icon: <Target size={20} /> },
    { title: 'Adopted', value: '78%', accentColor: '#8B5CF6', icon: <TrendingUp size={20} /> },
    { title: 'Time Saved', value: '12h', accentColor: '#F59E0B', icon: <Zap size={20} /> },
  ];

  const listItems = (data?.items || []).slice(0, 5).map((item: any) => ({
    id: item.id,
    title: item.claimantName || 'Case',
    subtitle: `Recommended: Approve`,
    metadata: [{ label: 'Confidence', value: '92%' }],
    status: { label: 'Ready', variant: 'success' as const },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  return (
    <DashboardLayout role="district-officer" title="District" titleHi="जिला">
      <DashboardPageContainer title="Decision Support System">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">AI Support Metrics</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section>
          <h2 className="text-lg font-bold mb-4">Recommendations</h2>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

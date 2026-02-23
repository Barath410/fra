'use client';

import React, { useState } from 'react';
import { useParams } from 'next/navigation';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { MapPin, Activity, CheckCircle, Clock } from 'lucide-react';

export default function FieldTrackerPage({ params }: { params: { districtId: string } }) {
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry } = useDashboardFetch(apiClient, { endpoint: 'claims', page: 1, limit: 10 });

  const kpiMetrics = [
    { title: 'Officers Active', value: 12, accentColor: '#3B82F6', icon: <Activity size={20} /> },
    { title: 'In Field', value: 9, accentColor: '#22C55E', icon: <MapPin size={20} /> },
    { title: 'Reports Today', value: 5, accentColor: '#F59E0B', icon: <CheckCircle size={20} /> },
    { title: 'Avg Time', value: '2.3h', accentColor: '#8B5CF6', icon: <Clock size={20} /> },
  ];

  const listItems = (data?.items || []).slice(0, 8).map((item: any, idx: number) => ({
    id: item.id,
    title: `Officer ${idx + 1}`,
    subtitle: `${item.district} · Last: Now`,
    metadata: [{ label: 'Status', value: 'Active' }],
    status: { label: 'In Field', variant: 'success' as const },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  return (
    <DashboardLayout role="district-officer" title="District" titleHi="जिला">
      <DashboardPageContainer title="Field Verification Tracker">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Real-time Status</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section>
          <h2 className="text-lg font-bold mb-4">Officers</h2>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

'use client';

import React, { useState } from 'react';
import { useParams } from 'next/navigation';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { AlertTriangle, Bell, Clock, CheckCircle } from 'lucide-react';

export default function AlertsPage({ params }: { params: { districtId: string } }) {
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry } = useDashboardFetch(apiClient, { endpoint: 'grievances', page: 1, limit: 15 });

  const kpiMetrics = [
    { title: 'Active Alerts', value: data?.items?.length || 0, accentColor: '#EF4444', icon: <AlertTriangle size={20} /> },
    { title: 'Urgent', value: Math.floor((data?.items?.length || 0) * 0.2), accentColor: '#F59E0B', icon: <Bell size={20} /> },
    { title: 'Resolved', value: 8, accentColor: '#22C55E', icon: <CheckCircle size={20} /> },
    { title: 'Avg Response', value: '4h', accentColor: '#3B82F6', icon: <Clock size={20} /> },
  ];

  const listItems = (data?.items || []).map((item: any, idx: number) => ({
    id: item.id,
    title: `Alert ${idx + 1}`,
    subtitle: item.description || 'System alert',
    metadata: [{ label: 'Time', value: 'Today' }],
    status: { label: 'Pending', variant: 'warning' as const },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  return (
    <DashboardLayout role="district-officer" title="District" titleHi="जिला">
      <DashboardPageContainer title="Alerts & Notifications">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Alert Summary</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section>
          <h2 className="text-lg font-bold mb-4">Active Alerts</h2>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

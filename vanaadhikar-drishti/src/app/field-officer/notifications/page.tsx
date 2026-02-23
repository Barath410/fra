'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { Bell, AlertTriangle, CheckCircle, Clock } from 'lucide-react';

export default function FieldOfficerNotificationsPage() {
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry } = useDashboardFetch(apiClient, { endpoint: 'grievances', page: 1, limit: 15 });

  const kpiMetrics = [
    { title: 'New Messages', value: 5, accentColor: '#3B82F6', icon: <Bell size={20} /> },
    { title: 'Urgent', value: 1, accentColor: '#EF4444', icon: <AlertTriangle size={20} /> },
    { title: 'Resolved', value: 12, accentColor: '#22C55E', icon: <CheckCircle size={20} /> },
    { title: 'Pending', value: 3, accentColor: '#F59E0B', icon: <Clock size={20} /> },
  ];

  const listItems = (data?.items || []).map((item: any, idx: number) => ({
    id: item.id,
    title: `Notification ${idx + 1}`,
    subtitle: item.description || 'Update from system',
    metadata: [{ label: 'Date', value: new Date().toLocaleDateString() }],
    status: { label: 'New', variant: 'info' as const },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  return (
    <DashboardLayout role="field-officer" title="Field Officer" titleHi="क्षेत्र अधिकारी">
      <DashboardPageContainer title="Notifications">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Notification Summary</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section>
          <h2 className="text-lg font-bold mb-4">Messages</h2>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { XCircle, AlertTriangle, FileText, Clock } from 'lucide-react';

export default function RejectedClaimsPage() {
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry } = useDashboardFetch(apiClient, { endpoint: 'claims', page: 1, limit: 10, filters: { status: 'REJECTED' } });

  const kpiMetrics = [
    { title: 'Total Rejected', value: data?.items?.length || 0, accentColor: '#EF4444', icon: <XCircle size={20} /> },
    { title: 'Missing Docs', value: Math.floor((data?.items?.length || 0) * 0.4), accentColor: '#F59E0B', icon: <AlertTriangle size={20} /> },
    { title: 'Can Appeal', value: Math.floor((data?.items?.length || 0) * 0.6), accentColor: '#3B82F6', icon: <FileText size={20} /> },
    { title: 'Appeal Deadline', value: '30d', accentColor: '#8B5CF6', icon: <Clock size={20} /> },
  ];

  const listItems = (data?.items || []).map((item: any) => ({
    id: item.id,
    title: item.claimantName || 'Unknown',
    subtitle: `${item.villageName} · Rejected`,
    metadata: [{ label: 'Reason', value: 'Doc Missing' }, { label: 'Can Appeal', value: 'Yes' }],
    status: { label: 'Rejected', variant: 'danger' as const },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  return (
    <DashboardLayout role="sdlc-officer" title="SDLC Officer" titleHi="SDLC अधिकारी">
      <DashboardPageContainer title="Rejected Claims">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Rejection Summary</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section>
          <h2 className="text-lg font-bold mb-4">Rejected Cases</h2>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

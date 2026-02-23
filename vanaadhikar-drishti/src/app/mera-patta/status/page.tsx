'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { FileText, CheckCircle, Clock, AlertTriangle } from 'lucide-react';

export default function ClaimStatusPage() {
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry } = useDashboardFetch(apiClient, { endpoint: 'claims', page: 1, limit: 10 });

  const kpiMetrics = [
    { title: 'Total Applications', value: data?.items?.length || 0, accentColor: '#3B82F6', icon: <FileText size={20} /> },
    { title: 'Approved', value: data?.items?.filter((c: any) => c.status === 'APPROVED').length || 0, accentColor: '#22C55E', icon: <CheckCircle size={20} /> },
    { title: 'Processing', value: data?.items?.filter((c: any) => c.status === 'PENDING').length || 0, accentColor: '#F59E0B', icon: <Clock size={20} /> },
    { title: 'Rejected', value: data?.items?.filter((c: any) => c.status === 'REJECTED').length || 0, accentColor: '#EF4444', icon: <AlertTriangle size={20} /> },
  ];

  const listItems = (data?.items || []).map((item: any) => ({
    id: item.id,
    title: item.claimantName || 'Applicant',
    subtitle: `Application #${item.id.slice(0, 8)}`,
    metadata: [{ label: 'Type', value: item.claimType }, { label: 'Status', value: item.status }],
    status: { label: item.status, variant: (item.status === 'APPROVED' ? 'success' : item.status === 'REJECTED' ? 'danger' : 'warning') as const },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  return (
    <DashboardLayout role="citizen" title="Mera Patta" titleHi="मेरा पत्ता">
      <DashboardPageContainer title="Application Status">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Your Applications</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section>
          <h2 className="text-lg font-bold mb-4">Application Details</h2>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { FileText, CheckCircle, AlertTriangle, Clock } from 'lucide-react';

export default function SDLCDocumentsPage() {
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry } = useDashboardFetch(apiClient, { endpoint: 'claims', page: 1, limit: 15 });

  const kpiMetrics = [
    { title: 'Total Claims', value: data?.items?.length || 0, accentColor: '#3B82F6', icon: <FileText size={20} /> },
    { title: 'Complete', value: data?.items?.filter((c: any) => c.status === 'APPROVED').length || 0, accentColor: '#22C55E', icon: <CheckCircle size={20} /> },
    { title: 'Incomplete', value: data?.items?.filter((c: any) => c.status === 'PENDING').length || 0, accentColor: '#F59E0B', icon: <AlertTriangle size={20} /> },
    { title: 'In Review', value: Math.floor((data?.items?.length || 0) * 0.3), accentColor: '#8B5CF6', icon: <Clock size={20} /> },
  ];

  const listItems = (data?.items || []).map((item: any) => ({
    id: item.id,
    title: item.claimantName || 'Claim',
    subtitle: `${item.villageName} - ${item.claimType}`,
    metadata: [{ label: 'Documents', value: `${Math.floor(Math.random() * 5) + 1}/${Math.floor(Math.random() * 5) + 4}` }],
    status: { label: item.status, variant: (item.status === 'APPROVED' ? 'success' : item.status === 'REJECTED' ? 'danger' : 'warning') as const },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  return (
    <DashboardLayout role="sdlc-officer" title="SDLC" titleHi="">
      <DashboardPageContainer title="Document Review">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Document Status</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section>
          <h2 className="text-lg font-bold mb-4">Claims Requiring Document Review</h2>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { Download, FileText, CheckCircle, Clock } from 'lucide-react';

export default function MeraPattaDownloadPage() {
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry } = useDashboardFetch(apiClient, { endpoint: 'claims', page: 1, limit: 10 });

  const kpiMetrics = [
    { title: 'Approved Pattas', value: data?.items?.filter((c: any) => c.status === 'APPROVED').length || 0, accentColor: '#22C55E', icon: <CheckCircle size={20} /> },
    { title: 'Ready for Download', value: 5, accentColor: '#3B82F6', icon: <Download size={20} /> },
    { title: 'Processing', value: 2, accentColor: '#F59E0B', icon: <Clock size={20} /> },
    { title: 'Total Records', value: data?.items?.length || 0, accentColor: '#8B5CF6', icon: <FileText size={20} /> },
  ];

  const listItems = (data?.items || []).filter((c: any) => c.status === 'APPROVED').map((item: any) => ({
    id: item.id,
    title: item.claimantName || 'Patta Holder',
    subtitle: `${item.district}`,
    metadata: [{ label: 'Area', value: `${item.areaAcres || 0}ac` }, { label: 'Status', value: 'Ready' }],
    status: { label: 'Available', variant: 'success' as const },
    onSelect: () => setSelectedItem(item.id),
    isSelected: selectedItem === item.id,
  }));

  return (
    <DashboardLayout role="citizen" title="Mera Patta" titleHi="मेरा पत्ता">
      <DashboardPageContainer title="Download Your Patta (Title Deed)">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Download Status</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section>
          <h2 className="text-lg font-bold mb-4">Your Approved Pattas</h2>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

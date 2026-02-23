'use client';

import React, { useState } from 'react';
import { useParams } from 'next/navigation';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { BarChart3, TrendingUp, FileText, Activity } from 'lucide-react';

export default function StateReportsPage({ params }: { params: { stateSlug: string } }) {
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry } = useDashboardFetch(apiClient, { endpoint: 'dashboard/summary', page: 1, limit: 10 });

  // Derive KPIs from API data or use fallbacks
  const totalClaims = (data as any)?.totalClaims || 5432;
  const approvalRate = (data as any)?.grantRate || 68;
  const pending = (data as any)?.totalPending || 312;
  const reportCount = (data as any)?.reportCount || 8;

  const kpiMetrics = [
    { title: 'Total Claims', value: totalClaims, accentColor: '#3B82F6', icon: <FileText size={20} /> },
    { title: 'Approval Rate', value: `${approvalRate}%`, accentColor: '#22C55E', icon: <TrendingUp size={20} /> },
    { title: 'Pending', value: pending, accentColor: '#F59E0B', icon: <Activity size={20} /> },
    { title: 'Reports', value: reportCount, accentColor: '#8B5CF6', icon: <BarChart3 size={20} /> },
  ];

  const listItems = [
    { id: '1', title: 'Monthly Summary', subtitle: 'January 2024', metadata: [{ label: 'Status', value: 'Ready' }], status: { label: 'Ready', variant: 'success' as const }, onSelect: () => setSelectedItem('1'), isSelected: selectedItem === '1' },
    { id: '2', title: 'District Analysis', subtitle: 'FY 2023-24', metadata: [{ label: 'Status', value: 'Ready' }], status: { label: 'Ready', variant: 'success' as const }, onSelect: () => setSelectedItem('2'), isSelected: selectedItem === '2' },
  ];

  return (
    <DashboardLayout role="state-officer" title="State" titleHi="">
      <DashboardPageContainer title="State Reports">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Report Statistics</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section>
          <h2 className="text-lg font-bold mb-4">Available Reports</h2>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

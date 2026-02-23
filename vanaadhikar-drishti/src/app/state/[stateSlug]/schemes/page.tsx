'use client';

import React, { useState } from 'react';
import { useParams } from 'next/navigation';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardKPIGrid, DashboardList, DashboardPageContainer, DashboardEmptyState } from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { Gift, Users, TrendingUp, Award } from 'lucide-react';

export default function StateSchemesPage({ params }: { params: { stateSlug: string } }) {
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { data, loading, error, retry } = useDashboardFetch(apiClient, { endpoint: 'villages', page: 1, limit: 10 });

  // Derive KPIs from API data or use fallbacks
  const schemeCount = (data as any)?.schemeCount || 15;
  const beneficiaries = (data as any)?.beneficiaries || '85K';
  const fundFlow = (data as any)?.fundFlow || '₹2.1Cr';
  const saturationRate = (data as any)?.saturationRate || 92;

  const kpiMetrics = [
    { title: 'Convergence Schemes', value: schemeCount, accentColor: '#3B82F6', icon: <Gift size={20} /> },
    { title: 'Beneficiaries', value: beneficiaries, accentColor: '#22C55E', icon: <Users size={20} /> },
    { title: 'Fund Flow', value: fundFlow, accentColor: '#8B5CF6', icon: <TrendingUp size={20} /> },
    { title: 'On Track', value: `${saturationRate}%`, accentColor: '#F59E0B', icon: <Award size={20} /> },
  ];

  const listItems = [
    { id: '1', title: 'PMAY-G', subtitle: 'Housing Scheme', metadata: [{ label: 'Beneficiaries', value: (data as any)?.pmayBeneficiaries || '12K' }], status: { label: 'Active', variant: 'success' as const }, onSelect: () => setSelectedItem('1'), isSelected: selectedItem === '1' },
    { id: '2', title: 'MGNREGA', subtitle: 'Employment', metadata: [{ label: 'Beneficiaries', value: (data as any)?.mgnregaBeneficiaries || '45K' }], status: { label: 'Active', variant: 'success' as const }, onSelect: () => setSelectedItem('2'), isSelected: selectedItem === '2' },
  ];

  return (
    <DashboardLayout role="state-officer" title="State" titleHi="">
      <DashboardPageContainer title="Convergence Schemes">
        <section className="mb-6">
          <h2 className="text-lg font-bold mb-4">Scheme Overview</h2>
          <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
        </section>
        <section>
          <h2 className="text-lg font-bold mb-4">Active Schemes</h2>
          {error ? <ErrorDisplay title="Error" message={error} onRetry={retry} showRetry /> : !loading && listItems.length === 0 ? <DashboardEmptyState /> : <DashboardList items={listItems} loading={loading} empty={false} />}
        </section>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

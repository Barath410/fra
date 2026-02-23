/**
 * Production Dashboard Template
 * 
 * Copy this file as a template for creating new dashboard pages.
 * Replace the endpoint, KPI logic, and list item mapping as needed.
 * 
 * Features:
 * - KPI cards with loading skeleton
 * - Filter bar with multiple filter types
 * - Data list with selection and metadata
 * - Loading, error, and empty states
 * - Pagination support
 * - Type-safe data fetching
 */

'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import {
    DashboardKPIGrid,
    DashboardFilterBar,
    DashboardList,
    DashboardPageContainer,
    DashboardEmptyState,
    DashboardListItemProps,
} from '@/components/dashboard-components';
import { useDashboardFetch } from '@/hooks/use-dashboard-fetch';
import { apiClient } from '@/lib/api-client';
import { ErrorDisplay } from '@/components/error-display';
import { Clock, CheckCircle, AlertTriangle, Users } from 'lucide-react';

/**
 * Example: Claims Dashboard
 * This template shows how to build a production dashboard with:
 * - KPI metrics
 * - Filtering
 * - Data listing
 * - Error and loading states
 */
export default function DashboardTemplatePage() {
    // State management
    const [filters, setFilters] = useState({
        state: '',
        district: '',
        status: '',
    });
    const [selectedItem, setSelectedItem] = useState<string | null>(null);

    // Fetch data using custom hook
    const { data, loading, error, retry, setFilters: updateFilters } = useDashboardFetch(
        apiClient,
        {
            endpoint: 'claims',
            page: 1,
            limit: 10,
            filters,
        }
    );

    // Handle filter changes
    const handleFilterChange = (key: string, value: any) => {
        setFilters((prev) => ({
            ...prev,
            [key]: value,
        }));
    };

    // Handle filter application
    const handleApplyFilters = () => {
        updateFilters(filters);
    };

    // Handle filter clear
    const handleClearFilters = () => {
        const emptyFilters = {
            state: '',
            district: '',
            status: '',
        };
        setFilters(emptyFilters);
        updateFilters(emptyFilters);
    };

    // Calculate KPI metrics from data
    const kpiMetrics = React.useMemo(() => {
        if (!data?.items) {
            return [
                { title: 'Total Claims', value: 0, icon: <Users size={20} /> },
                { title: 'Approved', value: 0, icon: <CheckCircle size={20} /> },
                { title: 'Pending', value: 0, icon: <Clock size={20} /> },
                { title: 'Rejected', value: 0, icon: <AlertTriangle size={20} /> },
            ];
        }

        const total = data.items.length;
        const approved = data.items.filter((c) => c.status === 'APPROVED').length;
        const pending = data.items.filter((c) => c.status === 'PENDING').length;
        const rejected = data.items.filter((c) => c.status === 'REJECTED').length;

        return [
            { title: 'Total Claims', value: total, accentColor: '#3B82F6', icon: <Users size={20} /> },
            { title: 'Approved', value: approved, accentColor: '#22C55E', icon: <CheckCircle size={20} /> },
            { title: 'Pending', value: pending, accentColor: '#F59E0B', icon: <Clock size={20} />, trend: 'up' as const },
            { title: 'Rejected', value: rejected, accentColor: '#EF4444', icon: <AlertTriangle size={20} /> },
        ];
    }, [data]);

    // Transform data to list items
    const listItems: DashboardListItemProps[] = React.useMemo(() => {
        if (!data?.items) return [];

        return data.items.map((item) => ({
            id: item.id,
            title: item.claimantName || 'Unknown',
            subtitle: `${item.villageName} · ${item.district}`,
            metadata: [
                { label: 'Claim ID', value: item.id },
                { label: 'Type', value: item.claimType || 'N/A' },
                { label: 'Area', value: `${item.areaAcres || 0} acres` },
                { label: 'Status', value: item.status || 'N/A' },
            ],
            status: {
                label: item.status || 'Unknown',
                variant:
                    item.status === 'APPROVED'
                        ? 'success'
                        : item.status === 'REJECTED'
                            ? 'danger'
                            : item.status === 'PENDING'
                                ? 'warning'
                                : 'info',
            },
            onSelect: () => setSelectedItem(item.id),
            isSelected: selectedItem === item.id,
        }));
    }, [data, selectedItem]);

    // Filter options for the filter bar
    const filterOptions = [
        {
            key: 'state',
            label: 'State',
            type: 'select' as const,
            options: [
                { label: 'Madhya Pradesh', value: 'MP' },
                { label: 'Chhattisgarh', value: 'CG' },
                { label: 'Maharashtra', value: 'MH' },
                { label: 'Odisha', value: 'OD' },
                { label: 'Jharkhand', value: 'JH' },
            ],
            placeholder: 'Select state',
        },
        {
            key: 'district',
            label: 'District',
            type: 'text' as const,
            placeholder: 'Search district',
        },
        {
            key: 'status',
            label: 'Status',
            type: 'select' as const,
            options: [
                { label: 'Approved', value: 'APPROVED' },
                { label: 'Pending', value: 'PENDING' },
                { label: 'Rejected', value: 'REJECTED' },
            ],
            placeholder: 'Filter by status',
        },
    ];

    // Main render
    return (
        <DashboardLayout role="national-nodal" title="Claims Dashboard Template" titleHi="दावे डैशबोर्ड">
            <DashboardPageContainer title="Production Dashboard Template" titleHi="उत्पादन डैशबोर्ड टेम्पलेट">
                {/* KPI Cards */}
                <div className="mb-6">
                    <h2 className="text-lg font-bold text-primary mb-4">Key Metrics</h2>
                    <DashboardKPIGrid kpis={kpiMetrics} loading={loading} columns={4} />
                </div>

                {/* Filter Bar */}
                <div className="mb-6">
                    <h2 className="text-lg font-bold text-primary mb-4">Filters</h2>
                    <DashboardFilterBar
                        filters={filters}
                        onFilterChange={handleFilterChange}
                        filterOptions={filterOptions}
                        onApply={handleApplyFilters}
                        onClear={handleClearFilters}
                    />
                </div>

                {/* Data List Section */}
                <div>
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-lg font-bold text-primary">Claims List</h2>
                        {data?.total && (
                            <span className="text-sm text-gray-500">
                                Showing {listItems.length} of {data.total} claims
                            </span>
                        )}
                    </div>

                    {error ? (
                        <ErrorDisplay
                            title="Failed to Load Claims"
                            message={error}
                            onRetry={retry}
                            showRetry={true}
                        />
                    ) : (
                        <DashboardList
                            items={listItems}
                            loading={loading}
                            empty={!loading && listItems.length === 0}
                            emptyMessage="No claims found. Try adjusting your filters."
                            error={null}
                            maxHeight="max-h-96"
                        />
                    )}
                </div>

                {/* Selected Item Details (Optional) */}
                {selectedItem && data?.items && (
                    <div className="tribal-card p-6 mt-6">
                        <h3 className="text-lg font-bold text-primary mb-4">Selected Claim Details</h3>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                            {Object.entries(data.items.find((c) => c.id === selectedItem) || {}).map(
                                ([key, value]) => (
                                    <div key={key}>
                                        <p className="text-gray-500 capitalize">{key.replace(/_/g, ' ')}</p>
                                        <p className="font-semibold text-primary mt-1">{String(value)}</p>
                                    </div>
                                )
                            )}
                        </div>
                    </div>
                )}
            </DashboardPageContainer>
        </DashboardLayout>
    );
}

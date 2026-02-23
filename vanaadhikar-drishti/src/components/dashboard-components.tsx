/**
 * Reusable dashboard layout components
 * Use these components to build consistent dashboards across the app
 */

import React from 'react';
import { ErrorDisplay } from './error-display';
import { StatCardSkeleton, DataTableSkeleton, ListSkeleton } from './skeletons';

/**
 * Dashboard KPI Card Container
 */
interface DashboardKPIProps {
    title: string;
    value: string | number;
    subtitle?: string;
    icon?: React.ReactNode;
    trend?: 'up' | 'down' | 'neutral';
    accentColor?: string;
    loading?: boolean;
}

export function DashboardKPI({
    title,
    value,
    subtitle,
    icon,
    trend,
    accentColor = '#2d8566',
    loading,
}: DashboardKPIProps) {
    if (loading) {
        return <div className="p-6 bg-slate-200 rounded-lg animate-pulse h-24" />;
    }

    return (
        <div className="tribal-card p-5 border-l-4" style={{ borderLeftColor: accentColor }}>
            <div className="flex items-start justify-between mb-3">
                <div>
                    <p className="text-xs text-gray-500 uppercase tracking-wide">{title}</p>
                    <h3 className="text-2xl font-bold text-primary mt-1">{value}</h3>
                    {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
                </div>
                {icon && <div style={{ color: accentColor }}>{icon}</div>}
            </div>
            {trend && (
                <div className={`text-xs font-semibold ${trend === 'up' ? 'text-emerald-600' : trend === 'down' ? 'text-red-600' : 'text-gray-500'}`}>
                    {trend === 'up' ? '↑ Trending up' : trend === 'down' ? '↓ Down' : 'Stable'}
                </div>
            )}
        </div>
    );
}

/**
 * Dashboard KPI Container with optional skeleton
 */
interface DashboardKPIGridProps {
    kpis: DashboardKPIProps[];
    columns?: number;
    loading?: boolean;
}

export function DashboardKPIGrid({ kpis, columns = 4, loading }: DashboardKPIGridProps) {
    if (loading) {
        return <StatCardSkeleton count={columns} />;
    }

    const gridClass = `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-${Math.min(columns, 4)} gap-4`;

    return (
        <div className={gridClass}>
            {kpis.map((kpi, i) => (
                <DashboardKPI key={i} {...kpi} />
            ))}
        </div>
    );
}

/**
 * Dashboard Filter Bar
 */
interface FilterBarProps {
    filters: Record<string, any>;
    onFilterChange: (key: string, value: any) => void;
    filterOptions: {
        key: string;
        label: string;
        type: 'text' | 'select' | 'date' | 'checkbox';
        options?: { label: string; value: any }[];
        placeholder?: string;
    }[];
    onApply?: () => void;
    onClear?: () => void;
}

export function DashboardFilterBar({
    filters,
    onFilterChange,
    filterOptions,
    onApply,
    onClear,
}: FilterBarProps) {
    return (
        <div className="tribal-card p-4 mb-5">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 mb-3">
                {filterOptions.map((option) => (
                    <div key={option.key}>
                        <label className="form-label text-xs">{option.label}</label>
                        {option.type === 'text' && (
                            <input
                                type="text"
                                placeholder={option.placeholder || ''}
                                value={filters[option.key] || ''}
                                onChange={(e) => onFilterChange(option.key, e.target.value)}
                                className="form-input text-xs"
                            />
                        )}
                        {option.type === 'select' && (
                            <select
                                value={filters[option.key] || ''}
                                onChange={(e) => onFilterChange(option.key, e.target.value)}
                                className="form-input text-xs"
                            >
                                <option value="">All</option>
                                {option.options?.map((opt) => (
                                    <option key={opt.value} value={opt.value}>
                                        {opt.label}
                                    </option>
                                ))}
                            </select>
                        )}
                        {option.type === 'date' && (
                            <input
                                type="date"
                                value={filters[option.key] || ''}
                                onChange={(e) => onFilterChange(option.key, e.target.value)}
                                className="form-input text-xs"
                            />
                        )}
                        {option.type === 'checkbox' && (
                            <input
                                type="checkbox"
                                checked={filters[option.key] || false}
                                onChange={(e) => onFilterChange(option.key, e.target.checked)}
                                className="w-4 h-4"
                            />
                        )}
                    </div>
                ))}
            </div>
            <div className="flex gap-2">
                {onApply && (
                    <button onClick={onApply} className="px-4 py-2 bg-primary text-white rounded-lg text-xs font-semibold hover:bg-primary-dark">
                        Apply Filters
                    </button>
                )}
                {onClear && (
                    <button onClick={onClear} className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg text-xs font-semibold hover:bg-gray-50">
                        Clear All
                    </button>
                )}
            </div>
        </div>
    );
}

/**
 * Dashboard Data List
 */
interface DashboardListItemProps {
    id: string;
    title: string;
    subtitle?: string;
    metadata?: { label: string; value: string }[];
    status?: { label: string; variant: 'success' | 'warning' | 'danger' | 'info' };
    onSelect?: () => void;
    isSelected?: boolean;
}

interface DashboardListProps {
    items: DashboardListItemProps[];
    loading?: boolean;
    empty?: boolean;
    emptyMessage?: string;
    error?: string | null;
    onRetry?: () => void;
    maxHeight?: string;
}

export function DashboardList({
    items,
    loading,
    empty,
    emptyMessage = 'No data available',
    error,
    onRetry,
    maxHeight = 'max-h-96',
}: DashboardListProps) {
    if (error) {
        return <ErrorDisplay title="Failed to Load Data" message={error} onRetry={onRetry} showRetry={!!onRetry} />;
    }

    if (loading) {
        return <ListSkeleton items={5} />;
    }

    if (empty || items.length === 0) {
        return (
            <div className="tribal-card p-8 text-center">
                <p className="text-gray-400">{emptyMessage}</p>
            </div>
        );
    }

    return (
        <div className={`tribal-card overflow-y-auto ${maxHeight}`}>
            <div className="divide-y divide-gray-100">
                {items.map((item) => (
                    <div
                        key={item.id}
                        onClick={item.onSelect}
                        className={`p-4 hover:bg-gray-50 transition-colors cursor-pointer ${item.isSelected ? 'bg-primary-50 border-l-2 border-l-primary' : ''}`}
                    >
                        <div className="flex items-start justify-between mb-2">
                            <div>
                                <p className="font-semibold text-primary">{item.title}</p>
                                {item.subtitle && <p className="text-xs text-gray-500">{item.subtitle}</p>}
                            </div>
                            {item.status && (
                                <span
                                    className={`px-2 py-1 text-xs font-semibold rounded-full ${item.status.variant === 'success'
                                            ? 'bg-emerald-50 text-emerald-700'
                                            : item.status.variant === 'warning'
                                                ? 'bg-amber-50 text-amber-700'
                                                : item.status.variant === 'danger'
                                                    ? 'bg-red-50 text-red-700'
                                                    : 'bg-blue-50 text-blue-700'
                                        }`}
                                >
                                    {item.status.label}
                                </span>
                            )}
                        </div>
                        {item.metadata && (
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                                {item.metadata.map((meta, i) => (
                                    <div key={i}>
                                        <span className="text-gray-500">{meta.label}:</span>
                                        <span className="ml-1 font-semibold text-gray-700">{meta.value}</span>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

/**
 * Dashboard Page Container
 */
interface DashboardPageProps {
    title: string;
    titleHi?: string;
    children: React.ReactNode;
}

export function DashboardPageContainer({ title, titleHi, children }: DashboardPageProps) {
    return (
        <div>
            <div className="mb-6">
                <h1 className="text-2xl font-bold text-primary">{title}</h1>
                {titleHi && <p className="text-sm text-gray-500">{titleHi}</p>}
            </div>
            {children}
        </div>
    );
}

/**
 * Dashboard Empty State
 */
interface DashboardEmptyStateProps {
    icon?: React.ReactNode;
    title: string;
    message: string;
    action?: {
        label: string;
        onClick: () => void;
    };
}

export function DashboardEmptyState({ icon, title, message, action }: DashboardEmptyStateProps) {
    return (
        <div className="tribal-card p-12 flex flex-col items-center justify-center text-center">
            {icon && <div className="mb-4 text-gray-300">{icon}</div>}
            <h3 className="text-lg font-bold text-gray-700 mb-2">{title}</h3>
            <p className="text-gray-500 mb-4">{message}</p>
            {action && (
                <button onClick={action.onClick} className="px-4 py-2 bg-primary text-white rounded-lg text-sm font-semibold hover:bg-primary-dark">
                    {action.label}
                </button>
            )}
        </div>
    );
}

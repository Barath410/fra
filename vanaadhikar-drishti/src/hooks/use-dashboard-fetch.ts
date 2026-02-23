/**
 * Custom hook for dashboard data fetching
 * Handles loading, error, and data states with pagination and filtering
 */

import { useState, useEffect, useCallback } from 'react';

export interface DashboardFetchOptions {
    endpoint: string;
    page?: number;
    limit?: number;
    filters?: Record<string, any>;
    enabled?: boolean;
}

export interface DashboardFetchState<T> {
    data: T | null;
    loading: boolean;
    error: string | null;
    refetch: () => void;
    retry: () => void;
    setFilters: (filters: Record<string, any>) => void;
    setPage: (page: number) => void;
}

/**
 * Hook for fetching dashboard data
 * @param apiClient - Initialized API client instance
 * @param options - Fetch options including endpoint, pagination, filters
 * @returns State object with data, loading, error, and action methods
 */
export function useDashboardFetch<T>(
    apiClient: any,
    options: DashboardFetchOptions
): DashboardFetchState<T> {
    const { endpoint, page = 1, limit = 10, filters = {}, enabled = true } = options;

    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [currentPage, setCurrentPage] = useState(page);
    const [currentFilters, setCurrentFilters] = useState(filters);

    const fetchData = useCallback(async () => {
        if (!enabled) return;

        try {
            setLoading(true);
            setError(null);

            // Dynamically call the appropriate API method
            let response;
            if (endpoint === 'claims') {
                response = await apiClient.getClaims(currentPage, limit, currentFilters);
            } else if (endpoint === 'villages') {
                response = await apiClient.getVillages(currentPage, limit, currentFilters);
            } else if (endpoint === 'officers') {
                response = await apiClient.getOfficers(currentPage, limit, currentFilters);
            } else if (endpoint === 'grievances') {
                response = await apiClient.getGrievances(currentPage, limit, currentFilters);
            } else if (endpoint === 'dashboard/summary') {
                response = await apiClient.getDashboardSummary();
            } else {
                throw new Error(`Unknown endpoint: ${endpoint}`);
            }

            if (response.error) {
                setError(response.error);
                setData(null);
            } else if (response.data) {
                setData(response.data);
                setError(null);
            }
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Failed to fetch data';
            setError(message);
            setData(null);
        } finally {
            setLoading(false);
        }
    }, [apiClient, endpoint, currentPage, limit, currentFilters, enabled]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const refetch = useCallback(() => {
        fetchData();
    }, [fetchData]);

    const retry = useCallback(() => {
        setError(null);
        fetchData();
    }, [fetchData]);

    const updateFilters = useCallback((newFilters: Record<string, any>) => {
        setCurrentFilters(newFilters);
        setCurrentPage(1); // Reset to first page when filters change
    }, []);

    return {
        data,
        loading,
        error,
        refetch,
        retry,
        setFilters: updateFilters,
        setPage: setCurrentPage,
    };
}

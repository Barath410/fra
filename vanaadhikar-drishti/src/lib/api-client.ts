/**
 * API Client for FRA Backend
 * Handles all communication with backend services
 */

import { clearAuthToken, getAuthToken } from '@/lib/auth';

const DEFAULT_BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
const API_URL = process.env.NEXT_PUBLIC_API_URL || `${DEFAULT_BACKEND}/api`;

function appendParam(params: URLSearchParams, key: string, value: unknown) {
    if (Array.isArray(value)) {
        value.forEach((entry) => appendParam(params, key, entry));
        return;
    }

    if (value === undefined || value === null || value === '') {
        return;
    }

    params.append(key, String(value));
}

function buildQueryParams(page: number, limit: number, filters?: Record<string, any>) {
    const params = new URLSearchParams();
    params.append('page', page.toString());
    params.append('limit', limit.toString());

    if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
            appendParam(params, key, value);
        });
    }

    return params.toString();
}

export interface ApiResponse<T> {
    data?: T;
    error?: string;
    status: number;
}

class ApiClient {
    private baseUrl: string;

    constructor() {
        this.baseUrl = API_URL;
    }

    private getHeaders(): HeadersInit {
        const headers: HeadersInit = {
            'Content-Type': 'application/json',
        };

        // Add auth token if available
        const token = getAuthToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        return headers;
    }

    async request<T>(endpoint: string, options?: RequestInit): Promise<ApiResponse<T>> {
        try {
            const url = `${this.baseUrl}${endpoint}`;
            const response = await fetch(url, {
                ...options,
                headers: {
                    ...this.getHeaders(),
                    ...options?.headers,
                },
            });

            if (!response.ok) {
                const error = await response.text();
                return {
                    error: error || `HTTP ${response.status}`,
                    status: response.status,
                };
            }

            const responseBody = await response.json();
            let normalizedData: any = responseBody;
            if (normalizedData && typeof normalizedData === 'object') {
                normalizedData = { ...normalizedData };
                if (Array.isArray(normalizedData.data) && !Array.isArray(normalizedData.items)) {
                    normalizedData.items = normalizedData.data;
                }
            }

            return {
                data: normalizedData,
                status: response.status,
            };
        } catch (error) {
            const message = error instanceof Error ? error.message : 'Network request failed';
            return {
                error: message,
                status: 0,
            };
        }
    }

    // Dashboard APIs
    async getDashboardSummary() {
        return this.request('/dashboard/summary');
    }

    async getStateDashboard(state: string) {
        return this.request(`/dashboard/state/${state}`);
    }

    async getDistrictDashboard(state: string, district: string) {
        return this.request(`/dashboard/district/${state}/${district}`);
    }

    async getCacheStats() {
        return this.request('/dashboard/cache/stats');
    }

    // Claims APIs
    async getClaims(page = 1, limit = 10, filters?: Record<string, any>) {
        const queryString = buildQueryParams(page, limit, filters);
        return this.request(`/claims?${queryString}`);
    }

    async getClaimById(id: string) {
        return this.request(`/claims/${id}`);
    }

    async createClaim(data: any) {
        return this.request('/claims', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async updateClaim(id: string, data: any) {
        return this.request(`/claims/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    // Villages APIs
    async getVillages(page = 1, limit = 10, filters?: Record<string, any>) {
        const queryString = buildQueryParams(page, limit, filters);
        return this.request(`/villages?${queryString}`);
    }

    async getVillageByCode(code: string) {
        return this.request(`/villages/${code}`);
    }

    // Officers APIs
    async getOfficers(page = 1, limit = 10, filters?: Record<string, any>) {
        const queryString = buildQueryParams(page, limit, filters);
        return this.request(`/officers?${queryString}`);
    }

    async getOfficerById(id: string) {
        return this.request(`/officers/${id}`);
    }

    // Grievances APIs
    async getGrievances(page = 1, limit = 10, filters?: Record<string, any>) {
        const queryString = buildQueryParams(page, limit, filters);
        return this.request(`/grievances?${queryString}`);
    }

    async getGrievanceById(id: string) {
        return this.request(`/grievances/${id}`);
    }

    async createGrievance(data: any) {
        return this.request('/grievances', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async updateGrievance(id: string, data: any) {
        return this.request(`/grievances/${id}`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    }

    // Auth APIs
    async getAuthMe() {
        return this.request('/auth/me');
    }

    async logout() {
        clearAuthToken();
        return this.request('/auth/logout', { method: 'POST' });
    }
}

export const apiClient = new ApiClient();

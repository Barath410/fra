import { DashboardSummary, FRAClaim, GrievanceTicket } from "@/types";

const DEFAULT_BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
const API_BASE = process.env.NEXT_PUBLIC_API_URL || `${DEFAULT_BACKEND}/api`;

export interface PaginatedResponse<T> {
    data: T[];
    total: number;
    page: number;
    limit: number;
    pages: number;
    filters: Record<string, unknown>;
}

function appendQueryParam(params: URLSearchParams, key: string, value?: string | string[]) {
    if (value === undefined || value === null || value === "") return;
    if (Array.isArray(value)) {
        value.forEach((item) => appendQueryParam(params, key, item));
        return;
    }
    params.append(key, value);
}

async function fetchJSON<T>(path: string, init?: RequestInit): Promise<T> {
    const res = await fetch(`${API_BASE}${path}`, {
        ...init,
        headers: {
            "Content-Type": "application/json",
            ...(init?.headers || {}),
        },
        cache: "no-store",
    });

    if (!res.ok) {
        const text = await res.text();
        throw new Error(`API ${res.status}: ${text}`);
    }
    return res.json();
}

export async function getDashboardSummary(): Promise<DashboardSummary> {
    return fetchJSON<DashboardSummary>(`/dashboard/summary`);
}

export async function getClaims(params?: { state?: string; status?: string | string[] }): Promise<PaginatedResponse<FRAClaim>> {
    const query = new URLSearchParams();
    appendQueryParam(query, "state", params?.state);
    appendQueryParam(query, "status", params?.status);
    const suffix = query.toString() ? `?${query.toString()}` : "";
    return fetchJSON<PaginatedResponse<FRAClaim>>(`/claims${suffix}`);
}

export async function createGrievance(payload: GrievanceTicket): Promise<GrievanceTicket> {
    const body = {
        grievance_id: payload.id,
        claimant_name: payload.claimantName,
        claim_id: payload.claimId,
        village_name: payload.villageName,
        block: payload.block,
        district: payload.district,
        state: payload.state,
        category: payload.category,
        status: payload.status,
        priority: payload.priority,
        description: payload.description,
        channel: payload.channel,
        mobile: payload.mobile,
        source: payload.source,
        assigned_officer_id: payload.assignedOfficerId,
        filed_date: payload.filedDate,
    };
    return fetchJSON<GrievanceTicket>(`/grievances`, {
        method: "POST",
        body: JSON.stringify(body),
    });
}
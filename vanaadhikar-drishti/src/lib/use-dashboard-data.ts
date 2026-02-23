"use client";

import { useEffect, useState } from "react";
import { getDashboardSummary } from "./api";
import type { DashboardSummary } from "@/types";

export function useDashboardData() {
    const [data, setData] = useState<DashboardSummary | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        getDashboardSummary()
            .then((res) => setData(res))
            .catch((err) => setError(err.message))
            .finally(() => setLoading(false));
    }, []);

    return { data, loading, error };
}
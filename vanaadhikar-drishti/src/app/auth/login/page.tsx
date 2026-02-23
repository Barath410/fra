"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export default function AuthLoginPage() {
    const [authUrl, setAuthUrl] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const params = useSearchParams();
    const queryNext = params.get("next") ?? "/";
    const safeNext = queryNext.startsWith("/") ? queryNext : "/";

    useEffect(() => {
        const fetchLoginUrl = async () => {
            try {
                const nextPath = `/auth/callback?next=${encodeURIComponent(safeNext)}`;
                const response = await fetch(`${API_BASE}/auth/google/login?next=${encodeURIComponent(nextPath)}`, {
                    cache: "no-store",
                });
                if (!response.ok) {
                    const text = await response.text();
                    throw new Error(text || "Unable to reach auth service");
                }
                const data = await response.json();
                setAuthUrl(data.auth_url);
            } catch (err) {
                setError(err instanceof Error ? err.message : "Unable to start login");
            } finally {
                setLoading(false);
            }
        };

        fetchLoginUrl();
    }, [safeNext]);

    const handleLogin = () => {
        if (!authUrl) return;
        window.location.href = authUrl;
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-slate-950 to-slate-900 text-white px-4">
            <div className="max-w-md w-full space-y-6 bg-white/5 border border-white/10 rounded-2xl p-8 shadow-lg backdrop-blur">
                <h1 className="text-2xl font-bold">Sign in with Google</h1>
                <p className="text-sm text-slate-300">
                    Authenticate using Forest Rights Act credentials so protected dashboards can read your data.
                </p>
                <button
                    onClick={handleLogin}
                    disabled={loading || !authUrl}
                    className="w-full flex items-center justify-center gap-2 rounded-lg px-4 py-3 bg-emerald-500 text-white font-semibold text-sm shadow-lg shadow-emerald-500/50 hover:bg-emerald-600 disabled:opacity-50"
                >
                    {loading ? "Preparing Google login…" : "Continue with Google"}
                </button>
                {error && <p className="text-xs text-red-400">{error}</p>}
            </div>
        </div>
    );
}

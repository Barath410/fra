"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { setAuthToken } from "@/lib/auth";

export default function AuthCallbackPage() {
    const params = useSearchParams();
    const router = useRouter();
    const [status, setStatus] = useState("Completing sign-in…");

    useEffect(() => {
        const token = params.get("token");
        const nextParam = params.get("next") ?? "/";
        const nextPath = nextParam.startsWith("/") ? nextParam : "/";

        if (!token) {
            setStatus("Authentication failed: missing token.");
            return;
        }

        setAuthToken(token);
        setStatus("Signed in! Redirecting you now…");

        const timeout = setTimeout(() => {
            router.replace(nextPath);
        }, 600);

        return () => clearTimeout(timeout);
    }, [params, router]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-950 text-white px-4">
            <div className="max-w-lg w-full space-y-4 text-center">
                <p className="text-lg font-semibold">{status}</p>
                <p className="text-sm text-slate-400">
                    You can close this tab if you are not redirected automatically.
                </p>
            </div>
        </div>
    );
}

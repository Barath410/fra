"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { LogOut } from "lucide-react";

export default function LogoutPage() {
    const router = useRouter();

    useEffect(() => {
        // Simulate logout process
        const timer = setTimeout(() => {
            // In a real app, this would clear session/tokens
            // For now, just redirect to home
            router.push("/");
        }, 2000);

        return () => clearTimeout(timer);
    }, [router]);

    return (
        <div className="min-h-screen bg-gradient-to-br from-primary-700 via-primary-800 to-primary-900 flex items-center justify-center">
            <div className="text-center text-white">
                <div className="w-20 h-20 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center mx-auto mb-6 animate-pulse">
                    <LogOut size={40} />
                </div>
                <h1 className="text-3xl font-bold mb-2">Logging Out...</h1>
                <p className="text-primary-100">Please wait while we securely log you out</p>
                <div className="mt-8 flex items-center justify-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-white animate-bounce" style={{ animationDelay: "0ms" }}></div>
                    <div className="w-2 h-2 rounded-full bg-white animate-bounce" style={{ animationDelay: "150ms" }}></div>
                    <div className="w-2 h-2 rounded-full bg-white animate-bounce" style={{ animationDelay: "300ms" }}></div>
                </div>
            </div>
        </div>
    );
}

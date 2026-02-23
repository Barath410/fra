"use client";
import * as React from "react";
import { cn } from "@/lib/utils";
import { CheckCircle, XCircle, AlertCircle, Info, X } from "lucide-react";

type ToastType = "success" | "error" | "warning" | "info";

export interface ToastData {
    id: string;
    type: ToastType;
    title: string;
    message?: string;
    duration?: number;
    action?: { label: string; onClick: () => void };
}

const ICONS: Record<ToastType, React.ReactNode> = {
    success: <CheckCircle size={16} className="text-green-500" />,
    error: <XCircle size={16} className="text-red-500" />,
    warning: <AlertCircle size={16} className="text-amber-500" />,
    info: <Info size={16} className="text-blue-500" />,
};

const BG: Record<ToastType, string> = {
    success: "border-green-200 bg-green-50",
    error: "border-red-200 bg-red-50",
    warning: "border-amber-200 bg-amber-50",
    info: "border-blue-200 bg-blue-50",
};

function Toast({ toast, onDismiss }: { toast: ToastData; onDismiss: (id: string) => void }) {
    React.useEffect(() => {
        const duration = toast.duration ?? 4000;
        if (duration > 0) {
            const t = setTimeout(() => onDismiss(toast.id), duration);
            return () => clearTimeout(t);
        }
    }, [toast.id, toast.duration, onDismiss]);

    return (
        <div
            role="alert"
            className={cn(
                "flex items-start gap-3 rounded-xl border p-3.5 shadow-card-lg animate-slide-in-right min-w-[280px] max-w-[380px]",
                BG[toast.type]
            )}
        >
            <span className="shrink-0 mt-0.5">{ICONS[toast.type]}</span>
            <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-gray-800">{toast.title}</p>
                {toast.message && <p className="text-xs text-gray-500 mt-0.5">{toast.message}</p>}
                {toast.action && (
                    <button
                        onClick={toast.action.onClick}
                        className="mt-1.5 text-xs font-bold text-forest-600 hover:text-forest-800 underline-offset-2 hover:underline"
                    >
                        {toast.action.label}
                    </button>
                )}
            </div>
            <button
                onClick={() => onDismiss(toast.id)}
                className="shrink-0 text-gray-400 hover:text-gray-600 transition-colors"
                aria-label="Dismiss notification"
            >
                <X size={14} />
            </button>
        </div>
    );
}

// ── Toast Container ───────────────────────────────────────────────────────────
interface ToastContainerProps { toasts: ToastData[]; onDismiss: (id: string) => void }

export function ToastContainer({ toasts, onDismiss }: ToastContainerProps) {
    return (
        <div className="fixed bottom-4 right-4 z-[100] flex flex-col gap-2 items-end">
            {toasts.map((t) => <Toast key={t.id} toast={t} onDismiss={onDismiss} />)}
        </div>
    );
}

// ── Toast Hook ────────────────────────────────────────────────────────────────
export function useToast() {
    const [toasts, setToasts] = React.useState<ToastData[]>([]);

    const toast = React.useCallback((data: Omit<ToastData, "id">) => {
        const id = Math.random().toString(36).slice(2);
        setToasts((prev) => [...prev, { ...data, id }]);
        return id;
    }, []);

    const dismiss = React.useCallback((id: string) => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
    }, []);

    const success = (title: string, message?: string) => toast({ type: "success", title, message });
    const error = (title: string, message?: string) => toast({ type: "error", title, message });
    const warning = (title: string, message?: string) => toast({ type: "warning", title, message });
    const info = (title: string, message?: string) => toast({ type: "info", title, message });

    return { toasts, toast, dismiss, success, error, warning, info };
}

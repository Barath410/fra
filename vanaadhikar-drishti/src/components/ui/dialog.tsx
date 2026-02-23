"use client";
import * as React from "react";
import { cn } from "@/lib/utils";
import { X } from "lucide-react";
import { Button } from "./button";

interface DialogProps {
    open: boolean;
    onClose: () => void;
    title?: string;
    description?: string;
    children: React.ReactNode;
    size?: "sm" | "md" | "lg" | "xl" | "full";
    hideCloseButton?: boolean;
    footer?: React.ReactNode;
}

const SIZE_CLASSES = {
    sm: "max-w-sm",
    md: "max-w-md",
    lg: "max-w-2xl",
    xl: "max-w-4xl",
    full: "max-w-[95vw] h-[90vh]",
};

export function Dialog({ open, onClose, title, description, children, size = "md", hideCloseButton, footer }: DialogProps) {
    // Close on ESC
    React.useEffect(() => {
        const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
        if (open) document.addEventListener("keydown", handler);
        return () => document.removeEventListener("keydown", handler);
    }, [open, onClose]);

    // Lock body scroll
    React.useEffect(() => {
        if (open) document.body.style.overflow = "hidden";
        else document.body.style.overflow = "";
        return () => { document.body.style.overflow = ""; };
    }, [open]);

    if (!open) return null;

    return (
        <div
            role="dialog"
            aria-modal="true"
            aria-label={title}
            className="fixed inset-0 z-50 flex items-center justify-center p-4"
        >
            {/* Backdrop */}
            <div
                className="absolute inset-0 bg-black/50 backdrop-blur-sm animate-fade-up"
                onClick={onClose}
                aria-hidden
            />

            {/* Panel */}
            <div
                className={cn(
                    "relative w-full bg-white rounded-2xl shadow-2xl overflow-hidden animate-fade-up flex flex-col",
                    SIZE_CLASSES[size],
                    size === "full" && "overflow-y-auto"
                )}
            >
                {/* Header */}
                {(title || !hideCloseButton) && (
                    <div className="flex items-start justify-between p-5 border-b border-gray-100 shrink-0">
                        <div>
                            {title && <h2 className="text-base font-bold text-forest-900">{title}</h2>}
                            {description && <p className="text-sm text-gray-500 mt-0.5">{description}</p>}
                        </div>
                        {!hideCloseButton && (
                            <button
                                onClick={onClose}
                                className="ml-4 shrink-0 text-gray-400 hover:text-gray-700 hover:bg-gray-100 rounded-lg p-1.5 transition-colors"
                                aria-label="Close dialog"
                            >
                                <X size={16} />
                            </button>
                        )}
                    </div>
                )}

                {/* Content */}
                <div className="p-5 flex-1 overflow-y-auto">
                    {children}
                </div>

                {/* Footer */}
                {footer && (
                    <div className="flex items-center justify-end gap-2 px-5 py-4 border-t border-gray-100 bg-gray-50 shrink-0">
                        {footer}
                    </div>
                )}
            </div>
        </div>
    );
}

// ── Confirm Dialog ─────────────────────────────────────────────────────────────
interface ConfirmDialogProps {
    open: boolean;
    onClose: () => void;
    onConfirm: () => void;
    title?: string;
    message: string;
    confirmLabel?: string;
    cancelLabel?: string;
    variant?: "danger" | "primary";
    loading?: boolean;
}

export function ConfirmDialog({
    open,
    onClose,
    onConfirm,
    title = "Confirm Action",
    message,
    confirmLabel = "Confirm",
    cancelLabel = "Cancel",
    variant = "primary",
    loading,
}: ConfirmDialogProps) {
    return (
        <Dialog
            open={open}
            onClose={onClose}
            title={title}
            size="sm"
            footer={
                <>
                    <Button variant="outline" onClick={onClose} disabled={loading}>
                        {cancelLabel}
                    </Button>
                    <Button
                        variant={variant === "danger" ? "danger" : "primary"}
                        onClick={onConfirm}
                        loading={loading}
                    >
                        {confirmLabel}
                    </Button>
                </>
            }
        >
            <p className="text-sm text-gray-600">{message}</p>
        </Dialog>
    );
}

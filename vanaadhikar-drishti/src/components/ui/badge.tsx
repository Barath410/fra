"use client";
import * as React from "react";
import { cn } from "@/lib/utils";

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
    variant?:
    | "default"
    | "secondary"
    | "outline"
    | "destructive"
    | "granted"
    | "pending"
    | "rejected"
    | "received"
    | "verified"
    | "critical"
    | "high"
    | "medium"
    | "low"
    | "pvtg"
    | "ifr"
    | "cfr"
    | "cr"
    | "info"
    | "warning"
    | "danger"
    | "success"
    | "neutral";
    size?: "sm" | "md" | "lg";
}

const variantStyles: Record<string, string> = {
    default: "bg-forest-800 text-white border-forest-800",
    secondary: "bg-parchment text-forest-800 border-parchment-dark",
    outline: "bg-transparent text-forest-700 border-forest-300",
    destructive: "bg-red-100 text-red-800 border-red-200",
    granted: "bg-emerald-50 text-emerald-800 border-emerald-200",
    pending: "bg-amber-50 text-amber-800 border-amber-200",
    rejected: "bg-red-50 text-red-800 border-red-200",
    received: "bg-blue-50 text-blue-800 border-blue-200",
    verified: "bg-indigo-50 text-indigo-800 border-indigo-200",
    critical: "bg-red-50 text-red-700 border-red-300 font-semibold",
    high: "bg-orange-50 text-orange-700 border-orange-200",
    medium: "bg-yellow-50 text-yellow-700 border-yellow-200",
    low: "bg-green-50 text-green-700 border-green-200",
    pvtg: "bg-purple-50 text-purple-800 border-purple-200",
    ifr: "bg-indigo-50 text-indigo-800 border-indigo-200",
    cfr: "bg-emerald-50 text-emerald-800 border-emerald-200",
    cr: "bg-amber-50 text-amber-800 border-amber-200",
    info: "bg-blue-50 text-blue-800 border-blue-200",
    warning: "bg-amber-50 text-amber-800 border-amber-200",
    danger: "bg-red-50 text-red-800 border-red-200",
    success: "bg-emerald-50 text-emerald-800 border-emerald-200",
    neutral: "bg-gray-50 text-gray-800 border-gray-200",
};

const sizeStyles: Record<string, string> = {
    sm: "text-[10px] px-1.5 py-0.5 rounded",
    md: "text-xs px-2 py-0.5 rounded-md",
    lg: "text-sm px-2.5 py-1 rounded-md",
};

export function Badge({
    variant = "default",
    size = "md",
    className,
    children,
    ...props
}: BadgeProps) {
    return (
        <span
            className={cn(
                "inline-flex items-center border font-medium whitespace-nowrap",
                variantStyles[variant],
                sizeStyles[size],
                className
            )}
            {...props}
        >
            {children}
        </span>
    );
}

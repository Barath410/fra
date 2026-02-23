"use client";
import * as React from "react";
import { cn } from "@/lib/utils";

interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
    value: number; // 0–100
    max?: number;
    variant?: "forest" | "saffron" | "danger" | "amber" | "blue" | "purple";
    size?: "xs" | "sm" | "md" | "lg";
    showLabel?: boolean;
    label?: string;
    animated?: boolean;
}

const variantGradients: Record<string, string> = {
    forest: "linear-gradient(90deg, #1a5542, #2d8566, #49a082)",
    saffron: "linear-gradient(90deg, #b5541a, #e87722, #ff9032)",
    danger: "linear-gradient(90deg, #dc2626, #ef4444, #f87171)",
    amber: "linear-gradient(90deg, #d97706, #f59e0b, #fbbf24)",
    blue: "linear-gradient(90deg, #1d4ed8, #3b82f6, #60a5fa)",
    purple: "linear-gradient(90deg, #6d28d9, #8b5cf6, #a78bfa)",
};

const sizeStyles: Record<string, string> = {
    xs: "h-1",
    sm: "h-1.5",
    md: "h-2",
    lg: "h-3",
};

export function Progress({
    value,
    max = 100,
    variant = "forest",
    size = "md",
    showLabel = false,
    label,
    animated = true,
    className,
    ...props
}: ProgressProps) {
    const pct = Math.min(Math.max((value / max) * 100, 0), 100);

    return (
        <div className={cn("w-full", className)} {...props}>
            {(showLabel || label) && (
                <div className="flex items-center justify-between mb-1.5">
                    {label && <span className="text-xs font-medium text-gray-600">{label}</span>}
                    {showLabel && (
                        <span className="text-xs font-bold tabular-nums" style={{ color: "#1a5542" }}>
                            {Math.round(pct)}%
                        </span>
                    )}
                </div>
            )}
            <div
                className={cn("w-full rounded-full overflow-hidden bg-gray-100", sizeStyles[size])}
                role="progressbar"
                aria-valuenow={value}
                aria-valuemin={0}
                aria-valuemax={max}
            >
                <div
                    className={cn("h-full rounded-full", animated && "transition-all duration-700 ease-out")}
                    style={{ width: `${pct}%`, background: variantGradients[variant] }}
                />
            </div>
        </div>
    );
}

/* ── Saturation Ring ─────────────────────────────────────────────────────── */
interface SaturationRingProps {
    value: number; // 0–100
    size?: number;
    strokeWidth?: number;
    label?: string;
    sublabel?: string;
    className?: string;
}

export function SaturationRing({
    value,
    size = 80,
    strokeWidth = 8,
    label,
    sublabel,
    className,
}: SaturationRingProps) {
    const r = (size - strokeWidth) / 2;
    const circ = 2 * Math.PI * r;
    const offset = circ - (value / 100) * circ;
    const color =
        value >= 75 ? "#22c55e" : value >= 50 ? "#f59e0b" : "#ef4444";

    return (
        <div className={cn("relative inline-flex items-center justify-center", className)}>
            <svg width={size} height={size} className="-rotate-90">
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={r}
                    fill="none"
                    stroke="#f3f4f6"
                    strokeWidth={strokeWidth}
                />
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={r}
                    fill="none"
                    stroke={color}
                    strokeWidth={strokeWidth}
                    strokeDasharray={circ}
                    strokeDashoffset={offset}
                    strokeLinecap="round"
                    className="transition-all duration-700 ease-out"
                />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-sm font-bold leading-none tabular-nums" style={{ color }}>
                    {Math.round(value)}%
                </span>
                {sublabel && (
                    <span className="text-[8px] font-medium text-gray-500 mt-0.5 leading-none">
                        {sublabel}
                    </span>
                )}
            </div>
        </div>
    );
}

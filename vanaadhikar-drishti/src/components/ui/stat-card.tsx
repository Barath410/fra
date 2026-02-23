"use client";
import React from "react";
import { cn } from "@/lib/utils";
import { formatNumber } from "@/lib/utils";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";

interface StatCardProps {
    title: string;
    titleHi?: string;
    value: string | number;
    subtitle?: string;
    change?: number;
    changeLabel?: string;
    icon?: React.ReactNode;
    accentColor?: string;
    trend?: "up" | "down" | "flat";
    onClick?: () => void;
    className?: string;
    loading?: boolean;
}

export function StatCard({
    title,
    titleHi,
    value,
    subtitle,
    change,
    changeLabel,
    icon,
    accentColor = "#1a5542",
    trend,
    onClick,
    className,
    loading,
}: StatCardProps) {
    const displayValue =
        typeof value === "number" ? formatNumber(value) : value;

    if (loading) {
        return (
            <div className={cn("tribal-card kpi-card", className)}>
                <div className="skeleton h-4 w-24 mb-2" />
                <div className="skeleton h-8 w-32 mb-1" />
                <div className="skeleton h-3 w-20" />
            </div>
        );
    }

    const trendIcon =
        trend === "up" ? (
            <TrendingUp className="w-3.5 h-3.5" />
        ) : trend === "down" ? (
            <TrendingDown className="w-3.5 h-3.5" />
        ) : (
            <Minus className="w-3.5 h-3.5" />
        );

    const trendColor =
        trend === "up"
            ? "text-emerald-600"
            : trend === "down"
                ? "text-red-500"
                : "text-gray-400";

    return (
        <div
            className={cn("tribal-card kpi-card", onClick && "cursor-pointer", className)}
            onClick={onClick}
            role={onClick ? "button" : undefined}
            tabIndex={onClick ? 0 : undefined}
        >
            {/* Top row: icon + title */}
            <div className="flex items-start justify-between mb-3">
                <div>
                    <p className="text-xs font-semibold text-text-muted uppercase tracking-wide leading-none">
                        {title}
                    </p>
                    {titleHi && (
                        <p className="text-[10px] text-text-light mt-0.5 font-medium">{titleHi}</p>
                    )}
                </div>
                {icon && (
                    <div
                        className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0 shadow-sm"
                        style={{ background: `${accentColor}15`, color: accentColor }}
                    >
                        {icon}
                    </div>
                )}
            </div>

            {/* Value */}
            <div className="kpi-value tabular-nums" style={{ color: accentColor }}>
                {displayValue}
            </div>

            {/* Subtitle + change */}
            <div className="flex items-center gap-2 mt-1.5">
                {subtitle && (
                    <span className="text-xs text-text-muted flex-1 leading-tight">
                        {subtitle}
                    </span>
                )}
                {(change !== undefined || trend) && (
                    <span
                        className={cn(
                            "inline-flex items-center gap-0.5 text-xs font-semibold",
                            trendColor
                        )}
                    >
                        {trendIcon}
                        {change !== undefined && (
                            <>
                                {change > 0 ? "+" : ""}
                                {change}%
                            </>
                        )}
                        {changeLabel && (
                            <span className="text-text-light font-normal ml-0.5">{changeLabel}</span>
                        )}
                    </span>
                )}
            </div>
        </div>
    );
}

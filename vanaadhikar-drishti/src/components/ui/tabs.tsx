"use client";
import * as React from "react";
import { cn } from "@/lib/utils";

interface Tab { id: string; label: string; icon?: React.ReactNode; badge?: string | number; disabled?: boolean }

interface TabsProps {
    tabs: Tab[];
    activeTab: string;
    onChange: (id: string) => void;
    variant?: "underline" | "pills" | "boxed";
    size?: "sm" | "md" | "lg";
    className?: string;
}

const SIZES = { sm: "text-xs px-3 py-1.5", md: "text-sm px-4 py-2", lg: "text-sm px-5 py-2.5" };

export function Tabs({ tabs, activeTab, onChange, variant = "underline", size = "md", className }: TabsProps) {
    return (
        <div
            role="tablist"
            className={cn(
                "flex gap-0.5",
                variant === "underline" && "border-b border-gray-200",
                variant === "pills" && "bg-gray-100 rounded-xl p-1",
                variant === "boxed" && "border border-gray-200 rounded-xl p-1 bg-white",
                className
            )}
        >
            {tabs.map((tab) => {
                const isActive = tab.id === activeTab;
                return (
                    <button
                        key={tab.id}
                        role="tab"
                        aria-selected={isActive}
                        disabled={tab.disabled}
                        onClick={() => !tab.disabled && onChange(tab.id)}
                        className={cn(
                            "flex items-center gap-1.5 font-medium rounded-lg transition-all whitespace-nowrap disabled:opacity-40 disabled:cursor-not-allowed",
                            SIZES[size],
                            variant === "underline" && [
                                "rounded-none border-b-2 -mb-px",
                                isActive ? "border-forest-600 text-forest-700" : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300",
                            ],
                            variant === "pills" && [
                                "rounded-lg",
                                isActive ? "bg-white shadow-sm text-forest-700 font-semibold" : "text-gray-500 hover:text-gray-700",
                            ],
                            variant === "boxed" && [
                                "rounded-lg",
                                isActive ? "bg-forest-900 text-white" : "text-gray-500 hover:text-gray-700 hover:bg-gray-50",
                            ]
                        )}
                    >
                        {tab.icon && <span className="opacity-80">{tab.icon}</span>}
                        {tab.label}
                        {tab.badge !== undefined && tab.badge !== "" && (
                            <span className={cn(
                                "ml-1 rounded-full px-1.5 py-0.5 text-[10px] font-bold leading-none",
                                isActive ? "bg-forest-100 text-forest-700" : "bg-gray-200 text-gray-500"
                            )}>
                                {tab.badge}
                            </span>
                        )}
                    </button>
                );
            })}
        </div>
    );
}

// ── Tab Panel ─────────────────────────────────────────────────────────────────
export function TabPanel({ id, activeTab, children, className }: { id: string; activeTab: string; children: React.ReactNode; className?: string }) {
    if (id !== activeTab) return null;
    return (
        <div role="tabpanel" className={cn("animate-fade-up", className)}>
            {children}
        </div>
    );
}

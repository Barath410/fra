"use client";
import React, { useState } from "react";
import Link from "next/link";
import {
    Bell,
    Search,
    ChevronDown,
    Menu,
    X,
    User,
    Settings,
    LogOut,
    RefreshCw,
    Download,
    AlertTriangle,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import type { UserRole } from "./sidebar";

const ROLE_LABELS: Record<UserRole, string> = {
    "mota-nodal": "MoTA National Nodal Officer",
    "state-commissioner": "State Tribal Welfare Commissioner",
    "district-collector": "District Collector / DRDA",
    "sdlc-officer": "Sub-Divisional Level Committee Officer",
    "range-officer": "Range Forest Officer",
    "gram-sabha": "Gram Sabha / FRC Member",
    "ngo-researcher": "NGO / Researcher",
    citizen: "Patta Holder",
};

const ROLE_COLORS: Record<UserRole, string> = {
    "mota-nodal": "bg-primary",
    "state-commissioner": "bg-warning",
    "district-collector": "bg-primary-600",
    "sdlc-officer": "bg-primary-700",
    "range-officer": "bg-success",
    "gram-sabha": "bg-success-600",
    "ngo-researcher": "bg-gray-600",
    citizen: "bg-primary-800",
};

interface TopNavbarProps {
    role: UserRole;
    pageName: string;
    pageNameHi?: string;
    stateName?: string;
    districtName?: string;
    alertCount?: number;
    onMenuToggle?: () => void;
    showSidebarToggle?: boolean;
    lastUpdated?: string;
}

export function TopNavbar({
    role,
    pageName,
    pageNameHi,
    stateName,
    districtName,
    alertCount = 0,
    onMenuToggle,
    showSidebarToggle = true,
    lastUpdated,
}: TopNavbarProps) {
    const [searchOpen, setSearchOpen] = useState(false);
    const [notiOpen, setNotiOpen] = useState(false);
    const [profileOpen, setProfileOpen] = useState(false);

    const SAMPLE_NOTIFICATIONS = [
        { id: 1, type: "danger", text: "Forest fire detected — Pachmarhi CFR Zone", time: "10 min ago" },
        { id: 2, type: "warn", text: "47 claims pending DLC approval > 60 days", time: "2 hours ago" },
        { id: 3, type: "info", text: "DA-JGUA MIS synced successfully", time: "5 hours ago" },
        { id: 4, type: "success", text: "OCR batch processing complete: 234 documents", time: "1 day ago" },
    ];

    return (
        <header className="gov-nav sticky top-0 z-30 shrink-0" aria-label="Top Navigation">
            <div className="h-14 px-4 flex items-center gap-3">
                {/* Sidebar toggle (mobile) */}
                {showSidebarToggle && (
                    <button
                        onClick={onMenuToggle}
                        className="text-white/80 hover:text-white p-1.5 rounded-md hover:bg-white/10 transition-colors lg:hidden"
                        aria-label="Toggle sidebar"
                    >
                        <Menu size={20} />
                    </button>
                )}

                {/* GOI Logo + Title */}
                <div className="flex items-center gap-3 flex-1 min-w-0">
                    {/* Emblem placeholder */}
                    <div className="shrink-0 hidden sm:flex items-center gap-2">
                        <div className="w-7 h-7 rounded-full bg-amber-400 flex items-center justify-center">
                            <span className="text-forest-900 font-black text-xs">🪷</span>
                        </div>
                    </div>

                    <div className="min-w-0">
                        <h1 className="text-white font-bold text-sm leading-tight truncate">
                            {pageName}
                            {pageNameHi && (
                                <span className="ml-2 text-white/50 font-normal text-xs hidden md:inline">
                                    {pageNameHi}
                                </span>
                            )}
                        </h1>
                        <div className="flex items-center gap-2 mt-0.5">
                            {stateName && (
                                <Badge variant="outline" size="sm" className="border-white/30 text-white text-[9px]">
                                    {stateName}
                                </Badge>
                            )}
                            {districtName && (
                                <span className="text-white/50 text-[10px]">/{districtName}</span>
                            )}
                            {lastUpdated && (
                                <span className="text-white/40 text-[10px] hidden md:inline">
                                    Updated: {lastUpdated}
                                </span>
                            )}
                        </div>
                    </div>
                </div>

                {/* Search */}
                <div className="relative hidden md:flex">
                    {searchOpen ? (
                        <div className="flex items-center gap-2">
                            <input
                                autoFocus
                                type="text"
                                placeholder="Search village, claim ID, patta..."
                                className="w-64 px-3 py-1.5 text-sm bg-white/15 text-white placeholder-white/50 border border-white/20 rounded-lg focus:outline-none focus:bg-white/20 focus:border-white/40"
                                onBlur={() => setSearchOpen(false)}
                            />
                            <button
                                onClick={() => setSearchOpen(false)}
                                className="text-white/70 hover:text-white"
                            >
                                <X size={16} />
                            </button>
                        </div>
                    ) : (
                        <button
                            onClick={() => setSearchOpen(true)}
                            className="flex items-center gap-2 px-3 py-1.5 text-sm text-white/60 bg-white/10 border border-white/15 rounded-lg hover:bg-white/15 transition-colors"
                        >
                            <Search size={14} />
                            <span className="hidden lg:inline">Search...</span>
                        </button>
                    )}
                </div>

                {/* Refresh */}
                <button
                    className="text-white/70 hover:text-white p-1.5 rounded-md hover:bg-white/10 transition-colors hidden sm:flex"
                    title="Refresh data"
                >
                    <RefreshCw size={16} />
                </button>

                {/* Download */}
                <button
                    className="text-white/70 hover:text-white p-1.5 rounded-md hover:bg-white/10 transition-colors hidden sm:flex"
                    title="Export current view"
                >
                    <Download size={16} />
                </button>

                {/* Alerts */}
                <div className="relative">
                    <button
                        onClick={() => setNotiOpen(!notiOpen)}
                        className="relative text-white/70 hover:text-white p-1.5 rounded-md hover:bg-white/10 transition-colors"
                        aria-label={`Notifications — ${alertCount} unread`}
                    >
                        <Bell size={18} />
                        {alertCount > 0 && (
                            <span className="absolute -top-0.5 -right-0.5 w-4 h-4 text-[9px] font-bold bg-red-500 text-white rounded-full flex items-center justify-center">
                                {alertCount > 9 ? "9+" : alertCount}
                            </span>
                        )}
                    </button>

                    {notiOpen && (
                        <div className="absolute right-0 top-full mt-2 w-80 bg-white rounded-xl shadow-card-lg border border-border z-50 overflow-hidden animate-fade-up">
                            <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-primary">
                                <span className="text-white font-semibold text-sm">Notifications</span>
                                <button
                                    onClick={() => setNotiOpen(false)}
                                    className="text-white/60 hover:text-white"
                                >
                                    <X size={14} />
                                </button>
                            </div>
                            <div className="divide-y divide-gray-50 max-h-64 overflow-y-auto">
                                {SAMPLE_NOTIFICATIONS.map((n) => (
                                    <div
                                        key={n.id}
                                        className="flex items-start gap-3 px-4 py-3 hover:bg-gray-50 cursor-pointer"
                                    >
                                        <span
                                            className={cn(
                                                "w-2 h-2 rounded-full mt-1.5 shrink-0",
                                                n.type === "danger" && "bg-red-500",
                                                n.type === "warn" && "bg-amber-500",
                                                n.type === "info" && "bg-blue-500",
                                                n.type === "success" && "bg-emerald-500"
                                            )}
                                        />
                                        <div className="flex-1 min-w-0">
                                            <p className="text-xs text-gray-700 leading-snug">{n.text}</p>
                                            <p className="text-[10px] text-gray-400 mt-0.5">{n.time}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <div className="px-4 py-2 border-t border-gray-100">
                                <Link
                                    href="/notifications"
                                    className="text-xs font-semibold text-primary hover:text-primary-700"
                                    onClick={() => setNotiOpen(false)}
                                >
                                    View all notifications →
                                </Link>
                            </div>
                        </div>
                    )}
                </div>

                {/* Profile */}
                <div className="relative">
                    <button
                        onClick={() => setProfileOpen(!profileOpen)}
                        className="flex items-center gap-2 pl-2 pr-1 py-1 rounded-lg hover:bg-white/10 transition-colors"
                    >
                        <div
                            className={cn(
                                "w-7 h-7 rounded-full flex items-center justify-center text-white text-xs font-bold shrink-0",
                                ROLE_COLORS[role]
                            )}
                        >
                            <User size={14} />
                        </div>
                        <div className="hidden md:block text-left min-w-0">
                            <p className="text-white text-xs font-medium leading-none truncate max-w-[120px]">
                                {ROLE_LABELS[role]}
                            </p>
                        </div>
                        <ChevronDown size={13} className="text-white/60 shrink-0" />
                    </button>

                    {profileOpen && (
                        <div className="absolute right-0 top-full mt-2 w-56 bg-white rounded-xl shadow-card-lg border border-border z-50 overflow-hidden animate-fade-up">
                            <div className="px-4 py-3 bg-primary">
                                <p className="text-white text-xs font-semibold">Logged In As</p>
                                <p className="text-white/70 text-[11px] mt-0.5">{ROLE_LABELS[role]}</p>
                            </div>
                            <div className="py-1">
                                <Link
                                    href="/profile"
                                    className="flex items-center gap-2.5 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                                    onClick={() => setProfileOpen(false)}
                                >
                                    <User size={14} className="text-gray-400" />
                                    My Profile
                                </Link>
                                <Link
                                    href="/settings"
                                    className="flex items-center gap-2.5 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                                    onClick={() => setProfileOpen(false)}
                                >
                                    <Settings size={14} className="text-gray-400" />
                                    Settings
                                </Link>
                                <hr className="my-1 border-gray-100" />
                                <Link
                                    href="/logout"
                                    className="flex items-center gap-2.5 px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                                    onClick={() => setProfileOpen(false)}
                                >
                                    <LogOut size={14} />
                                    Sign Out
                                </Link>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
}

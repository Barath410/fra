"use client";
import React from "react";
import { GovTopBanner } from "./gov-top-banner";
import { TopNavigation, type UserRole } from "./top-navigation";

interface DashboardLayoutProps {
    children: React.ReactNode;
    role: UserRole;
    pageName?: string;
    pageNameHi?: string;
    title?: string;
    titleHi?: string;
    stateName?: string;
    stateColor?: string;
    districtName?: string;
    userName?: string;
    userDesignation?: string;
    alertCount?: number;
    lastUpdated?: string;
}

export function DashboardLayout({
    children,
    role,
    pageName,
    pageNameHi,
    title,
    titleHi,
    stateName,
    stateColor,
    districtName,
    userName,
    userDesignation,
    alertCount = 0,
    lastUpdated,
}: DashboardLayoutProps) {
    return (
        <div className="min-h-screen flex flex-col bg-slate-50">
            {/* Government top band */}
            <GovTopBanner />

            {/* Top Navigation */}
            <TopNavigation role={role} userName={userName} userDesignation={userDesignation} />

            {/* Main layout */}
            <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
                <main
                    id="main-content"
                    className="flex-1 overflow-y-auto p-4 lg:p-8"
                >
                    <div className="max-w-[1600px] mx-auto animate-fade-up">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
}

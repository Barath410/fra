"use client";
import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
    LayoutDashboard, Map, FileText, Users, BarChart3, Settings, LogOut,
    ChevronDown, FlameIcon, Layers, Cpu, ClipboardList, GitMerge, Search,
    ShieldCheck, TreePine, Building2, HelpCircle, FileSearch, AlertTriangle,
    PieChart, MapPin, Menu, X, Bell
} from "lucide-react";
import { cn } from "@/lib/utils";

export type UserRole =
    | "mota-nodal"
    | "state-commissioner"
    | "district-collector"
    | "sdlc-officer"
    | "range-officer"
    | "gram-sabha"
    | "ngo-researcher"
    | "citizen";

interface NavItem {
    icon: React.ReactNode;
    label: string;
    labelHi: string;
    href: string;
    badge?: number;
    badgeVariant?: "danger" | "info" | "warn";
    children?: NavItem[];
}

const NAV_BY_ROLE: Record<UserRole, NavItem[]> = {
    "mota-nodal": [
        { icon: <LayoutDashboard size={18} />, label: "Dashboard", labelHi: "डैशबोर्ड", href: "/national-dashboard" },
        { icon: <Map size={18} />, label: "Atlas", labelHi: "एटलस", href: "/atlas" },
        { icon: <BarChart3 size={18} />, label: "Analytics", labelHi: "विश्लेषण", href: "/national-dashboard/analytics" },
        { icon: <GitMerge size={18} />, label: "DA-JGUA", labelHi: "DA-JGUA", href: "/national-dashboard/dajgua", badge: 3, badgeVariant: "warn" },
        { icon: <Cpu size={18} />, label: "DSS", labelHi: "DSS", href: "/dss" },
        { icon: <FlameIcon size={18} />, label: "Fire Alerts", labelHi: "अग्नि चेतावनी", href: "/national-dashboard/fire-alerts", badge: 5, badgeVariant: "danger" },
        { icon: <FileText size={18} />, label: "Policy", labelHi: "नीति", href: "/national-dashboard/documents" },
        { icon: <ClipboardList size={18} />, label: "Grievances", labelHi: "शिकायतें", href: "/grievances", badge: 12, badgeVariant: "danger" },
        { icon: <Layers size={18} />, label: "API", labelHi: "API", href: "/national-dashboard/integrations" },
    ],
    "state-commissioner": [
        { icon: <LayoutDashboard size={18} />, label: "Dashboard", labelHi: "डैशबोर्ड", href: "/state/MP/dashboard" },
        { icon: <Map size={18} />, label: "Atlas", labelHi: "एटलस", href: "/atlas?state=MP" },
        { icon: <ClipboardList size={18} />, label: "Claims", labelHi: "दावा", href: "/state/MP/claims" },
        { icon: <BarChart3 size={18} />, label: "Reports", labelHi: "रिपोर्ट", href: "/state/MP/reports" },
        { icon: <GitMerge size={18} />, label: "DA-JGUA", labelHi: "DA-JGUA", href: "/state/MP/dajgua" },
        { icon: <Users size={18} />, label: "Officers", labelHi: "अधिकारी", href: "/state/MP/officers", badge: 2, badgeVariant: "warn" },
        { icon: <PieChart size={18} />, label: "Schemes", labelHi: "योजनाएं", href: "/state/MP/schemes" },
        { icon: <AlertTriangle size={18} />, label: "Grievances", labelHi: "शिकायतें", href: "/grievances?state=MP", badge: 38, badgeVariant: "danger" },
    ],
    "district-collector": [
        { icon: <LayoutDashboard size={18} />, label: "Dashboard", labelHi: "डैशबोर्ड", href: "/district/MP-MAN/dashboard" },
        { icon: <Map size={18} />, label: "Atlas", labelHi: "एटलस", href: "/atlas?district=MP-MAN" },
        { icon: <ClipboardList size={18} />, label: "Queue", labelHi: "कतार", href: "/district/MP-MAN/claims", badge: 24, badgeVariant: "warn" },
        { icon: <Cpu size={18} />, label: "DSS", labelHi: "DSS", href: "/district/MP-MAN/dss" },
        { icon: <MapPin size={18} />, label: "Tracking", labelHi: "ट्रैकिंग", href: "/district/MP-MAN/field-tracker" },
        { icon: <GitMerge size={18} />, label: "Gaps", labelHi: "अंतराल", href: "/district/MP-MAN/gaps" },
        { icon: <TreePine size={18} />, label: "Assets", labelHi: "संपत्ति", href: "/district/MP-MAN/assets" },
        { icon: <AlertTriangle size={18} />, label: "Alerts", labelHi: "चेतावनी", href: "/district/MP-MAN/alerts", badge: 3, badgeVariant: "danger" },
    ],
    "sdlc-officer": [
        { icon: <ClipboardList size={18} />, label: "Queue", labelHi: "कतार", href: "/sdlc/adjudication", badge: 47, badgeVariant: "warn" },
        { icon: <Search size={18} />, label: "Review", labelHi: "समीक्षा", href: "/sdlc/documents" },
        { icon: <ShieldCheck size={18} />, label: "Approved", labelHi: "स्वीकृत", href: "/sdlc/approved" },
        { icon: <FileSearch size={18} />, label: "Rejected", labelHi: "अस्वीकृत", href: "/sdlc/rejected" },
        { icon: <Building2 size={18} />, label: "RoR", labelHi: "RoR", href: "/sdlc/ror" },
        { icon: <Users size={18} />, label: "Hearings", labelHi: "सुनवाई", href: "/sdlc/hearings" },
        { icon: <AlertTriangle size={18} />, label: "Appeals", labelHi: "अपीलें", href: "/sdlc/appeals", badge: 8, badgeVariant: "info" },
        { icon: <Map size={18} />, label: "GIS", labelHi: "GIS", href: "/atlas?sdlc=true" },
    ],
    "range-officer": [
        { icon: <MapPin size={18} />, label: "Assignments", labelHi: "नियुक्तियां", href: "/field-officer/assignments", badge: 7, badgeVariant: "warn" },
        { icon: <Map size={18} />, label: "Map", labelHi: "नक्शा", href: "/field-officer/map" },
        { icon: <ClipboardList size={18} />, label: "New Report", labelHi: "नई रिपोर्ट", href: "/field-officer/new-report" },
        { icon: <FileText size={18} />, label: "Reports", labelHi: "रिपोर्ट", href: "/field-officer/reports" },
        { icon: <AlertTriangle size={18} />, label: "Notifs", labelHi: "सूचनाएं", href: "/field-officer/notifications", badge: 3, badgeVariant: "danger" },
        { icon: <HelpCircle size={18} />, label: "Guidelines", labelHi: "दिशानिर्देश", href: "/field-officer/guidelines" },
    ],
    "gram-sabha": [
        { icon: <LayoutDashboard size={18} />, label: "Village", labelHi: "गांव", href: "/gram-sabha/village" },
        { icon: <FileText size={18} />, label: "File Claim", labelHi: "दावा दर्ज", href: "/gram-sabha/new-claim" },
        { icon: <ClipboardList size={18} />, label: "My Claims", labelHi: "मेरे दावे", href: "/gram-sabha/claims" },
        { icon: <Map size={18} />, label: "CFR Map", labelHi: "CFR नक्शा", href: "/gram-sabha/map" },
        { icon: <Cpu size={18} />, label: "Schemes", labelHi: "योजनाएं", href: "/gram-sabha/schemes" },
        { icon: <AlertTriangle size={18} />, label: "Grievance", labelHi: "शिकायत", href: "/gram-sabha/grievance" },
    ],
    "ngo-researcher": [
        { icon: <Map size={18} />, label: "Atlas", labelHi: "एटलस", href: "/analytics/atlas" },
        { icon: <BarChart3 size={18} />, label: "Builder", labelHi: "बिल्डर", href: "/analytics/builder" },
        { icon: <BarChart3 size={18} />, label: "Trends", labelHi: "रुझान", href: "/analytics/trends" },
        { icon: <TreePine size={18} />, label: "Forest Health", labelHi: "वन स्वास्थ्य", href: "/analytics/ndvi" },
        { icon: <FileText size={18} />, label: "Downloads", labelHi: "डाउनलोड", href: "/analytics/download" },
        { icon: <Settings size={18} />, label: "API", labelHi: "API", href: "/analytics/api" },
    ],
    citizen: [
        { icon: <ClipboardList size={18} />, label: "Status", labelHi: "स्थिति", href: "/mera-patta/status" },
        { icon: <Cpu size={18} />, label: "Eligibility", labelHi: "पात्रता", href: "/mera-patta/schemes" },
        { icon: <FileText size={18} />, label: "Patta", labelHi: "पट्टा", href: "/mera-patta/download" },
        { icon: <AlertTriangle size={18} />, label: "Grievance", labelHi: "शिकायत", href: "/mera-patta/grievance" },
        { icon: <HelpCircle size={18} />, label: "FAQ", labelHi: "FAQ", href: "/mera-patta/help" },
    ],
};

interface HeaderNavProps {
    role: UserRole;
    userName?: string;
    userDesignation?: string;
    pendingCount?: number;
}

export function HeaderNav({
    role,
    userName = "Officer Name",
    userDesignation = "Government Official",
    pendingCount = 0,
}: HeaderNavProps) {
    const pathname = usePathname();
    const navItems = NAV_BY_ROLE[role] ?? [];
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    const isActive = (href: string) => pathname === href || pathname.startsWith(href + "/");

    return (
        <header className="flex-col relative z-50 shadow-md">
            {/* 1. Branding & Profile Bar (White) */}
            <div className="bg-white border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
                    {/* Brand */}
                    <div className="flex items-center gap-3">
                         <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center shrink-0 shadow-lg text-white">
                            <TreePine size={20} />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-gray-900 leading-none">VanAdhikar <span className="text-blue-600">Drishti</span></h1>
                            <p className="text-[10px] text-gray-500 font-medium tracking-wider uppercase">Ministry of Tribal Affairs</p>
                        </div>
                    </div>

                    {/* Desktop Actions */}
                    <div className="hidden md:flex items-center gap-6">
                        {/* Search & Notif */}
                        <div className="flex items-center gap-3 border-r border-gray-200 pr-6">
                            <button className="p-2 text-gray-500 hover:bg-gray-100 rounded-full transition-colors relative">
                                <Bell size={20} />
                                {pendingCount > 0 && <span className="absolute top-1.5 right-1.5 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-white"></span>}
                            </button>
                            <button className="p-2 text-gray-500 hover:bg-gray-100 rounded-full transition-colors">
                                <Settings size={20} />
                            </button>
                             <button className="p-2 text-gray-500 hover:bg-gray-100 rounded-full transition-colors">
                                <HelpCircle size={20} />
                            </button>
                        </div>

                        {/* Profile User */}
                        <div className="flex items-center gap-3">
                            <div className="text-right hidden lg:block">
                                <p className="text-sm font-bold text-gray-800 leading-tight">{userName}</p>
                                <p className="text-xs text-gray-500">{userDesignation}</p>
                            </div>
                            <div className="w-10 h-10 rounded-full bg-blue-100 border border-blue-200 flex items-center justify-center text-blue-700 font-bold shadow-sm">
                                {userName.charAt(0)}
                            </div>
                            <Link href="/logout" className="p-2 text-red-500 hover:bg-red-50 rounded-full transition-colors" title="Logout">
                                <LogOut size={18} />
                            </Link>
                        </div>
                    </div>

                    {/* Mobile Menu Toggle */}
                    <button 
                        className="md:hidden p-2 text-gray-600"
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                    >
                        {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
                    </button>
                </div>
            </div>

            {/* 2. Navigation Bar (Use requested solid blue #2563eb) */}
            <div className="bg-[#2563eb] text-white shadow-inner hidden md:block">
                <div className="max-w-7xl mx-auto px-4">
                    <nav className="flex items-center gap-1 overflow-x-auto no-scrollbar py-0">
                        {navItems.map((item) => {
                            const active = isActive(item.href);
                            return (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    className={cn(
                                        "flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-4 transition-all whitespace-nowrap",
                                        active 
                                            ? "border-white bg-[#1d4ed8]" // Darker blue bg for active
                                            : "border-transparent hover:bg-[#1d4ed8] hover:border-blue-300/50 text-blue-100 hover:text-white"
                                    )}
                                >
                                    {item.icon}
                                    <span>{item.label}</span>
                                    {item.badge && (
                                        <span className={cn(
                                            "text-[10px] px-1.5 py-0.5 rounded-full font-bold ml-1",
                                             item.badgeVariant === "danger" ? "bg-red-500 text-white" :
                                             item.badgeVariant === "warn" ? "bg-amber-400 text-gray-900" :
                                             "bg-blue-800 text-white"
                                        )}>
                                            {item.badge}
                                        </span>
                                    )}
                                </Link>
                            )
                        })}
                    </nav>
                </div>
            </div>

            {/* Mobile Drawer */}
            {mobileMenuOpen && (
                <div className="md:hidden bg-slate-50 border-b border-gray-200 shadow-xl max-h-[80vh] overflow-y-auto">
                     <nav className="p-4 space-y-2">
                        {navItems.map((item) => (
                            <Link
                                key={item.href}
                                href={item.href}
                                onClick={() => setMobileMenuOpen(false)}
                                className={cn(
                                    "flex items-center gap-3 px-4 py-3 rounded-xl font-medium",
                                    isActive(item.href)
                                        ? "bg-blue-100 text-blue-700" 
                                        : "bg-white text-gray-700 hover:bg-gray-100"
                                )}
                            >
                                {item.icon}
                                <span className="flex-1">{item.label}</span>
                                {item.badge && (
                                    <span className="bg-gray-200 text-gray-700 px-2 py-0.5 rounded-full text-xs font-bold">{item.badge}</span>
                                )}
                            </Link>
                        ))}
                         <div className="border-t border-gray-200 mt-4 pt-4 flex gap-4">
                            <Link href="/settings" className="flex-1 flex items-center justify-center gap-2 p-2 bg-white border border-gray-200 rounded-lg text-sm font-medium">
                                <Settings size={16}/> Settings
                            </Link>
                            <Link href="/logout" className="flex-1 flex items-center justify-center gap-2 p-2 bg-red-50 border border-red-100 text-red-600 rounded-lg text-sm font-medium">
                                <LogOut size={16}/> Logout
                            </Link>
                        </div>
                    </nav>
                </div>
            )}
        </header>
    );
}

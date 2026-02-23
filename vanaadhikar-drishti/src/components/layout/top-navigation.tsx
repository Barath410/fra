"use client";
import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
    LayoutDashboard,
    Map,
    FileText,
    Users,
    BarChart3,
    Settings,
    LogOut,
    ChevronDown,
    FlameIcon,
    Layers,
    Cpu,
    ClipboardList,
    GitMerge,
    Search,
    ShieldCheck,
    TreePine,
    Building2,
    HelpCircle,
    FileSearch,
    AlertTriangle,
    PieChart,
    MapPin,
    Menu,
    X
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
        { icon: <LayoutDashboard size={16} />, label: "Dashboard", labelHi: "डैशबोर्ड", href: "/national-dashboard" },
        { icon: <Map size={16} />, label: "Atlas", labelHi: "एटलस", href: "/atlas" },
        { icon: <BarChart3 size={16} />, label: "Analytics", labelHi: "विश्लेषण", href: "/national-dashboard/analytics" },
        { icon: <GitMerge size={16} />, label: "Tracker", labelHi: "ट्रैकर", href: "/national-dashboard/dajgua", badge: 3, badgeVariant: "warn" },
        { icon: <Cpu size={16} />, label: "DSS", labelHi: "DSS", href: "/dss" },
        { icon: <FlameIcon size={16} />, label: "Fire Alerts", labelHi: "अग्नि चेतावनी", href: "/national-dashboard/fire-alerts", badge: 5, badgeVariant: "danger" },
        { icon: <FileText size={16} />, label: "Policy", labelHi: "नीति", href: "/national-dashboard/documents" },
        { icon: <ClipboardList size={16} />, label: "Grievances", labelHi: "शिकायत", href: "/grievances", badge: 12, badgeVariant: "danger" },
        { icon: <Settings size={16} />, label: "Settings", labelHi: "सेटिंग", href: "/settings" },
    ],
    "state-commissioner": [
        { icon: <LayoutDashboard size={16} />, label: "Dashboard", labelHi: "डैशबोर्ड", href: "/state/MP/dashboard" },
        { icon: <Map size={16} />, label: "Atlas", labelHi: "एटलस", href: "/atlas?state=MP" },
        { icon: <ClipboardList size={16} />, label: "Claims", labelHi: "दावा", href: "/state/MP/claims" },
        { icon: <BarChart3 size={16} />, label: "Reports", labelHi: "रिपोर्ट", href: "/state/MP/reports" },
        { icon: <GitMerge size={16} />, label: "DA-JGUA", labelHi: "DA-JGUA", href: "/state/MP/dajgua" },
        { icon: <PieChart size={16} />, label: "Schemes", labelHi: "योजनाएं", href: "/state/MP/schemes" },
        { icon: <AlertTriangle size={16} />, label: "Grievances", labelHi: "शिकायतें", href: "/grievances?state=MP", badge: 38, badgeVariant: "danger" },
        { icon: <Settings size={16} />, label: "Settings", labelHi: "सेटिंग", href: "/settings" },
    ],
    "district-collector": [
        { icon: <LayoutDashboard size={16} />, label: "Dashboard", labelHi: "डैशबोर्ड", href: "/district/MP-MAN/dashboard" },
        { icon: <Map size={16} />, label: "GIS Atlas", labelHi: "एटलस", href: "/atlas?district=MP-MAN" },
        { icon: <ClipboardList size={16} />, label: "Claims", labelHi: "दावा", href: "/district/MP-MAN/claims", badge: 24, badgeVariant: "warn" },
        { icon: <Cpu size={16} />, label: "DSS", labelHi: "DSS", href: "/district/MP-MAN/dss" },
        { icon: <MapPin size={16} />, label: "Tracking", labelHi: "ट्रैकिंग", href: "/district/MP-MAN/field-tracker" },
        { icon: <GitMerge size={16} />, label: "Gaps", labelHi: "अंतराल", href: "/district/MP-MAN/gaps" },
        { icon: <AlertTriangle size={16} />, label: "Alerts", labelHi: "चेतावनी", href: "/district/MP-MAN/alerts", badge: 3, badgeVariant: "danger" },
        { icon: <Settings size={16} />, label: "Settings", labelHi: "सेटिंग", href: "/settings" },
    ],
    "sdlc-officer": [
        { icon: <ClipboardList size={16} />, label: "Queue", labelHi: "कतार", href: "/sdlc/adjudication", badge: 47, badgeVariant: "warn" },
        { icon: <Search size={16} />, label: "Review", labelHi: "समीक्षा", href: "/sdlc/documents" },
        { icon: <ShieldCheck size={16} />, label: "Approved", labelHi: "स्वीकृत", href: "/sdlc/approved" },
        { icon: <FileSearch size={16} />, label: "Rejected", labelHi: "अस्वीकृत", href: "/sdlc/rejected" },
        { icon: <Building2 size={16} />, label: "RoR", labelHi: "RoR", href: "/sdlc/ror" },
        { icon: <Map size={16} />, label: "GIS", labelHi: "GIS", href: "/atlas?sdlc=true" },
    ],
    "range-officer": [
        { icon: <MapPin size={16} />, label: "Tasks", labelHi: "कार्य", href: "/field-officer/assignments", badge: 7, badgeVariant: "warn" },
        { icon: <Map size={16} />, label: "Map", labelHi: "नक्शा", href: "/field-officer/map" },
        { icon: <ClipboardList size={16} />, label: "Report", labelHi: "रिपोर्ट", href: "/field-officer/new-report" },
        { icon: <AlertTriangle size={16} />, label: "Alerts", labelHi: "सूचनाएं", href: "/field-officer/notifications", badge: 3, badgeVariant: "danger" },
    ],
    "gram-sabha": [
        { icon: <LayoutDashboard size={16} />, label: "Home", labelHi: "होम", href: "/gram-sabha/village" },
        { icon: <FileText size={16} />, label: "New Claim", labelHi: "नया दावा", href: "/gram-sabha/new-claim" },
        { icon: <ClipboardList size={16} />, label: "My Claims", labelHi: "मेरे दावे", href: "/gram-sabha/claims" },
        { icon: <Map size={16} />, label: "Map", labelHi: "नक्शा", href: "/gram-sabha/map" },
        { icon: <AlertTriangle size={16} />, label: "Grievance", labelHi: "शिकायत", href: "/gram-sabha/grievance" },
    ],
    "ngo-researcher": [
        { icon: <Map size={16} />, label: "Atlas", labelHi: "एटलस", href: "/analytics/atlas" },
        { icon: <BarChart3 size={16} />, label: "Analytics", labelHi: "एनालिटिक्स", href: "/analytics/builder" },
        { icon: <TreePine size={16} />, label: "Forest", labelHi: "वन", href: "/analytics/ndvi" },
        { icon: <FileText size={16} />, label: "Data", labelHi: "डेटा", href: "/analytics/download" },
    ],
    citizen: [
        { icon: <ClipboardList size={16} />, label: "Status", labelHi: "स्थिति", href: "/mera-patta/status" },
        { icon: <Cpu size={16} />, label: "Schemes", labelHi: "योजनाएं", href: "/mera-patta/schemes" },
        { icon: <FileText size={16} />, label: "Download", labelHi: "डाउनलोड", href: "/mera-patta/download" },
        { icon: <HelpCircle size={16} />, label: "Help", labelHi: "सहायता", href: "/mera-patta/help" },
    ],
};

export function TopNavigation({
    role,
    userName = "Officer",
    userDesignation,
}: {
    role: UserRole;
    userName?: string;
    userDesignation?: string;
}) {
    const pathname = usePathname();
    const navItems = NAV_BY_ROLE[role] ?? [];
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [activeDropdown, setActiveDropdown] = useState<string | null>(null);

    const isActive = (href: string) => pathname === href || pathname.startsWith(href + "/");

    return (
        <>
            {/* Desktop Top Navigation Bar */}
            <div className="hidden lg:flex items-center justify-between px-6 py-0 bg-white border-b border-gray-200 shadow-sm sticky top-0 z-30 h-16">
                {/* Logo Area */}
                <div className="flex items-center gap-3 shrink-0 mr-8">
                    <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center shrink-0 shadow-lg">
                        <TreePine size={20} className="text-white" />
                    </div>
                    <div className="min-w-0">
                        <p className="text-gray-900 font-bold text-base leading-none tracking-tight">
                            VanAdhikar
                        </p>
                        <p className="text-blue-600 text-[10px] font-bold mt-0.5 tracking-wide uppercase">
                            Drishti Portal
                        </p>
                    </div>
                </div>

                {/* Navigation Items */}
                <nav className="flex-1 flex items-center gap-1 overflow-x-auto no-scrollbar mask-gradient-right">
                    {navItems.map((item) => {
                        const active = isActive(item.href);
                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={cn(
                                    "flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 whitespace-nowrap",
                                    active
                                        ? "bg-blue-600 text-white shadow-md shadow-blue-600/20"
                                        : "text-gray-600 hover:bg-blue-50 hover:text-blue-700"
                                )}
                            >
                                <span className={cn("shrink-0", active ? "text-white" : "text-gray-400 group-hover:text-blue-500")}>
                                    {item.icon}
                                </span>
                                <span>{item.label}</span>
                                {item.badge && (
                                    <span
                                        className={cn(
                                            "ml-1 px-1.5 py-0.5 rounded-full text-[10px] font-bold",
                                            active ? "bg-white/20 text-white" :
                                                item.badgeVariant === "danger" ? "bg-red-100 text-red-600" :
                                                    item.badgeVariant === "warn" ? "bg-amber-100 text-amber-600" :
                                                        "bg-blue-100 text-blue-600"
                                        )}
                                    >
                                        {item.badge}
                                    </span>
                                )}
                            </Link>
                        );
                    })}
                </nav>

                {/* Right Actions */}
                <div className="flex items-center gap-4 pl-4 border-l border-gray-100 shrink-0 ml-4">
                    <div className="text-right hidden xl:block">
                        <p className="text-sm font-semibold text-gray-900 leading-tight">{userName}</p>
                        <p className="text-xs text-gray-500">{userDesignation}</p>
                    </div>
                    <div className="w-9 h-9 rounded-full bg-blue-100 border border-blue-200 flex items-center justify-center text-blue-700 font-bold shadow-sm">
                        {userName.charAt(0)}
                    </div>
                    <Link
                        href="/help"
                        className="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-colors"
                        title="Help"
                    >
                        <HelpCircle size={20} />
                    </Link>
                    <Link
                        href="/logout"
                        className="p-2 text-red-500 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors"
                        title="Logout"
                    >
                        <LogOut size={20} />
                    </Link>
                </div>
            </div>

            {/* Mobile Header */}
            <div className="lg:hidden flex items-center justify-between px-4 py-3 bg-white border-b border-gray-200 sticky top-0 z-30">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center shadow-md">
                        <TreePine size={18} className="text-white" />
                    </div>
                    <span className="font-bold text-gray-900">VanAdhikar</span>
                </div>
                <button
                    onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                    className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg bg-gray-50 border border-gray-200"
                >
                    {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
                </button>
            </div>

            {/* Mobile Menu Overlay */}
            {mobileMenuOpen && (
                <div className="lg:hidden fixed inset-0 z-20 bg-white pt-20 px-4 pb-6 overflow-y-auto">
                    <div className="flex flex-col gap-2">
                        {navItems.map((item) => {
                            const active = isActive(item.href);
                            return (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    onClick={() => setMobileMenuOpen(false)}
                                    className={cn(
                                        "flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all",
                                        active
                                            ? "bg-blue-600 text-white shadow-md shadow-blue-600/20"
                                            : "bg-gray-50 text-gray-700 border border-gray-100"
                                    )}
                                >
                                    {item.icon}
                                    <span>{item.label}</span>
                                    {item.badge && (
                                        <span className="ml-auto bg-white/20 px-2 py-0.5 rounded-full text-xs">
                                            {item.badge}
                                        </span>
                                    )}
                                </Link>
                            );
                        })}
                        <hr className="my-2 border-gray-200" />
                        <div className="flex items-center gap-3 px-4 py-3">
                            <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold">
                                {userName.charAt(0)}
                            </div>
                            <div>
                                <p className="font-semibold text-gray-900">{userName}</p>
                                <p className="text-xs text-gray-500">{userDesignation}</p>
                            </div>
                        </div>
                        <Link
                            href="/logout"
                            className="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-red-600 bg-red-50 border border-red-100"
                        >
                            <LogOut size={18} />
                            Sign Out
                        </Link>
                    </div>
                </div>
            )}
        </>
    );
}

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
    ChevronRight,
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
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

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
        { icon: <LayoutDashboard size={16} />, label: "National Dashboard", labelHi: "राष्ट्रीय डैशबोर्ड", href: "/national-dashboard" },
        { icon: <Map size={16} />, label: "FRA National Atlas", labelHi: "FRA राष्ट्रीय एटलस", href: "/atlas" },
        { icon: <BarChart3 size={16} />, label: "Analytics & Reports", labelHi: "विश्लेषण एवं रिपोर्ट", href: "/national-dashboard/analytics" },
        { icon: <GitMerge size={16} />, label: "DA-JGUA Tracker", labelHi: "DA-JGUA ट्रैकर", href: "/national-dashboard/dajgua", badge: 3, badgeVariant: "warn" },
        { icon: <Cpu size={16} />, label: "DSS Engine", labelHi: "DSS इंजन", href: "/dss" },
        { icon: <FlameIcon size={16} />, label: "Forest Fire Alerts", labelHi: "वन अग्नि चेतावनी", href: "/national-dashboard/fire-alerts", badge: 5, badgeVariant: "danger" },
        { icon: <FileText size={16} />, label: "Policy Documents", labelHi: "नीति दस्तावेज़", href: "/national-dashboard/documents" },
        { icon: <ClipboardList size={16} />, label: "Grievance Inbox", labelHi: "शिकायत इनबॉक्स", href: "/grievances", badge: 12, badgeVariant: "danger" },
        { icon: <Layers size={16} />, label: "API Integrations", labelHi: "API एकीकरण", href: "/national-dashboard/integrations" },
        { icon: <Settings size={16} />, label: "System Settings", labelHi: "सिस्टम सेटिंग", href: "/settings" },
    ],
    "state-commissioner": [
        { icon: <LayoutDashboard size={16} />, label: "State Dashboard", labelHi: "राज्य डैशबोर्ड", href: "/state/MP/dashboard" },
        { icon: <Map size={16} />, label: "State FRA Atlas", labelHi: "राज्य FRA एटलस", href: "/atlas?state=MP" },
        { icon: <ClipboardList size={16} />, label: "Claims Pipeline", labelHi: "दावा पाइपलाइन", href: "/state/MP/claims" },
        { icon: <BarChart3 size={16} />, label: "District Reports", labelHi: "जिला रिपोर्ट", href: "/state/MP/reports" },
        { icon: <GitMerge size={16} />, label: "DA-JGUA", labelHi: "DA-JGUA", href: "/state/MP/dajgua" },
        { icon: <Users size={16} />, label: "Officer Management", labelHi: "अधिकारी प्रबंधन", href: "/state/MP/officers", badge: 2, badgeVariant: "warn" },
        { icon: <PieChart size={16} />, label: "CSS Saturation", labelHi: "CSS संतृप्ति", href: "/state/MP/schemes" },
        { icon: <AlertTriangle size={16} />, label: "Grievances", labelHi: "शिकायतें", href: "/grievances?state=MP", badge: 38, badgeVariant: "danger" },
        { icon: <FileText size={16} />, label: "MoTA Reports", labelHi: "MoTA रिपोर्ट", href: "/state/MP/mota-reports" },
        { icon: <Settings size={16} />, label: "Settings", labelHi: "सेटिंग", href: "/settings" },
    ],
    "district-collector": [
        { icon: <LayoutDashboard size={16} />, label: "District Dashboard", labelHi: "जिला डैशबोर्ड", href: "/district/MP-MAN/dashboard" },
        { icon: <Map size={16} />, label: "District GIS Atlas", labelHi: "जिला GIS एटलस", href: "/atlas?district=MP-MAN" },
        { icon: <ClipboardList size={16} />, label: "Claims Queue", labelHi: "दावा कतार", href: "/district/MP-MAN/claims", badge: 24, badgeVariant: "warn" },
        { icon: <Cpu size={16} />, label: "DSS Recommendations", labelHi: "DSS अनुशंसाएं", href: "/district/MP-MAN/dss" },
        { icon: <MapPin size={16} />, label: "Field Officers GPS", labelHi: "फील्ड ऑफिसर GPS", href: "/district/MP-MAN/field-tracker" },
        { icon: <GitMerge size={16} />, label: "Scheme Gap Analysis", labelHi: "योजना अंतराल विश्लेषण", href: "/district/MP-MAN/gaps" },
        { icon: <TreePine size={16} />, label: "Village Assets", labelHi: "गांव की संपत्ति", href: "/district/MP-MAN/assets" },
        { icon: <AlertTriangle size={16} />, label: "Alerts", labelHi: "चेतावनी", href: "/district/MP-MAN/alerts", badge: 3, badgeVariant: "danger" },
        { icon: <FileText size={16} />, label: "Convergence Meeting", labelHi: "संगम बैठक", href: "/district/MP-MAN/meetings" },
        { icon: <Settings size={16} />, label: "Settings", labelHi: "सेटिंग", href: "/settings" },
    ],
    "sdlc-officer": [
        { icon: <ClipboardList size={16} />, label: "Adjudication Queue", labelHi: "अधिनिर्णय कतार", href: "/sdlc/adjudication", badge: 47, badgeVariant: "warn" },
        { icon: <Search size={16} />, label: "Document Review", labelHi: "दस्तावेज़ समीक्षा", href: "/sdlc/documents" },
        { icon: <ShieldCheck size={16} />, label: "Approved Claims", labelHi: "स्वीकृत दावे", href: "/sdlc/approved" },
        { icon: <FileSearch size={16} />, label: "Rejected Claims", labelHi: "अस्वीकृत दावे", href: "/sdlc/rejected" },
        { icon: <Building2 size={16} />, label: "RoR Issuance", labelHi: "RoR जारी करना", href: "/sdlc/ror" },
        { icon: <Users size={16} />, label: "Hearing Schedule", labelHi: "सुनवाई अनुसूची", href: "/sdlc/hearings" },
        { icon: <AlertTriangle size={16} />, label: "Appeals", labelHi: "अपीलें", href: "/sdlc/appeals", badge: 8, badgeVariant: "info" },
        { icon: <Map size={16} />, label: "Block GIS View", labelHi: "ब्लॉक GIS दृश्य", href: "/atlas?sdlc=true" },
    ],
    "range-officer": [
        { icon: <MapPin size={16} />, label: "My Assignments", labelHi: "मेरी नियुक्तियां", href: "/field-officer/assignments", badge: 7, badgeVariant: "warn" },
        { icon: <Map size={16} />, label: "Offline Map", labelHi: "ऑफलाइन नक्शा", href: "/field-officer/map" },
        { icon: <ClipboardList size={16} />, label: "Submit Visit Report", labelHi: "विज़िट रिपोर्ट जमा करें", href: "/field-officer/new-report" },
        { icon: <FileText size={16} />, label: "My Reports", labelHi: "मेरी रिपोर्ट", href: "/field-officer/reports" },
        { icon: <AlertTriangle size={16} />, label: "Notifications", labelHi: "सूचनाएं", href: "/field-officer/notifications", badge: 3, badgeVariant: "danger" },
        { icon: <HelpCircle size={16} />, label: "FRA Guidelines", labelHi: "FRA दिशानिर्देश", href: "/field-officer/guidelines" },
    ],
    "gram-sabha": [
        { icon: <LayoutDashboard size={16} />, label: "Village Dashboard", labelHi: "गांव का डैशबोर्ड", href: "/gram-sabha/village" },
        { icon: <FileText size={16} />, label: "File New Claim", labelHi: "नया दावा दर्ज करें", href: "/gram-sabha/new-claim" },
        { icon: <ClipboardList size={16} />, label: "My Claims", labelHi: "मेरे दावे", href: "/gram-sabha/claims" },
        { icon: <Map size={16} />, label: "Village CFR Map", labelHi: "गांव CFR नक्शा", href: "/gram-sabha/map" },
        { icon: <Cpu size={16} />, label: "Scheme Benefits", labelHi: "योजना लाभ", href: "/gram-sabha/schemes" },
        { icon: <AlertTriangle size={16} />, label: "File Grievance", labelHi: "शिकायत दर्ज करें", href: "/gram-sabha/grievance" },
        { icon: <HelpCircle size={16} />, label: "Help", labelHi: "सहायता", href: "/gram-sabha/help" },
    ],
    "ngo-researcher": [
        { icon: <Map size={16} />, label: "Open FRA Atlas", labelHi: "ओपन FRA एटलस", href: "/analytics/atlas" },
        { icon: <BarChart3 size={16} />, label: "Analytics Builder", labelHi: "एनालिटिक्स बिल्डर", href: "/analytics/builder" },
        { icon: <BarChart3 size={16} />, label: "Progress Trends", labelHi: "प्रगति रुझान", href: "/analytics/trends" },
        { icon: <TreePine size={16} />, label: "Forest Health Monitor", labelHi: "वन स्वास्थ्य मॉनिटर", href: "/analytics/ndvi" },
        { icon: <FileText size={16} />, label: "Data Downloads", labelHi: "डेटा डाउनलोड", href: "/analytics/download" },
        { icon: <Settings size={16} />, label: "API Access", labelHi: "API एक्सेस", href: "/analytics/api" },
    ],
    citizen: [
        { icon: <ClipboardList size={16} />, label: "My Claim Status", labelHi: "मेरा दावा स्थिति", href: "/mera-patta/status" },
        { icon: <Cpu size={16} />, label: "Scheme Eligibility", labelHi: "योजना पात्रता", href: "/mera-patta/schemes" },
        { icon: <FileText size={16} />, label: "Download Patta", labelHi: "पट्टा डाउनलोड करें", href: "/mera-patta/download" },
        { icon: <AlertTriangle size={16} />, label: "File Grievance", labelHi: "शिकायत दर्ज करें", href: "/mera-patta/grievance" },
        { icon: <HelpCircle size={16} />, label: "Help & FAQ", labelHi: "सहायता और FAQ", href: "/mera-patta/help" },
    ],
};

interface SidebarProps {
    role: UserRole;
    stateName?: string;
    userName?: string;
    userDesignation?: string;
    collapsed?: boolean;
    onToggleCollapse?: () => void;
    pendingCount?: number;
}

export function Sidebar({
    role,
    stateName,
    userName = "Officer Name",
    userDesignation = "Government Official",
    collapsed = false,
    onToggleCollapse,
    pendingCount,
}: SidebarProps) {
    const pathname = usePathname();
    const navItems = NAV_BY_ROLE[role] ?? [];
    const [expandedGroups, setExpandedGroups] = useState<string[]>([]);

    const toggleGroup = (label: string) => {
        setExpandedGroups((prev) =>
            prev.includes(label) ? prev.filter((g) => g !== label) : [...prev, label]
        );
    };

    const isActive = (href: string) =>
        pathname === href || pathname.startsWith(href + "/");

    return (
        <aside
            className={cn(
                "h-screen sticky top-0 flex flex-col transition-all duration-300 z-40 bg-sidebar border-r border-blue-100 shadow-xl",
                collapsed ? "w-[70px]" : "w-[260px]"
            )}
            aria-label="Sidebar Navigation"
        >
            {/* Logo Area - Redesigned for Light Theme */}
            <div className={`flex items-center gap-3 px-5 py-5 border-b border-blue-100/50 shrink-0 ${collapsed ? "justify-center" : ""}`}>
                {/* Emblem Icon */}
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-blue-700 flex items-center justify-center shrink-0 shadow-lg ring-2 ring-blue-100">
                    <TreePine size={20} className="text-white" />
                </div>
                {!collapsed && (
                    <div className="min-w-0 animate-fade-in">
                        <p className="text-gray-900 font-bold text-lg leading-none tracking-tight">
                            VanAdhikar
                        </p>
                        <p className="text-blue-600 text-xs font-bold mt-1 tracking-wide uppercase">
                            Drishti Portal
                        </p>
                    </div>
                )}
            </div>

            {/* Compact Role chip */}
            {!collapsed && (
                <div className="px-4 py-4 shrink-0 bg-blue-50/50">
                    <div className="flex items-center gap-3 p-3 bg-white border border-blue-100/60 rounded-xl shadow-sm">
                        <div className="w-9 h-9 rounded-full bg-blue-100 flex items-center justify-center shrink-0 text-blue-700 font-bold text-sm border border-blue-200">
                            {userName.charAt(0).toUpperCase()}
                        </div>
                        <div className="min-w-0">
                            <p className="text-gray-900 text-sm font-semibold truncate">{userName}</p>
                            <p className="text-gray-500 text-xs truncate">{userDesignation}</p>
                        </div>
                    </div>
                    {stateName && (
                        <div className="mt-2 text-[10px] font-bold tracking-wider uppercase text-center py-1.5 rounded-full bg-blue-100/50 text-blue-700 border border-blue-200/50">
                            {stateName} Region
                        </div>
                    )}
                </div>
            )}

            {/* Nav Items */}
            <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1 scrollbar-thin scrollbar-thumb-blue-200 scrollbar-track-transparent">
                {navItems.map((item) => {
                    const active = isActive(item.href);
                    if (item.children) {
                        const isOpen = expandedGroups.includes(item.label);
                        return (
                            <div key={item.label} className="mb-1">
                                <button
                                    onClick={() => toggleGroup(item.label)}
                                    className={cn(
                                        "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200",
                                        active
                                            ? "bg-blue-100/80 text-blue-800 shadow-sm"
                                            : "text-gray-600 hover:bg-white hover:text-blue-600 hover:shadow-sm"
                                    )}
                                >
                                    <span className={cn("shrink-0", active ? "text-blue-600" : "text-gray-400")}>{item.icon}</span>
                                    {!collapsed && (
                                        <>
                                            <span className="flex-1 text-left">{item.label}</span>
                                            {isOpen ? (
                                                <ChevronDown size={14} className="text-blue-400" />
                                            ) : (
                                                <ChevronRight size={14} className="text-gray-300" />
                                            )}
                                        </>
                                    )}
                                </button>
                                {isOpen && !collapsed && (
                                    <div className="ml-4 mt-1 space-y-1 mb-2 border-l-2 border-blue-100 pl-3">
                                        {item.children.map((child) => (
                                            <Link
                                                key={child.href}
                                                href={child.href}
                                                className={cn(
                                                    "flex items-center gap-2 px-3 py-2 rounded-md text-sm transition-colors",
                                                    isActive(child.href)
                                                        ? "text-blue-700 font-semibold bg-blue-50"
                                                        : "text-gray-500 hover:text-blue-600 hover:bg-blue-50/50"
                                                )}
                                            >
                                                {child.icon}
                                                <span>{child.label}</span>
                                                {child.badge && (
                                                    <span className="ml-auto text-[10px] font-bold bg-blue-100 text-blue-600 px-1.5 py-0.5 rounded-full">{child.badge}</span>
                                                )}
                                            </Link>
                                        ))}
                                    </div>
                                )}
                            </div>
                        );
                    }
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 group relative",
                                active
                                    ? "bg-gradient-to-r from-blue-600 to-blue-500 text-white shadow-md shadow-blue-500/20"
                                    : "text-gray-600 hover:bg-white hover:text-blue-700 hover:shadow-sm"
                            )}
                            title={collapsed ? item.label : undefined}
                        >
                            <span className={cn("shrink-0 transition-colors", active ? "text-white" : "text-gray-400 group-hover:text-blue-500")}>{item.icon}</span>
                            {!collapsed && (
                                <>
                                    <span className="flex-1">{item.label}</span>
                                    {item.badge && (
                                        <span
                                            className={cn(
                                                "px-2 py-0.5 rounded-full text-[10px] font-bold shadow-sm",
                                                item.badgeVariant === "danger" ? "bg-red-500 text-white" :
                                                    item.badgeVariant === "warn" ? "bg-amber-400 text-white" :
                                                        "bg-blue-200 text-blue-800"
                                            )}
                                        >
                                            {item.badge > 99 ? "99+" : item.badge}
                                        </span>
                                    )}
                                </>
                            )}

                            {/* Active Indicator Strip */}
                            {active && !collapsed && (
                                <div className="absolute left-0 top-1/2 -translate-y-1/2 h-8 w-1 bg-white/20 rounded-r-full" />
                            )}
                        </Link>
                    );
                })}
            </nav>

            {/* Bottom actions & Collapse Toggle */}
            <div className="p-3 border-t border-blue-100 bg-white/50 space-y-2 shrink-0">
                {!collapsed && (
                    <div className="mb-2 p-3 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-100/60 shadow-inner">
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-xs font-bold text-blue-800">Support Center</span>
                            <div className="w-5 h-5 rounded-full bg-blue-200 flex items-center justify-center text-blue-700 text-[10px] font-bold">?</div>
                        </div>
                        <button className="w-full text-xs bg-white border border-blue-200 text-blue-600 font-semibold py-1.5 rounded-lg hover:bg-blue-50 transition-colors shadow-sm">
                            Get Help
                        </button>
                    </div>
                )}

                <div className="flex items-center gap-1">
                    <button
                        onClick={onToggleCollapse}
                        className="flex-1 flex items-center justify-center p-2 rounded-lg text-gray-500 hover:bg-gray-100 hover:text-blue-600 transition-colors"
                        title={collapsed ? "Expand Sidebar" : "Collapse Sidebar"}
                    >
                        {collapsed ? <ChevronRight size={18} /> : <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider"><ChevronRight className="rotate-180" size={14} /> <span>Collapse</span></div>}
                    </button>

                    <Link
                        href="/logout"
                        className={cn(
                            "flex items-center justify-center p-2 rounded-lg text-red-500 hover:bg-red-50 hover:text-red-600 transition-colors",
                            !collapsed && "flex-1 gap-2"
                        )}
                        title="Logout"
                    >
                        <LogOut size={18} />
                        {!collapsed && <span className="text-sm font-semibold">Logout</span>}
                    </Link>
                </div>
            </div>
        </aside>
    );
}

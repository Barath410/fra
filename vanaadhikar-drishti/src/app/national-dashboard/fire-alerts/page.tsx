"use client";
import Link from "next/link";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Flame, MapPin, Calendar, AlertTriangle } from "lucide-react";

export default function FireAlertsPage() {
    const alerts = [
        {
            id: "FA-2026-MP-001",
            state: "Madhya Pradesh",
            district: "Balaghat",
            village: "Silpidi",
            date: "Feb 18, 2026",
            severity: "critical",
            areaAffected: 45,
            isCFRZone: true,
            status: "active",
        },
        {
            id: "FA-2026-MH-023",
            state: "Maharashtra",
            district: "Gadchiroli",
            village: "Kurkheda",
            date: "Feb 17, 2026",
            severity: "high",
            areaAffected: 28,
            isCFRZone: true,
            status: "contained",
        },
        {
            id: "FA-2026-CG-015",
            state: "Chhattisgarh",
            district: "Bastar",
            village: "Dantewada",
            date: "Feb 16, 2026",
            severity: "medium",
            areaAffected: 12,
            isCFRZone: false,
            status: "monitoring",
        },
    ];

    return (
        <DashboardLayout role="mota-nodal" title="Forest Fire Alerts" titleHi="वन अग्नि चेतावनी">
            <div className="mb-5">
                <Link href="/national-dashboard" className="inline-flex items-center gap-2 text-sm text-accent hover:underline mb-4">
                    <ArrowLeft size={16} /> Back to National Dashboard
                </Link>
                <h1 className="text-2xl font-bold text-primary">Forest Fire Alerts in CFR Zones</h1>
                <p className="text-sm text-gray-600">Real-time monitoring of fire incidents in Community Forest Resource areas</p>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                {[
                    { label: "Active Alerts", value: 147, color: "text-red-600" },
                    { label: "CFR Zones Affected", value: 89, color: "text-amber-600" },
                    { label: "Total Area (ha)", value: "4,234", color: "text-primary" },
                    { label: "Contained", value: 234, color: "text-emerald-600" },
                ].map((stat, i) => (
                    <div key={i} className="tribal-card p-4">
                        <p className="text-sm text-gray-500 mb-1">{stat.label}</p>
                        <p className={`text-2xl font-bold ${stat.color}`}>{stat.value}</p>
                    </div>
                ))}
            </div>

            {/* Alerts List */}
            <div className="space-y-4">
                {alerts.map((alert) => (
                    <div key={alert.id} className="tribal-card p-5">
                        <div className="flex items-start justify-between mb-3">
                            <div className="flex items-center gap-3">
                                <div
                                    className={`w-12 h-12 rounded-full flex items-center justify-center ${alert.severity === "critical"
                                            ? "bg-red-100 text-red-600"
                                            : alert.severity === "high"
                                                ? "bg-amber-100 text-amber-600"
                                                : "bg-blue-100 text-blue-600"
                                        }`}
                                >
                                    <Flame size={24} />
                                </div>
                                <div>
                                    <h3 className="text-lg font-bold text-primary">{alert.village}</h3>
                                    <p className="text-sm text-gray-600">
                                        {alert.district}, {alert.state}
                                    </p>
                                </div>
                            </div>
                            <div className="flex flex-col items-end gap-2">
                                <Badge
                                    variant={
                                        alert.severity === "critical"
                                            ? "danger"
                                            : alert.severity === "high"
                                                ? "warning"
                                                : "info"
                                    }
                                >
                                    {alert.severity.toUpperCase()}
                                </Badge>
                                {alert.isCFRZone && <Badge variant="info">CFR Zone</Badge>}
                            </div>
                        </div>

                        <div className="grid grid-cols-3 gap-4 text-sm">
                            <div className="flex items-center gap-2">
                                <Calendar size={16} className="text-gray-400" />
                                <span className="text-gray-600">{alert.date}</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <MapPin size={16} className="text-gray-400" />
                                <span className="text-gray-600">{alert.areaAffected} hectares</span>
                            </div>
                            <div>
                                <span
                                    className={`text-xs px-2 py-1 rounded-full ${alert.status === "active"
                                            ? "bg-red-100 text-red-700"
                                            : alert.status === "contained"
                                                ? "bg-emerald-100 text-emerald-700"
                                                : "bg-blue-100 text-blue-700"
                                        }`}
                                >
                                    {alert.status.toUpperCase()}
                                </span>
                            </div>
                        </div>

                        <div className="mt-4 flex gap-2">
                            <button className="px-4 py-2 bg-primary text-white rounded-lg text-sm font-semibold shadow-md hover:shadow-lg transition-all">
                                View Details
                            </button>
                            <button className="px-4 py-2 border-2 border-gray-300 text-gray-700 rounded-lg text-sm font-semibold hover:bg-gray-50 transition-all">
                                Mark as Resolved
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </DashboardLayout>
    );
}

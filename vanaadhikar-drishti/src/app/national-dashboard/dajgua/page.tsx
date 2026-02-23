"use client";
import Link from "next/link";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Target, TrendingUp, CheckCircle, Clock } from "lucide-react";

export default function DAJGUAPage() {
    const interventions = [
        {
            id: "PMAY-G",
            name: "Pradhan Mantri Awaas Yojana - Gramin",
            targetVillages: 12458,
            completedVillages: 10234,
            saturationPct: 82,
            ministry: "Ministry of Rural Development",
            status: "on-track",
        },
        {
            id: "JJM",
            name: "Jal Jeevan Mission",
            targetVillages: 15632,
            completedVillages: 12987,
            saturationPct: 83,
            ministry: "Ministry of Jal Shakti",
            status: "on-track",
        },
        {
            id: "MGNREGA",
            name: "Mahatma Gandhi NREGA",
            targetVillages: 18456,
            completedVillages: 14389,
            saturationPct: 78,
            ministry: "Ministry of Rural Development",
            status: "needs-attention",
        },
        {
            id: "PMKISAN",
            name: "PM-KISAN",
            targetVillages: 14234,
            completedVillages: 10106,
            saturationPct: 71,
            ministry: "Ministry of Agriculture",
            status: "needs-attention",
        },
    ];

    return (
        <DashboardLayout role="mota-nodal" title="DA-JGUA Convergence" titleHi="DA-JGUA अभिसरण">
            <div className="mb-5">
                <Link href="/national-dashboard" className="inline-flex items-center gap-2 text-sm text-accent hover:underline mb-4">
                    <ArrowLeft size={16} /> Back to National Dashboard
                </Link>
                <h1 className="text-2xl font-bold text-primary">Development Action through Joint Governance & Unified Action (DA-JGUA)</h1>
                <p className="text-sm text-gray-600">Scheme convergence monitoring for FRA beneficiaries</p>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                {[
                    { label: "Total Schemes", value: 25, icon: <Target size={20} />, color: "text-primary" },
                    { label: "Avg Saturation", value: "73.2%", icon: <TrendingUp size={20} />, color: "text-accent" },
                    { label: "Villages Covered", value: "63,843", icon: <CheckCircle size={20} />, color: "text-emerald-600" },
                    { label: "In Progress", value: 8, icon: <Clock size={20} />, color: "text-amber-600" },
                ].map((stat, i) => (
                    <div key={i} className="tribal-card p-4">
                        <div className="flex items-center gap-2 mb-2">
                            <div className={stat.color}>{stat.icon}</div>
                            <p className={`text-2xl font-bold ${stat.color}`}>{stat.value}</p>
                        </div>
                        <p className="text-sm text-gray-500">{stat.label}</p>
                    </div>
                ))}
            </div>

            {/* Schemes List */}
            <div className="space-y-4">
                {interventions.map((scheme) => (
                    <div key={scheme.id} className="tribal-card p-5">
                        <div className="flex items-start justify-between mb-4">
                            <div>
                                <h3 className="text-lg font-bold text-primary">{scheme.name}</h3>
                                <p className="text-sm text-gray-600 mt-1">{scheme.ministry}</p>
                            </div>
                            <Badge variant={scheme.status === "on-track" ? "success" : "warning"}>
                                {scheme.status === "on-track" ? "On Track" : "Needs Attention"}
                            </Badge>
                        </div>

                        <div className="grid grid-cols-3 gap-4 mb-4">
                            <div>
                                <p className="text-xs text-gray-500 mb-1">Target Villages</p>
                                <p className="text-xl font-bold text-primary">{scheme.targetVillages.toLocaleString()}</p>
                            </div>
                            <div>
                                <p className="text-xs text-gray-500 mb-1">Completed</p>
                                <p className="text-xl font-bold text-emerald-600">{scheme.completedVillages.toLocaleString()}</p>
                            </div>
                            <div>
                                <p className="text-xs text-gray-500 mb-1">Saturation</p>
                                <p className="text-xl font-bold text-accent">{scheme.saturationPct}%</p>
                            </div>
                        </div>

                        {/* Progress Bar */}
                        <div className="relative h-3 bg-gray-200 rounded-full overflow-hidden">
                            <div
                                className={`h-full rounded-full transition-all duration-700 ${scheme.saturationPct >= 75 ? "bg-emerald-500" : "bg-amber-500"
                                    }`}
                                style={{ width: `${scheme.saturationPct}%` }}
                            ></div>
                        </div>

                        <div className="mt-4 flex gap-2">
                            <button className="px-4 py-2 bg-primary text-white rounded-lg text-sm font-semibold shadow-md hover:shadow-lg transition-all">
                                View Details
                            </button>
                            <Link
                                href="/dss"
                                className="px-4 py-2 border-2 border-primary text-primary rounded-lg text-sm font-semibold hover:bg-primary-50 transition-all"
                            >
                                DSS Recommendations
                            </Link>
                        </div>
                    </div>
                ))}
            </div>
        </DashboardLayout>
    );
}

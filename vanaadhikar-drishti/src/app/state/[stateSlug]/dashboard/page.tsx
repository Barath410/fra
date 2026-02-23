"use client";
import React, { useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
    Download, RefreshCw, Filter, Users, FileText,
    BarChart3, CheckCircle, Clock, XCircle, ChevronRight,
    MapPin, TrendingUp, AlertTriangle, ArrowUpRight,
    Printer, Send,
} from "lucide-react";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { StatCard } from "@/components/ui/stat-card";
import { Badge } from "@/components/ui/badge";
import { formatNumber } from "@/lib/utils";
import { BarChartWrapper, AreaChartWrapper, RadialChartWrapper } from "@/components/charts";
import { useDashboardData } from "@/lib/use-dashboard-data";
import type { StateStat, DistrictStat, Officer } from "@/types";

const SAMPLE_DISTRICTS = [
    { name: "Indore", grants: 1250, pending: 320, saturation: 79, population: 845000 },
    { name: "Katni", grants: 980, pending: 180, saturation: 84, population: 234000 },
    { name: "Rewa", grants: 850, pending: 210, saturation: 71, population: 456000 },
    { name: "Seoni", grants: 1100, pending: 280, saturation: 79, population: 342000 },
];

const STATE_DISTRICTS: Record<string, typeof SAMPLE_DISTRICTS> = {
    "madhya-pradesh": SAMPLE_DISTRICTS,
    odisha: SAMPLE_DISTRICTS.slice(0, 4),
    tripura: SAMPLE_DISTRICTS.slice(0, 2),
    telangana: SAMPLE_DISTRICTS.slice(0, 3),
};

const STATE_LABEL: Record<string, string> = {
    "madhya-pradesh": "Madhya Pradesh",
    odisha: "Odisha",
    tripura: "Tripura",
    telangana: "Telangana",
};

export default function StateDashboardPage() {
    const params = useParams();
    const stateSlug = (params?.stateSlug as string) ?? "madhya-pradesh";
    const { data, loading, error } = useDashboardData();

    const stateStats = (data?.stateStats as StateStat[]) ?? [];
    const stateData = stateStats.find((s) => s.slug === stateSlug) ?? stateStats[0];
    const stateCode = stateData?.id;

    const districtStats = (stateCode && data?.districtStats ? (data.districtStats[stateCode] as DistrictStat[] | undefined) : []) ?? [];
    const pipelineStages = data?.datasets?.claimPipeline ?? [];
    const monthlyData = (data?.datasets?.monthlyProgress ?? []).filter((m) => !stateCode || m.state === stateCode);
    const interventions = (data?.datasets?.dajguaInterventions ?? []).filter((itv) => !stateCode || itv.state === stateCode);
    const officers = ((data?.officers as Officer[] | undefined) ?? []).filter((o) => !stateCode || o.state === stateCode);
    const [activeTab, setActiveTab] = useState<"overview" | "districts" | "dajgua" | "officers">("overview");

    const tabs = [
        { id: "overview", label: "Overview" },
        { id: "districts", label: "Districts" },
        { id: "dajgua", label: "DA-JGUA" },
        { id: "officers", label: "Officers" },
    ] as const;

    if (loading) {
        return (
            <DashboardLayout role="state-commissioner" title="State Dashboard" titleHi="राज्य डैशबोर्ड">
                <div className="p-6">Loading state dashboard data…</div>
            </DashboardLayout>
        );
    }

    if (!stateData) {
        return (
            <DashboardLayout role="state-commissioner" title="State Dashboard" titleHi="राज्य डैशबोर्ड">
                <div className="p-6 text-sm text-red-600">No data available for this state.</div>
            </DashboardLayout>
        );
    }

    const monthlyTrend = monthlyData.map((m) => ({
        name: m.month,
        Granted: m.claimsGranted,
        Received: m.claimsReceived,
    }));

    const pipelineData = pipelineStages.map((s) => ({
        name: s.label.replace(" ", "\n"),
        Count: s.count > 10000 ? Math.floor(s.count / 1000) : s.count,
        color: s.color,
        label: s.label,
        labelHi: s.labelHi,
    }));

    const districtTableData = districtStats.map((d) => ({
        ...d,
        total: d.grants + d.pending + d.rejected,
        grantRate: Math.round((d.grants / Math.max(1, d.grants + d.pending + d.rejected)) * 100),
    }));

    const totalInterventions = interventions.length;
    const totalTargetVillages = interventions.reduce((sum, itv) => sum + (itv.targetVillages ?? 0), 0);
    const budgetAllocatedCr = interventions.reduce((sum, itv) => sum + (itv.budgetAllocatedCr ?? 0), 0);
    const budgetUtilizedCr = interventions.reduce((sum, itv) => sum + (itv.budgetUtilizedCr ?? 0), 0);
    const avgSaturation = interventions.length
        ? Math.round(interventions.reduce((sum, itv) => sum + (itv.saturationPct ?? 0), 0) / interventions.length)
        : 0;

    return (
        <DashboardLayout
            role="state-commissioner"
            title={`${stateData.name} — State Dashboard`}
            titleHi="राज्य डैशबोर्ड"
            stateColor={stateData.color}
        >
            {/* Header */}
            <div className="flex items-center justify-between mb-5">
                <div className="flex items-center gap-3">
                    <span
                        className="text-sm font-bold px-3 py-1 rounded-full text-white"
                        style={{ background: stateData.color }}
                    >
                        {stateData.id}
                    </span>
                    <div>
                        <h1 className="text-xl font-bold text-primary">{stateData.name} — FRA Status</h1>
                        <p className="text-xs text-gray-500">{stateData.districts} Districts · {formatNumber(stateData.villagesCovered)} Villages</p>
                    </div>
                </div>
                <div className="flex gap-2 no-print">
                    <button className="flex items-center gap-2 text-xs px-3 py-1.5 border border-gray-200 rounded-lg hover:bg-gray-50">
                        <Printer size={13} /> Print Report
                    </button>
                    <button className="flex items-center gap-2 text-xs px-3 py-1.5 border border-gray-200 rounded-lg hover:bg-gray-50">
                        <Send size={13} /> Send to MoTA
                    </button>
                    <button className="flex items-center gap-2 text-xs px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-600 transition-all shadow-md hover:shadow-lg">
                        <Download size={13} /> Export
                    </button>
                </div>
            </div>

            {/* KPI Row */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-5">
                <StatCard
                    title="Total Claims"
                    titleHi="कुल दावे"
                    value={stateData.totalClaims}
                    icon={<FileText size={18} />}
                    accentColor="#3B82F6"
                    change={2.3}
                    trend="up"
                />
                <StatCard
                    title="Pattas Granted"
                    titleHi="पट्टे जारी"
                    value={stateData.granted}
                    icon={<CheckCircle size={18} />}
                    accentColor="#22C55E"
                    subtitle={`${Math.round((stateData.granted / stateData.totalClaims) * 100)}% rate`}
                    trend="up"
                    change={1.2}
                />
                <StatCard
                    title="Pending Review"
                    titleHi="समीक्षाधीन"
                    value={stateData.pending}
                    icon={<Clock size={18} />}
                    accentColor="#F59E0B"
                    trend="down"
                    change={-0.8}
                />
                <StatCard
                    title="DA-JGUA Saturation"
                    titleHi="DA-JGUA संतृप्ति"
                    value={`${stateData.dajguaSaturation}%`}
                    icon={<BarChart3 size={18} />}
                    accentColor="#0D9488"
                    trend="up"
                    change={3.1}
                />
            </div>

            {/* Tabs */}
            <div className="flex gap-1 mb-5 bg-gray-100 p-1 rounded-lg w-fit no-print">
                {tabs.map((t) => (
                    <button
                        key={t.id}
                        onClick={() => setActiveTab(t.id)}
                        className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all ${activeTab === t.id
                            ? "bg-white text-primary shadow-md"
                            : "text-gray-500 hover:text-gray-700"
                            }`}
                    >
                        {t.label}
                    </button>
                ))}
            </div>

            {/* Overview Tab */}
            {activeTab === "overview" && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
                    {/* Claim Pipeline */}
                    <div className="tribal-card p-5 lg:col-span-2">
                        <h3 className="font-bold text-primary text-sm mb-4">Claim Pipeline (Kanban View)</h3>
                        <div className="grid grid-cols-3 lg:grid-cols-6 gap-2">
                            {pipelineData.map((stage) => (
                                <div key={stage.name} className="text-center">
                                    <div
                                        className="rounded-lg p-3 mb-2"
                                        style={{ background: `${stage.color}15` }}
                                    >
                                        <p className="text-lg font-bold" style={{ color: stage.color }}>
                                            {stage.Count > 100000 ? formatNumber(stage.Count) : stage.Count.toLocaleString()}
                                        </p>
                                    </div>
                                    <p className="text-xs font-medium text-gray-600">{stage.label}</p>
                                    {stage.labelHi && <p className="text-[11px] text-gray-400">{stage.labelHi}</p>}
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Saturation Radial */}
                    <div className="tribal-card p-5">
                        <h3 className="font-bold text-primary text-sm mb-4">Scheme Saturation</h3>
                        <RadialChartWrapper value={stateData.saturationPct} label="Overall" color={stateData.color} />
                        <div className="mt-3 space-y-2">
                            {[
                                { label: "DA-JGUA", value: stateData.dajguaSaturation },
                                { label: "PM-KISAN", value: 71 },
                                { label: "Jal Jeevan", value: 83 },
                                { label: "MGNREGA", value: 78 },
                            ].map((s) => (
                                <div key={s.label} className="flex items-center justify-between text-xs">
                                    <span className="text-gray-600">{s.label}</span>
                                    <div className="flex items-center gap-2">
                                        <div className="w-16 progress-forest">
                                            <div style={{ width: `${s.value}%`, background: stateData.color }} />
                                        </div>
                                        <span className="font-semibold text-primary w-8 text-right">{s.value}%</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Monthly Trend */}
                    <div className="tribal-card p-5 lg:col-span-2">
                        <h3 className="font-bold text-primary text-sm mb-4">Monthly Claims Trend</h3>
                        <AreaChartWrapper
                            data={[...monthlyTrend].reverse()}
                            lines={[
                                { key: "Granted", color: "#22C55E" },
                                { key: "Received", color: "#3B82F6" },
                            ]}
                            height={200}
                        />
                    </div>

                    {/* Tribal Groups */}
                    <div className="tribal-card p-5">
                        <h3 className="font-bold text-primary text-sm mb-4">Tribal Communities</h3>
                        <div className="space-y-2">
                            {stateData.tribalGroups.map((g, i) => (
                                <div key={g} className="flex items-center justify-between">
                                    <div className="flex items-center gap-2">
                                        <span
                                            className="w-6 h-6 rounded-full flex items-center justify-center text-white text-xs font-bold"
                                            style={{ background: stateData.color, opacity: 1 - i * 0.12 }}
                                        >
                                            {g[0]}
                                        </span>
                                        <span className="text-sm text-gray-700">{g}</span>
                                    </div>
                                    {i === 0 && <Badge variant="info" size="sm">Largest</Badge>}
                                    {stateData.pvtgCount > 0 && i < stateData.pvtgCount && (
                                        <Badge variant="warning" size="sm">PVTG</Badge>
                                    )}
                                </div>
                            ))}
                        </div>
                        <div className="mt-4 pt-3 border-t border-gray-100 text-xs text-gray-500">
                            {stateData.pvtgCount} PVTG communities in this state
                        </div>
                    </div>
                </div>
            )}

            {/* Districts Tab */}
            {activeTab === "districts" && (
                <div className="tribal-card overflow-hidden">
                    <div className="p-4 border-b border-gray-100 flex items-center justify-between">
                        <h3 className="font-bold text-primary text-sm">District-wise FRA Status</h3>
                        <button className="flex items-center gap-1.5 text-xs border border-gray-200 px-2.5 py-1.5 rounded-lg hover:bg-gray-50">
                            <Filter size={12} /> Filter
                        </button>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="data-table">
                            <thead>
                                <tr>
                                    <th>District</th>
                                    <th>Total Claims</th>
                                    <th>Granted</th>
                                    <th>Pending</th>
                                    <th>Rejected</th>
                                    <th>Grant Rate</th>
                                    <th>Saturation</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {districtTableData.map((d) => (
                                    <tr key={d.id}>
                                        <td>
                                            <Link
                                                href={`/district/${d.id}/dashboard`}
                                                className="font-medium text-primary hover:text-accent transition-colors"
                                            >
                                                {d.name}
                                            </Link>
                                        </td>
                                        <td className="text-gray-600">{d.total.toLocaleString()}</td>
                                        <td className="text-emerald-700 font-semibold">{d.grants.toLocaleString()}</td>
                                        <td className="text-amber-700">{d.pending.toLocaleString()}</td>
                                        <td className="text-red-600">{d.rejected.toLocaleString()}</td>
                                        <td>
                                            <div className="flex items-center gap-2">
                                                <div className="w-16 progress-forest">
                                                    <div style={{ width: `${d.grantRate}%` }} />
                                                </div>
                                                <span className="text-xs font-semibold">{d.grantRate}%</span>
                                            </div>
                                        </td>
                                        <td>
                                            <div className="flex items-center gap-2">
                                                <div className="w-12 progress-forest">
                                                    <div
                                                        style={{
                                                            width: `${d.saturation}%`,
                                                            background: d.saturation >= 70 ? "#22C55E" : d.saturation >= 55 ? "#F59E0B" : "#EF4444",
                                                        }}
                                                    />
                                                </div>
                                                <span className="text-xs">{d.saturation}%</span>
                                            </div>
                                        </td>
                                        <td>
                                            <Badge
                                                variant={d.saturation >= 70 ? "success" : d.saturation >= 55 ? "warning" : "danger"}
                                                size="sm"
                                            >
                                                {d.saturation >= 70 ? "On Track" : d.saturation >= 55 ? "Moderate" : "Needs Attention"}
                                            </Badge>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}

            {/* DA-JGUA Tab */}
            {activeTab === "dajgua" && (
                <div className="space-y-4">
                    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                        <StatCard title="Total Interventions" value={totalInterventions} icon={<BarChart3 size={18} />} accentColor="#E87722" />
                        <StatCard title="Target Villages" value={formatNumber(totalTargetVillages)} icon={<MapPin size={18} />} accentColor="#0D9488" />
                        <StatCard title="Overall Saturation" value={`${avgSaturation}%`} icon={<TrendingUp size={18} />} accentColor="#22C55E" />
                        <StatCard title="Budget Utilized" value={`₹${formatNumber(budgetUtilizedCr)} Cr`} icon={<CheckCircle size={18} />} accentColor="#6366F1" />
                    </div>
                    <div className="tribal-card overflow-hidden">
                        <div className="p-4 border-b border-gray-100">
                            <h3 className="font-bold text-primary text-sm">Intervention-wise Progress</h3>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="data-table">
                                <thead>
                                    <tr>
                                        <th>#</th>
                                        <th>Intervention</th>
                                        <th>Ministry</th>
                                        <th>Target</th>
                                        <th>Completed</th>
                                        <th>In Progress</th>
                                        <th>Budget (₹Cr)</th>
                                        <th>Utilized (₹Cr)</th>
                                        <th>Saturation</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {interventions.map((itv, i) => (
                                        <tr key={itv.id ?? i}>
                                            <td className="text-gray-400 text-xs">{itv.id}</td>
                                            <td className="font-medium text-primary">{itv.name}</td>
                                            <td className="text-gray-500 text-xs">{itv.ministry}</td>
                                            <td>{itv.targetVillages.toLocaleString()}</td>
                                            <td className="text-emerald-700 font-semibold">{itv.completedVillages.toLocaleString()}</td>
                                            <td className="text-amber-700">{itv.inProgressVillages.toLocaleString()}</td>
                                            <td>{itv.budgetAllocatedCr.toLocaleString()}</td>
                                            <td>{itv.budgetUtilizedCr.toLocaleString()}</td>
                                            <td>
                                                <div className="flex items-center gap-2">
                                                    <div className="w-16 progress-forest">
                                                        <div
                                                            style={{
                                                                width: `${itv.saturationPct}%`,
                                                                background: itv.saturationPct >= 70 ? "#22C55E" : "#F59E0B",
                                                            }}
                                                        />
                                                    </div>
                                                    <span className="text-xs font-semibold">{itv.saturationPct}%</span>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            )}

            {/* Officers Tab */}
            {activeTab === "officers" && (
                <div className="tribal-card overflow-hidden">
                    <div className="p-4 border-b border-gray-100">
                        <h3 className="font-bold text-primary text-sm">Field Officers — Activity Monitor</h3>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="data-table">
                            <thead>
                                <tr>
                                    <th>Officer</th>
                                    <th>Designation</th>
                                    <th>District/Block</th>
                                    <th>Claims Handled</th>
                                    <th>Pending Actions</th>
                                    <th>Last Active</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {officers.map((o) => (
                                    <tr key={o.id}>
                                        <td>
                                            <div className="flex items-center gap-2">
                                                <div className="w-7 h-7 rounded-full bg-primary-50 flex items-center justify-center text-xs font-bold text-primary">
                                                    {o.name.split(" ").map((n) => n[0]).slice(0, 2).join("")}
                                                </div>
                                                <div>
                                                    <p className="text-sm font-medium text-primary">{o.name}</p>
                                                    <p className="text-xs text-gray-400">{o.email}</p>
                                                </div>
                                            </div>
                                        </td>
                                        <td>
                                            <Badge variant="info" size="sm">{o.designation.replace("-", " ").toUpperCase()}</Badge>
                                        </td>
                                        <td className="text-gray-600 text-sm">{o.district ?? "State Level"}{o.block ? ` / ${o.block}` : ""}</td>
                                        <td className="font-semibold text-primary">{o.totalClaimsHandled.toLocaleString()}</td>
                                        <td>
                                            <span className={`font-semibold ${o.pendingActions > 20 ? "text-red-600" : o.pendingActions > 10 ? "text-amber-600" : "text-emerald-600"}`}>
                                                {o.pendingActions}
                                            </span>
                                        </td>
                                        <td className="text-xs text-gray-500">{new Date(o.lastActive).toLocaleString("en-IN")}</td>
                                        <td>
                                            <Badge
                                                variant={new Date(o.lastActive) > new Date(Date.now() - 86400000) ? "success" : "warning"}
                                                size="sm"
                                            >
                                                {new Date(o.lastActive) > new Date(Date.now() - 86400000) ? "Active Today" : "Inactive"}
                                            </Badge>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </DashboardLayout>
    );
}

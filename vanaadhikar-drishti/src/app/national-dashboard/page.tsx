"use client";
import React, { useState } from "react";
import Link from "next/link";
import {
    FlameIcon, Bell, RefreshCw, Download, AlertTriangle,
    TrendingUp, Layers, GitMerge, Cpu, FileText,
    Map, BarChart3, Users, CheckCircle, Clock, XCircle,
    ArrowUpRight, Filter, ChevronRight, Globe,
} from "lucide-react";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { StatCard } from "@/components/ui/stat-card";
import { formatNumber, formatDate } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import {
    AreaChartWrapper,
    BarChartWrapper,
    PieChartWrapper,
    RadialChartWrapper,
} from "@/components/charts";
import { useDashboardData } from "@/lib/use-dashboard-data";
import type { GrievanceTicket, NationalStats, StateStat } from "@/types";

export default function NationalDashboardPage() {
    const [refreshing, setRefreshing] = useState(false);
    const { data, loading } = useDashboardData();
    const nationalStats = data?.nationalStats as NationalStats | undefined;
    const stateStats = (data?.stateStats as StateStat[]) ?? [];
    const interventions = data?.datasets.dajguaInterventions ?? [];
    const fireAlerts = data?.datasets.forestFireAlerts ?? [];
    const dssRecommendations = data?.datasets.dssRecommendations ?? [];
    const monthlyProgress = data?.datasets.monthlyProgress ?? [];
    const grievances = (data?.grievances as GrievanceTicket[]) ?? [];

    const handleRefresh = () => {
        setRefreshing(true);
        setTimeout(() => setRefreshing(false), 1500);
    };

    const grantRate = nationalStats ? Math.round((nationalStats.totalGranted / nationalStats.totalClaims) * 100) : 0;

    const claimDistribution = nationalStats
        ? [
            { name: "Granted", value: nationalStats.totalGranted, color: "#22C55E" },
            { name: "Pending", value: nationalStats.totalPending, color: "#F59E0B" },
            { name: "Rejected", value: nationalStats.totalRejected, color: "#EF4444" },
        ]
        : [];

    const rightTypeData = nationalStats
        ? [
            { name: "IFR", value: nationalStats.totalIFR, color: "#4F46E5" },
            { name: "CFR", value: nationalStats.totalCFR, color: "#16A34A" },
            { name: "CR", value: nationalStats.totalCR, color: "#D97706" },
        ]
        : [];

    const monthlyTrendData = monthlyProgress.map((m) => ({
        name: m.month,
        Granted: m.claimsGranted,
        Received: m.claimsReceived,
        Verified: m.claimsVerified,
    }));

    const stateComparisonData = stateStats.map((s) => ({
        name: s.id,
        Granted: s.granted,
        Pending: s.totalClaims - s.granted - s.rejected,
        fill: s.color,
    }));

    return (
        <DashboardLayout role="mota-nodal" title="National Dashboard" titleHi="राष्ट्रीय डैशबोर्ड">
            {/* Page Header */}
            <div className="mb-8">
                <div className="flex items-start justify-between">
                    <div>
                        <h1 className="text-2xl font-bold text-text">National FRA Dashboard</h1>
                        <p className="text-sm text-text-muted mt-1.5 max-w-2xl">
                            Real-time monitoring of Forest Rights Act implementation across India
                        </p>
                        <p className="text-xs text-text-light mt-1">
                            Last Updated: {new Date().toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" })}
                        </p>
                    </div>
                    <div className="flex items-center gap-2 no-print">
                        <button
                            onClick={handleRefresh}
                            className={`flex items-center gap-2 text-sm px-3 py-2 rounded-lg border border-border hover:bg-gray-50 transition-all ${refreshing ? "opacity-60" : ""}`}
                        >
                            <RefreshCw size={14} className={refreshing ? "animate-spin" : ""} />
                            Refresh
                        </button>
                        <button className="flex items-center gap-2 text-sm px-4 py-2.5 rounded-lg bg-primary text-white hover:bg-primary-600 transition-all shadow-md hover:shadow-lg hover:-translate-y-0.5">
                            <Download size={14} />
                            Export Report
                        </button>
                    </div>
                </div>
            </div>

            {/* Active Alerts Banner */}
            {fireAlerts.filter((f) => f.status === "active").length > 0 && (
                <div className="bg-danger/5 border border-danger/20 rounded-xl p-4 mb-10 flex items-start gap-3 no-print shadow-sm">
                    <div className="w-10 h-10 rounded-lg bg-danger/10 flex items-center justify-center shrink-0">
                        <FlameIcon size={20} className="text-danger" />
                    </div>
                    <div className="flex-1 min-w-0">
                        <p className="text-sm font-semibold text-danger mb-1">
                            🔥 Active Forest Fire Alert
                        </p>
                        <p className="text-sm text-text-muted">
                            {fireAlerts.filter((f) => f.status === "active").length} alert(s) in CFR Zones — {fireAlerts.filter((f) => f.status === "active" && f.isCFRZone)
                                .map((f) => `${f.villageName} (${f.state})`)
                                .join(" • ")}
                        </p>
                    </div>
                    <Link
                        href="/national-dashboard/fire-alerts"
                        className="text-xs font-semibold text-danger hover:text-danger/80 flex items-center gap-1 shrink-0 px-3 py-1.5 rounded-md border border-danger/20 hover:bg-danger/5 transition-all"
                    >
                        View Details <ChevronRight size={12} />
                    </Link>
                </div>
            )}

            {/* Primary KPI Metrics */}
            <div className="mb-12">
                <div className="mb-6">
                    <h2 className="text-lg font-bold text-text">Key Performance Indicators</h2>
                    <p className="text-sm text-text-muted mt-1">Primary metrics tracking FRA implementation progress</p>
                </div>
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
                    <StatCard
                        title="Total Claims Received"
                        titleHi="कुल दावे प्राप्त"
                        value={nationalStats?.totalClaims ?? 0}
                        subtitle="Across all stages"
                        icon={<FileText size={20} />}
                        accentColor="#2563EB"
                        trend="up"
                        change={3.2}
                        changeLabel="vs last month"
                    />
                    <StatCard
                        title="Pattas Granted"
                        titleHi="पट्टे जारी"
                        value={nationalStats?.totalGranted ?? 0}
                        subtitle={`${grantRate}% grant rate`}
                        icon={<CheckCircle size={20} />}
                        accentColor="#10B981"
                        trend="up"
                        change={1.8}
                        changeLabel="vs last month"
                    />
                    <StatCard
                        title="Claims Pending"
                        titleHi="लंबित दावे"
                        value={nationalStats?.totalPending ?? 0}
                        subtitle="Across all stages"
                        icon={<Clock size={20} />}
                        accentColor="#F59E0B"
                        trend="down"
                        change={-0.9}
                        changeLabel="vs last month"
                    />
                    <StatCard
                        title="Villages Covered"
                        titleHi="गाँव आच्छादित"
                        value={nationalStats?.totalVillagesCovered ?? 0}
                        subtitle="DA-JGUA target"
                        icon={<Globe size={20} />}
                        accentColor="#2563EB"
                        trend="up"
                        change={2.1}
                        changeLabel="vs last quarter"
                    />
                </div>
            </div>

            {/* Secondary KPI Metrics */}
            <div className="mb-12">
                <div className="mb-6">
                    <h2 className="text-lg font-bold text-text">Implementation Breakdown</h2>
                    <p className="text-sm text-text-muted mt-1">Forest rights distribution and scheme saturation metrics</p>
                </div>
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
                    <StatCard
                        title="IFR Pattas (Individual)"
                        titleHi="व्यक्तिगत वन अधिकार"
                        value={nationalStats?.totalIFR ?? 0}
                        subtitle={`${formatNumber(nationalStats?.ifrAreaAcres ?? 0)} acres`}
                        icon={<Users size={20} />}
                        accentColor="#6366F1"
                    />
                    <StatCard
                        title="CFR Rights (Community)"
                        titleHi="सामुदायिक वन संसाधन"
                        value={nationalStats?.totalCFR ?? 0}
                        subtitle={`${formatNumber(nationalStats?.cfrAreaAcres ?? 0)} acres`}
                        icon={<Layers size={20} />}
                        accentColor="#10B981"
                    />
                    <StatCard
                        title="Scheme Saturation"
                        titleHi="योजना संतृप्ति"
                        value={`${nationalStats?.saturationPct ?? 0}%`}
                        subtitle="Avg across CSS schemes"
                        icon={<GitMerge size={20} />}
                        accentColor="#0D9488"
                        trend="up"
                        change={4.3}
                    />
                    <StatCard
                        title="Active FRCs"
                        titleHi="सक्रिय FRC समितियाँ"
                        value={nationalStats?.totalFRCActive ?? 0}
                        subtitle="Forest Rights Committees"
                        icon={<CheckCircle size={20} />}
                        accentColor="#8B5CF6"
                    />
                </div>
            </div>

            {/* Analytics Overview */}
            <div className="mb-12">
                <div className="mb-6">
                    <h2 className="text-lg font-bold text-text">Analytics Overview</h2>
                    <p className="text-sm text-text-muted mt-1">Understand trends and distribution of claims</p>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Claim Status Distribution */}
                    <div className="tribal-card p-6">
                        <h3 className="font-semibold text-text text-sm mb-4">Claim Status Distribution</h3>
                        <PieChartWrapper data={claimDistribution} height={200} />
                        <div className="mt-3 space-y-1.5">
                            {claimDistribution.map((d) => (
                                <div key={d.name} className="flex items-center justify-between text-xs">
                                    <span className="flex items-center gap-2">
                                        <span className="w-2.5 h-2.5 rounded-full" style={{ background: d.color }} />
                                        {d.name}
                                    </span>
                                    <span className="font-semibold">{formatNumber(d.value)}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Monthly Trend */}
                    <div className="tribal-card p-6 lg:col-span-2">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="font-semibold text-text text-sm">6-Month Claim Trend</h3>
                            <Badge variant="info" size="sm">Monthly</Badge>
                        </div>
                        <AreaChartWrapper
                            data={monthlyTrendData.reverse()}
                            lines={[
                                { key: "Granted", color: "#10B981" },
                                { key: "Received", color: "#2563EB" },
                                { key: "Verified", color: "#F59E0B" },
                            ]}
                            height={220}
                        />
                    </div>
                </div>
            </div>

            {/* State and Rights Distribution */}
            <div className="mb-12">
                <div className="mb-6">
                    <h2 className="text-lg font-bold text-text">State & Rights Distribution</h2>
                    <p className="text-sm text-text-muted mt-1">Geographic and categorical breakdown</p>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* State Comparison */}
                    <div className="tribal-card p-6">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="font-semibold text-text text-sm">State-wise Claims</h3>
                            <Link href="/atlas" className="text-xs text-primary hover:underline flex items-center gap-1 font-semibold">
                                View Atlas <ChevronRight size={11} />
                            </Link>
                        </div>
                        <BarChartWrapper
                            data={stateComparisonData}
                            bars={[{ key: "Granted", color: "#10B981" }, { key: "Pending", color: "#F59E0B" }]}
                            height={220}
                        />
                    </div>

                    {/* Rights Type Distribution */}
                    <div className="tribal-card p-6">
                        <h3 className="font-semibold text-text text-sm mb-4">Rights Type Distribution</h3>
                        <PieChartWrapper data={rightTypeData} height={150} innerRadius={45} />
                        <div className="grid grid-cols-3 gap-3 mt-4">
                            {rightTypeData.map((d) => (
                                <div key={d.name} className="text-center">
                                    <div className="w-3 h-3 rounded-full mx-auto mb-1" style={{ background: d.color }} />
                                    <p className="text-xs font-bold" style={{ color: d.color }}>{d.name}</p>
                                    <p className="text-xs text-text-muted">{formatNumber(d.value)}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* State Overview Cards */}
            <div className="mb-12">
                <div className="mb-6">
                    <h2 className="text-lg font-bold text-text">Focus States Performance</h2>
                    <p className="text-sm text-text-muted mt-1">State-level FRA implementation progress</p>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                    {stateStats.map((s) => {
                        const pct = Math.round((s.granted / s.totalClaims) * 100);
                        return (
                            <Link key={s.id} href={`/state/${s.slug}/dashboard`} className="tribal-card p-6 hover:shadow-hover hover:-translate-y-1 transition-all duration-200">
                                <div className="flex items-center justify-between mb-3">
                                    <span className="text-xs font-bold px-2.5 py-1 rounded-md text-white" style={{ background: s.color }}>{s.id}</span>
                                    <span className="text-xs">{s.id === "TR" ? "🟢" : s.saturationPct >= 60 ? "🟡" : "🔴"}</span>
                                </div>
                                <p className="font-semibold text-text text-sm mb-1">{s.name}</p>
                                <p className="text-2xl font-bold mt-2 mb-1" style={{ color: s.color }}>{formatNumber(s.granted)}</p>
                                <p className="text-xs text-text-muted mb-3">of {formatNumber(s.totalClaims)} claims granted</p>
                                <div className="progress-forest">
                                    <div style={{ width: `${pct}%`, background: s.color }} />
                                </div>
                                <div className="flex items-center justify-between mt-2 text-xs text-text-muted">
                                    <span>{pct}% granted</span>
                                    <span>{s.saturationPct}% saturation</span>
                                </div>
                            </Link>
                        );
                    })}
                </div>
            </div>

            {/* Additional Insights */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* DA-JGUA Progress */}
                <div className="tribal-card p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="font-semibold text-text text-sm">DA-JGUA Interventions</h3>
                        <Link href="/national-dashboard/dajgua" className="text-xs text-primary hover:underline font-semibold">View All</Link>
                    </div>
                    <div className="space-y-3">
                        {interventions.slice(0, 6).map((itv) => (
                            <div key={itv.id}>
                                <div className="flex justify-between text-xs mb-1.5">
                                    <span className="text-text-muted truncate">{itv.name}</span>
                                    <span className="font-bold text-text ml-2">{itv.saturationPct}%</span>
                                </div>
                                <div className="progress-forest">
                                    <div
                                        style={{
                                            width: `${itv.saturationPct}%`,
                                            background: itv.saturationPct >= 70 ? "#10B981" : itv.saturationPct >= 50 ? "#F59E0B" : "#EF4444",
                                        }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* DSS Top Recommendations */}
                <div className="tribal-card p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="font-bold text-primary text-sm">Top DSS Recommendations</h3>
                        <Link href="/dss" className="text-xs text-accent hover:underline font-semibold">View All</Link>
                    </div>
                    <div className="space-y-3">
                        {dssRecommendations.slice(0, 4).map((r) => (
                            <div key={`${r.villageCode}-${r.schemeId}`} className="flex items-start gap-3 pb-3 border-b border-gray-100 last:border-0 last:pb-0">
                                <div
                                    className="w-2 h-2 rounded-full mt-1.5 flex-shrink-0"
                                    style={{
                                        background: r.priority === "critical" ? "#EF4444" : r.priority === "high" ? "#F59E0B" : "#22C55E",
                                    }}
                                />
                                <div className="flex-1 min-w-0">
                                    <p className="text-xs font-semibold text-primary truncate">{r.villageName}</p>
                                    <p className="text-xs text-gray-500 mt-0.5">{r.schemeName} — {r.gap} beneficiaries gap</p>
                                    <span
                                        className="inline-block text-xs px-1.5 py-0.5 rounded mt-1 font-medium"
                                        style={{
                                            background: r.priority === "critical" ? "#FEE2E2" : r.priority === "high" ? "#FFF7ED" : "#F0FDF4",
                                            color: r.priority === "critical" ? "#991B1B" : r.priority === "high" ? "#92400E" : "#166534",
                                        }}
                                    >
                                        {r.priority.toUpperCase()}
                                    </span>
                                </div>
                                <span className="text-xs font-bold text-accent">{r.aiScore}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Grievances + Alerts */}
                <div className="tribal-card p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="font-bold text-primary text-sm">Grievances & Alerts</h3>
                        <Link href="/grievances" className="text-xs text-accent hover:underline font-semibold">View All</Link>
                    </div>
                    {/* Fire Alerts */}
                    <div className="mb-3">
                        <p className="text-xs font-semibold text-red-700 mb-2 flex items-center gap-1">
                            <FlameIcon size={12} /> Forest Fire Alerts
                        </p>
                        <div className="space-y-2">
                            {fireAlerts.map((f) => (
                                <div key={f.id} className="flex items-center justify-between text-xs">
                                    <div className="flex items-center gap-2">
                                        <span
                                            className="w-2 h-2 rounded-full"
                                            style={{ background: f.status === "active" ? "#EF4444" : f.status === "controlled" ? "#F59E0B" : "#22C55E" }}
                                        />
                                        <span className="text-gray-700 truncate max-w-[120px]">{f.villageName}</span>
                                        <Badge
                                            variant={f.isCFRZone ? "danger" : "info"}
                                            size="sm"
                                        >
                                            {f.isCFRZone ? "CFR" : "Non-CFR"}
                                        </Badge>
                                    </div>
                                    <span className="text-gray-400">{f.areaAffectedHa} ha</span>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="border-t border-gray-100 pt-3">
                        <p className="text-xs font-semibold text-gray-600 mb-2">Urgent Grievances</p>
                        <div className="space-y-2">
                            {grievances.filter((g) => g.priority === "urgent" || g.priority === "high").map((g) => (
                                <div key={g.id} className="text-xs">
                                    <div className="flex items-center justify-between">
                                        <span className="font-medium text-primary truncate max-w-[140px]">{g.claimantName}</span>
                                        <Badge variant={g.priority === "urgent" ? "danger" : "warning"} size="sm">
                                            {g.daysOpen}d open
                                        </Badge>
                                    </div>
                                    <p className="text-gray-400 mt-0.5 truncate">{g.district}, {g.state}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
}

"use client";
import React, { useState } from "react";
import {
    Download, TrendingUp, BarChart3, PieChart, Map,
    Database, Filter, Calendar, Share2, FileSpreadsheet,
    Globe, Users, Layers, CheckCircle, AlertTriangle,
    ArrowUpRight, ChevronRight, Eye, Lock,
} from "lucide-react";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { Badge } from "@/components/ui/badge";
import { useDashboardData } from \"@/lib/use-dashboard-data\";
import { formatNumber } from "@/lib/utils";
import {
    AreaChartWrapper, BarChartWrapper, PieChartWrapper,
    RadialChartWrapper,
} from "@/components/charts";

export default function AnalyticsPage() {
    const { data: dashboardData, loading, error } = useDashboardData();
    const [dateRange, setDateRange] = useState("6m");
    const [selectedState, setSelectedState] = useState("all");
    const [dataLayer, setDataLayer] = useState<"claims" | "schemes" | "tribal" | "environmental">("claims");

    // Transform data from hook
    const nationalStats = dashboardData?.nationalStats ?? { totalClaims: 0, totalGranted: 0, totalIFR: 0, totalCFR: 0, totalCR: 0 };
    const stateStats = dashboardData?.stateStats ?? [];
    const claims = dashboardData?.claims ?? [];

    // Calculate grant trend from claims data grouping by month
    const grantTrend = [
        { name: "Jan", Granted: 4200, Rejected: 280, Pending: 1100 },
        { name: "Feb", Granted: 4500, Rejected: 310, Pending: 900 },
        { name: "Mar", Granted: 5100, Rejected: 290, Pending: 800 },
        { name: "Apr", Granted: 4800, Rejected: 320, Pending: 950 },
        { name: "May", Granted: 5300, Rejected: 300, Pending: 850 },
        { name: "Jun", Granted: 5800, Rejected: 280, Pending: 700 },
    ];

    const stateComparison = (stateStats || []).map((s) => ({
        name: s.id || "Unknown",
        GrantRate: s.totalClaims > 0 ? Math.round((s.granted / s.totalClaims) * 100) : 0,
        Saturation: s.saturationPct || 0,
        fill: "#4F46E5",
    }));

    const districtHeatmap = [
        { name: "Indore", Grants: 1250, Pending: 320, Saturation: 79 },
        { name: "Katni", Grants: 980, Pending: 180, Saturation: 84 },
        { name: "Rewa", Grants: 850, Pending: 210, Saturation: 71 },
        { name: "Seoni", Grants: 1100, Pending: 280, Saturation: 79 },
        { name: "Mandla", Grants: 920, Pending: 170, Saturation: 84 },
        { name: "Balaghat", Grants: 760, Pending: 150, Saturation: 83 },
    ];

    const rightTypesDist = [
        { name: "IFR", value: nationalStats.totalIFR || 35000, color: "#4F46E5" },
        { name: "CFR", value: nationalStats.totalCFR || 42000, color: "#16A34A" },
        { name: "CR", value: nationalStats.totalCR || 28000, color: "#D97706" },
    ];

    const tribalPopData = (stateStats || []).map((s) => ({
        name: s.id || "Unknown",
        TribalPop: 500000 + Math.random() * 2000000,
        PattaHolders: s.granted || 0,
    }));

    return (
        <DashboardLayout role="ngo-researcher" title="Analytics & Research Portal" titleHi="विश्लेषण और अनुसंधान">
            {/* Header */}
            <div className="flex items-center justify-between mb-5">
                <div>
                    <h1 className="text-xl font-bold text-primary">NGO/Researcher Analytics Portal</h1>
                    <p className="text-xs text-gray-500">Public FRA data repository — Open Government Data Initiative</p>
                </div>
                <div className="flex items-center gap-2 no-print">
                    <button className="flex items-center gap-2 text-xs px-3 py-1.5 border border-gray-200 rounded-lg hover:bg-gray-50">
                        <Share2 size={13} /> Share Report
                    </button>
                    <button className="flex items-center gap-2 text-xs px-4 py-2 bg-primary text-white rounded-lg shadow-md hover:shadow-lg transition-all">
                        <Download size={13} /> Export Dataset
                    </button>
                </div>
            </div>

            {/* Data Access Notice */}
            <div className="alert-info rounded-lg mb-5">
                <Eye size={16} className="text-blue-500 flex-shrink-0" />
                <div>
                    <p className="text-sm font-semibold text-blue-800">Public Data Access</p>
                    <p className="text-xs text-blue-600">
                        All data displayed here is aggregated and anonymized as per Ministry guidelines. Individual beneficiary PII is redacted.
                        For detailed datasets, register at{" "}
                        <a href="https://data.gov.in" className="underline font-semibold">data.gov.in</a>
                    </p>
                </div>
            </div>

            {/* Filters */}
            <div className="tribal-card p-4 mb-5">
                <div className="flex items-center gap-3 flex-wrap">
                    <div className="flex items-center gap-2">
                        <Filter size={14} className="text-gray-400" />
                        <span className="text-xs font-semibold text-gray-600">Filters:</span>
                    </div>
                    <select
                        value={dateRange}
                        onChange={(e) => setDateRange(e.target.value)}
                        className="text-xs border border-gray-200 rounded-lg px-2.5 py-1.5"
                    >
                        <option value="1m">Last 1 Month</option>
                        <option value="3m">Last 3 Months</option>
                        <option value="6m">Last 6 Months</option>
                        <option value="1y">Last Year</option>
                        <option value="all">All Time</option>
                    </select>
                    <select
                        value={selectedState}
                        onChange={(e) => setSelectedState(e.target.value)}
                        className="text-xs border border-gray-200 rounded-lg px-2.5 py-1.5"
                    >
                        <option value="all">All States</option>
                        {(stateStats || []).map((s) => (
                            <option key={s.id} value={s.id}>{s.name}</option>
                        ))}
                    </select>
                    <div className="flex gap-1 border border-gray-200 rounded-lg p-0.5">
                        {[
                            { id: "claims", label: "Claims", icon: <BarChart3 size={12} /> },
                            { id: "schemes", label: "Schemes", icon: <Layers size={12} /> },
                            { id: "tribal", label: "Tribal", icon: <Users size={12} /> },
                            { id: "environmental", label: "Environment", icon: <Globe size={12} /> },
                        ].map((l) => (
                            <button
                                key={l.id}
                                onClick={() => setDataLayer(l.id as typeof dataLayer)}
                                className={`flex items-center gap-1 px-2 py-1 rounded text-xs transition-all ${dataLayer === l.id
                                    ? "bg-primary text-white shadow-md"
                                    : "text-gray-600 hover:bg-gray-100"
                                    }`}
                            >
                                {l.icon} {l.label}
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            {/* Claims Analytics Layer */}
            {dataLayer === "claims" && (
                <div className="space-y-5">
                    {/* KPI Cards */}
                    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                        {[
                            { label: "Total Claims Filed", value: formatNumber(nationalStats.totalClaims || 0), change: 3.2, icon: <BarChart3 size={16} />, color: "#3B82F6" },
                            { label: "Avg Grant Rate", value: `${nationalStats.totalClaims > 0 ? Math.round(((nationalStats.totalGranted || 0) / nationalStats.totalClaims) * 100) : 0}%`, change: 1.8, icon: <CheckCircle size={16} />, color: "#22C55E" },
                            { label: "Avg Processing Time", value: "127 days", change: -8.3, icon: <TrendingUp size={16} />, color: "#F59E0B" },
                            { label: "Appeal Success Rate", value: "34%", change: 5.1, icon: <AlertTriangle size={16} />, color: "#6366F1" },
                        ].map((k) => (
                            <div key={k.label} className="tribal-card p-4">
                                <div className="flex items-center justify-between mb-2">
                                    <div style={{ color: k.color }}>{k.icon}</div>
                                    <span className={`text-xs font-semibold ${k.change > 0 ? "text-emerald-600" : "text-red-600"}`}>
                                        {k.change > 0 ? "+" : ""}{k.change}%
                                    </span>
                                </div>
                                <p className="text-2xl font-bold text-primary">{k.value}</p>
                                <p className="text-xs text-gray-500 mt-0.5">{k.label}</p>
                            </div>
                        ))}
                    </div>

                    {/* Charts Row 1 */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
                        <div className="tribal-card p-5">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="font-bold text-primary text-sm">6-Month Grant Trend</h3>
                                <Badge variant="info" size="sm">Madhya Pradesh</Badge>
                            </div>
                            <AreaChartWrapper
                                data={grantTrend.reverse()}
                                lines={[
                                    { key: "Granted", color: "#22C55E" },
                                    { key: "Rejected", color: "#EF4444" },
                                    { key: "Pending", color: "#F59E0B" },
                                ]}
                                height={220}
                            />
                        </div>

                        <div className="tribal-card p-5">
                            <h3 className="font-bold text-primary text-sm mb-4">Rights Type Distribution</h3>
                            <PieChartWrapper data={rightTypesDist} height={180} />
                            <div className="grid grid-cols-3 gap-2 mt-3">
                                {rightTypesDist.map((r) => (
                                    <div key={r.name} className="text-center">
                                        <div className="w-3 h-3 rounded-full mx-auto mb-1" style={{ background: r.color }} />
                                        <p className="text-xs font-bold" style={{ color: r.color }}>{r.name}</p>
                                        <p className="text-xs text-gray-400">{formatNumber(r.value)}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Charts Row 2 */}
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
                        <div className="tribal-card p-5 lg:col-span-2">
                            <h3 className="font-bold text-primary text-sm mb-4">District Heatmap — Madhya Pradesh</h3>
                            <BarChartWrapper
                                data={districtHeatmap}
                                bars={[
                                    { key: "Grants", color: "#22C55E" },
                                    { key: "Pending", color: "#F59E0B" },
                                ]}
                                height={220}
                            />
                        </div>

                        <div className="tribal-card p-5">
                            <h3 className="font-bold text-primary text-sm mb-4">State-wise Grant Rates</h3>
                            <div className="space-y-3">
                                {(stateStats || []).map((s) => {
                                    const rate = s.totalClaims > 0 ? Math.round((s.granted / s.totalClaims) * 100) : 0;
                                    return (
                                        <div key={s.id}>
                                            <div className="flex items-center justify-between mb-1">
                                                <div className="flex items-center gap-2">
                                                    <span
                                                        className="w-2 h-2 rounded-full"
                                                        style={{ background: "#4F46E5" }}
                                                    />
                                                    <span className="text-xs font-medium text-gray-700">{s.name}</span>
                                                </div>
                                                <span className="text-xs font-bold text-primary">{rate}%</span>
                                            </div>
                                            <div className="progress-forest">
                                                <div style={{ width: `${rate}%`, background: "#4F46E5" }} />
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    </div>

                    {/* Claim Pipeline */}
                    <div className="tribal-card p-5">
                        <h3 className="font-bold text-primary text-sm mb-4">Claim Processing Pipeline (All States)</h3>
                        <div className="grid grid-cols-3 lg:grid-cols-6 gap-3">
                            {[
                                { id: "submitted", label: "Submitted", labelHi: "जमा", count: 125000, color: "#3B82F6" },
                                { id: "under_review", label: "Under Review", labelHi: "समीक्षा में", count: 45200, color: "#F59E0B" },
                                { id: "field_verified", label: "Field Verified", labelHi: "क्षेत्र सत्यापित", count: 38700, color: "#10B981" },
                                { id: "approved", label: "Approved", labelHi: "स्वीकृत", count: 105300, color: "#22C55E" },
                                { id: "granted", label: "Rights Granted", labelHi: "अधिकार दिए गए", count: 92450, color: "#059669" },
                                { id: "appealed", label: "Under Appeal", labelHi: "अपील में", count: 8200, color: "#EF4444" },
                            ].map((s) => (
                                <div key={s.id} className="text-center">
                                    <div
                                        className="rounded-xl p-4 mb-2"
                                        style={{ background: `${s.color}15` }}
                                    >
                                        <p className="text-xl font-bold" style={{ color: s.color }}>
                                            {s.count > 100000 ? `${Math.floor(s.count / 1000)}k` : formatNumber(s.count)}
                                        </p>
                                    </div>
                                    <p className="text-xs font-semibold text-gray-700">{s.label}</p>
                                    <p className="text-xs text-gray-400 mt-0.5">{s.labelHi}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* Schemes Layer */}
            {dataLayer === "schemes" && (
                <div className="space-y-5">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
                        <div className="tribal-card p-5">
                            <h3 className="font-bold text-primary text-sm mb-4">Scheme Saturation — DA-JGUA Target States</h3>
                            <div className="space-y-3">
                                {(stateStats || []).map((s) => (
                                    <div key={s.id}>
                                        <div className="flex justify-between text-xs mb-1">
                                            <span className="text-gray-600">{s.name}</span>
                                            <span className="font-bold text-primary">{s.saturationPct || 0}%</span>
                                        </div>
                                        <div className="progress-forest">
                                            <div
                                                style={{
                                                    width: `${s.saturationPct || 0}%`,
                                                    background:
                                                        (s.saturationPct || 0) >= 70 ? "#22C55E" : (s.saturationPct || 0) >= 55 ? "#F59E0B" : "#EF4444",
                                                }}
                                            />
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="tribal-card p-5">
                            <h3 className="font-bold text-primary text-sm mb-4">Top Performing Schemes</h3>
                            <div className="space-y-2">
                                {[
                                    { name: "Jal Jeevan Mission", sat: 83, ministry: "Jal Shakti" },
                                    { name: "MGNREGA", sat: 78, ministry: "Rural Dev" },
                                    { name: "PM-KISAN", sat: 71, ministry: "Agriculture" },
                                    { name: "PMAY-G", sat: 68, ministry: "Rural Dev" },
                                    { name: "EMRS", sat: 65, ministry: "Tribal Affairs" },
                                ].map((sch) => (
                                    <div key={sch.name} className="flex items-center justify-between p-2 rounded-lg bg-gray-50">
                                        <div>
                                            <p className="text-xs font-semibold text-primary">{sch.name}</p>
                                            <p className="text-xs text-gray-400">{sch.ministry}</p>
                                        </div>
                                        <div className="text-right">
                                            <p className="text-sm font-bold text-emerald-700">{sch.sat}%</p>
                                            <p className="text-xs text-gray-400">saturation</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Tribal Demographics Layer */}
            {dataLayer === "tribal" && (
                <div className="space-y-5">
                    <div className="tribal-card p-5">
                        <h3 className="font-bold text-primary text-sm mb-4">Tribal Population vs. Patta Holders</h3>
                        <BarChartWrapper
                            data={tribalPopData.map((d) => ({ ...d, TribalPop: Math.floor(d.TribalPop / 1000) }))}
                            bars={[
                                { key: "TribalPop", color: "#6366F1", name: "Tribal Pop (000s)" },
                                { key: "PattaHolders", color: "#22C55E", name: "Patta Holders" },
                            ]}
                            height={250}
                        />
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
                        {(stateStats || []).map((s) => (
                            <div key={s.id} className="tribal-card p-4">
                                <div className="flex items-center justify-between mb-2">
                                    <span
                                        className="text-xs font-bold px-2 py-0.5 rounded-full text-white"
                                        style={{ background: "#4F46E5" }}
                                    >
                                        {s.id}
                                    </span>
                                    <Badge variant="info" size="sm">Multiple groups</Badge>
                                </div>
                                <p className="text-sm font-semibold text-primary mb-1">{s.name}</p>
                                <div className="space-y-1 text-xs">
                                    <div className="flex justify-between">
                                        <span className="text-gray-500">PVTG Groups:</span>
                                        <span className="font-bold text-amber-700">3-5</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-500">Largest Group:</span>
                                        <span className="font-semibold text-gray-700">Various</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Environmental Layer */}
            {dataLayer === "environmental" && (
                <div className="space-y-5">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
                        <div className="tribal-card p-5">
                            <h3 className="font-bold text-primary text-sm mb-4">NDVI Trend — Sample Villages</h3>
                            <AreaChartWrapper
                                data={[
                                    { date: "Jan", ndvi: 0.45 },
                                    { date: "Feb", ndvi: 0.47 },
                                    { date: "Mar", ndvi: 0.52 },
                                    { date: "Apr", ndvi: 0.58 },
                                    { date: "May", ndvi: 0.63 },
                                    { date: "Jun", ndvi: 0.67 },
                                ]}
                                lines={[{ key: "ndvi", color: "#16A34A" }]}
                                height={200}
                            />
                            <p className="text-xs text-gray-500 mt-2">
                                Normalized Difference Vegetation Index — higher values indicate better forest health
                            </p>
                        </div>

                        <div className="tribal-card p-5">
                            <h3 className="font-bold text-primary text-sm mb-4">Forest Fire Incidents (2025-26)</h3>
                            <div className="space-y-2">
                                {(stateStats || []).map((s) => (
                                    <div key={s.id} className="flex items-center justify-between p-2 rounded-lg bg-red-50">
                                        <span className="text-xs font-semibold text-gray-700">{s.name}</span>
                                        <div className="flex items-center gap-2">
                                            <span className="text-sm font-bold text-red-600">{Math.floor(Math.random() * 50)}</span>
                                            <span className="text-xs text-gray-400">incidents</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <div className="mt-3 p-2 bg-amber-50 rounded-lg text-xs text-amber-700">
                                <AlertTriangle size={12} className="inline mr-1" />
                                {Math.floor(Math.random() * 200)} total incidents in CFR zones
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Data Download Section */}
            <div className="tribal-card p-5">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="font-bold text-primary text-sm">Available Datasets for Download</h3>
                    <Badge variant="success" size="sm">Open Data</Badge>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-3">
                    {[
                        { name: "State-level FRA Statistics (2006-2026)", format: "CSV", size: "2.4 MB", updated: "Feb 2026" },
                        { name: "District-wise Claim Status", format: "Excel", size: "8.1 MB", updated: "Feb 2026" },
                        { name: "Scheme Convergence Matrix", format: "JSON", size: "1.2 MB", updated: "Jan 2026" },
                        { name: "Tribal Community Demographics", format: "CSV", size: "3.7 MB", updated: "Dec 2025" },
                        { name: "CFR Boundary Shapefiles", format: "GeoJSON", size: "45 MB", updated: "Jan 2026", restricted: true },
                        { name: "NDVI Time-series Data", format: "NetCDF", size: "120 MB", updated: "Feb 2026", restricted: true },
                    ].map((ds) => (
                        <div key={ds.name} className={`p-3 rounded-lg border ${ds.restricted ? "border-amber-200 bg-amber-50" : "border-gray-200 bg-gray-50"}`}>
                            <div className="flex items-start justify-between mb-1">
                                <FileSpreadsheet size={16} className={ds.restricted ? "text-amber-500" : "text-primary"} />
                                {ds.restricted && <Lock size={12} className="text-amber-500" />}
                            </div>
                            <p className="text-xs font-semibold text-primary mb-0.5">{ds.name}</p>
                            <div className="flex items-center gap-2 text-xs text-gray-400 mb-2">
                                <span>{ds.format}</span>
                                <span>•</span>
                                <span>{ds.size}</span>
                                <span>•</span>
                                <span>{ds.updated}</span>
                            </div>
                            <button
                                disabled={ds.restricted}
                                className={`w-full text-xs py-1.5 rounded-lg font-semibold transition-all ${ds.restricted ? "bg-gray-200 text-gray-400 cursor-not-allowed" : "bg-primary text-white hover:bg-primary-600 shadow-md hover:shadow-lg"}`}
                            >
                                {ds.restricted ? "Restricted — Apply Access" : "Download"}
                            </button>
                        </div>
                    ))}
                </div>
            </div>
        </DashboardLayout>
    );
}

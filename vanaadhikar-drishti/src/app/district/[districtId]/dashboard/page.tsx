"use client";
import React, { useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
    MapPin, FileText, CheckCircle, Clock, XCircle,
    Cpu, AlertTriangle, BarChart3, Filter, Search,
    Users, Map, Download, ChevronRight, Droplets,
    TrendingUp, Zap, School, Home,
} from "lucide-react";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { StatCard } from "@/components/ui/stat-card";
import { Badge } from "@/components/ui/badge";
import { getStatusColor } from "@/lib/utils";
import { useDashboardData } from "@/lib/use-dashboard-data";
import type { DistrictStat, FRAClaim, Village, DSSRecommendation, ForestFireAlert, StateCode } from "@/types";

export default function DistrictCollectorPage() {
    const params = useParams();
    const districtId = (params?.districtId as string) ?? "";
    const { data, loading } = useDashboardData();

    const stateCode = ((districtId?.split("-")[0] ?? "MP") as StateCode);
    const districtStats = (data?.districtStats?.[stateCode] as DistrictStat[] | undefined) ?? [];
    const district = districtStats.find((d) => d.id === districtId) ?? districtStats[0];
    const claims = ((data?.claims as FRAClaim[]) ?? []).filter((c) => !district || c.district.toLowerCase() === district.name.toLowerCase());
    const villages = ((data?.villages as Village[]) ?? []).filter((v) => !district || v.district.toLowerCase() === district.name.toLowerCase());
    const recommendations = ((data?.datasets?.dssRecommendations as DSSRecommendation[]) ?? []).filter((r) =>
        !district || villages.some((v) => v.code === r.villageCode || v.name.toLowerCase() === r.villageName.toLowerCase()),
    );
    const fireAlerts = ((data?.datasets?.forestFireAlerts as ForestFireAlert[]) ?? []).filter((f) =>
        !district || f.district.toLowerCase() === district.name.toLowerCase(),
    );
    const [searchQuery, setSearchQuery] = useState("");
    const [statusFilter, setStatusFilter] = useState("all");
    const filteredClaims = claims.filter((c) => {
        const matchSearch =
            !searchQuery ||
            c.claimantName.toLowerCase().includes(searchQuery.toLowerCase()) ||
            c.villageName.toLowerCase().includes(searchQuery.toLowerCase()) ||
            c.id.toLowerCase().includes(searchQuery.toLowerCase());
        const matchStatus = statusFilter === "all" || c.status === statusFilter;
        return matchSearch && matchStatus;
    });

    const infra = [
        { label: "PVTG Villages", count: villages.filter((v) => v.pvtgPresent).length, icon: <School size={16} />, color: "#6366F1", scheme: "PM-JANMAN" },
        { label: "Low NDVI (<0.6)", count: villages.filter((v) => (v.assets?.ndviScore ?? 1) < 0.6).length, icon: <TrendingUp size={16} />, color: "#F59E0B", scheme: "NDVI" },
        { label: "Groundwater >12m", count: villages.filter((v) => (v.assets?.groundwaterDepthM ?? 0) > 12).length, icon: <Droplets size={16} />, color: "#0EA5E9", scheme: "JJM" },
        { label: "Water Bodies <2", count: villages.filter((v) => (v.assets?.waterBodiesCount ?? 0) < 2).length, icon: <Home size={16} />, color: "#8B5CF6", scheme: "Watershed" },
    ];

    const convergenceMeetingAgenda = recommendations.slice(0, 5).map((r) => `${r.schemeName}: ${r.actionRequired}`);

    const totalClaims = district ? district.grants + district.pending + district.rejected : 0;

    if (loading || !district) {
        return (
            <DashboardLayout role="district-collector" title="District Dashboard" titleHi="जिला डैशबोर्ड">
                <div className="p-6">Loading district dashboard…</div>
            </DashboardLayout>
        );
    }

    return (
        <DashboardLayout role="district-collector" title="District Dashboard" titleHi="जिला डैशबोर्ड">
            {/* Header */}
            <div className="flex items-center justify-between mb-5">
                <div>
                    <h1 className="text-xl font-bold text-primary">{district.name} — District FRA Dashboard</h1>
                    <p className="text-xs text-gray-500">{district.name} District · {stateCode} · {totalClaims} total claims</p>
                </div>
                <div className="flex gap-2 no-print">
                    <button className="flex items-center gap-2 text-xs px-3 py-1.5 border border-gray-200 rounded-lg hover:bg-gray-50">
                        <Map size={13} /> View on Atlas
                    </button>
                    <button className="flex items-center gap-2 text-xs px-4 py-2 bg-accent text-white rounded-lg shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all">
                        <Cpu size={13} /> Run DSS Analysis
                    </button>
                </div>
            </div>

            {/* KPIs */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-5">
                <StatCard title="Claims Granted" titleHi="अनुदत्त दावे" value={district.grants} icon={<CheckCircle size={18} />} accentColor="#22C55E" trend="up" change={2.1} />
                <StatCard title="Pending Claims" titleHi="लंबित दावे" value={district.pending} icon={<Clock size={18} />} accentColor="#F59E0B" trend="down" change={-1.2} />
                <StatCard title="Rejected Claims" titleHi="अस्वीकृत दावे" value={district.rejected} icon={<XCircle size={18} />} accentColor="#EF4444" />
                <StatCard title="Saturation Score" titleHi="संतृप्ति स्कोर" value={`${district.saturation}%`} icon={<BarChart3 size={18} />} accentColor="#0D9488" trend="up" change={4.2} />
            </div>

            {/* Main 3-col Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 mb-5">
                {/* DSS Intervention Map */}
                <div className="tribal-card p-5 lg:col-span-2">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="font-bold text-primary text-sm">DSS Recommended Interventions</h3>
                        <Link href="/dss" className="text-xs text-accent hover:underline flex items-center gap-1 font-semibold">
                            Full DSS Engine <ChevronRight size={11} />
                        </Link>
                    </div>
                    <div className="space-y-3">
                        {recommendations.map((r) => (
                            <div
                                key={`${r.villageCode}-${r.schemeId}`}
                                className="flex items-start gap-3 p-3 rounded-lg border"
                                style={{
                                    borderColor: r.priority === "critical" ? "#FCA5A5" : r.priority === "high" ? "#FCD34D" : "#BBF7D0",
                                    background: r.priority === "critical" ? "#FEF2F2" : r.priority === "high" ? "#FFFBEB" : "#F0FDF4",
                                }}
                            >
                                <div className="flex-shrink-0 mt-0.5">
                                    <div
                                        className="w-2.5 h-2.5 rounded-full"
                                        style={{
                                            background: r.priority === "critical" ? "#EF4444" : r.priority === "high" ? "#F59E0B" : "#22C55E",
                                        }}
                                    />
                                </div>
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center gap-2 mb-0.5 flex-wrap">
                                        <span className="text-xs font-bold text-primary">{r.villageName}</span>
                                        <span className="text-xs text-gray-400">{r.block}</span>
                                        <span className="text-xs font-semibold text-accent">{r.schemeName}</span>
                                        <Badge
                                            variant={r.priority === "critical" ? "danger" : r.priority === "high" ? "warning" : "success"}
                                            size="sm"
                                        >
                                            {r.priority.toUpperCase()}
                                        </Badge>
                                    </div>
                                    <p className="text-xs text-gray-600">{r.actionRequired}</p>
                                    <div className="flex items-center gap-4 mt-1.5 text-xs text-gray-500">
                                        <span>Eligible: <b className="text-primary">{r.eligibleBeneficiaries}</b></span>
                                        <span>Enrolled: <b className="text-emerald-700">{r.currentlyEnrolled}</b></span>
                                        <span>Gap: <b className="text-red-600">{r.gap}</b></span>
                                        <span>AI Score: <b className="text-accent">{r.aiScore}/100</b></span>
                                    </div>
                                </div>
                                {r.deadline && (
                                    <span className="text-xs text-gray-400 flex-shrink-0">By {r.deadline}</span>
                                )}
                            </div>
                        ))}
                        {recommendations.length === 0 && (
                            <div className="text-xs text-gray-500">No DSS recommendations available for this district.</div>
                        )}
                    </div>
                </div>

                {/* Infrastructure Proximity Gaps */}
                <div className="space-y-4">
                    <div className="tribal-card p-5">
                        <h3 className="font-bold text-primary text-sm mb-4">Infrastructure Gaps</h3>
                        <div className="space-y-2.5">
                            {infra.map((item) => (
                                <div key={item.label} className="flex items-center justify-between p-2.5 rounded-lg" style={{ background: `${item.color}10` }}>
                                    <div className="flex items-center gap-2" style={{ color: item.color }}>
                                        {item.icon}
                                        <span className="text-xs text-gray-700">{item.label}</span>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-sm font-bold" style={{ color: item.color }}>{item.count}</p>
                                        <p className="text-xs text-gray-400">{item.scheme}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Convergence Meeting Generator */}
                    <div className="tribal-card p-5">
                        <h3 className="font-bold text-primary text-sm mb-3">Convergence Meeting Generator</h3>
                        <p className="text-xs text-gray-500 mb-3">Auto-generate meeting agenda for line departments based on current DSS gaps</p>
                        <div className="space-y-2 mb-4">
                            {convergenceMeetingAgenda.length === 0 && <div className="text-xs text-gray-500">No pending agenda items for this district.</div>}
                            {convergenceMeetingAgenda.map((item, i) => (
                                <div key={i} className="flex items-start gap-2 text-xs">
                                    <span className="w-4 h-4 rounded-full bg-primary text-white flex items-center justify-center flex-shrink-0 text-xs font-bold mt-0.5">{i + 1}</span>
                                    <span className="text-gray-600">{item}</span>
                                </div>
                            ))}
                        </div>
                        <button className="w-full text-xs bg-primary text-white py-2.5 rounded-lg hover:bg-primary-600 transition-all shadow-md hover:shadow-lg">
                            Generate Meeting Notice (PDF)
                        </button>
                    </div>
                </div>
            </div>

            {/* Claims Table */}
            <div className="tribal-card overflow-hidden mb-5">
                <div className="p-4 border-b border-gray-100 flex items-center gap-3 flex-wrap">
                    <h3 className="font-bold text-primary text-sm flex-1">Active Claims — {district.name}</h3>
                    <div className="flex items-center gap-2 flex-wrap">
                        <div className="relative">
                            <Search size={13} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-400" />
                            <input
                                type="text"
                                placeholder="Search claimant, village, ID..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="pl-7 pr-3 py-1.5 text-xs border border-gray-200 rounded-lg w-48 focus:outline-none focus:border-primary"
                            />
                        </div>
                        <select
                            value={statusFilter}
                            onChange={(e) => setStatusFilter(e.target.value)}
                            className="text-xs border border-gray-200 rounded-lg px-2.5 py-1.5 focus:outline-none"
                        >
                            <option value="all">All Status</option>
                            <option value="pending">Pending</option>
                            <option value="frc-verified">FRC Verified</option>
                            <option value="sdlc-approved">SDLC Approved</option>
                            <option value="granted">Granted</option>
                            <option value="rejected">Rejected</option>
                        </select>
                    </div>
                </div>
                <div className="overflow-x-auto">
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>Claim ID</th>
                                <th>Claimant</th>
                                <th>Village</th>
                                <th>Type</th>
                                <th>Area (Ac)</th>
                                <th>Filed</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredClaims.map((c) => (
                                <tr key={c.id}>
                                    <td className="font-mono text-xs text-primary">{c.id}</td>
                                    <td>
                                        <div>
                                            <p className="font-medium text-sm text-primary">{c.claimantName}</p>
                                            <p className="text-xs text-gray-400">{c.tribalGroup}{c.isPVTG ? " (PVTG)" : ""}</p>
                                        </div>
                                    </td>
                                    <td className="text-sm text-gray-600">{c.villageName}, {c.block}</td>
                                    <td>
                                        <Badge
                                            variant={c.claimType === "IFR" ? "info" : c.claimType === "CFR" ? "success" : "warning"}
                                            size="sm"
                                        >
                                            {c.claimType}
                                        </Badge>
                                    </td>
                                    <td className="font-semibold">{c.areaAcres}</td>
                                    <td className="text-xs text-gray-500">{new Date(c.claimDate).toLocaleDateString("en-IN")}</td>
                                    <td>
                                        <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${getStatusColor(c.status)}`}>
                                            {c.status.replace(/-/g, " ")}
                                        </span>
                                    </td>
                                    <td>
                                        <div className="flex items-center gap-1">
                                            <Link
                                                href={`/sdlc/claims/${c.id}`}
                                                className="text-xs text-primary hover:text-accent font-medium"
                                            >
                                                View
                                            </Link>
                                            {c.status === "frc-verified" && (
                                                <button className="text-xs text-emerald-600 hover:underline ml-2">Approve</button>
                                            )}
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Village Asset Overview */}
            <div className="tribal-card p-5">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="font-bold text-primary text-sm">Village Asset Summary (District)</h3>
                    <Link href="/atlas" className="text-xs text-accent hover:underline flex items-center gap-1 font-semibold">
                        View on Atlas <ChevronRight size={11} />
                    </Link>
                </div>
                <div className="overflow-x-auto">
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>Village</th>
                                <th>Claims</th>
                                <th>IFR Area</th>
                                <th>CFR Area</th>
                                <th>Water Bodies</th>
                                <th>NDVI</th>
                                <th>Groundwater (m)</th>
                                <th>Sat. Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            {villages.map((v) => (
                                <tr key={v.code}>
                                    <td>
                                        <p className="font-medium text-primary">{v.name}</p>
                                        <p className="text-xs text-gray-400">{v.block}, {v.district}</p>
                                    </td>
                                    <td>
                                        <div className="text-xs">
                                            <span className="text-emerald-700 font-semibold">{v.grantedClaims}</span>
                                            <span className="text-gray-400">/{v.totalClaims}</span>
                                        </div>
                                    </td>
                                    <td className="text-sm">{v.ifrGrantedArea.toFixed(1)} ac</td>
                                    <td className="text-sm">{v.cfrGrantedArea.toFixed(1)} ac</td>
                                    <td className="text-center">{v.assets?.waterBodiesCount}</td>
                                    <td>
                                        <div className="flex items-center gap-1.5">
                                            <div
                                                className="w-2.5 h-2.5 rounded-full"
                                                style={{
                                                    background: (v.assets?.ndviScore ?? 0) >= 0.65 ? "#22C55E" : (v.assets?.ndviScore ?? 0) >= 0.4 ? "#F59E0B" : "#EF4444",
                                                }}
                                            />
                                            <span className="text-xs">{(v.assets?.ndviScore ?? 0).toFixed(2)}</span>
                                            <span className="text-xs text-gray-400">({v.assets?.ndviTrend ?? "-"})</span>
                                        </div>
                                    </td>
                                    <td className={`text-sm font-medium ${(v.assets?.groundwaterDepthM ?? 0) > 12 ? "text-red-600" : "text-emerald-700"}`}>
                                        {v.assets?.groundwaterDepthM ?? "-"}m
                                    </td>
                                    <td>
                                        <div className="flex items-center gap-1.5">
                                            <div className="w-12 progress-forest">
                                                <div style={{
                                                    width: `${v.saturationScore}%`,
                                                    background: v.saturationScore >= 70 ? "#22C55E" : "#F59E0B",
                                                }} />
                                            </div>
                                            <span className="text-xs font-semibold">{v.saturationScore}%</span>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </DashboardLayout>
    );
}

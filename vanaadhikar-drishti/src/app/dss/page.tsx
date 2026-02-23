"use client";
import React, { useState } from "react";
import {
    TrendingUp, Target, Zap, Cpu, Database, BarChart3,
    ChevronRight, Filter, Download, Brain, Layers,
    AlertTriangle, CheckCircle, MapPin, Users, Calendar,
    Sparkles, ArrowUpRight, Eye, Scale,
} from "lucide-react";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { Badge } from "@/components/ui/badge";
import { formatNumber } from "@/lib/utils";
import { BarChartWrapper, RadialChartWrapper } from "@/components/charts";
import { apiClient } from "@/lib/api-client";
import { ErrorDisplay } from "@/components/error-display";
import { DataTableSkeleton, StatCardSkeleton, ChartSkeleton } from "@/components/skeletons";

export default function DSSPage() {
    const [selectedState, setSelectedState] = useState("MP");
    const [priorityFilter, setPriorityFilter] = useState<"all" | "critical" | "high" | "medium">("all");

    // Mock DSS recommendations data
    const DSS_RECOMMENDATIONS = [
        { id: "rec-1", state: "MP", district: "Mandla", priority: "critical", title: "PM-KISAN enrollment gap", desc: "1,247 eligible pattas not enrolled", impact: "₹74.8L annual benefit lost", recommended: "SMS campaign + ASHA visits", actionBy: "BLCO" },
        { id: "rec-2", state: "MP", district: "Seoni", priority: "high", title: "JJM saturation low", desc: "Only 34% households have tap connections", impact: "Health outcomes risk", recommended: "Fast-track pipeline approval", actionBy: "PHED" },
        { id: "rec-3", state: "MP", district: "Balaghat", priority: "high", title: "MGNREGA underutilization", desc: "Employment demand < 30% capacity", impact: "₹8.2Cr wage fund unspent", recommended: "Skill training linkage", actionBy: "NREGA Coord" },
        { id: "rec-4", state: "OR", district: "Sundargarh", priority: "medium", title: "School enrollment gap", desc: "PVTG girls dropout at 40%", impact: "Future skill deficit", recommended: "EMRS expansion + scholarships", actionBy: "ST Welfare" },
        { id: "rec-5", state: "JH", district: "West Singhbhum", priority: "medium", title: "Crop insurance awareness", desc: "PM-Fasal uptake 12%", impact: "Income volatility risk", recommended: "Gram Sabha briefings", actionBy: "Agri Dept" },
    ];

    const DAJGUA_INTERVENTIONS = [
        { id: "i1", name: "Infrastructure Upgrade", targetVillages: 500, completedVillages: 423, saturationPct: 85 },
        { id: "i2", name: "Skills Training", targetVillages: 450, completedVillages: 312, saturationPct: 69 },
        { id: "i3", name: "Market Linkage", targetVillages: 400, completedVillages: 287, saturationPct: 72 },
        { id: "i4", name: "Eco Tourism", targetVillages: 150, completedVillages: 98, saturationPct: 65 },
        { id: "i5", name: "Cluster Dev", targetVillages: 250, completedVillages: 189, saturationPct: 76 },
        { id: "i6", name: "Heritage Cons", targetVillages: 80, completedVillages: 52, saturationPct: 65 },
        { id: "i7", name: "NTFP Value Add", targetVillages: 200, completedVillages: 134, saturationPct: 67 },
        { id: "i8", name: "Livelihood Div", targetVillages: 300, completedVillages: 198, saturationPct: 66 },
    ];

    const [selectedRec, setSelectedRec] = useState<(typeof DSS_RECOMMENDATIONS)[0] | null>(null);

    const filteredRecs = DSS_RECOMMENDATIONS.filter(
        (r) => priorityFilter === "all" || r.priority === priorityFilter
    );

    const schemeGapData = DAJGUA_INTERVENTIONS.slice(0, 8).map((itv) => ({
        name: itv.name.slice(0, 15),
        Gap: itv.targetVillages - itv.completedVillages,
        Saturation: itv.saturationPct,
    }));

    return (
        <DashboardLayout role="mota-nodal" title="Decision Support System (DSS)" titleHi="निर्णय समर्थन प्रणाली">
            {/* Header */}
            <div className="flex items-center justify-between mb-5">
                <div>
                    <h1 className="text-xl font-bold text-primary">AI-Powered Decision Support System (DSS)</h1>
                    <p className="text-xs text-gray-500">
                        Predictive analytics for scheme convergence optimization using ML models
                    </p>
                </div>
                <div className="flex items-center gap-2 no-print">
                    <button className="flex items-center gap-2 text-xs px-3 py-1.5 border border-gray-200 rounded-lg hover:bg-gray-50">
                        <Download size={13} /> Export Report
                    </button>
                    <button className="flex items-center gap-2 text-xs px-3 py-1.5 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg">
                        <Sparkles size={13} /> Run Analysis
                    </button>
                </div>
            </div>

            {/* AI Engine Status */}
            <div className="tribal-card p-5 mb-5 bg-gradient-to-r from-primary-50 to-white border-2 border-accent">
                <div className="flex items-center gap-3 mb-3">
                    <div className="w-10 h-10 rounded-full bg-accent flex items-center justify-center text-white">
                        <Brain size={20} />
                    </div>
                    <div>
                        <h3 className="font-bold text-primary">DSS Engine v2.3 — Active</h3>
                        <p className="text-xs text-gray-500">Random Forest Classifier + XGBoost Regressor · Last trained: Feb 15, 2026</p>
                    </div>
                </div>
                <div className="grid grid-cols-2 lg:grid-cols-5 gap-3">
                    {[
                        { label: "Model Accuracy", value: "91.4%", icon: <Target size={14} /> },
                        { label: "Recommendations Generated", value: "1,247", icon: <Zap size={14} /> },
                        { label: "Villages Analyzed", value: "63,843", icon: <MapPin size={14} /> },
                        { label: "Interventions Prioritized", value: "25", icon: <Layers size={14} /> },
                        { label: "Potential Impact", value: "₹320 Cr", icon: <TrendingUp size={14} /> },
                    ].map((s) => (
                        <div key={s.label} className="bg-white rounded-lg p-2.5 text-center">
                            <div className="flex items-center justify-center gap-1 mb-1 text-accent">
                                {s.icon}
                                <span className="text-lg font-bold">{s.value}</span>
                            </div>
                            <p className="text-xs text-gray-600">{s.label}</p>
                        </div>
                    ))}
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
                        value={selectedState}
                        onChange={(e) => setSelectedState(e.target.value)}
                        className="text-xs border border-gray-200 rounded-lg px-2.5 py-1.5"
                    >
                        {[
                            { id: "MP", name: "Madhya Pradesh" },
                            { id: "OR", name: "Odisha" },
                            { id: "JH", name: "Jharkhand" },
                            { id: "AS", name: "Assam" },
                            { id: "TR", name: "Tripura" },
                        ].map((s) => (
                            <option key={s.id} value={s.id}>{s.name}</option>
                        ))}
                    </select>
                    <div className="flex gap-1 border border-gray-200 rounded-lg p-0.5">
                        {["all", "critical", "high", "medium"].map((p) => (
                            <button
                                key={p}
                                onClick={() => setPriorityFilter(p as typeof priorityFilter)}
                                className={`px-3 py-1 rounded text-xs font-medium transition-all capitalize ${priorityFilter === p
                                    ? p === "critical" ? "bg-red-500 text-white" :
                                        p === "high" ? "bg-amber-500 text-white" :
                                            p === "medium" ? "bg-blue-500 text-white" :
                                                "bg-primary text-white shadow-md"
                                    : "text-gray-600 hover:bg-gray-100"
                                    }`}
                            >
                                {p}
                            </button>
                        ))}
                    </div>
                    <span className="text-xs text-gray-400 ml-auto">
                        {filteredRecs.length} recommendations
                    </span>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
                {/* Recommendations List */}
                <div className="lg:col-span-2 space-y-3">
                    {filteredRecs.map((rec) => (
                        <div
                            key={`${rec.villageCode}-${rec.schemeId}`}
                            className={`tribal-card p-5 cursor-pointer hover:shadow-md transition-all ${selectedRec?.villageCode === rec.villageCode && selectedRec?.schemeId === rec.schemeId
                                ? "border-2 border-accent"
                                : ""
                                }`}
                            onClick={() => setSelectedRec(rec)}
                        >
                            {/* Header */}
                            <div className="flex items-start justify-between mb-3">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                        <h3 className="font-bold text-primary text-sm">{rec.villageName}</h3>
                                        <ChevronRight size={12} className="text-gray-300" />
                                        <span className="text-xs font-semibold text-accent">{rec.schemeName}</span>
                                    </div>
                                    <p className="text-xs text-gray-500">{rec.district} District · {rec.block} Block</p>
                                </div>
                                <div className="flex items-center gap-2">
                                    <Badge
                                        variant={
                                            rec.priority === "critical" ? "danger" :
                                                rec.priority === "high" ? "warning" : "info"
                                        }
                                    >
                                        {rec.priority.toUpperCase()}
                                    </Badge>
                                    <div className="text-center">
                                        <p className="text-lg font-bold text-accent">{rec.aiScore}</p>
                                        <p className="text-xs text-gray-400">AI Score</p>
                                    </div>
                                </div>
                            </div>

                            {/* Metrics */}
                            <div className="grid grid-cols-3 gap-2 mb-3">
                                <div className="bg-blue-50 rounded p-2 text-center">
                                    <p className="text-xs text-gray-500 mb-0.5">Eligible</p>
                                    <p className="font-bold text-blue-700">{rec.eligibleBeneficiaries}</p>
                                </div>
                                <div className="bg-emerald-50 rounded p-2 text-center">
                                    <p className="text-xs text-gray-500 mb-0.5">Enrolled</p>
                                    <p className="font-bold text-emerald-700">{rec.currentlyEnrolled}</p>
                                </div>
                                <div className="bg-red-50 rounded p-2 text-center">
                                    <p className="text-xs text-gray-500 mb-0.5">Gap</p>
                                    <p className="font-bold text-red-700">{rec.gap}</p>
                                </div>
                            </div>

                            {/* Trigger & Action */}
                            <div className="space-y-2">
                                <div className="p-2 rounded-lg bg-purple-50 text-xs">
                                    <p className="text-purple-600 font-semibold mb-0.5">🎯 Trigger Condition:</p>
                                    <p className="text-gray-700">{rec.trigger}</p>
                                </div>
                                <div className="p-2 rounded-lg bg-amber-50 text-xs">
                                    <p className="text-amber-700 font-semibold mb-0.5">⚡ Recommended Action:</p>
                                    <p className="text-gray-700">{rec.actionRequired}</p>
                                </div>
                            </div>

                            {/* ML Features */}
                            <div className="mt-3 pt-3 border-t border-gray-100">
                                <p className="text-xs font-semibold text-gray-600 mb-1.5">🤖 ML Feature Weights:</p>
                                <div className="grid grid-cols-2 gap-2 text-xs">
                                    <div className="flex justify-between">
                                        <span className="text-gray-500">Proximity to facility:</span>
                                        <span className="font-semibold">{((Math.random() * 0.3) + 0.15).toFixed(2)}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-500">Household count:</span>
                                        <span className="font-semibold">{((Math.random() * 0.25) + 0.1).toFixed(2)}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-500">Patta holder ratio:</span>
                                        <span className="font-semibold">{((Math.random() * 0.2) + 0.15).toFixed(2)}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-500">Historical enrollment:</span>
                                        <span className="font-semibold">{((Math.random() * 0.15) + 0.08).toFixed(2)}</span>
                                    </div>
                                </div>
                            </div>

                            {/* Action Buttons */}
                            {rec.deadline && (
                                <div className="mt-3 flex items-center justify-between">
                                    <span className="text-xs text-gray-400">
                                        <Calendar size={11} className="inline mr-1" />
                                        Deadline: {rec.deadline}
                                    </span>
                                    <button className="text-xs bg-accent text-white px-3 py-1 rounded-lg font-semibold shadow-md hover:shadow-lg transition-all">
                                        Generate Meeting Notice
                                    </button>
                                </div>
                            )}
                        </div>
                    ))}
                </div>

                {/* Right Sidebar — Analytics */}
                <div className="space-y-4">
                    {/* Scheme Gap Analysis */}
                    <div className="tribal-card p-5">
                        <h4 className="font-bold text-primary text-sm mb-4">Scheme Gap Analysis</h4>
                        <div className="space-y-3">
                            {DAJGUA_INTERVENTIONS.slice(0, 6).map((itv) => (
                                <div key={itv.id}>
                                    <div className="flex items-center justify-between text-xs mb-1">
                                        <span className="text-gray-600 truncate">{itv.name.slice(0, 18)}</span>
                                        <span className="font-bold text-red-600">{formatNumber(itv.targetVillages - itv.completedVillages)}</span>
                                    </div>
                                    <div className="progress-forest">
                                        <div
                                            style={{
                                                width: `${itv.saturationPct}%`,
                                                background: itv.saturationPct >= 70 ? "#22C55E" : "#F59E0B",
                                            }}
                                        />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Priority Distribution */}
                    <div className="tribal-card p-5">
                        <h4 className="font-bold text-primary text-sm mb-4">Priority Distribution</h4>
                        <div className="space-y-2">
                            {[
                                { label: "Critical", count: DSS_RECOMMENDATIONS.filter(r => r.priority === "critical").length, color: "#EF4444" },
                                { label: "High", count: DSS_RECOMMENDATIONS.filter(r => r.priority === "high").length, color: "#F59E0B" },
                                { label: "Medium", count: DSS_RECOMMENDATIONS.filter(r => r.priority === "medium").length, color: "#3B82F6" },
                            ].map((p) => (
                                <div key={p.label} className="flex items-center gap-2">
                                    <div className="w-3 h-3 rounded-full" style={{ background: p.color }} />
                                    <span className="text-xs text-gray-600 flex-1">{p.label}</span>
                                    <span className="text-sm font-bold" style={{ color: p.color }}>{p.count}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Model Performance */}
                    <div className="tribal-card p-5">
                        <h4 className="font-bold text-primary text-sm mb-4">Model Performance</h4>
                        <div className="space-y-3">
                            {[
                                { label: "Accuracy", value: 91.4 },
                                { label: "Precision", value: 89.2 },
                                { label: "Recall", value: 93.7 },
                                { label: "F1-Score", value: 91.4 },
                            ].map((m) => (
                                <div key={m.label}>
                                    <div className="flex justify-between text-xs mb-1">
                                        <span className="text-gray-600">{m.label}</span>
                                        <span className="font-bold text-primary">{m.value}%</span>
                                    </div>
                                    <div className="progress-forest">
                                        <div style={{ width: `${m.value}%`, background: "#6366F1" }} />
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className="mt-4 pt-3 border-t border-gray-100 text-xs text-gray-500">
                            <Cpu size={12} className="inline mr-1" />
                            Training dataset: 63,843 villages · 180K records
                        </div>
                    </div>

                    {/* Top Features */}
                    <div className="tribal-card p-5">
                        <h4 className="font-bold text-primary text-sm mb-4">Feature Importance</h4>
                        <div className="space-y-2">
                            {[
                                { name: "Groundwater Depth", weight: 0.23 },
                                { name: "Distance to School", weight: 0.19 },
                                { name: "Patta Holder Count", weight: 0.17 },
                                { name: "Historical Enrollment", weight: 0.14 },
                                { name: "NDVI Score", weight: 0.12 },
                                { name: "Road Connectivity", weight: 0.09 },
                            ].map((f) => (
                                <div key={f.name}>
                                    <div className="flex justify-between text-xs mb-1">
                                        <span className="text-gray-600">{f.name}</span>
                                        <span className="font-bold text-purple-600">{(f.weight * 100).toFixed(0)}%</span>
                                    </div>
                                    <div className="progress-forest">
                                        <div style={{ width: `${f.weight * 100}%`, background: "#8B5CF6" }} />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Model Info Footer */}
            <div className="tribal-card p-5 mt-5 bg-gradient-to-r from-purple-50 to-blue-50">
                <div className="flex items-start gap-3">
                    <Brain size={20} className="text-purple-600 flex-shrink-0 mt-0.5" />
                    <div>
                        <h4 className="font-bold text-[#1a3c2e] text-sm mb-2">About the DSS Engine</h4>
                        <p className="text-xs text-gray-600 leading-relaxed mb-2">
                            The Decision Support System uses ensemble machine learning models (Random Forest + XGBoost) trained on 180,000+ historical records
                            from 63,843 villages. The model analyzes 47 features including demographic data, infrastructure proximity, historical enrollment
                            patterns, environmental indicators (NDVI, groundwater), and scheme-specific eligibility criteria to generate prioritized
                            recommendations for scheme convergence interventions.
                        </p>
                        <div className="flex items-center gap-4 text-xs text-gray-500">
                            <span><Database size={11} className="inline mr-1" />PostgreSQL + TimescaleDB</span>
                            <span><Cpu size={11} className="inline mr-1" />Python 3.11 · scikit-learn · XGBoost</span>
                            <span><Zap size={11} className="inline mr-1" />Avg inference: 42ms</span>
                        </div>
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
}

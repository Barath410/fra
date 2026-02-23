"use client";
import React, { useEffect, useState } from "react";
import {
    MessageSquare, AlertTriangle, Clock, CheckCircle, XCircle,
    Search, Filter, Eye, Send, Phone, Mail, MapPin,
    Calendar, User, FileText, ChevronRight, TrendingUp,
    BarChart3,
} from "lucide-react";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { Badge } from "@/components/ui/badge";
import { formatDate } from "@/lib/utils";
import { BarChartWrapper } from "@/components/charts";
import { useDashboardData } from "@/lib/use-dashboard-data";
import type { GrievanceTicket, StateStat } from "@/types";

export default function GrievancesPage() {
    const { data, loading } = useDashboardData();
    const grievances = ((data?.grievances as GrievanceTicket[] | undefined) ?? []);
    const stateStats = (data?.stateStats as StateStat[] | undefined) ?? [];
    const [selectedGrievance, setSelectedGrievance] = useState<GrievanceTicket | null>(null);
    const [statusFilter, setStatusFilter] = useState<"all" | "open" | "in-progress" | "resolved" | "closed">("all");
    const [priorityFilter, setPriorityFilter] = useState<"all" | "urgent" | "high" | "medium" | "low">("all");

    useEffect(() => {
        if (!selectedGrievance && grievances.length > 0) {
            setSelectedGrievance(grievances[0]);
        }
    }, [grievances, selectedGrievance]);

    const filteredGrievances = grievances.filter((g) => {
        const matchStatus = statusFilter === "all" || g.status === statusFilter;
        const matchPriority = priorityFilter === "all" || g.priority === priorityFilter;
        return matchStatus && matchPriority;
    });

    const totalOpen = grievances.filter((g) => g.status === "open" || g.status === "in-progress" || g.status === "in-review" || g.status === "escalated").length;
    const totalResolved = grievances.filter((g) => g.status === "resolved" || g.status === "closed").length;
    const avgResolutionDays = (() => {
        const resolved = grievances.filter((g) => g.status === "resolved" || g.status === "closed");
        if (!resolved.length) return 0;
        return Math.round(resolved.reduce((sum, g) => sum + (g.daysOpen ?? 0), 0) / resolved.length);
    })();

    const grievancesByState = stateStats.map((s) => ({
        name: s.id,
        Open: grievances.filter((g) => g.state === s.id && (g.status === "open" || g.status === "in-progress" || g.status === "in-review" || g.status === "escalated")).length,
        Resolved: grievances.filter((g) => g.state === s.id && (g.status === "resolved" || g.status === "closed")).length,
        fill: s.color,
    }));

    if (loading) {
        return (
            <DashboardLayout role="mota-nodal" title="Grievance Redressal" titleHi="शिकायत निवारण">
                <div className="p-6">Loading grievances…</div>
            </DashboardLayout>
        );
    }

    return (
        <DashboardLayout role="mota-nodal" title="Grievance Redressal" titleHi="शिकायत निवारण">
            {/* Header */}
            <div className="flex items-center justify-between mb-5">
                <div>
                    <h1 className="text-xl font-bold text-primary">FRA Grievance Redressal System</h1>
                    <p className="text-xs text-gray-500">
                        Centralized grievance tracking & resolution portal — Toll-Free Helpline: 1800-11-0130
                    </p>
                </div>
                <div className="flex items-center gap-2 no-print">
                    <button className="flex items-center gap-2 text-xs px-3 py-1.5 bg-accent text-white rounded-lg shadow-md hover:shadow-lg transition-all">
                        <MessageSquare size={13} /> File New Grievance
                    </button>
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-2 lg:grid-cols-5 gap-4 mb-5">
                {[
                    { label: "Total Grievances", value: grievances.length, icon: <MessageSquare size={16} />, color: "#3B82F6" },
                    { label: "Open", value: totalOpen, icon: <Clock size={16} />, color: "#F59E0B" },
                    { label: "In Progress", value: grievances.filter((g) => g.status === "in-progress" || g.status === "in-review").length, icon: <TrendingUp size={16} />, color: "#6366F1" },
                    { label: "Resolved", value: totalResolved, icon: <CheckCircle size={16} />, color: "#22C55E" },
                    { label: "Avg Resolution Time", value: `${avgResolutionDays} days`, icon: <Clock size={16} />, color: "#8B5CF6" },
                ].map((s) => (
                    <div key={s.label} className="tribal-card p-4">
                        <div className="flex items-center gap-2 mb-1" style={{ color: s.color }}>
                            {s.icon}
                            <span className="text-xl font-bold">{s.value}</span>
                        </div>
                        <p className="text-xs text-gray-500">{s.label}</p>
                    </div>
                ))}
            </div>

            {/* Filters */}
            <div className="tribal-card p-4 mb-5">
                <div className="flex items-center gap-3 flex-wrap">
                    <div className="flex items-center gap-2">
                        <Filter size={14} className="text-gray-400" />
                        <span className="text-xs font-semibold text-gray-600">Filters:</span>
                    </div>
                    <div className="flex gap-1 border border-gray-200 rounded-lg p-0.5">
                        <span className="text-xs text-gray-500 px-2 py-1">Status:</span>
                        {["all", "open", "in-progress", "resolved", "closed"].map((s) => (
                            <button
                                key={s}
                                onClick={() => setStatusFilter(s as typeof statusFilter)}
                                className={`px-2 py-1 rounded text-xs font-medium capitalize transition-all ${statusFilter === s ? "bg-primary text-white shadow-md" : "text-gray-600 hover:bg-gray-100"
                                    }`}
                            >
                                {s.replace("-", " ")}
                            </button>
                        ))}
                    </div>
                    <div className="flex gap-1 border border-gray-200 rounded-lg p-0.5">
                        <span className="text-xs text-gray-500 px-2 py-1">Priority:</span>
                        {["all", "urgent", "high", "medium", "low"].map((p) => (
                            <button
                                key={p}
                                onClick={() => setPriorityFilter(p as typeof priorityFilter)}
                                className={`px-2 py-1 rounded text-xs font-medium capitalize transition-all ${priorityFilter === p
                                    ? p === "urgent" ? "bg-red-500 text-white" :
                                        p === "high" ? "bg-amber-500 text-white" :
                                            "bg-primary text-white shadow-md"
                                    : "text-gray-600 hover:bg-gray-100"
                                    }`}
                            >
                                {p}
                            </button>
                        ))}
                    </div>
                    <span className="text-xs text-gray-400 ml-auto">{filteredGrievances.length} grievances</span>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-5 gap-5">
                {/* Grievance List */}
                <div className="lg:col-span-2 tribal-card overflow-hidden">
                    <div className="p-3 border-b border-gray-100 flex items-center gap-2">
                        <div className="relative flex-1">
                            <Search size={12} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-400" />
                            <input
                                type="text"
                                placeholder="Search by ID, name, village..."
                                className="w-full pl-7 pr-3 py-1.5 text-xs border border-gray-200 rounded-lg"
                            />
                        </div>
                    </div>
                    <div className="overflow-y-auto max-h-[700px]">
                        {filteredGrievances.map((g) => (
                            <button
                                key={g.id}
                                onClick={() => setSelectedGrievance(g)}
                                className={`w-full text-left px-3 py-3 border-b border-gray-50 hover:bg-[#f4ede3] transition-colors ${selectedGrievance?.id === g.id ? "bg-[#f4ede3] border-l-2 border-l-[#e87722]" : ""
                                    }`}
                            >
                                <div className="flex items-center justify-between mb-1">
                                    <span className="text-xs font-mono text-gray-400">{g.id}</span>
                                    <div className="flex items-center gap-1">
                                        <Badge
                                            variant={
                                                g.priority === "urgent" ? "danger" :
                                                    g.priority === "high" ? "warning" :
                                                        g.priority === "medium" ? "info" : "neutral"
                                            }
                                            size="sm"
                                        >
                                            {g.priority}
                                        </Badge>
                                        {g.daysOpen > 15 && <AlertTriangle size={12} className="text-red-500" />}
                                    </div>
                                </div>
                                <p className="text-sm font-medium text-primary">{g.claimantName}</p>
                                <p className="text-xs text-gray-500 mt-0.5">{g.category} · {g.villageName}</p>
                                <div className="flex items-center justify-between mt-1.5">
                                    <span className={`text-xs px-1.5 py-0.5 rounded-full ${g.status === "open" ? "bg-amber-100 text-amber-700" :
                                        g.status === "in-progress" ? "bg-blue-100 text-blue-700" :
                                            g.status === "resolved" ? "bg-emerald-100 text-emerald-700" :
                                                "bg-gray-100 text-gray-600"
                                        }`}>
                                        {g.status.replace("-", " ").toUpperCase()}
                                    </span>
                                    <span className="text-xs text-gray-400">{g.daysOpen}d open</span>
                                </div>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Grievance Detail */}
                <div className="lg:col-span-3">
                    {selectedGrievance ? (
                        <div className="space-y-4">
                            {/* Header */}
                            <div className="tribal-card p-5">
                                <div className="flex items-start justify-between mb-3">
                                    <div>
                                        <p className="text-xs text-gray-400 mb-0.5">{selectedGrievance.id}</p>
                                        <h2 className="text-lg font-bold text-primary">{selectedGrievance.category}</h2>
                                        <p className="text-sm text-gray-600 mt-0.5">{selectedGrievance.claimantName} · {selectedGrievance.villageName}, {selectedGrievance.district}</p>
                                    </div>
                                    <div className="flex flex-col items-end gap-2">
                                        <Badge
                                            variant={
                                                selectedGrievance.status === "resolved" ? "success" :
                                                    selectedGrievance.status === "in-progress" ? "info" :
                                                        selectedGrievance.status === "open" ? "warning" : "neutral"
                                            }
                                        >
                                            {selectedGrievance.status.toUpperCase()}
                                        </Badge>
                                        <Badge
                                            variant={
                                                selectedGrievance.priority === "urgent" ? "danger" :
                                                    selectedGrievance.priority === "high" ? "warning" : "info"
                                            }
                                        >
                                            {selectedGrievance.priority.toUpperCase()} PRIORITY
                                        </Badge>
                                    </div>
                                </div>

                                <div className="grid grid-cols-3 gap-2">
                                    <div className="bg-gray-50 rounded p-2">
                                        <p className="text-xs text-gray-400 mb-0.5">Filed On</p>
                                        <p className="text-sm font-semibold text-primary">{formatDate(selectedGrievance.filedDate || selectedGrievance.createdAt)}</p>
                                    </div>
                                    <div className="bg-gray-50 rounded p-2">
                                        <p className="text-xs text-gray-400 mb-0.5">Days Open</p>
                                        <p className="text-sm font-semibold text-primary">{selectedGrievance.daysOpen} days</p>
                                    </div>
                                    <div className="bg-gray-50 rounded p-2">
                                        <p className="text-xs text-gray-400 mb-0.5">Source</p>
                                        <p className="text-sm font-semibold text-primary">{selectedGrievance.source}</p>
                                    </div>
                                </div>
                            </div>

                            {/* Complainant Details */}
                            <div className="tribal-card p-5">
                                <h3 className="font-bold text-primary text-sm mb-3">Complainant Details</h3>
                                <div className="space-y-2 text-sm">
                                    <div className="flex items-center gap-2">
                                        <User size={14} className="text-gray-400" />
                                        <span className="text-gray-600">Name:</span>
                                        <span className="font-semibold text-primary">{selectedGrievance.claimantName}</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <Phone size={14} className="text-gray-400" />
                                        <span className="text-gray-600">Mobile:</span>
                                        <a href={`tel:${selectedGrievance.mobile}`} className="font-semibold text-accent hover:underline">
                                            {selectedGrievance.mobile}
                                        </a>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <MapPin size={14} className="text-gray-400" />
                                        <span className="text-gray-600">Location:</span>
                                        <span className="font-semibold text-primary">{selectedGrievance.villageName}, {selectedGrievance.block}, {selectedGrievance.district}, {selectedGrievance.state}</span>
                                    </div>
                                    {selectedGrievance.claimId && (
                                        <div className="flex items-center gap-2">
                                            <FileText size={14} className="text-gray-400" />
                                            <span className="text-gray-600">Related Claim:</span>
                                            <span className="font-mono font-semibold text-primary">{selectedGrievance.claimId}</span>
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* Grievance Description */}
                            <div className="tribal-card p-5">
                                <h3 className="font-bold text-primary text-sm mb-3">Grievance Description</h3>
                                <p className="text-sm text-gray-700 leading-relaxed">{selectedGrievance.description}</p>
                            </div>

                            {/* Response/Action */}
                            {selectedGrievance.assignedTo && (
                                <div className="tribal-card p-5">
                                    <h3 className="font-bold text-primary text-sm mb-3">Assigned Officer</h3>
                                    <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                                        <div>
                                            <p className="text-sm font-semibold text-primary">{selectedGrievance.assignedTo}</p>
                                            <p className="text-xs text-gray-500">SDLC Officer — {selectedGrievance.district}</p>
                                        </div>
                                        <button className="text-xs bg-primary text-white px-3 py-1.5 rounded-lg shadow-md hover:shadow-lg transition-all">
                                            Contact Officer
                                        </button>
                                    </div>
                                </div>
                            )}

                            {/* Response Box (if resolved) */}
                            {selectedGrievance.status === "resolved" && (
                                <div className="tribal-card p-5 border-2 border-emerald-200 bg-emerald-50">
                                    <div className="flex items-start gap-2">
                                        <CheckCircle size={18} className="text-emerald-600 flex-shrink-0 mt-0.5" />
                                        <div>
                                            <h4 className="font-bold text-emerald-800 text-sm mb-2">Resolution</h4>
                                            <p className="text-xs text-emerald-700 leading-relaxed">
                                                The rejection was reviewed by SDLC committee. After site visit and FSI boundary verification, the claim has been
                                                re-approved. Patta will be issued within 7 working days. Tracking ID: {selectedGrievance.id}
                                            </p>
                                            <p className="text-xs text-emerald-600 mt-2">Resolved on: {new Date().toLocaleDateString("en-IN")}</p>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* Action Panel (if open/in-progress) */}
                            {(selectedGrievance.status === "open" || selectedGrievance.status === "in-progress") && (
                                <div className="tribal-card p-5">
                                    <h3 className="font-bold text-[#1a3c2e] text-sm mb-3">Take Action</h3>
                                    <div className="space-y-3">
                                        {selectedGrievance.status === "open" && (
                                            <div>
                                                <label className="form-label">Assign To</label>
                                                <select className="form-input text-sm">
                                                    <option>Select Officer</option>
                                                    <option>SDLC Officer — Mandla</option>
                                                    <option>District Collector — Mandla</option>
                                                    <option>Range Officer — Bichhiya</option>
                                                </select>
                                            </div>
                                        )}
                                        <div>
                                            <label className="form-label">Response / Action Taken</label>
                                            <textarea
                                                className="form-input resize-none h-20"
                                                placeholder="Enter response or action taken..."
                                            />
                                        </div>
                                        <div className="flex gap-2">
                                            <button className="flex-1 py-2 bg-blue-600 text-white rounded-lg text-sm font-semibold flex items-center justify-center gap-2">
                                                <Send size={14} /> Update Status
                                            </button>
                                            <button className="flex-1 py-2 bg-emerald-600 text-white rounded-lg text-sm font-semibold flex items-center justify-center gap-2">
                                                <CheckCircle size={14} /> Mark Resolved
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="tribal-card p-10 flex flex-col items-center justify-center text-center h-full">
                            <MessageSquare size={40} className="text-gray-200 mb-3" />
                            <p className="text-gray-400 text-sm">Select a grievance to view details</p>
                        </div>
                    )}
                </div>
            </div>

            {/* State-wise Chart */}
            <div className="tribal-card p-5 mt-5">
                <h3 className="font-bold text-[#1a3c2e] text-sm mb-4">State-wise Grievance Status</h3>
                <BarChartWrapper
                    data={grievancesByState}
                    bars={[
                        { key: "Open", color: "#F59E0B" },
                        { key: "Resolved", color: "#22C55E" },
                    ]}
                    height={200}
                />
            </div>
        </DashboardLayout>
    );
}

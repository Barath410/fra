"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
    FileText, CheckCircle, Clock, XCircle, AlertTriangle,
    Eye, Download, Search, Filter, ChevronRight,
    GitMerge, Users, Stamp, Send, RotateCcw,
    CalendarDays, MessageSquare, Scale,
} from "lucide-react";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { StatCard } from "@/components/ui/stat-card";
import { Badge } from "@/components/ui/badge";
import { getStatusColor } from "@/lib/utils";
import { apiClient } from "@/lib/api-client";
import { ErrorDisplay } from "@/components/error-display";
import { DataTableSkeleton, StatCardSkeleton } from "@/components/skeletons";

const STATUS_WORKFLOW = [
    { from: "received", to: "frc-verified", actor: "FRC", label: "FRC Verification" },
    { from: "frc-verified", to: "sdlc-approved", actor: "SDLC", label: "SDLC Approval" },
    { from: "sdlc-approved", to: "dlc-approved", actor: "DLC", label: "DLC Approval" },
    { from: "dlc-approved", to: "granted", actor: "Collector", label: "Patta Grant" },
];

export default function SDLCDashboardPage() {
    const [selectedClaim, setSelectedClaim] = useState<any | null>(null);
    const [action, setAction] = useState<"approve" | "reject" | "query" | null>(null);
    const [remarksText, setRemarksText] = useState("");
    const [claims, setClaims] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Fetch claims from API
    useEffect(() => {
        const fetchClaims = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await apiClient.getClaims(1, 100, { status: ["frc-verified", "received", "sdlc-approved", "rejected"] });
                if (response.error) {
                    setError(response.error);
                } else if (response.data?.items) {
                    setClaims(response.data.items);
                } else {
                    setError("No claims data received");
                }
            } catch (err) {
                setError(err instanceof Error ? err.message : "Failed to fetch claims");
            } finally {
                setLoading(false);
            }
        };

        fetchClaims();
    }, []);

    const pendingForSDLC = claims.filter((c) => c.status === "frc-verified" || c.status === "received");
    const reviewed = claims.filter((c) => c.status === "sdlc-approved" || c.status === "rejected");

    if (error) {
        return (
            <DashboardLayout role="sdlc-officer" title="SDLC/DLC Officer Portal" titleHi="SDLC अधिकारी पोर्टल">
                <ErrorDisplay
                    title="Failed to Load Claims"
                    message={error}
                    onRetry={() => window.location.reload()}
                    showRetry
                />
            </DashboardLayout>
        );
    }

    return (
        <DashboardLayout role="sdlc-officer" title="SDLC/DLC Officer Portal" titleHi="SDLC अधिकारी पोर्टल">
            {/* Header */}
            <div className="flex items-center justify-between mb-5">
                <div>
                    <h1 className="text-xl font-bold text-primary">SDLC/DLC Claims Review Portal</h1>
                    <p className="text-xs text-gray-500">Sub-Divisional Level Committee · Mandla Division, MP</p>
                </div>
                <div className="flex gap-2 no-print">
                    <button className="flex items-center gap-2 text-xs px-3 py-1.5 border border-gray-200 rounded-lg hover:bg-gray-50">
                        <Download size={13} /> Export Pending
                    </button>
                    <button className="flex items-center gap-2 text-xs px-4 py-2 bg-accent text-white rounded-lg shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all">
                        <Stamp size={13} /> Bulk Approve
                    </button>
                </div>
            </div>

            {/* KPIs */}
            {loading ? (
                <StatCardSkeleton count={4} />
            ) : (
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-5">
                    <StatCard title="Pending Review" titleHi="समीक्षाधीन" value={pendingForSDLC.length} icon={<Clock size={18} />} accentColor="#F59E0B" trend="up" change={pendingForSDLC.length > 0 ? 1 : 0} />
                    <StatCard title="Approved This Week" titleHi="इस सप्ताह अनुमोदित" value={reviewed.filter(c => c.status === "sdlc-approved").length} icon={<CheckCircle size={18} />} accentColor="#22C55E" />
                    <StatCard title="Returned for Correction" titleHi="सुधार हेतु वापस" value={0} icon={<RotateCcw size={18} />} accentColor="#8B5CF6" />
                    <StatCard title="Under Appeal" titleHi="अपील में" value={0} icon={<Scale size={18} />} accentColor="#EF4444" />
                </div>
            )}

            {/* Workflow Progress */}
            <div className="tribal-card p-5 mb-5">
                <h3 className="font-bold text-primary text-sm mb-4">Claim Processing Workflow</h3>
                <div className="flex items-center gap-2 overflow-x-auto pb-2">
                    {[
                        { id: "submitted", label: "Submitted", labelHi: "जमा", count: 125000, color: "#3B82F6" },
                        { id: "under_review", label: "Under Review", labelHi: "समीक्षा में", count: 45200, color: "#F59E0B" },
                        { id: "field_verified", label: "Field Verified", labelHi: "क्षेत्र सत्यापित", count: 38700, color: "#10B981" },
                        { id: "approved", label: "Approved", labelHi: "स्वीकृत", count: 105300, color: "#22C55E" },
                        { id: "granted", label: "Granted", labelHi: "अनुदानित", count: 92450, color: "#059669" },
                        { id: "appealed", label: "Appealed", labelHi: "अपील", count: 8200, color: "#EF4444" },
                    ].map((stage, i) => (
                        <React.Fragment key={stage.id}>
                            <div className="flex-shrink-0 text-center min-w-[90px]">
                                <div
                                    className="w-12 h-12 rounded-full mx-auto flex items-center justify-center text-white text-sm font-bold mb-1"
                                    style={{ background: stage.color }}
                                >
                                    {stage.count > 100000 ? `${Math.floor(stage.count / 1000)}k` : stage.count > 1000 ? `${(stage.count / 1000).toFixed(0)}k` : stage.count}
                                </div>
                                <p className="text-xs font-semibold text-gray-700">{stage.label}</p>
                                <p className="text-xs text-gray-400">{stage.labelHi}</p>
                            </div>
                            {i < 5 && (
                                <ChevronRight size={16} className="text-gray-300 flex-shrink-0" />
                            )}
                        </React.Fragment>
                    ))}
                </div>
            </div>

            {/* Split View */}
            <div className="grid grid-cols-1 lg:grid-cols-5 gap-5">
                {/* Claims List */}
                <div className="lg:col-span-2 tribal-card overflow-hidden">
                    <div className="p-3 border-b border-gray-100 flex items-center gap-2">
                        <div className="relative flex-1">
                            <Search size={12} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-400" />
                            <input
                                type="text"
                                placeholder="Search claims..."
                                className="w-full pl-7 pr-3 py-1.5 text-xs border border-gray-200 rounded-lg focus:outline-none focus:border-[#2d8566]"
                            />
                        </div>
                        <button className="flex items-center gap-1 text-xs border border-gray-200 px-2 py-1.5 rounded-lg">
                            <Filter size={11} />
                        </button>
                    </div>
                    <div className="overflow-y-auto max-h-[600px]">
                        {loading ? (
                            <div className="p-4">
                                <DataTableSkeleton rows={5} />
                            </div>
                        ) : claims.length === 0 ? (
                            <div className="p-4 text-center text-gray-400 text-xs">
                                <FileText size={24} className="mx-auto mb-2 opacity-50" />
                                No claims found
                            </div>
                        ) : (
                            <>
                                {/* Pending for SDLC */}
                                {pendingForSDLC.length > 0 && (
                                    <>
                                        <div className="px-3 pt-3 pb-1">
                                            <span className="text-xs font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded-full">⏳ Pending Review ({pendingForSDLC.length})</span>
                                        </div>
                                        {pendingForSDLC.map((c) => (
                                            <button
                                                key={c.id}
                                                onClick={() => { setSelectedClaim(c); setAction(null); setRemarksText(""); }}
                                                className={`w-full text-left px-3 py-3 border-b border-gray-50 hover:bg-[#f4ede3] transition-colors ${selectedClaim?.id === c.id ? "bg-[#f4ede3] border-l-2 border-l-[#e87722]" : ""}`}
                                            >
                                                <div className="flex items-center justify-between mb-0.5">
                                                    <span className="text-xs font-mono text-primary">{c.id}</span>
                                                    <Badge
                                                        variant={c.claimType === "IFR" ? "info" : "success"}
                                                        size="sm"
                                                    >{c.claimType || "FRA"}</Badge>
                                                </div>
                                                <p className="text-sm font-medium text-primary">{c.claimantName || "Unknown"}</p>
                                                <p className="text-xs text-gray-400">{c.villageName || "N/A"} · {c.areaAcres || 0} acres</p>
                                            </button>
                                        ))}
                                    </>
                                )}
                                {/* Previously processed */}
                                {reviewed.length > 0 && (
                                    <>
                                        <div className="px-3 pt-3 pb-1">
                                            <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full">✅ Recently Processed ({reviewed.length})</span>
                                        </div>
                                        {reviewed.map((c) => (
                                            <button
                                                key={c.id}
                                                onClick={() => { setSelectedClaim(c); setAction(null); }}
                                                className={`w-full text-left px-3 py-3 border-b border-gray-50 hover:bg-gray-50 transition-colors ${selectedClaim?.id === c.id ? "bg-gray-50" : ""}`}
                                            >
                                                <div className="flex items-center justify-between mb-0.5">
                                                    <span className="text-xs font-mono text-primary">{c.id}</span>
                                                    <span className={`text-xs px-1.5 py-0.5 rounded-full ${getStatusColor(c.status)}`}>{c.status || "N/A"}</span>
                                                </div>
                                                <p className="text-sm font-medium text-primary">{c.claimantName || "Unknown"}</p>
                                                <p className="text-xs text-gray-400">{c.villageName || "N/A"} · {c.areaAcres || 0} acres</p>
                                            </button>
                                        ))}
                                    </>
                                )}
                            </>
                        )}
                    </div>
                </div>

                {/* Claim Detail Panel */}
                <div className="lg:col-span-3">
                    {selectedClaim ? (
                        <div className="space-y-4">
                            {/* Claim Header */}
                            <div className="tribal-card p-5">
                                <div className="flex items-start justify-between mb-3">
                                    <div>
                                        <div className="flex items-center gap-2 mb-1">
                                            <span className="font-mono text-sm font-bold text-primary">{selectedClaim.id}</span>
                                            <Badge variant={selectedClaim.claimType === "IFR" ? "info" : "success"}>
                                                {selectedClaim.claimType}
                                            </Badge>
                                            {selectedClaim.isPVTG && <Badge variant="warning">PVTG</Badge>}
                                        </div>
                                        <h2 className="text-lg font-bold text-primary">{selectedClaim.claimantName}</h2>
                                        <p className="text-sm text-gray-500">{selectedClaim.tribalGroup} · {selectedClaim.villageName}, {selectedClaim.block}, {selectedClaim.district}</p>
                                    </div>
                                    <span className={`text-xs px-2.5 py-1 rounded-full border font-semibold ${getStatusColor(selectedClaim.status)}`}>
                                        {selectedClaim.status.replace(/-/g, " ").toUpperCase()}
                                    </span>
                                </div>

                                <div className="grid grid-cols-3 gap-3 text-xs">
                                    <div className="bg-gray-50 rounded p-2.5">
                                        <p className="text-gray-400 mb-0.5">Claimed Area</p>
                                        <p className="font-bold text-primary">{selectedClaim.areaAcres} acres</p>
                                    </div>
                                    <div className="bg-gray-50 rounded p-2.5">
                                        <p className="text-gray-400 mb-0.5">Claim Date</p>
                                        <p className="font-bold text-primary">{selectedClaim.claimDate}</p>
                                    </div>
                                    <div className="bg-gray-50 rounded p-2.5">
                                        <p className="text-gray-400 mb-0.5">Documents</p>
                                        <p className="font-bold text-primary">{selectedClaim.documents?.length || 0} uploaded</p>
                                    </div>
                                </div>
                            </div>

                            {/* OCR Extraction Summary */}
                            {selectedClaim.ocrData && (
                                <div className="tribal-card p-5">
                                    <div className="flex items-center justify-between mb-3">
                                        <h3 className="font-bold text-primary text-sm">🤖 OCR/AI Extraction Summary</h3>
                                        <Badge variant={selectedClaim.ocrData.status === "completed" ? "success" : "warning"} size="sm">
                                            {Math.round(selectedClaim.ocrData.confidence * 100)}% confidence
                                        </Badge>
                                    </div>
                                    <div className="grid grid-cols-2 gap-2 text-xs">
                                        {Object.entries(selectedClaim.ocrData.extractedFields).map(([key, val]) => (
                                            <div key={key} className="flex justify-between py-1 border-b border-gray-100">
                                                <span className="text-gray-500 capitalize">{key.replace(/_/g, " ")}</span>
                                                <span className="font-semibold text-primary ml-2 text-right">{String(val)}</span>
                                            </div>
                                        ))}
                                        {selectedClaim.ocrData.nerEntities?.map((e) => (
                                            <div key={`${e.text}-${e.type}`} className="flex items-center gap-2 py-1 border-b border-gray-100">
                                                <Badge variant="info" size="sm">{e.type}</Badge>
                                                <span className="font-medium">{e.text}</span>
                                                {e.verified && <CheckCircle size={10} className="text-emerald-500" />}
                                            </div>
                                        ))}
                                    </div>
                                    {selectedClaim.ocrData.flags && selectedClaim.ocrData.flags.length > 0 && (
                                        <div className="mt-3 p-2.5 bg-amber-50 rounded text-xs text-amber-800">
                                            <AlertTriangle size={12} className="inline mr-1" />
                                            {selectedClaim.ocrData.flags.join("; ")}
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* Documents */}
                            <div className="tribal-card p-5">
                                <h3 className="font-bold text-primary text-sm mb-3">Attached Documents</h3>
                                <div className="space-y-2">
                                    {selectedClaim.documents?.map((doc) => (
                                        <div key={doc.id} className="flex items-center justify-between p-2.5 rounded-lg bg-gray-50">
                                            <div className="flex items-center gap-2">
                                                <FileText size={14} className="text-accent" />
                                                <div>
                                                    <p className="text-xs font-medium text-primary">{doc.name}</p>
                                                    <p className="text-xs text-gray-400">{doc.type} · {doc.fileSize}</p>
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                {doc.isVerified ? (
                                                    <CheckCircle size={14} className="text-emerald-500" />
                                                ) : (
                                                    <AlertTriangle size={14} className="text-amber-500" />
                                                )}
                                                <button className="text-xs text-accent hover:underline font-semibold">View</button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Action Panel */}
                            {(selectedClaim.status === "frc-verified" || selectedClaim.status === "received") && (
                                <div className="tribal-card p-5">
                                    <h3 className="font-bold text-primary text-sm mb-3">SDLC Decision</h3>
                                    {!action ? (
                                        <div className="flex gap-3">
                                            <button
                                                onClick={() => setAction("approve")}
                                                className="flex-1 flex items-center justify-center gap-2 py-2.5 bg-emerald-600 text-white rounded-lg text-sm font-semibold hover:bg-emerald-700 transition-colors"
                                            >
                                                <CheckCircle size={15} /> Approve
                                            </button>
                                            <button
                                                onClick={() => setAction("query")}
                                                className="flex-1 flex items-center justify-center gap-2 py-2.5 bg-amber-500 text-white rounded-lg text-sm font-semibold hover:bg-amber-600 transition-colors"
                                            >
                                                <MessageSquare size={15} /> Send Query
                                            </button>
                                            <button
                                                onClick={() => setAction("reject")}
                                                className="flex-1 flex items-center justify-center gap-2 py-2.5 bg-red-500 text-white rounded-lg text-sm font-semibold hover:bg-red-600 transition-colors"
                                            >
                                                <XCircle size={15} /> Reject
                                            </button>
                                        </div>
                                    ) : (
                                        <div>
                                            <div className={`p-3 rounded-lg mb-3 text-sm font-semibold ${action === "approve" ? "bg-emerald-50 text-emerald-800" : action === "reject" ? "bg-red-50 text-red-800" : "bg-amber-50 text-amber-800"}`}>
                                                {action === "approve" ? "✅ Approving claim for DLC review" : action === "reject" ? "❌ Rejecting claim — reason required" : "💬 Querying FRC Officer for additional info"}
                                            </div>
                                            <textarea
                                                value={remarksText}
                                                onChange={(e) => setRemarksText(e.target.value)}
                                                placeholder={`Enter ${action === "approve" ? "approval notes (optional)" : action === "reject" ? "rejection reason (required)" : "query details"}`}
                                                className="w-full text-xs p-3 border border-gray-200 rounded-lg mb-3 resize-none h-20 focus:outline-none focus:border-[#2d8566]"
                                            />
                                            <div className="flex gap-2">
                                                <button
                                                    onClick={() => setAction(null)}
                                                    className="px-4 py-2 text-xs border border-gray-200 rounded-lg hover:bg-gray-50"
                                                >
                                                    Cancel
                                                </button>
                                                <button
                                                    onClick={() => { setAction(null); setRemarksText(""); }}
                                                    className={`flex-1 py-2 text-white text-xs rounded-lg font-semibold ${action === "approve" ? "bg-emerald-600 hover:bg-emerald-700" : action === "reject" ? "bg-red-500 hover:bg-red-600" : "bg-amber-500 hover:bg-amber-600"}`}
                                                >
                                                    <Send size={12} className="inline mr-1" />
                                                    Confirm {action === "approve" ? "Approval" : action === "reject" ? "Rejection" : "Query"}
                                                </button>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="tribal-card p-10 flex flex-col items-center justify-center text-center h-full">
                            <FileText size={40} className="text-gray-200 mb-3" />
                            <p className="text-gray-400 text-sm">Select a claim from the list to review</p>
                        </div>
                    )}
                </div>
            </div>
        </DashboardLayout>
    );
}

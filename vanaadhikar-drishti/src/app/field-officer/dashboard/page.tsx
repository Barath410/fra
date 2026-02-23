"use client";
import React, { useState } from "react";
import {
    MapPin, Camera, Wifi, WifiOff, Upload, CheckCircle, Clock,
    AlertTriangle, FileText, Video, Mic, Navigation, Phone,
    Battery, Signal, User, ChevronRight, Map, Plus,
} from "lucide-react";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { Badge } from "@/components/ui/badge";
import { formatDate } from "@/lib/utils";
import { apiClient } from "@/lib/api-client";
import { ErrorDisplay } from "@/components/error-display";
import { DataTableSkeleton, StatCardSkeleton } from "@/components/skeletons";

export default function FieldOfficerDashboardPage() {
    const [isOffline, setIsOffline] = useState(false);
    const [activeVisit, setActiveVisit] = useState(false);
    const [currentStep, setCurrentStep] = useState(0);

    const pendingVisits = [
        { id: "FV-001", village: "Sonpur Jungle", claimId: "FRA-2026-MP-00342", priority: "high", type: "IFR boundary verification" },
        { id: "FV-002", village: "Laxmipur", claimId: "FRA-2026-MP-00517", priority: "medium", type: "CFR community meeting" },
        { id: "FV-003", village: "Ghinora Tola", claimId: "FRA-2026-OD-00121", priority: "high", type: "PVTG household survey" },
    ];

    const visitSteps = [
        { id: 1, label: "Arrive at Village", icon: <Navigation size={16} />, desc: "Mark GPS arrival point" },
        { id: 2, label: "Identify Claimant", icon: <User size={16} />, desc: "Match Aadhaar / photo ID" },
        { id: 3, label: "Capture GPS Boundary", icon: <Map size={16} />, desc: "Walk perimeter with GPS" },
        { id: 4, label: "Upload Photos/Video", icon: <Camera size={16} />, desc: "Min 4 geotagged photos" },
        { id: 5, label: "Record Community Statement", icon: <Mic size={16} />, desc: "FRC member testimony" },
        { id: 6, label: "Submit Report", icon: <Upload size={16} />, desc: "Auto-sync when online" },
    ];

    return (
        <DashboardLayout role="range-officer" title="Field Officer PWA" titleHi="क्षेत्र अधिकारी">
            {/* PWA Status Bar */}
            <div className={`flex items-center justify-between p-3 rounded-lg mb-5 text-sm ${isOffline ? "bg-amber-50 border border-amber-200" : "bg-emerald-50 border border-emerald-200"}`}>
                <div className="flex items-center gap-2">
                    {isOffline ? <WifiOff size={16} className="text-amber-600" /> : <Wifi size={16} className="text-emerald-600" />}
                    <span className={`font-semibold ${isOffline ? "text-amber-700" : "text-emerald-700"}`}>
                        {isOffline ? "Offline Mode — Changes saved locally" : "Online — All data synced"}
                    </span>
                </div>
                <div className="flex items-center gap-3 text-xs text-gray-500">
                    <span className="flex items-center gap-1"><Battery size={12} /> 84%</span>
                    <span className="flex items-center gap-1"><Signal size={12} /> 4G</span>
                    <button
                        onClick={() => setIsOffline(!isOffline)}
                        className="px-2.5 py-1 rounded border border-gray-200 bg-white text-gray-600 hover:bg-gray-50"
                    >
                        Simulate {isOffline ? "Online" : "Offline"}
                    </button>
                </div>
            </div>

            {/* Offline Warning */}
            {isOffline && (
                <div className="alert-warning mb-5 rounded-lg">
                    <AlertTriangle size={16} className="text-amber-600 flex-shrink-0" />
                    <div>
                        <p className="text-sm font-semibold text-amber-800">Offline Mode Active</p>
                        <p className="text-xs text-amber-600">3 visit reports pending sync · Map tiles cached for Mandla district · Claim forms available offline</p>
                    </div>
                </div>
            )}

            {/* Quick Stats */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-5">
                {[
                    { label: "Pending Visits", value: 3, color: "#F59E0B", icon: <Clock size={16} /> },
                    { label: "Completed Today", value: 2, color: "#22C55E", icon: <CheckCircle size={16} /> },
                    { label: "Photos Uploaded", value: 24, color: "#3B82F6", icon: <Camera size={16} /> },
                    { label: "Claims in Queue", value: 7, color: "#8B5CF6", icon: <FileText size={16} /> },
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

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
                {/* Pending Visit List */}
                <div className="tribal-card overflow-hidden">
                    <div className="p-4 border-b border-gray-100 flex items-center justify-between">
                        <h3 className="font-bold text-[#1a3c2e] text-sm">Assigned Visits</h3>
                        <button className="flex items-center gap-1 text-xs text-[#e87722]">
                            <Plus size={12} /> New
                        </button>
                    </div>
                    <div className="divide-y divide-gray-50">
                        {pendingVisits.map((v) => (
                            <button
                                key={v.id}
                                onClick={() => setActiveVisit(true)}
                                className="w-full text-left p-4 hover:bg-[#f4ede3] transition-colors"
                            >
                                <div className="flex items-start justify-between mb-1">
                                    <span className="text-xs font-bold text-primary">{v.village}</span>
                                    <Badge
                                        variant={v.priority === "high" ? "danger" : "warning"}
                                        size="sm"
                                    >
                                        {v.priority}
                                    </Badge>
                                </div>
                                <p className="text-xs text-gray-500">{v.type}</p>
                                <p className="text-xs font-mono text-gray-400 mt-1">{v.claimId}</p>
                                <div className="flex items-center gap-2 mt-2">
                                    <button className="text-xs bg-primary text-white px-2.5 py-1 rounded flex items-center gap-1 shadow-md">
                                        <Navigation size={10} /> Directions
                                    </button>
                                    <button className="text-xs border border-primary text-primary px-2.5 py-1 rounded flex items-center gap-1 hover:bg-primary-50">
                                        <Phone size={10} /> Contact FRC
                                    </button>
                                </div>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Visit Wizard / Active Visit */}
                <div className="tribal-card overflow-hidden lg:col-span-2">
                    {activeVisit ? (
                        <div>
                            <div className="p-4 border-b border-gray-100 bg-[#f4ede3]">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-xs text-gray-500">Active Visit</p>
                                        <h3 className="font-bold text-primary">Sonpur Jungle — FRA-2026-MP-00342</h3>
                                    </div>
                                    <button
                                        onClick={() => setActiveVisit(false)}
                                        className="text-xs text-gray-500 border border-gray-200 px-2.5 py-1 rounded"
                                    >
                                        Cancel
                                    </button>
                                </div>
                            </div>
                            {/* Progress Steps */}
                            <div className="p-4">
                                <div className="flex items-center gap-1 mb-6 overflow-x-auto pb-2">
                                    {visitSteps.map((step, i) => (
                                        <React.Fragment key={step.id}>
                                            <button
                                                onClick={() => setCurrentStep(i)}
                                                className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all ${i < currentStep
                                                    ? "bg-emerald-500 text-white"
                                                    : i === currentStep
                                                        ? "bg-primary text-white ring-2 ring-offset-1 ring-accent"
                                                        : "bg-gray-100 text-gray-400"
                                                    }`}
                                            >
                                                {i < currentStep ? <CheckCircle size={14} /> : step.id}
                                            </button>
                                            {i < visitSteps.length - 1 && (
                                                <div className={`flex-shrink-0 h-0.5 w-4 ${i < currentStep ? "bg-emerald-400" : "bg-gray-200"}`} />
                                            )}
                                        </React.Fragment>
                                    ))}
                                </div>

                                {/* Active Step Content */}
                                <div className="border-2 border-accent border-dashed rounded-xl p-6 mb-4 text-center">
                                    <div className="w-12 h-12 rounded-full bg-accent/10 flex items-center justify-center mx-auto mb-3 text-accent">
                                        {visitSteps[currentStep].icon}
                                    </div>
                                    <h4 className="font-bold text-primary mb-1">{visitSteps[currentStep].label}</h4>
                                    <p className="text-xs text-gray-500 mb-4">{visitSteps[currentStep].desc}</p>

                                    {currentStep === 0 && (
                                        <div className="space-y-3">
                                            <div className="bg-gray-100 rounded-lg p-3 text-xs font-mono text-gray-600">
                                                📍 GPS: 22.048332 N, 80.381218 E<br />
                                                Accuracy: ±4.2m · Altitude: 643m
                                            </div>
                                            <button
                                                onClick={() => setCurrentStep(1)}
                                                className="w-full py-2.5 bg-primary text-white rounded-lg text-sm font-semibold shadow-md hover:shadow-lg transition-all"
                                            >
                                                Mark Arrival Point
                                            </button>
                                        </div>
                                    )}
                                    {currentStep === 1 && (
                                        <div className="space-y-3">
                                            <input
                                                type="text"
                                                placeholder="Enter Aadhaar last 4 digits or Photo ID"
                                                className="w-full text-sm px-3 py-2 border border-gray-200 rounded-lg text-center"
                                            />
                                            <button
                                                onClick={() => setCurrentStep(2)}
                                                className="w-full py-2.5 bg-primary text-white rounded-lg text-sm font-semibold shadow-md hover:shadow-lg transition-all"
                                            >
                                                Verify Identity
                                            </button>
                                        </div>
                                    )}
                                    {currentStep === 2 && (
                                        <div className="space-y-3">
                                            <div className="bg-emerald-50 rounded-lg p-3 text-xs text-emerald-700">
                                                Walk the perimeter of the claimed land. GPS points will be recorded automatically every 10 seconds.
                                            </div>
                                            <div className="text-xs text-gray-500">4 boundary points recorded so far</div>
                                            <button
                                                onClick={() => setCurrentStep(3)}
                                                className="w-full py-2.5 bg-primary text-white rounded-lg text-sm font-semibold shadow-md hover:shadow-lg transition-all"
                                            >
                                                Complete Boundary Walk
                                            </button>
                                        </div>
                                    )}
                                    {currentStep >= 3 && (
                                        <div className="space-y-3">
                                            {currentStep === 3 && (
                                                <>
                                                    <div className="grid grid-cols-4 gap-2">
                                                        {[1, 2, 3, 4].map((n) => (
                                                            <div key={n} className="aspect-square bg-gray-200 rounded-lg flex items-center justify-center text-gray-400 text-xs">
                                                                {n <= 2 ? "📸" : <Camera size={14} />}
                                                            </div>
                                                        ))}
                                                    </div>
                                                    <button
                                                        onClick={() => setCurrentStep(4)}
                                                        className="w-full py-2.5 bg-primary text-white rounded-lg text-sm font-semibold shadow-md hover:shadow-lg transition-all"
                                                    >
                                                        Upload Photos (2/4)
                                                    </button>
                                                </>
                                            )}
                                            {currentStep === 4 && (
                                                <button
                                                    onClick={() => setCurrentStep(5)}
                                                    className="w-full py-2.5 bg-primary text-white rounded-lg text-sm font-semibold flex items-center justify-center gap-2 shadow-md hover:shadow-lg transition-all"
                                                >
                                                    <Mic size={14} /> Start Recording
                                                </button>
                                            )}
                                            {currentStep === 5 && (
                                                <div className="space-y-3">
                                                    <div className={`p-3 rounded-lg text-sm font-semibold text-center ${isOffline ? "bg-amber-50 text-amber-700" : "bg-emerald-50 text-emerald-700"}`}>
                                                        {isOffline ? "📴 Report saved locally — will sync when online" : "✅ Report ready for immediate upload"}
                                                    </div>
                                                    <button
                                                        onClick={() => { setActiveVisit(false); setCurrentStep(0); }}
                                                        className="w-full py-2.5 bg-emerald-600 text-white rounded-lg text-sm font-semibold flex items-center justify-center gap-2"
                                                    >
                                                        <Upload size={14} /> Submit Visit Report
                                                    </button>
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>

                                {/* Step Navigation */}
                                <div className="flex justify-between">
                                    <button
                                        disabled={currentStep === 0}
                                        onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
                                        className="text-xs px-3 py-1.5 border border-gray-200 rounded-lg disabled:opacity-40"
                                    >
                                        ← Back
                                    </button>
                                    <span className="text-xs text-gray-400 self-center">
                                        Step {currentStep + 1} of {visitSteps.length}
                                    </span>
                                    <button
                                        disabled={currentStep === visitSteps.length - 1}
                                        onClick={() => setCurrentStep(Math.min(visitSteps.length - 1, currentStep + 1))}
                                        className="text-xs px-3 py-1.5 border border-gray-200 rounded-lg disabled:opacity-40"
                                    >
                                        Skip →
                                    </button>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div>
                            <div className="p-4 border-b border-gray-100">
                                <h3 className="font-bold text-primary text-sm">Recent Visit Reports</h3>
                            </div>
                            <div className="divide-y divide-gray-50">
                                {FIELD_VISIT_REPORTS.map((r) => (
                                    <div key={r.id} className="p-4">
                                        <div className="flex items-start justify-between mb-1">
                                            <div>
                                                <p className="font-semibold text-sm text-primary">{r.villageName}</p>
                                                <p className="text-xs text-gray-500">{r.claimId} · {formatDate(r.visitDate)}</p>
                                            </div>
                                            <Badge
                                                variant={r.gpsVerified && r.photosUploaded ? "success" : "warning"}
                                                size="sm"
                                            >
                                                {r.gpsVerified && r.photosUploaded ? "Submitted" : "Pending"}
                                            </Badge>
                                        </div>
                                        <p className="text-xs text-gray-600 mt-1">{r.observations}</p>
                                        <div className="flex items-center gap-3 mt-2 text-xs text-gray-400">
                                            <span className={r.gpsVerified ? "text-emerald-600" : "text-gray-400"}>📍 GPS {r.gpsVerified ? "✓" : "pending"}</span>
                                            <span className={r.photosUploaded ? "text-emerald-600" : "text-gray-400"}>📷 Photos {r.photosUploaded ? "✓" : "pending"}</span>
                                            <span className={r.communityConsentObtained ? "text-emerald-600" : "text-gray-400"}>📋 Consent {r.communityConsentObtained ? "✓" : "pending"}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </DashboardLayout>
    );
}

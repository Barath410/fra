"use client";
import React, { useRef, useState } from "react";
import Link from "next/link";
import {
    Users, FileText, CheckCircle, Upload, Camera, Mic,
    MessageSquare, Book, HelpCircle, Bell, Globe,
    ChevronRight, Info, Scale, MapPin, Clock, AlertTriangle,
    ExternalLink, Download,
} from "lucide-react";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { Badge } from "@/components/ui/badge";
import { DocumentUploadResult, uploadDocumentRequest } from "@/lib/document-upload";
import { apiClient } from "@/lib/api-client";
import { ErrorDisplay } from "@/components/error-display";
import { DataTableSkeleton, StatCardSkeleton } from "@/components/skeletons";

const SCHEMES_INFO = [
    { name: "PM-KISAN", desc: "₹6000/year for patta holders with farmland", eligible: true, enrolled: false },
    { name: "Jal Jeevan Mission", desc: "Tap water connection to every household", eligible: true, enrolled: true },
    { name: "MGNREGA", desc: "100 days guaranteed employment", eligible: true, enrolled: false },
    { name: "PMAY-G", desc: "Pucca house construction support", eligible: true, enrolled: true },
    { name: "PM-JANMAN", desc: "PVTG welfare mission", eligible: false, enrolled: false },
    { name: "EMRS", desc: "Residential school for tribal children", eligible: true, enrolled: true },
];

const RIGHTS_CATEGORIES = [
    { id: "IFR", label: "Individual Forest Rights", labelHi: "व्यक्तिगत वन अधिकार", icon: "🌾", count: 234 },
    { id: "CFR", label: "Community Forest Rights", labelHi: "सामुदायिक वन अधिकार", icon: "🌳", count: 1 },
    { id: "NTFP", label: "NTFP Collection Rights", labelHi: "NTFP संग्रह अधिकार", icon: "🍃", count: 342 },
    { id: "DIVERSION", label: "Conversion/Diversion Rights", labelHi: "परिवर्तन अधिकार", icon: "🏘️", count: 12 },
];

export default function GramSabhaPage() {
    // Default village data (would come from API in production)
    const village = {
        id: "village-001",
        name: "Badel Khas",
        state: "Madhya Pradesh",
        district: "Mandla",
        block: "Samnapur",
        cluster: "Cluster 5",
        population: 340,
        totalFamilies: 68,
        tribalGroups: ["Kol"],
        totalClaims: 234,
        grantedClaims: 189,
        rejectedClaims: 12,
        pendingClaims: 33,
        saturationScore: 85,
        gpsCenter: { lat: 22.45, lng: 81.23 },
        lastUpdated: "2025-02-15"
    };
    const [lang, setLang] = useState<"en" | "hi">("hi");
    const [showNewClaim, setShowNewClaim] = useState(false);
    const [showUploadModal, setShowUploadModal] = useState(false);
    const [activeTab, setActiveTab] = useState<"dashboard" | "claims" | "schemes" | "rights" | "meetings">("dashboard");
    const [uploadFile, setUploadFile] = useState<File | null>(null);
    const [uploadDocType, setUploadDocType] = useState("");
    const [uploadLanguage, setUploadLanguage] = useState("");
    const [uploadStatus, setUploadStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
    const [uploadError, setUploadError] = useState<string | null>(null);
    const [uploadResult, setUploadResult] = useState<DocumentUploadResult | null>(null);
    const uploadInputRef = useRef<HTMLInputElement | null>(null);

    const resetUploadState = () => {
        setUploadFile(null);
        setUploadDocType("");
        setUploadLanguage("");
        setUploadStatus("idle");
        setUploadError(null);
        setUploadResult(null);
        if (uploadInputRef.current) {
            uploadInputRef.current.value = "";
        }
    };

    const handleUploadFilePick = (event: React.ChangeEvent<HTMLInputElement>) => {
        const nextFile = event.target.files?.[0] ?? null;
        setUploadFile(nextFile);
        setUploadError(null);
        setUploadStatus("idle");
    };

    const openUploadModal = () => {
        resetUploadState();
        setShowUploadModal(true);
    };

    const handleUploadSubmit = async () => {
        if (!uploadFile) {
            setUploadError(lang === "hi" ? "कृपया फ़ाइल चुनें" : "Please choose a file first");
            setUploadStatus("error");
            return;
        }
        setUploadError(null);
        setUploadResult(null);
        setUploadStatus("uploading");
        try {
            const result = await uploadDocumentRequest({
                file: uploadFile,
                documentType: uploadDocType || undefined,
                language: uploadLanguage || undefined,
            });
            setUploadResult(result);
            setUploadStatus("success");
        } catch (error) {
            setUploadStatus("error");
            setUploadError(error instanceof Error ? error.message : lang === "hi" ? "अज्ञात त्रुटि" : "Unknown error");
        }
    };

    const handleUploadDrop = (event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        if (event.dataTransfer.files?.[0]) {
            setUploadFile(event.dataTransfer.files[0]);
            setUploadError(null);
            setUploadStatus("idle");
        }
    };

    const tabs = [
        { id: "dashboard", label: lang === "hi" ? "होम" : "Home" },
        { id: "claims", label: lang === "hi" ? "दावे" : "Claims" },
        { id: "schemes", label: lang === "hi" ? "योजनाएं" : "Schemes" },
        { id: "rights", label: lang === "hi" ? "अधिकार" : "Rights" },
        { id: "meetings", label: lang === "hi" ? "बैठकें" : "Meetings" },
    ] as const;

    return (
        <DashboardLayout role="gram-sabha" title="Gram Sabha Portal" titleHi="ग्राम सभा पोर्टल">
            {/* Language Toggle */}
            <div className="flex items-center justify-between mb-5">
                <div>
                    <h1 className="text-xl font-bold text-primary">
                        {lang === "hi" ? `${village.name} — ग्राम सभा पोर्टल` : `${village.name} — Gram Sabha Portal`}
                    </h1>
                    <p className="text-xs text-gray-500">
                        {lang === "hi"
                            ? `${village.block} ब्लॉक, ${village.district} जिला, मध्यप्रदेश`
                            : `${village.block} Block, ${village.district} District, MP`}
                    </p>
                </div>
                <div className="flex items-center gap-2">
                    <button
                        onClick={() => setLang("hi")}
                        className={`lang-btn ${lang === "hi" ? "active" : ""}`}
                    >
                        हिंदी
                    </button>
                    <button
                        onClick={() => setLang("en")}
                        className={`lang-btn ${lang === "en" ? "active" : ""}`}
                    >
                        English
                    </button>
                </div>
            </div>

            {/* Village Summary Strip */}
            <div className="grid grid-cols-2 lg:grid-cols-5 gap-3 mb-5">
                {[
                    { label: lang === "hi" ? "कुल परिवार" : "Total Households", value: village.totalHouseholds, color: "#3B82F6" },
                    { label: lang === "hi" ? "पट्टेदार" : "Patta Holders", value: village.grantedClaims, color: "#22C55E" },
                    { label: lang === "hi" ? "लंबित दावे" : "Pending Claims", value: village.totalClaims - village.grantedClaims, color: "#F59E0B" },
                    { label: lang === "hi" ? "IFR क्षेत्र (एकड़)" : "IFR Area (Acres)", value: village.ifrGrantedArea.toFixed(1), color: "#6366F1" },
                    { label: lang === "hi" ? "CFR क्षेत्र (एकड़)" : "CFR Area (Acres)", value: village.cfrGrantedArea.toFixed(1), color: "#16A34A" },
                ].map((s) => (
                    <div key={s.label} className="tribal-card p-3 text-center">
                        <p className="text-2xl font-bold" style={{ color: s.color }}>{s.value}</p>
                        <p className="text-xs text-gray-500 mt-0.5">{s.label}</p>
                    </div>
                ))}
            </div>

            {/* Tabs */}
            <div className="flex gap-1 mb-5 overflow-x-auto bg-gray-100 p-1 rounded-lg w-fit no-print">
                {tabs.map((t) => (
                    <button
                        key={t.id}
                        onClick={() => setActiveTab(t.id)}
                        className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all whitespace-nowrap ${activeTab === t.id ? "bg-white text-primary shadow-md" : "text-gray-500 hover:text-gray-700"}`}
                    >
                        {t.label}
                    </button>
                ))}
            </div>

            {/* Dashboard Tab */}
            {activeTab === "dashboard" && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
                    {/* Quick Actions */}
                    <div className="tribal-card p-5">
                        <h3 className="font-bold text-[#1a3c2e] text-sm mb-4">
                            {lang === "hi" ? "त्वरित कार्रवाई" : "Quick Actions"}
                        </h3>
                        <div className="grid grid-cols-2 gap-3">
                            {[
                                { icon: <FileText size={20} />, label: lang === "hi" ? "नया दावा" : "New Claim", color: "#4F46E5", action: () => setShowNewClaim(true) },
                                { icon: <Upload size={20} />, label: lang === "hi" ? "दस्तावेज़" : "Upload Doc", color: "#16A34A", action: openUploadModal },
                                { icon: <MessageSquare size={20} />, label: lang === "hi" ? "शिकायत" : "Grievance", color: "#F59E0B" },
                                { icon: <CheckCircle size={20} />, label: lang === "hi" ? "स्थिति जानें" : "Check Status", color: "#0D9488" },
                            ].map((a) => (
                                <button
                                    key={a.label}
                                    onClick={() => a.action?.()}
                                    className="flex flex-col items-center justify-center p-4 rounded-xl border-2 border-dashed hover:border-solid transition-all"
                                    style={{ borderColor: `${a.color}40`, background: `${a.color}08` }}
                                >
                                    <div style={{ color: a.color }}>{a.icon}</div>
                                    <span className="text-xs font-semibold mt-2 text-gray-700">{a.label}</span>
                                </button>
                            ))}
                        </div>
                        <div className="mt-4 pt-4 border-t border-gray-100">
                            <p className="text-xs font-semibold text-gray-600 mb-2">
                                {lang === "hi" ? "हेल्पलाइन" : "Helpline"}
                            </p>
                            <a href="tel:1800-11-0130" className="flex items-center gap-2 text-sm text-accent font-bold hover:underline">
                                📞 1800-11-0130 (Toll Free)
                            </a>
                            <p className="text-xs text-gray-400 mt-0.5">
                                {lang === "hi" ? "सोम–शनि, सुबह 9 से शाम 5 बजे" : "Mon–Sat, 9AM–5PM"}
                            </p>
                        </div>
                    </div>

                    {/* Village Rights Status */}
                    <div className="tribal-card p-5 lg:col-span-2">
                        <h3 className="font-bold text-primary text-sm mb-4">
                            {lang === "hi" ? "अधिकारों का उपयोग (ग्राम)" : "Rights Utilization"}
                        </h3>
                        <div className="grid grid-cols-2 gap-3">
                            {RIGHTS_CATEGORIES.map((r) => (
                                <div key={r.id} className="p-3 bg-[#f4ede3] rounded-xl">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-2xl">{r.icon}</span>
                                        <Badge variant="info" size="sm">{r.count}</Badge>
                                    </div>
                                    <p className="text-xs font-bold text-primary">{lang === "hi" ? r.labelHi : r.label}</p>
                                    <p className="text-xs text-gray-400">{r.id}</p>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Pending Notices */}
                    <div className="tribal-card p-5 lg:col-span-3">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="font-bold text-primary text-sm">
                                {lang === "hi" ? "लंबित सूचनाएं / नोटिस" : "Pending Notices"}
                            </h3>
                            <Badge variant="danger" size="sm">3 urgent</Badge>
                        </div>
                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-3">
                            {[
                                { type: "FRC Meeting", date: "Jan 15, 2026", desc: "IFR claim verification for Ramcharan Banjara — boundary walk required", urgent: true },
                                { type: "Scheme Enrollment", date: "Jan 20, 2026", desc: "Deadline: PM-KISAN enrollment for 36 patta-holder households", urgent: true },
                                { type: "Document Submission", date: "Feb 5, 2026", desc: "Submit updated CFR boundary map (revised survey)", urgent: false },
                            ].map((n, i) => (
                                <div
                                    key={i}
                                    className={`p-3 rounded-xl border ${n.urgent ? "border-red-200 bg-red-50" : "border-gray-200 bg-gray-50"}`}
                                >
                                    <div className="flex items-center gap-2 mb-1">
                                        <Bell size={12} className={n.urgent ? "text-red-500" : "text-gray-400"} />
                                        <span className={`text-xs font-bold ${n.urgent ? "text-red-700" : "text-gray-600"}`}>{n.type}</span>
                                    </div>
                                    <p className="text-xs text-gray-600">{n.desc}</p>
                                    <p className="text-xs text-gray-400 mt-1">{n.date}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* Claims Tab */}
            {activeTab === "claims" && (
                <div className="space-y-4">
                    <div className="flex items-center justify-between">
                        <h3 className="font-semibold text-primary">
                            {lang === "hi" ? "ग्राम के सभी दावे" : "All Village Claims"}
                        </h3>
                        <button
                            onClick={() => setShowNewClaim(true)}
                            className="flex items-center gap-2 text-xs bg-accent text-white px-4 py-2 rounded-lg shadow-md hover:shadow-lg transition-all"
                        >
                            <FileText size={13} /> {lang === "hi" ? "नया दावा दर्ज करें" : "File New Claim"}
                        </button>
                    </div>
                    {SAMPLE_CLAIMS.map((c) => (
                        <div key={c.id} className="tribal-card p-4">
                            <div className="flex items-start justify-between">
                                <div>
                                    <div className="flex items-center gap-2 mb-0.5">
                                        <span className="font-mono text-xs text-gray-400">{c.id}</span>
                                        <Badge variant={c.claimType === "IFR" ? "info" : "success"} size="sm">{c.claimType}</Badge>
                                        {c.isPVTG && <Badge variant="warning" size="sm">PVTG</Badge>}
                                    </div>
                                    <p className="font-bold text-primary">{c.claimantName}</p>
                                    <p className="text-xs text-gray-500">{c.areaAcres} acres · {c.claimDate}</p>
                                </div>
                                <div className="text-right">
                                    <span className={`text-xs px-2 py-1 rounded-full font-medium border capitalize ${c.status === "granted" ? "bg-emerald-50 text-emerald-700 border-emerald-200" :
                                        c.status === "rejected" ? "bg-red-50 text-red-700 border-red-200" :
                                            "bg-amber-50 text-amber-700 border-amber-200"
                                        }`}>
                                        {lang === "hi"
                                            ? c.status === "granted" ? "अनुदत्त" : c.status === "rejected" ? "अस्वीकृत" : "प्रक्रियाधीन"
                                            : c.status.replace(/-/g, " ")}
                                    </span>
                                </div>
                            </div>
                            {c.status !== "granted" && c.status !== "rejected" && (
                                <div className="mt-3 pt-3 border-t border-gray-100">
                                    <p className="text-xs text-gray-500 mb-1">
                                        {lang === "hi" ? "अगला चरण:" : "Next step:"}
                                    </p>
                                    <p className="text-xs font-semibold text-primary">
                                        {c.status === "received" ? (lang === "hi" ? "FRC जमीन सत्यापन की प्रतीक्षा" : "Awaiting FRC land verification") :
                                            c.status === "frc-verified" ? (lang === "hi" ? "SDLC समिति समीक्षा" : "SDLC committee review") :
                                                lang === "hi" ? "DLC अनुमोदन प्रक्रिया" : "DLC approval processing"}
                                    </p>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}

            {/* Schemes Tab */}
            {activeTab === "schemes" && (
                <div className="space-y-3">
                    <div className="alert-info rounded-lg mb-4">
                        <Info size={16} className="text-blue-500 flex-shrink-0" />
                        <p className="text-sm text-blue-700">
                            {lang === "hi"
                                ? "ये योजनाएं पट्टाधारियों के लिए उपलब्ध हैं। अपात्र योजनाओं के लिए अधिकारी से संपर्क करें।"
                                : "These schemes are available to patta holders in your village. Contact officer for ineligible schemes."}
                        </p>
                    </div>
                    {SCHEMES_INFO.map((s) => (
                        <div key={s.name} className={`tribal-card p-4 ${!s.eligible ? "opacity-60" : ""}`}>
                            <div className="flex items-start justify-between">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                        <span className="font-bold text-primary">{s.name}</span>
                                        {s.enrolled && <Badge variant="success" size="sm">{lang === "hi" ? "नामांकित" : "Enrolled"}</Badge>}
                                        {s.eligible && !s.enrolled && <Badge variant="warning" size="sm">{lang === "hi" ? "नामांकन बाकी" : "Not Enrolled"}</Badge>}
                                        {!s.eligible && <Badge variant="neutral" size="sm">{lang === "hi" ? "अपात्र" : "Ineligible"}</Badge>}
                                    </div>
                                    <p className="text-xs text-gray-600">{s.desc}</p>
                                </div>
                                {s.eligible && !s.enrolled && (
                                    <button className="text-xs bg-accent text-white px-3 py-1.5 rounded-lg ml-3 flex-shrink-0 shadow-md hover:shadow-lg transition-all">
                                        {lang === "hi" ? "आवेदन करें" : "Apply Now"}
                                    </button>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Rights Info Tab */}
            {activeTab === "rights" && (
                <div className="space-y-4">
                    <div className="tribal-card p-5">
                        <h3 className="font-bold text-primary mb-3">
                            {lang === "hi" ? "वन अधिकार अधिनियम 2006 — मूल बातें" : "Forest Rights Act 2006 — Key Points"}
                        </h3>
                        <div className="space-y-3">
                            {[
                                { q: "Who can claim rights?", a: "Scheduled Tribes and Other Traditional Forest Dwellers who have been cultivating forest land before Dec 13, 2005", qHi: "कौन अधिकार माँग सकता है?", aHi: "अनुसूचित जनजाति और अन्य पारंपरिक वन निवासी जो 13 दिसंबर 2005 से पहले वन भूमि पर खेती कर रहे थे" },
                                { q: "What documents are needed?", a: "Village records, traditional ownership proof, Aadhaar, community testimony, 3 generations of occupation evidence", qHi: "कौन से दस्तावेज़ चाहिए?", aHi: "ग्राम अभिलेख, पारंपरिक स्वामित्व प्रमाण, आधार, सामुदायिक गवाही, 3 पीढ़ी के कब्जे के साक्ष्य" },
                                { q: "What is the process?", a: "FRC → SDLC Committee → DLC Committee → Collector → Patta Grant", qHi: "प्रक्रिया क्या है?", aHi: "FRC → SDLC समिति → DLC समिति → कलेक्टर → पट्टा प्रदान" },
                                { q: "What if claim is rejected?", a: "You can file an appeal with the Sub-Divisional Level Committee within 60 days of rejection notice", qHi: "यदि दावा अस्वीकृत हो जाए?", aHi: "अस्वीकृति नोटिस के 60 दिनों के भीतर SDLC में अपील दे सकते हैं" },
                            ].map((item) => (
                                <div key={item.q} className="border border-gray-100 rounded-xl overflow-hidden">
                                    <div className="p-3 bg-accent/5">
                                        <p className="text-sm font-bold text-primary">{lang === "hi" ? item.qHi : item.q}</p>
                                    </div>
                                    <div className="p-3">
                                        <p className="text-xs text-gray-600">{lang === "hi" ? item.aHi : item.a}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* Meetings Tab */}
            {activeTab === "meetings" && (
                <div className="space-y-4">
                    <div className="tribal-card p-5">
                        <h3 className="font-bold text-[#1a3c2e] text-sm mb-4">
                            {lang === "hi" ? "ग्राम सभा की आगामी बैठकें" : "Upcoming Gram Sabha Meetings"}
                        </h3>
                        {[
                            { date: "Jan 15, 2026", time: "10:00 AM", subject: "IFR Claim Verification — Ramcharan Banjara & 5 others", venue: "Panchayat Bhawan", mandatory: true },
                            { date: "Jan 22, 2026", time: "11:00 AM", subject: "CFR Plan Finalization — Sonpur Forest Block", venue: "Community Hall", mandatory: true },
                            { date: "Feb 5, 2026", time: "9:30 AM", subject: "Scheme Enrollment Camp — PM-KISAN, MGNREGA", venue: "School Ground", mandatory: false },
                        ].map((m, i) => (
                            <div key={i} className={`p-4 rounded-xl mb-3 border ${m.mandatory ? "border-accent bg-accent/5" : "border-gray-200 bg-gray-50"}`}>
                                <div className="flex items-start justify-between mb-2">
                                    <div>
                                        <div className="flex items-center gap-2 mb-1">
                                            <span className="text-sm font-bold text-primary">{m.date}</span>
                                            <span className="text-xs text-gray-500">{m.time}</span>
                                            {m.mandatory && <Badge variant="warning" size="sm">{lang === "hi" ? "अनिवार्य" : "Mandatory"}</Badge>}
                                        </div>
                                        <p className="text-xs font-semibold text-gray-700">{m.subject}</p>
                                        <p className="text-xs text-gray-400 mt-0.5">📍 {m.venue}</p>
                                    </div>
                                    <button className="text-xs border border-gray-200 px-2.5 py-1 rounded-lg hover:bg-gray-100">
                                        <Download size={11} className="inline mr-1" />
                                        Notice
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Document Upload Modal */}
            {showUploadModal && (
                <div className="fixed inset-0 bg-black/50 z-50 flex items-end lg:items-center justify-center p-4">
                    <div className="bg-white rounded-2xl w-full max-w-xl max-h-[80vh] overflow-y-auto">
                        <div className="p-5 border-b border-gray-100 flex items-center justify-between">
                            <h3 className="font-bold text-primary">
                                {lang === "hi" ? "सहायक दस्तावेज़ अपलोड करें" : "Upload Supporting Documents"}
                            </h3>
                            <button onClick={() => { setShowUploadModal(false); resetUploadState(); }} className="text-gray-400 hover:text-gray-600 text-xl">×</button>
                        </div>
                        <div className="p-5 space-y-4">
                            <p className="text-xs text-gray-500">
                                {lang === "hi"
                                    ? "AI आधारित सत्यापन के लिए पट्टा दावा दस्तावेज़ अपलोड करें।"
                                    : "Submit claim paperwork for AI-based verification."}
                            </p>
                            <input
                                ref={uploadInputRef}
                                type="file"
                                accept="application/pdf,image/*"
                                className="hidden"
                                onChange={handleUploadFilePick}
                            />
                            <div
                                className="border-2 border-dashed border-gray-200 rounded-xl p-5 text-center cursor-pointer hover:border-primary transition"
                                onClick={() => uploadInputRef.current?.click()}
                                onDragOver={(e) => e.preventDefault()}
                                onDrop={handleUploadDrop}
                            >
                                <Upload size={24} className="mx-auto mb-2 text-primary" />
                                <p className="text-sm font-semibold text-primary">
                                    {uploadFile ? uploadFile.name : lang === "hi" ? "यहाँ क्लिक करें या फ़ाइल गिराएँ" : "Click or drop a file"}
                                </p>
                                <p className="text-xs text-gray-500">
                                    {lang === "hi" ? "PDF, JPG या PNG • अधिकतम 15 MB" : "PDF, JPG or PNG • up to 15 MB"}
                                </p>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                <div>
                                    <label className="form-label">{lang === "hi" ? "दस्तावेज़ प्रकार" : "Document Type"}</label>
                                    <input
                                        type="text"
                                        className="form-input"
                                        value={uploadDocType}
                                        onChange={(e) => setUploadDocType(e.target.value)}
                                        placeholder={lang === "hi" ? "जैसे: Form-A" : "e.g., Form-A"}
                                    />
                                </div>
                                <div>
                                    <label className="form-label">{lang === "hi" ? "भाषा" : "Language"}</label>
                                    <select
                                        className="form-input"
                                        value={uploadLanguage}
                                        onChange={(e) => setUploadLanguage(e.target.value)}
                                    >
                                        <option value="">{lang === "hi" ? "स्वचालित" : "Auto Detect"}</option>
                                        <option value="hi">हिंदी</option>
                                        <option value="en">English</option>
                                        <option value="mr">Marathi</option>
                                        <option value="or">Odia</option>
                                        <option value="bn">Bengali</option>
                                    </select>
                                </div>
                            </div>
                            {uploadError && (
                                <div className="p-3 bg-red-50 text-red-600 text-xs rounded-lg">{uploadError}</div>
                            )}
                            {uploadResult && (
                                <div className="p-3 bg-emerald-50 text-emerald-700 text-xs rounded-lg space-y-1">
                                    <p className="font-semibold">{lang === "hi" ? "सफलतापूर्वक अपलोड हुआ" : "Upload successful"}</p>
                                    <p>ID #{uploadResult.document_id} • {uploadResult.document_type ?? "-"}</p>
                                    <p>{lang === "hi" ? "स्थिति" : "Status"}: {uploadResult.processing_status}</p>
                                </div>
                            )}
                            <button
                                onClick={handleUploadSubmit}
                                disabled={uploadStatus === "uploading"}
                                className="w-full py-3 bg-primary text-white rounded-xl font-bold shadow-lg hover:shadow-xl transition disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {uploadStatus === "uploading"
                                    ? lang === "hi" ? "अपलोड हो रहा है..." : "Uploading..."
                                    : lang === "hi" ? "सबमिट करें" : "Submit"}
                            </button>
                            {uploadStatus === "uploading" && (
                                <p className="text-center text-xs text-gray-500">
                                    {lang === "hi" ? "कृपया प्रतीक्षा करें" : "Please wait"}
                                </p>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* New Claim Modal */}
            {showNewClaim && (
                <div className="fixed inset-0 bg-black/50 z-50 flex items-end lg:items-center justify-center p-4">
                    <div className="bg-white rounded-2xl w-full max-w-xl max-h-[80vh] overflow-y-auto">
                        <div className="p-5 border-b border-gray-100 flex items-center justify-between">
                            <h3 className="font-bold text-primary">
                                {lang === "hi" ? "नया दावा दर्ज करें" : "File New FRA Claim"}
                            </h3>
                            <button onClick={() => setShowNewClaim(false)} className="text-gray-400 hover:text-gray-600 text-xl">×</button>
                        </div>
                        <div className="p-5 space-y-4">
                            <div>
                                <label className="form-label">{lang === "hi" ? "दावेदार का नाम *" : "Claimant Name *"}</label>
                                <input type="text" className="form-input" placeholder={lang === "hi" ? "पूरा नाम" : "Full name"} />
                            </div>
                            <div>
                                <label className="form-label">{lang === "hi" ? "जनजाति का नाम *" : "Tribal Community *"}</label>
                                <select className="form-input">
                                    <option>Gond</option><option>Baiga</option><option>Bhil</option><option>Korku</option>
                                </select>
                            </div>
                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label className="form-label">{lang === "hi" ? "अधिकार प्रकार *" : "Claim Type *"}</label>
                                    <select className="form-input">
                                        <option value="IFR">{lang === "hi" ? "व्यक्तिगत (IFR)" : "Individual (IFR)"}</option>
                                        <option value="CFR">{lang === "hi" ? "सामुदायिक (CFR)" : "Community (CFR)"}</option>
                                    </select>
                                </div>
                                <div>
                                    <label className="form-label">{lang === "hi" ? "क्षेत्रफल (एकड़) *" : "Area (acres) *"}</label>
                                    <input type="number" className="form-input" placeholder="e.g. 2.5" />
                                </div>
                            </div>
                            <div>
                                <label className="form-label">{lang === "hi" ? "दस्तावेज़ अपलोड करें" : "Upload Documents"}</label>
                                <div className="dropzone text-center text-xs text-gray-500">
                                    <Upload size={20} className="mx-auto mb-1 text-gray-300" />
                                    {lang === "hi" ? "फ़ाइलें यहाँ खींचें या क्लिक करें" : "Drop files here or click to browse"}
                                </div>
                            </div>
                            <button
                                onClick={() => setShowNewClaim(false)}
                                className="w-full py-3 bg-accent text-white rounded-xl font-bold shadow-lg hover:shadow-xl transition-all"
                            >
                                {lang === "hi" ? "दावा जमा करें" : "Submit Claim"}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </DashboardLayout>
    );
}


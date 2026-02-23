"use client";
import React, { useRef, useState } from "react";
import {
    Search, FileText, Download, MapPin, Calendar,
    CheckCircle, Clock, XCircle, AlertTriangle, Smartphone,
    Eye, Star, Share2, Bell, HelpCircle, Phone,
    Upload, ChevronRight, Scale, MessageSquare, Globe,
} from "lucide-react";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { Badge } from "@/components/ui/badge";
import { getStatusColor, formatDate } from "@/lib/utils";
import { DocumentUploadResult, uploadDocumentRequest } from "@/lib/document-upload";
import { apiClient } from "@/lib/api-client";
import { ErrorDisplay } from "@/components/error-display";

export default function MeraPattaPage() {
    const [lang, setLang] = useState<"en" | "hi">("hi");
    const [searchQuery, setSearchQuery] = useState("");
    const [activeTab, setActiveTab] = useState<"search" | "track" | "grievance" | "info">("search");
    const [claimId, setClaimId] = useState("");
    const [mobileNumber, setMobileNumber] = useState("");
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [documentTypeInput, setDocumentTypeInput] = useState("");
    const [documentLanguage, setDocumentLanguage] = useState("");
    const [uploadStatus, setUploadStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
    const [uploadResult, setUploadResult] = useState<DocumentUploadResult | null>(null);
    const [uploadError, setUploadError] = useState<string | null>(null);
    const [searchResults, setSearchResults] = useState<any[]>([]);
    const [searchLoading, setSearchLoading] = useState(false);
    const [searchError, setSearchError] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement | null>(null);

    const tabs = [
        { id: "search", label: lang === "hi" ? "अपना पट्टा खोजें" : "Find Patta", icon: <Search size={14} /> },
        { id: "track", label: lang === "hi" ? "स्थिति जांचें" : "Track Status", icon: <Eye size={14} /> },
        { id: "grievance", label: lang === "hi" ? "शिकायत दर्ज करें" : "File Grievance", icon: <MessageSquare size={14} /> },
        { id: "info", label: lang === "hi" ? "जानकारी" : "Information", icon: <HelpCircle size={14} /> },
    ] as const;

    const handleSearch = async () => {
        if (!searchQuery.trim()) {
            setSearchError(lang === "hi" ? "कृपया खोज क्वेरी दर्ज करें" : "Please enter a search query");
            return;
        }

        setSearchLoading(true);
        setSearchError(null);
        setSearchResults([]);

        try {
            const response = await apiClient.getClaims(1, 5, { claimantName: searchQuery });
            if (response.error) {
                setSearchError(response.error);
            } else if (response.data?.items && response.data.items.length > 0) {
                setSearchResults(response.data.items);
            } else {
                setSearchError(lang === "hi" ? "कोई पट्टा नहीं मिला" : "No patta found");
            }
        } catch (err) {
            setSearchError(err instanceof Error ? err.message : lang === "hi" ? "खोज विफल रही" : "Search failed");
        } finally {
            setSearchLoading(false);
        }
    };

    const handleFilePick = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            setSelectedFile(file);
            setUploadError(null);
            setUploadStatus("idle");
        }
    };

    const triggerFileDialog = () => {
        fileInputRef.current?.click();
    };

    const handleDocumentUpload = async () => {
        if (!selectedFile) {
            setUploadError(lang === "hi" ? "कृपया पहले फ़ाइल चुनें" : "Please select a file first");
            setUploadStatus("error");
            return;
        }

        setUploadError(null);
        setUploadResult(null);
        setUploadStatus("uploading");

        try {
            const data = await uploadDocumentRequest({
                file: selectedFile,
                documentType: documentTypeInput || undefined,
                language: documentLanguage || undefined,
            });
            setUploadResult(data);
            setUploadStatus("success");
        } catch (error) {
            setUploadStatus("error");
            setUploadError(error instanceof Error ? error.message : lang === "hi" ? "अज्ञात त्रुटि" : "Unknown error");
        }
    };

    return (
        <DashboardLayout role="citizen" title="Mera Patta — Citizen Portal" titleHi="मेरा पट्टा — नागरिक पोर्टल">
            {/* Hero Header */}
            <div className="bg-gradient-to-r from-[#1a3c2e] to-[#2d8566] rounded-2xl p-6 mb-6 text-white">
                <div className="flex items-center justify-between mb-3">
                    <div>
                        <h1 className="text-2xl font-bold mb-1">
                            {lang === "hi" ? "मेरा पट्टा — नागरिक पोर्टल" : "Mera Patta — Citizen Portal"}
                        </h1>
                        <p className="text-sm opacity-90">
                            {lang === "hi"
                                ? "वन अधिकार अधिनियम (FRA) — अपना पट्टा खोजें और स्थिति जांचें"
                                : "Forest Rights Act (FRA) — Search your patta and track status"}
                        </p>
                    </div>
                    <div className="flex items-center gap-2">
                        <button
                            onClick={() => setLang("hi")}
                            className={`px-3 py-1.5 rounded-lg text-sm font-semibold transition-all ${lang === "hi" ? "bg-white text-primary shadow-md" : "bg-white/20 hover:bg-white/30"}`}
                        >
                            हिंदी
                        </button>
                        <button
                            onClick={() => setLang("en")}
                            className={`px-3 py-1.5 rounded-lg text-sm font-semibold transition-all ${lang === "en" ? "bg-white text-primary shadow-md" : "bg-white/20 hover:bg-white/30"}`}
                        >
                            English
                        </button>
                    </div>
                </div>

                {/* Quick Stats */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
                    {[
                        { label: lang === "hi" ? "कुल पट्टे जारी" : "Total Pattas Issued", value: "24.2 L" },
                        { label: lang === "hi" ? "राज्य" : "States Covered", value: "28" },
                        { label: lang === "hi" ? "औसत प्रोसेसिंग समय" : "Avg Processing", value: "127 days" },
                        { label: lang === "hi" ? "हेल्पलाइन" : "Helpline", value: "1800-110-130" },
                    ].map((s) => (
                        <div key={s.label} className="bg-white/10 backdrop-blur-sm rounded-lg p-3 text-center">
                            <p className="text-xl font-bold">{s.value}</p>
                            <p className="text-xs opacity-80 mt-0.5">{s.label}</p>
                        </div>
                    ))}
                </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 mb-5 overflow-x-auto bg-gray-100 p-1 rounded-xl no-print">
                {tabs.map((t) => (
                    <button
                        key={t.id}
                        onClick={() => setActiveTab(t.id)}
                        className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${activeTab === t.id ? "bg-white text-primary shadow-md" : "text-gray-500 hover:text-gray-700"}`}
                    >
                        {t.icon}
                        {t.label}
                    </button>
                ))}
            </div>

            {/* Search Tab */}
            {activeTab === "search" && (
                <div className="max-w-3xl mx-auto">
                    <div className="tribal-card p-6">
                        <h3 className="font-bold text-primary text-lg mb-4 text-center">
                            {lang === "hi" ? "🔍 अपना पट्टा खोजें" : "🔍 Search Your Patta"}
                        </h3>
                        <p className="text-sm text-gray-600 text-center mb-6">
                            {lang === "hi"
                                ? "अपना पट्टा नंबर, नाम, आधार नंबर या मोबाइल नंबर से खोजें"
                                : "Search using Patta Number, Name, Aadhaar or Mobile Number"}
                        </p>

                        <div className="space-y-4">
                            {/* Search Input */}
                            <div className="relative">
                                <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                                <input
                                    type="text"
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    placeholder={lang === "hi" ? "पट्टा नंबर, नाम, आधार या मोबाइल..." : "Patta ID, Name, Aadhaar or Mobile..."}
                                    className="w-full pl-11 pr-4 py-3 text-sm border-2 border-gray-200 rounded-xl focus:outline-none focus:border-primary"
                                />
                            </div>

                            {/* State Filter */}
                            <div>
                                <label className="form-label">
                                    {lang === "hi" ? "राज्य चुनें (वैकल्पिक)" : "Select State (Optional)"}
                                </label>
                                <select className="form-input">
                                    <option value="">{lang === "hi" ? "सभी राज्य" : "All States"}</option>
                                    {[
                                        { id: "mp", name: "Madhya Pradesh" },
                                        { id: "cg", name: "Chhattisgarh" },
                                        { id: "jh", name: "Jharkhand" },
                                        { id: "od", name: "Odisha" },
                                        { id: "as", name: "Assam" },
                                        { id: "tr", name: "Tripura" },
                                        { id: "mz", name: "Mizoram" }
                                    ].map((s) => (
                                        <option key={s.id} value={s.id}>{s.name}</option>
                                    ))}
                                </select>
                            </div>

                            <button className="w-full py-3 bg-gradient-to-r from-primary via-primary-600 to-primary-700 text-white rounded-xl font-bold text-sm shadow-md hover:shadow-lg transition-all">
                                {lang === "hi" ? "खोजें" : "Search Patta"}
                            </button>
                        </div>

                        {/* Sample Result */}
                        {searchQuery && (
                            <div className="mt-6 border-t border-gray-100 pt-5">
                                <p className="text-xs font-semibold text-gray-500 mb-3">
                                    {lang === "hi" ? "खोज परिणाम (1)" : "Search Results (1)"}
                                </p>
                                <div className="patta-certificate">
                                    <div className="mb-4 border-b-2 border-accent pb-3">
                                        <div className="flex items-center justify-between mb-2">
                                            <div className="flex items-center gap-2">
                                                <img src="/emblem.svg" alt="Emblem" className="w-8 h-8" onError={(e) => e.currentTarget.style.display = 'none'} />
                                                <div>
                                                    <p className="text-xs font-semibold text-gray-700">भारत सरकार / Government of India</p>
                                                    <p className="text-xs text-gray-500">जनजातीय कार्य मंत्रालय / Ministry of Tribal Affairs</p>
                                                </div>
                                            </div>
                                            <Badge variant="success">
                                                {lang === "hi" ? "अनुदत्त" : "GRANTED"}
                                            </Badge>
                                        </div>
                                        <h4 className="text-lg font-bold text-primary text-center">
                                            {lang === "hi" ? "वन अधिकार पट्टा" : "Forest Rights Patta"}
                                        </h4>
                                    </div>

                                    <div className="grid grid-cols-2 gap-3 text-sm mb-4">
                                        <div>
                                            <p className="text-xs text-gray-500">{lang === "hi" ? "पट्टा संख्या" : "Patta Number"}</p>
                                            <p className="font-mono font-bold text-primary">{sampleClaim.id}</p>
                                        </div>
                                        <div>
                                            <p className="text-xs text-gray-500">{lang === "hi" ? "दावेदार का नाम" : "Claimant Name"}</p>
                                            <p className="font-bold text-primary">{sampleClaim.claimantName}</p>
                                        </div>
                                        <div>
                                            <p className="text-xs text-gray-500">{lang === "hi" ? "गांव" : "Village"}</p>
                                            <p className="font-semibold text-gray-700">{sampleClaim.villageName}</p>
                                        </div>
                                        <div>
                                            <p className="text-xs text-gray-500">{lang === "hi" ? "जिला" : "District"}</p>
                                            <p className="font-semibold text-gray-700">{sampleClaim.district}</p>
                                        </div>
                                        <div>
                                            <p className="text-xs text-gray-500">{lang === "hi" ? "अधिकार प्रकार" : "Rights Type"}</p>
                                            <Badge variant={sampleClaim.claimType === "IFR" ? "info" : "success"}>{sampleClaim.claimType}</Badge>
                                        </div>
                                        <div>
                                            <p className="text-xs text-gray-500">{lang === "hi" ? "क्षेत्रफल" : "Area"}</p>
                                            <p className="font-bold text-primary">{sampleClaim.areaAcres} acres</p>
                                        </div>
                                    </div>

                                    <div className="flex gap-2">
                                        <button className="flex-1 flex items-center justify-center gap-2 py-2 bg-accent text-white rounded-lg text-xs font-semibold shadow-md hover:shadow-lg transition-all">
                                            <Download size={13} /> {lang === "hi" ? "पट्टा डाउनलोड करें" : "Download Patta"}
                                        </button>
                                        <button className="flex-1 flex items-center justify-center gap-2 py-2 border-2 border-primary text-primary rounded-lg text-xs font-semibold hover:bg-primary-50 transition-all">
                                            <Share2 size={13} /> {lang === "hi" ? "साझा करें" : "Share"}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Instructions */}
                    <div className="tribal-card p-5 mt-5">
                        <h4 className="font-bold text-[#1a3c2e] text-sm mb-3">
                            {lang === "hi" ? "📌 महत्वपूर्ण निर्देश" : "📌 Important Instructions"}
                        </h4>
                        <ul className="space-y-2 text-xs text-gray-600">
                            <li className="flex items-start gap-2">
                                <span className="text-[#e87722] mt-0.5">•</span>
                                <span>{lang === "hi" ? "पट्टा नंबर FRA-YYYY-ST-XXXXX प्रारूप में होता है (जैसे: FRA-2026-MP-00342)" : "Patta format: FRA-YYYY-ST-XXXXX (e.g., FRA-2026-MP-00342)"}</span>
                            </li>
                            <li className="flex items-start gap-2">
                                <span className="text-[#e87722] mt-0.5">•</span>
                                <span>{lang === "hi" ? "यदि पट्टा नहीं मिल रहा, तो अपने ग्राम सभा अधिकारी से संपर्क करें" : "If patta not found, contact your Gram Sabha officer"}</span>
                            </li>
                            <li className="flex items-start gap-2">
                                <span className="text-[#e87722] mt-0.5">•</span>
                                <span>{lang === "hi" ? "डाउनलोड किया गया पट्टा कानूनी रूप से मान्य है और सभी सरकारी योजनाओं के लिए उपयोग किया जा सकता है" : "Downloaded patta is legally valid for all govt schemes"}</span>
                            </li>
                        </ul>
                    </div>

                    {/* Document Upload */}
                    <div className="tribal-card p-5 mt-5">
                        <div className="flex items-center justify-between mb-2">
                            <h4 className="font-bold text-[#1a3c2e] text-sm">
                                {lang === "hi" ? "📤 दस्तावेज़ अपलोड करें" : "📤 Upload Supporting Documents"}
                            </h4>
                            <Badge variant="info">Beta</Badge>
                        </div>
                        <p className="text-xs text-gray-500 mb-4">
                            {lang === "hi"
                                ? "AI आधारित प्रसंस्करण और सत्यापन के लिए अपने दावे के दस्तावेज़ अपलोड करें।"
                                : "Send your claim documents for AI-powered processing and verification."}
                        </p>

                        <input
                            ref={fileInputRef}
                            type="file"
                            accept="application/pdf,image/*"
                            className="hidden"
                            onChange={handleFilePick}
                        />

                        <div
                            className="border-2 border-dashed border-gray-200 rounded-xl p-4 text-center mb-4 cursor-pointer hover:border-primary transition"
                            onClick={triggerFileDialog}
                        >
                            <Upload size={20} className="mx-auto mb-2 text-primary" />
                            <p className="text-sm font-semibold text-primary">
                                {selectedFile ? selectedFile.name : lang === "hi" ? "फ़ाइल चुनने के लिए क्लिक करें" : "Click to choose a file"}
                            </p>
                            <p className="text-xs text-gray-500">
                                {lang === "hi" ? "PDF, JPG या PNG • अधिकतम 15 MB" : "PDF, JPG or PNG • up to 15 MB"}
                            </p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                            <div>
                                <label className="form-label">{lang === "hi" ? "दस्तावेज़ प्रकार (वैकल्पिक)" : "Document Type (optional)"}</label>
                                <input
                                    type="text"
                                    className="form-input"
                                    value={documentTypeInput}
                                    onChange={(e) => setDocumentTypeInput(e.target.value)}
                                    placeholder={lang === "hi" ? "जैसे: CFR दावा" : "e.g., CFR Claim"}
                                />
                            </div>
                            <div>
                                <label className="form-label">{lang === "hi" ? "भाषा" : "Language"}</label>
                                <select
                                    className="form-input"
                                    value={documentLanguage}
                                    onChange={(e) => setDocumentLanguage(e.target.value)}
                                >
                                    <option value="">{lang === "hi" ? "स्वचालित पहचान" : "Auto Detect"}</option>
                                    <option value="hi">हिंदी</option>
                                    <option value="en">English</option>
                                    <option value="mr">Marathi</option>
                                    <option value="or">Odia</option>
                                    <option value="bn">বাংলা / Bengali</option>
                                </select>
                            </div>
                        </div>

                        {uploadError && (
                            <div className="mb-3 p-3 bg-red-50 text-red-600 text-xs rounded-lg">
                                {uploadError}
                            </div>
                        )}

                        {uploadResult && (
                            <div className="mb-3 p-4 bg-emerald-50 text-emerald-700 rounded-lg text-xs space-y-1">
                                <p className="font-semibold">
                                    {lang === "hi" ? "दस्तावेज़ सफलतापूर्वक प्राप्त" : "Document received successfully"}
                                </p>
                                <p>
                                    ID #{uploadResult.document_id} • {uploadResult.document_type ?? "Unknown"}
                                </p>
                                <p>
                                    {lang === "hi" ? "स्थिति:" : "Status:"} {uploadResult.processing_status}
                                </p>
                                <p>
                                    Template: {uploadResult.template_id ?? "-"}
                                </p>
                                <p>
                                    {new Date(uploadResult.created_at).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" })}
                                </p>
                            </div>
                        )}

                        <button
                            onClick={handleDocumentUpload}
                            disabled={uploadStatus === "uploading"}
                            className="w-full py-3 bg-primary text-white rounded-xl font-bold text-sm shadow-md hover:shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {uploadStatus === "uploading"
                                ? lang === "hi" ? "अपलोड हो रहा है..." : "Uploading..."
                                : lang === "hi" ? "प्रसंस्करण हेतु भेजें" : "Send for Processing"}
                        </button>
                        {uploadStatus === "uploading" && (
                            <p className="text-center text-xs text-gray-500 mt-2">
                                {lang === "hi" ? "यह प्रक्रिया कुछ सेकंड ले सकती है" : "Processing may take a few seconds"}
                            </p>
                        )}
                    </div>
                </div>
            )}

            {/* Track Status Tab */}
            {activeTab === "track" && (
                <div className="max-w-3xl mx-auto">
                    <div className="tribal-card p-6">
                        <h3 className="font-bold text-[#1a3c2e] text-lg mb-4 text-center">
                            {lang === "hi" ? "📍 दावे की स्थिति जांचें" : "📍 Track Your Claim Status"}
                        </h3>

                        <div className="space-y-4 mb-6">
                            <div>
                                <label className="form-label">
                                    {lang === "hi" ? "दावा संख्या *" : "Claim ID *"}
                                </label>
                                <input
                                    type="text"
                                    value={claimId}
                                    onChange={(e) => setClaimId(e.target.value)}
                                    placeholder="FRA-2026-MP-00342"
                                    className="form-input font-mono"
                                />
                            </div>
                            <div>
                                <label className="form-label">
                                    {lang === "hi" ? "मोबाइल नंबर (सत्यापन के लिए) *" : "Mobile Number (for verification) *"}
                                </label>
                                <input
                                    type="tel"
                                    value={mobileNumber}
                                    onChange={(e) => setMobileNumber(e.target.value)}
                                    placeholder="+91 XXXXX XXXXX"
                                    className="form-input"
                                />
                            </div>
                            <button className="w-full py-3 bg-primary text-white rounded-xl font-bold text-sm shadow-md hover:shadow-lg transition-all">
                                {lang === "hi" ? "स्थिति जांचें" : "Check Status"}
                            </button>
                        </div>

                        {/* Status Timeline */}
                        {claimId && (
                            <div className="border-t border-gray-100 pt-5">
                                <div className="flex items-center justify-between mb-4">
                                    <h4 className="font-bold text-primary text-sm">
                                        {lang === "hi" ? "प्रक्रिया स्थिति" : "Processing Status"}
                                    </h4>
                                    <Badge variant="warning">
                                        {lang === "hi" ? "SDLC समीक्षाधीन" : "Under SDLC Review"}
                                    </Badge>
                                </div>

                                <div className="space-y-3">
                                    {[
                                        { step: "Received", label: lang === "hi" ? "दावा प्राप्त" : "Claim Received", date: "Dec 10, 2025", status: "completed" },
                                        { step: "FRC Verified", label: lang === "hi" ? "FRC सत्यापन" : "FRC Verification", date: "Dec 28, 2025", status: "completed" },
                                        { step: "SDLC Review", label: lang === "hi" ? "SDLC समीक्षा" : "SDLC Review", date: "In Progress", status: "in-progress" },
                                        { step: "DLC Approval", label: lang === "hi" ? "DLC अनुमोदन" : "DLC Approval", date: "Pending", status: "pending" },
                                        { step: "Patta Grant", label: lang === "hi" ? "पट्टा जारी" : "Patta Granted", date: "Pending", status: "pending" },
                                    ].map((s) => (
                                        <div key={s.step} className="flex items-center gap-3">
                                            <div
                                                className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${s.status === "completed"
                                                    ? "bg-emerald-500 text-white"
                                                    : s.status === "in-progress"
                                                        ? "bg-amber-500 text-white animate-pulse"
                                                        : "bg-gray-200 text-gray-400"
                                                    }`}
                                            >
                                                {s.status === "completed" ? <CheckCircle size={16} /> : s.status === "in-progress" ? <Clock size={16} /> : <div className="w-2 h-2 rounded-full bg-current" />}
                                            </div>
                                            <div className="flex-1">
                                                <p className="text-sm font-semibold text-primary">{s.label}</p>
                                                <p className="text-xs text-gray-400">{s.date}</p>
                                            </div>
                                        </div>
                                    ))}
                                </div>

                                <div className="mt-5 p-3 bg-blue-50 rounded-lg text-xs text-blue-700">
                                    <Clock size={12} className="inline mr-1" />
                                    {lang === "hi"
                                        ? "अनुमानित पूर्णता: 45-60 दिन । आपको SMS/WhatsApp पर अपडेट मिलेगी।"
                                        : "Estimated completion: 45-60 days. You will receive SMS/WhatsApp updates."}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Grievance Tab */}
            {activeTab === "grievance" && (
                <div className="max-w-3xl mx-auto">
                    <div className="tribal-card p-6">
                        <h3 className="font-bold text-[#1a3c2e] text-lg mb-4 text-center">
                            {lang === "hi" ? "📝 शिकायत दर्ज करें" : "📝 File a Grievance"}
                        </h3>

                        <div className="space-y-4">
                            <div className="grid grid-cols-2 gap-3">
                                <div>
                                    <label className="form-label">{lang === "hi" ? "आपका नाम *" : "Your Name *"}</label>
                                    <input type="text" className="form-input" />
                                </div>
                                <div>
                                    <label className="form-label">{lang === "hi" ? "मोबाइल नंबर *" : "Mobile Number *"}</label>
                                    <input type="tel" className="form-input" placeholder="+91" />
                                </div>
                            </div>

                            <div>
                                <label className="form-label">{lang === "hi" ? "दावा संख्या (यदि लागू हो)" : "Claim ID (if applicable)"}</label>
                                <input type="text" className="form-input font-mono" placeholder="FRA-YYYY-ST-XXXXX" />
                            </div>

                            <div>
                                <label className="form-label">{lang === "hi" ? "शिकायत का प्रकार *" : "Grievance Type *"}</label>
                                <select className="form-input">
                                    <option value="">{lang === "hi" ? "चुनें" : "Select"}</option>
                                    <option>{lang === "hi" ? "दावा अस्वीकृति पर आपत्ति" : "Objection to Claim Rejection"}</option>
                                    <option>{lang === "hi" ? "सीमा विवाद" : "Boundary Dispute"}</option>
                                    <option>{lang === "hi" ? "प्रक्रिया में देरी" : "Processing Delay"}</option>
                                    <option>{lang === "hi" ? "दस्तावेज़ समस्या" : "Document Issue"}</option>
                                    <option>{lang === "hi" ? "अन्य" : "Other"}</option>
                                </select>
                            </div>

                            <div>
                                <label className="form-label">{lang === "hi" ? "विवरण लिखें *" : "Description *"}</label>
                                <textarea className="form-input resize-none h-24" placeholder={lang === "hi" ? "अपनी शिकायत विस्तार से लिखें..." : "Describe your grievance in detail..."} />
                            </div>

                            <div>
                                <label className="form-label">{lang === "hi" ? "सहायक दस्तावेज़ (वैकल्पिक)" : "Supporting Documents (optional)"}</label>
                                <div className="dropzone text-center text-xs">
                                    <Upload size={18} className="mx-auto mb-1 text-gray-300" />
                                    {lang === "hi" ? "फ़ाइलें अपलोड करें (PDF, JPG, PNG)" : "Upload files (PDF, JPG, PNG)"}
                                </div>
                            </div>

                            <button className="w-full py-3 bg-accent text-white rounded-xl font-bold text-sm shadow-md hover:shadow-lg transition-all">
                                {lang === "hi" ? "शिकायत सबमिट करें" : "Submit Grievance"}
                            </button>
                        </div>
                    </div>

                    {/* Helpline */}
                    <div className="tribal-card p-5 mt-5 text-center">
                        <Phone size={20} className="mx-auto text-accent mb-2" />
                        <p className="font-bold text-primary mb-1">
                            {lang === "hi" ? "तत्काल सहायता के लिए हेल्पलाइन" : "Helpline for Immediate Support"}
                        </p>
                        <a href="tel:1800-11-0130" className="text-2xl font-bold text-accent">1800-11-0130</a>
                        <p className="text-xs text-gray-500 mt-1">
                            {lang === "hi" ? "टॉल-फ्री · सोम–शनि 9 AM – 5 PM" : "Toll-Free · Mon–Sat 9 AM – 5 PM"}
                        </p>
                    </div>
                </div>
            )}

            {/* Information Tab */}
            {activeTab === "info" && (
                <div className="max-w-4xl mx-auto space-y-5">
                    {/* FAQs */}
                    <div className="tribal-card p-5">
                        <h3 className="font-bold text-[#1a3c2e] mb-4">
                            {lang === "hi" ? "प्रायः पूछे जाने वाले प्रश्न (FAQ)" : "Frequently Asked Questions (FAQ)"}
                        </h3>
                        <div className="space-y-3">
                            {[
                                {
                                    q: "What is Forest Rights Act (FRA)?",
                                    qHi: "वन अधिकार अधिनियम (FRA) क्या है?",
                                    a: "The FRA 2006 recognizes the rights of forest-dwelling tribal communities and other traditional forest dwellers to forest resources, which they have been traditionally using.",
                                    aHi: "FRA 2006 वन निवासी जनजातीय समुदायों और अन्य पारंपरिक वन निवासियों के वन संसाधनों पर अधिकार को मान्यता देता है।",
                                },
                                {
                                    q: "Who can apply for FRA rights?",
                                    qHi: "FRA अधिकारों के लिए कौन आवेदन कर सकता है?",
                                    a: "Scheduled Tribes and Other Traditional Forest Dwellers who have been residing in forest areas before Dec 13, 2005 and depend on forests for livelihood.",
                                    aHi: "अनुसूचित जनजाति और अन्य पारंपरिक वन निवासी जो 13 दिसंबर 2005 से पहले से वन क्षेत्रों में रह रहे हैं।",
                                },
                                {
                                    q: "How long does the claim process take?",
                                    qHi: "दावे की प्रक्रिया में कितना समय लगता है?",
                                    a: "Typically 4-6 months from filing to patta grant, but can vary by state and claim complexity.",
                                    aHi: "आमतौर पर 4-6 महीने, लेकिन राज्य और दावे की जटिलता के अनुसार भिन्न हो सकता है।",
                                },
                                {
                                    q: "Can I use my FRA patta for bank loans?",
                                    qHi: "क्या मैं बैंक ऋण के लिए FRA पट्टा उपयोग कर सकता हूं?",
                                    a: "Yes, FRA patta can be used for agricultural loans and enrollment in government schemes like PM-KISAN, PMAY-G, etc.",
                                    aHi: "हां, FRA पट्टा कृषि ऋण और PM-KISAN, PMAY-G जैसी सरकारी योजनाओं में नामांकन के लिए उपयोग किया जा सकता है।",
                                },
                            ].map((faq, i) => (
                                <details key={i} className="border border-gray-100 rounded-xl overflow-hidden">
                                    <summary className="p-3 bg-[#f4ede3] cursor-pointer text-sm font-bold text-[#1a3c2e] hover:bg-[#ede4d8]">
                                        {lang === "hi" ? faq.qHi : faq.q}
                                    </summary>
                                    <div className="p-3 text-xs text-gray-600">
                                        {lang === "hi" ? faq.aHi : faq.a}
                                    </div>
                                </details>
                            ))}
                        </div>
                    </div>

                    {/* Useful Links */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                        <div className="tribal-card p-5">
                            <h4 className="font-bold text-[#1a3c2e] text-sm mb-3">
                                {lang === "hi" ? "उपयोगी लिंक" : "Useful Links"}
                            </h4>
                            <div className="space-y-2">
                                {[
                                    { label: "Ministry of Tribal Affairs", url: "https://tribal.nic.in" },
                                    { label: "National Portal of India", url: "https://india.gov.in" },
                                    { label: "DigiLocker", url: "https://digilocker.gov.in" },
                                    { label: "Umang App", url: "https://web.umang.gov.in" },
                                ].map((link) => (
                                    <a
                                        key={link.label}
                                        href={link.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex items-center justify-between p-2 rounded-lg hover:bg-gray-50 transition-colors text-sm"
                                    >
                                        <span className="text-[#1a3c2e]">{link.label}</span>
                                        <ChevronRight size={14} className="text-gray-400" />
                                    </a>
                                ))}
                            </div>
                        </div>

                        <div className="tribal-card p-5">
                            <h4 className="font-bold text-[#1a3c2e] text-sm mb-3">
                                {lang === "hi" ? "संपर्क जानकारी" : "Contact Information"}
                            </h4>
                            <div className="space-y-3 text-xs">
                                <div>
                                    <p className="text-gray-500 mb-0.5">{lang === "hi" ? "राष्ट्रीय हेल्पलाइन" : "National Helpline"}</p>
                                    <a href="tel:1800-11-0130" className="font-bold text-[#e87722]">1800-11-0130 (Toll-Free)</a>
                                </div>
                                <div>
                                    <p className="text-gray-500 mb-0.5">{lang === "hi" ? "ईमेल" : "Email"}</p>
                                    <a href="mailto:fra-help@tribal.gov.in" className="font-semibold text-[#1a3c2e] hover:underline">fra-help@tribal.gov.in</a>
                                </div>
                                <div>
                                    <p className="text-gray-500 mb-0.5">{lang === "hi" ? "पता" : "Address"}</p>
                                    <p className="text-gray-700">Ministry of Tribal Affairs, Shastri Bhawan, New Delhi - 110001</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </DashboardLayout>
    );
}

"use client";
import React, { useRef, useState } from "react";
import {
    Upload, FileText, CheckCircle, XCircle, Clock, Eye,
    Zap, Database, Download, AlertTriangle, Cpu, Layers,
    Search, Filter, RotateCcw, Edit3, Save, Trash2,
    ChevronRight, Sparkles, Brain, Target,
} from "lucide-react";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { Badge } from "@/components/ui/badge";
import { formatDate } from "@/lib/utils";
import { DocumentUploadResult, uploadDocumentRequest } from "@/lib/document-upload";
import { apiClient } from "@/lib/api-client";
import { ErrorDisplay } from "@/components/error-display";
import { DataTableSkeleton, StatCardSkeleton } from "@/components/skeletons";

type BulkUploadItem = {
    fileName: string;
    status: "uploading" | "success" | "error";
    message?: string;
    result?: DocumentUploadResult;
};

export default function DigitizationPage() {
    const [activeTab, setActiveTab] = useState<"upload" | "queue" | "verified" | "rejected">("upload");
    const [selectedDoc, setSelectedDoc] = useState<any>(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [bulkUploads, setBulkUploads] = useState<BulkUploadItem[]>([]);
    const [bulkStatus, setBulkStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
    const [bulkError, setBulkError] = useState<string | null>(null);
    const [processingDocType, setProcessingDocType] = useState("FRA Claim Form (Form-A)");
    const [primaryLanguage, setPrimaryLanguage] = useState("");
    const fileInputRef = useRef<HTMLInputElement | null>(null);

    const mockDocs = [
        {
            id: "DOC-001",
            fileName: "claim_form_ramcharan.pdf",
            uploadedBy: "DLC Officer - Mandla",
            uploadDate: "2026-02-18T14:30:00",
            status: "processing",
            ocrConfidence: 0.94,
            nerEntities: [
                { type: "PERSON", text: "Ramcharan Banjara", verified: true },
                { type: "LOCATION", text: "Sonpur Jungle", verified: true },
                { type: "DATE", text: "2005-08-12", verified: false },
                { type: "AREA", text: "2.5 acres", verified: true },
            ],
            extractedFields: {
                claimant_name: "Ramcharan Banjara",
                village: "Sonpur Jungle",
                district: "Mandla",
                area_acres: "2.5",
                claim_type: "IFR",
                tribal_group: "Baiga",
            },
            flags: ["Date format inconsistent", "Signature quality low"],
        },
        {
            id: "DOC-002",
            fileName: "land_document_govind_gond.jpg",
            uploadedBy: "FRC Member - Laxmipur",
            uploadDate: "2026-02-18T10:15:00",
            status: "completed",
            ocrConfidence: 0.89,
            nerEntities: [],
            extractedFields: {},
            flags: [],
        },
        {
            id: "DOC-003",
            fileName: "community_cert_scan.pdf",
            uploadedBy: "Range Officer - Bichhiya",
            uploadDate: "2026-02-17T16:45:00",
            status: "failed",
            ocrConfidence: 0.42,
            nerEntities: [],
            extractedFields: {},
            flags: ["Low resolution", "Handwritten text", "Multiple languages detected"],
        },
    ];

    const tabs = [
        { id: "upload", label: "Upload Documents", count: 0 },
        { id: "queue", label: "Processing Queue", count: 12 },
        { id: "verified", label: "Verified", count: 234 },
        { id: "rejected", label: "Needs Review", count: 8 },
    ] as const;

    return (
        <DashboardLayout role="mota-nodal" title="OCR Digitization Module" titleHi="OCR डिजिटाइज़ेशन">
            {/* Header */}
            <div className="flex items-center justify-between mb-5">
                <div>
                    <h1 className="text-xl font-bold text-primary">AI-Powered OCR Digitization Module</h1>
                    <p className="text-xs text-gray-500">Automated extraction from scanned FRA documents using OCR + NER</p>
                </div>
                <div className="flex items-center gap-2 no-print">
                    <button className="flex items-center gap-2 text-xs px-3 py-1.5 border border-gray-200 rounded-lg hover:bg-gray-50">
                        <Database size={13} /> Export to Database
                    </button>
                    <button className="flex items-center gap-2 text-xs px-3 py-1.5 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg">
                        <Sparkles size={13} /> Batch Process
                    </button>
                </div>
            </div>

            {/* AI Model Status */}
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-3 mb-5">
                {[
                    { label: "OCR Accuracy", value: "94.2%", icon: <Eye size={16} />, color: "#22C55E" },
                    { label: "NER F1-Score", value: "91.8%", icon: <Brain size={16} />, color: "#6366F1" },
                    { label: "Avg Processing Time", value: "8.3s", icon: <Zap size={16} />, color: "#F59E0B" },
                    { label: "Documents Processed", value: "12,458", icon: <FileText size={16} />, color: "#0D9488" },
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

            {/* Tabs */}
            <div className="flex gap-2 mb-5 overflow-x-auto no-print">
                {tabs.map((t) => (
                    <button
                        key={t.id}
                        onClick={() => setActiveTab(t.id)}
                        className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${activeTab === t.id ? "bg-primary text-white shadow-md" : "bg-gray-100 text-gray-600 hover:bg-gray-200"}`}
                    >
                        {t.label}
                        {t.count > 0 && (
                            <Badge variant={activeTab === t.id ? "neutral" : "info"} size="sm">
                                {t.count}
                            </Badge>
                        )}
                    </button>
                ))}
            </div>

            {/* Upload Tab */}
            {activeTab === "upload" && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
                    {/* Upload Zone */}
                    <div className="tribal-card p-6">
                        <h3 className="font-bold text-primary text-sm mb-4">📤 Bulk Document Upload</h3>
                        <input
                            ref={fileInputRef}
                            type="file"
                            multiple
                            accept="application/pdf,image/*"
                            className="hidden"
                            onChange={async (event) => {
                                if (!event.target.files?.length) return;
                                const pickedFiles = Array.from(event.target.files);
                                setBulkStatus("uploading");
                                setBulkError(null);
                                setBulkUploads(pickedFiles.map((file) => ({ fileName: file.name, status: "uploading" })));
                                const results: BulkUploadItem[] = [];
                                for (const file of pickedFiles) {
                                    let outcome: BulkUploadItem;
                                    try {
                                        const result = await uploadDocumentRequest({
                                            file,
                                            documentType: processingDocType,
                                            language: primaryLanguage || undefined,
                                        });
                                        outcome = { fileName: file.name, status: "success", result };
                                    } catch (error) {
                                        outcome = {
                                            fileName: file.name,
                                            status: "error",
                                            message: error instanceof Error ? error.message : "Upload failed",
                                        };
                                    }
                                    results.push(outcome);
                                    setBulkUploads((prev) => prev.map((item) => (item.fileName === file.name ? outcome : item)));
                                }
                                setBulkUploads(results);
                                fileInputRef.current && (fileInputRef.current.value = "");
                                if (results.some((item) => item.status === "error")) {
                                    setBulkStatus("error");
                                    setBulkError("One or more uploads failed. Please review the list below.");
                                } else {
                                    setBulkStatus("success");
                                }
                            }}
                        />
                        <div
                            className="border-2 border-dashed border-gray-300 rounded-2xl p-10 text-center hover:border-[#2d8566] transition-all cursor-pointer bg-gradient-to-br from-gray-50 to-white"
                            onClick={() => fileInputRef.current?.click()}
                        >
                            <Upload size={40} className="mx-auto text-gray-300 mb-3" />
                            <p className="font-semibold text-primary mb-1">Drag & Drop Files Here</p>
                            <p className="text-xs text-gray-500 mb-3">or click to browse</p>
                            <p className="text-xs text-gray-400">Supported: PDF, JPG, PNG, TIFF · Max 10MB per file</p>
                            <button className="mt-4 px-4 py-2 bg-accent text-white rounded-lg text-sm font-semibold shadow-md hover:shadow-lg transition-all">
                                Select Files
                            </button>
                        </div>

                        {bulkUploads.length > 0 && (
                            <div className="mt-4 space-y-2">
                                {bulkUploads.map((item) => (
                                    <div key={item.fileName} className="flex items-center justify-between rounded-lg border px-3 py-2 text-xs">
                                        <span className="truncate pr-3 text-gray-600">{item.fileName}</span>
                                        {item.status === "uploading" && <span className="text-amber-600">Uploading…</span>}
                                        {item.status === "success" && <span className="text-emerald-600">Stored · ID #{item.result?.document_id}</span>}
                                        {item.status === "error" && <span className="text-red-500">{item.message ?? "Failed"}</span>}
                                    </div>
                                ))}
                                {bulkError && <p className="text-xs text-red-500">{bulkError}</p>}
                                {bulkStatus === "success" && !bulkError && (
                                    <p className="text-xs text-emerald-600">All documents were ingested successfully.</p>
                                )}
                            </div>
                        )}

                        <div className="mt-5 bg-blue-50 rounded-xl p-4 text-xs text-blue-700">
                            <Cpu size={14} className="inline mr-1" />
                            <b>AI Models Active:</b> Tesseract OCR 5.0 + spaCy NER (en_core_web_trf) + Custom FRA entity model
                        </div>
                    </div>

                    {/* Processing Options */}
                    <div className="tribal-card p-6">
                        <h3 className="font-bold text-primary text-sm mb-4">⚙️ Processing Options</h3>
                        <div className="space-y-4">
                            <div>
                                <label className="form-label">Document Type</label>
                                <select className="form-input" value={processingDocType} onChange={(e) => setProcessingDocType(e.target.value)}>
                                    <option value="FRA Claim Form (Form-A)">FRA Claim Form (Form-A)</option>
                                    <option value="Land Possession Certificate">Land Possession Certificate</option>
                                    <option value="Community Resolution Letter">Community Resolution Letter</option>
                                    <option value="Aadhaar Card">Aadhaar Card</option>
                                    <option value="Revenue Records">Revenue Records</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>

                            <div>
                                <label className="form-label">Primary Language</label>
                                <select className="form-input" value={primaryLanguage} onChange={(e) => setPrimaryLanguage(e.target.value)}>
                                    <option value="">Auto Detect</option>
                                    <option value="en">English</option>
                                    <option value="hi">Hindi</option>
                                    <option value="mr">Marathi</option>
                                    <option value="or">Odia</option>
                                    <option value="bn">Bengali</option>
                                </select>
                            </div>

                            <div>
                                <label className="form-label">Language Detection</label>
                                <div className="flex gap-2">
                                    {["English", "Hindi", "Marathi", "Odia", "Telugu"].map((l) => (
                                        <label key={l} className="flex items-center gap-1 text-xs">
                                            <input type="checkbox" defaultChecked={l === "English" || l === "Hindi"} className="rounded" />
                                            {l}
                                        </label>
                                    ))}
                                </div>
                            </div>

                            <div>
                                <label className="form-label">Quality Enhancement</label>
                                <div className="space-y-2 text-xs">
                                    <label className="flex items-center gap-2">
                                        <input type="checkbox" defaultChecked className="rounded" />
                                        <span>Auto-rotate and deskew</span>
                                    </label>
                                    <label className="flex items-center gap-2">
                                        <input type="checkbox" defaultChecked className="rounded" />
                                        <span>Denoise and sharpen</span>
                                    </label>
                                    <label className="flex items-center gap-2">
                                        <input type="checkbox" className="rounded" />
                                        <span>Binarization (for handwritten docs)</span>
                                    </label>
                                </div>
                            </div>

                            <div>
                                <label className="form-label">Named Entity Recognition (NER)</label>
                                <div className="flex gap-1 flex-wrap">
                                    {["PERSON", "LOCATION", "DATE", "AREA", "TRIBAL_GROUP"].map((e) => (
                                        <span key={e} className="text-xs px-2 py-0.5 bg-purple-100 text-purple-700 rounded-full">{e}</span>
                                    ))}
                                </div>
                            </div>

                            <button
                                onClick={() => setIsProcessing(true)}
                                className="w-full py-2.5 bg-gradient-to-r from-[#1a3c2e] to-[#2d8566] text-white rounded-lg font-semibold text-sm flex items-center justify-center gap-2"
                            >
                                <Zap size={14} /> Start Processing
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Queue Tab */}
            {activeTab === "queue" && (
                <div className="grid grid-cols-1 lg:grid-cols-5 gap-5">
                    {/* Document List */}
                    <div className="lg:col-span-2 tribal-card overflow-hidden">
                        <div className="p-3 border-b border-gray-100 flex items-center gap-2">
                            <div className="relative flex-1">
                                <Search size={12} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-400" />
                                <input
                                    type="text"
                                    placeholder="Search documents..."
                                    className="w-full pl-7 pr-3 py-1.5 text-xs border border-gray-200 rounded-lg"
                                />
                            </div>
                            <button className="flex items-center gap-1 text-xs border border-gray-200 px-2 py-1.5 rounded-lg">
                                <Filter size={11} />
                            </button>
                        </div>
                        <div className="overflow-y-auto max-h-[600px]">
                            {mockDocs.map((doc) => (
                                <button
                                    key={doc.id}
                                    onClick={() => setSelectedDoc(doc)}
                                    className={`w-full text-left px-3 py-3 border-b border-gray-50 hover:bg-[#f4ede3] transition-colors ${selectedDoc?.id === doc.id ? "bg-[#f4ede3] border-l-2 border-l-[#e87722]" : ""}`}
                                >
                                    <div className="flex items-center justify-between mb-1">
                                        <span className="text-xs font-mono text-gray-400">{doc.id}</span>
                                        {doc.status === "processing" && <Clock size={12} className="text-amber-500 animate-spin" />}
                                        {doc.status === "completed" && <CheckCircle size={12} className="text-emerald-500" />}
                                        {doc.status === "failed" && <XCircle size={12} className="text-red-500" />}
                                    </div>
                                    <p className="text-xs font-medium text-primary truncate">{doc.fileName}</p>
                                    <p className="text-xs text-gray-400 mt-0.5">{formatDate(doc.uploadDate)}</p>
                                    {doc.ocrConfidence > 0 && (
                                        <div className="mt-1.5 flex items-center gap-1.5">
                                            <div className="flex-1 progress-forest">
                                                <div
                                                    style={{
                                                        width: `${doc.ocrConfidence * 100}%`,
                                                        background: doc.ocrConfidence >= 0.85 ? "#22C55E" : doc.ocrConfidence >= 0.7 ? "#F59E0B" : "#EF4444",
                                                    }}
                                                />
                                            </div>
                                            <span className="text-xs font-semibold text-gray-600">{Math.round(doc.ocrConfidence * 100)}%</span>
                                        </div>
                                    )}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Document Detail Panel */}
                    <div className="lg:col-span-3">
                        {selectedDoc ? (
                            <div className="space-y-4">
                                {/* Header */}
                                <div className="tribal-card p-5">
                                    <div className="flex items-start justify-between mb-3">
                                        <div>
                                            <p className="text-xs text-gray-400 mb-0.5">{selectedDoc.id}</p>
                                            <h3 className="font-bold text-primary text-lg">{selectedDoc.fileName}</h3>
                                            <p className="text-xs text-gray-500 mt-0.5">Uploaded by {selectedDoc.uploadedBy} · {formatDate(selectedDoc.uploadDate)}</p>
                                        </div>
                                        <Badge
                                            variant={
                                                selectedDoc.status === "completed" ? "success" :
                                                    selectedDoc.status === "processing" ? "warning" : "danger"
                                            }
                                        >
                                            {selectedDoc.status.toUpperCase()}
                                        </Badge>
                                    </div>

                                    <div className="grid grid-cols-2 gap-2 text-xs">
                                        <div className="bg-gray-50 rounded p-2">
                                            <p className="text-gray-400 mb-0.5">OCR Confidence</p>
                                            <p className="font-bold text-primary">{Math.round(selectedDoc.ocrConfidence * 100)}%</p>
                                        </div>
                                        <div className="bg-gray-50 rounded p-2">
                                            <p className="text-gray-400 mb-0.5">Entities Extracted</p>
                                            <p className="font-bold text-primary">{selectedDoc.nerEntities.length}</p>
                                        </div>
                                    </div>
                                </div>

                                {/* Extracted Fields */}
                                <div className="tribal-card p-5">
                                    <div className="flex items-center justify-between mb-3">
                                        <h4 className="font-bold text-primary text-sm">🤖 Extracted Fields</h4>
                                        <button className="text-xs text-accent hover:underline flex items-center gap-1">
                                            <Edit3 size={11} /> Edit
                                        </button>
                                    </div>
                                    <div className="grid grid-cols-2 gap-2">
                                        {Object.entries(selectedDoc.extractedFields).map(([key, val]) => (
                                            <div key={key} className="p-2 rounded-lg bg-gray-50">
                                                <p className="text-xs text-gray-400 mb-0.5 capitalize">{key.replace(/_/g, " ")}</p>
                                                <p className="text-sm font-semibold text-primary">{String(val)}</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {/* Named Entities */}
                                {selectedDoc.nerEntities.length > 0 && (
                                    <div className="tribal-card p-5">
                                        <h4 className="font-bold text-primary text-sm mb-3">🏷️ Named Entities (NER)</h4>
                                        <div className="space-y-2">
                                            {selectedDoc.nerEntities.map((e: any, i: number) => (
                                                <div key={i} className="flex items-center justify-between p-2 rounded-lg bg-purple-50">
                                                    <div className="flex items-center gap-2">
                                                        <Badge variant="info" size="sm">{e.type}</Badge>
                                                        <span className="text-sm font-medium text-primary">{e.text}</span>
                                                    </div>
                                                    {e.verified ? (
                                                        <CheckCircle size={14} className="text-emerald-500" />
                                                    ) : (
                                                        <button className="text-xs text-accent hover:underline">Verify</button>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Flags */}
                                {selectedDoc.flags.length > 0 && (
                                    <div className="tribal-card p-5 border-2 border-amber-200 bg-amber-50">
                                        <div className="flex items-start gap-2">
                                            <AlertTriangle size={16} className="text-amber-600 flex-shrink-0 mt-0.5" />
                                            <div>
                                                <h4 className="font-bold text-amber-800 text-sm mb-2">Quality Flags</h4>
                                                <ul className="space-y-1 text-xs text-amber-700">
                                                    {selectedDoc.flags.map((f: string, i: number) => (
                                                        <li key={i}>• {f}</li>
                                                    ))}
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                )}

                                {/* Actions */}
                                <div className="flex gap-2">
                                    <button className="flex-1 py-2 bg-emerald-600 text-white rounded-lg text-sm font-semibold flex items-center justify-center gap-2">
                                        <CheckCircle size={14} /> Approve & Create Claim
                                    </button>
                                    <button className="flex-1 py-2 border-2 border-amber-500 text-amber-700 rounded-lg text-sm font-semibold flex items-center justify-center gap-2">
                                        <RotateCcw size={14} /> Re-process
                                    </button>
                                    <button className="px-4 py-2 border-2 border-red-500 text-red-600 rounded-lg text-sm font-semibold">
                                        <Trash2 size={14} />
                                    </button>
                                </div>
                            </div>
                        ) : (
                            <div className="tribal-card p-10 flex flex-col items-center justify-center text-center h-full">
                                <FileText size={40} className="text-gray-200 mb-3" />
                                <p className="text-gray-400 text-sm">Select a document to view extraction results</p>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Verified Tab */}
            {activeTab === "verified" && (
                <div className="tribal-card overflow-hidden">
                    <div className="p-4 border-b border-gray-100">
                        <h3 className="font-bold text-[#1a3c2e] text-sm">✅ Verified & Integrated Documents (234)</h3>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="data-table">
                            <thead>
                                <tr>
                                    <th>Document ID</th>
                                    <th>File Name</th>
                                    <th>Claimant</th>
                                    <th>Village</th>
                                    <th>Verified Date</th>
                                    <th>OCR Score</th>
                                    <th>Claim Created</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {[...Array(10)].map((_, i) => (
                                    <tr key={i}>
                                        <td className="font-mono text-xs">DOC-{String(i + 100).padStart(3, "0")}</td>
                                        <td className="text-xs">claim_form_{i + 1}.pdf</td>
                                        <td className="font-medium text-sm">Sample Claimant {i + 1}</td>
                                        <td className="text-xs text-gray-600">Village {i + 1}</td>
                                        <td className="text-xs text-gray-500">Feb {15 + (i % 4)}, 2026</td>
                                        <td>
                                            <div className="flex items-center gap-1">
                                                <div className="w-12 progress-forest">
                                                    <div style={{ width: `${85 + i}%` }} />
                                                </div>
                                                <span className="text-xs">{85 + i}%</span>
                                            </div>
                                        </td>
                                        <td><Badge variant="success" size="sm">FRA-2026-MP-{String(i + 400).padStart(5, "0")}</Badge></td>
                                        <td>
                                            <button className="text-xs text-primary hover:text-accent transition-all">View</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}

            {/* Rejected Tab */}
            {activeTab === "rejected" && (
                <div className="tribal-card p-5">
                    <h3 className="font-bold text-primary text-sm mb-4">⚠️ Documents Needing Manual Review (8)</h3>
                    <div className="space-y-3">
                        {mockDocs.filter(d => d.status === "failed").map((doc) => (
                            <div key={doc.id} className="p-4 rounded-xl border-2 border-red-200 bg-red-50">
                                <div className="flex items-start justify-between mb-2">
                                    <div>
                                        <p className="font-semibold text-primary text-sm">{doc.fileName}</p>
                                        <p className="text-xs text-gray-500">{doc.id} · Confidence: {Math.round(doc.ocrConfidence * 100)}%</p>
                                    </div>
                                    <Badge variant="danger">Failed</Badge>
                                </div>
                                <div className="text-xs text-red-700 mb-3">
                                    <AlertTriangle size={12} className="inline mr-1" />
                                    <b>Issues:</b> {doc.flags.join(", ")}
                                </div>
                                <div className="flex gap-2">
                                    <button className="text-xs px-3 py-1.5 bg-primary text-white rounded-lg shadow-md hover:shadow-lg transition-all">
                                        Re-upload Better Scan
                                    </button>
                                    <button className="text-xs px-3 py-1.5 border border-gray-200 rounded-lg">
                                        Manual Entry
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </DashboardLayout>
    );
}

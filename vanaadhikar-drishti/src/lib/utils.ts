import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

export function formatNumber(num: number): string {
    if (num >= 10000000) return `${(num / 10000000).toFixed(2)} Cr`;
    if (num >= 100000) return `${(num / 100000).toFixed(2)} L`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
}

export function formatArea(acres: number): string {
    if (acres >= 100000) return `${(acres / 100000).toFixed(2)} L Acres`;
    if (acres >= 1000) return `${(acres / 1000).toFixed(1)}K Acres`;
    return `${acres.toFixed(2)} Acres`;
}

export function formatDate(dateStr: string): string {
    const d = new Date(dateStr);
    return d.toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
    });
}

export function getStatusColor(status: string): string {
    const map: Record<string, string> = {
        granted: "text-emerald-700 bg-emerald-50 border-emerald-200",
        approved: "text-emerald-700 bg-emerald-50 border-emerald-200",
        "in-process": "text-amber-700 bg-amber-50 border-amber-200",
        pending: "text-amber-700 bg-amber-50 border-amber-200",
        rejected: "text-red-700 bg-red-50 border-red-200",
        received: "text-blue-700 bg-blue-50 border-blue-200",
        verified: "text-indigo-700 bg-indigo-50 border-indigo-200",
        patented: "text-purple-700 bg-purple-50 border-purple-200",
    };
    return map[status.toLowerCase()] ?? "text-gray-700 bg-gray-50 border-gray-200";
}

export function getStateBadgeColor(state: string): string {
    const map: Record<string, string> = {
        "madhya-pradesh": "bg-orange-100 text-orange-800",
        odisha: "bg-red-100 text-red-800",
        tripura: "bg-green-100 text-green-800",
        telangana: "bg-teal-100 text-teal-800",
    };
    return map[state.toLowerCase().replace(" ", "-")] ?? "bg-gray-100 text-gray-800";
}

export function slugify(str: string): string {
    return str
        .toLowerCase()
        .replace(/\s+/g, "-")
        .replace(/[^a-z0-9-]/g, "");
}

export function truncate(str: string, length: number): string {
    if (str.length <= length) return str;
    return str.slice(0, length) + "…";
}

export function percentOf(part: number, total: number): number {
    if (total === 0) return 0;
    return Math.round((part / total) * 100);
}

export const STATES = [
    { id: "MP", name: "Madhya Pradesh", slug: "madhya-pradesh", color: "#E87722", districts: 52 },
    { id: "OD", name: "Odisha", slug: "odisha", color: "#BE3144", districts: 30 },
    { id: "TR", name: "Tripura", slug: "tripura", color: "#2D6A4F", districts: 8 },
    { id: "TG", name: "Telangana", slug: "telangana", color: "#0D9488", districts: 33 },
];

export const CLAIM_TYPES = [
    { id: "IFR", label: "Individual Forest Rights", color: "#4F46E5" },
    { id: "CFR", label: "Community Forest Resource Rights", color: "#16A34A" },
    { id: "CR", label: "Community Rights", color: "#D97706" },
];

export const CSS_SCHEMES = [
    { id: "PM-KISAN", label: "PM-KISAN", ministry: "Ministry of Agriculture", color: "#16A34A" },
    { id: "JJM", label: "Jal Jeevan Mission", ministry: "Ministry of Jal Shakti", color: "#0EA5E9" },
    { id: "MGNREGA", label: "MGNREGA", ministry: "Ministry of Rural Development", color: "#F59E0B" },
    { id: "PMAY-G", label: "PMAY Gramin", ministry: "Ministry of Rural Development", color: "#8B5CF6" },
    { id: "DAJGUA", label: "DA-JGUA", ministry: "Ministry of Tribal Affairs", color: "#E87722" },
    { id: "PM-JANMAN", label: "PM-JANMAN", ministry: "Ministry of Tribal Affairs", color: "#EC4899" },
    { id: "EMRS", label: "EMRS Schools", ministry: "Ministry of Tribal Affairs", color: "#14B8A6" },
    { id: "SAUBHAGYA", label: "SAUBHAGYA", ministry: "Ministry of Power", color: "#EAB308" },
    { id: "BHARATNET", label: "BharatNet", ministry: "Ministry of Communications", color: "#6366F1" },
    { id: "VDVK", label: "Van Dhan Vikas Kendra", ministry: "Ministry of Tribal Affairs", color: "#22C55E" },
];

"use client";
import React, { useState } from "react";
import dynamic from "next/dynamic";
import {
    Layers, Filter, Search, Download, Eye, EyeOff,
    MapPin, TrendingUp, Droplets, Flame, CheckCircle,
    Home, School, Zap, Users, ChevronRight,
} from "lucide-react";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { Badge } from "@/components/ui/badge";
import { apiClient } from "@/lib/api-client";
import { ErrorDisplay } from "@/components/error-display";
import { DataTableSkeleton, MapSkeleton } from "@/components/skeletons";
import { formatNumber } from "@/lib/utils";

// Dynamic import to prevent SSR issues with Leaflet
const MapContainer = dynamic(
    () => import("react-leaflet").then((mod) => mod.MapContainer),
    { ssr: false }
);
const TileLayer = dynamic(
    () => import("react-leaflet").then((mod) => mod.TileLayer),
    { ssr: false }
);
const Marker = dynamic(
    () => import("react-leaflet").then((mod) => mod.Marker),
    { ssr: false }
);
const Popup = dynamic(
    () => import("react-leaflet").then((mod) => mod.Popup),
    { ssr: false }
);

export default function AtlasPage() {
    const [activeLayers, setActiveLayers] = useState<string[]>(["claims", "villages"]);
    const [selectedState, setSelectedState] = useState("all");
    const [mapView, setMapView] = useState<"india" | "state" | "district">("india");
    const [states, setStates] = useState<any[]>([]);
    const [claims, setClaims] = useState<any[]>([]);
    const [fireAlerts, setFireAlerts] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const toggleLayer = (layer: string) => {
        setActiveLayers((prev) =>
            prev.includes(layer) ? prev.filter((l) => l !== layer) : [...prev, layer]
        );
    };

    const layers = [
        { id: "claims", label: "FRA Claims", icon: <CheckCircle size={14} />, color: "#22C55E", count: formatNumber(claims.length) },
        { id: "villages", label: "Villages", icon: <MapPin size={14} />, color: "#3B82F6", count: formatNumber(63843) },
        { id: "fire-alerts", label: "Fire Alerts", icon: <Flame size={14} />, color: "#EF4444", count: fireAlerts.length },
        { id: "ndvi", label: "NDVI/Forest Health", icon: <TrendingUp size={14} />, color: "#16A34A", count: "Satellite" },
        { id: "groundwater", label: "Groundwater Depth", icon: <Droplets size={14} />, color: "#0EA5E9", count: "Raster" },
        { id: "schools", label: "Schools (>5km)", icon: <School size={14} />, color: "#8B5CF6", count: "12" },
        { id: "roads", label: "Road Network", icon: <Home size={14} />, color: "#F59E0B", count: "OSM" },
        { id: "electricity", label: "Electricity", icon: <Zap size={14} />, color: "#EC4899", count: "234 HH" },
    ];

    React.useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                setError(null);

                const [claimsRes, statesRes] = await Promise.all([
                    apiClient.getClaims(1, 100),
                    apiClient.getDashboardSummary(),
                ]);

                if (claimsRes.data?.items) {
                    setClaims(claimsRes.data.items);
                }

                if (statesRes.data?.claims) {
                    // Extract states from dashboard summary
                    const stateList = statesRes.data.claims.by_state ? Object.keys(statesRes.data.claims.by_state).map((state) => ({
                        id: state,
                        name: state,
                    })) : [];
                    setStates(stateList);
                }
            } catch (err) {
                setError(err instanceof Error ? err.message : "Failed to load atlas data");
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const toggleLayer = (layer: string) => {
        <DashboardLayout role="mota-nodal" title="FRA WebGIS Atlas" titleHi="FRA भूस्थानिक मानचित्र">
            {/* Header */}
            <div className="flex items-center justify-between mb-5">
                <div>
                    <h1 className="text-xl font-bold text-primary">FRA WebGIS Atlas — Interactive Mapping Portal</h1>
                    <p className="text-xs text-gray-500">
                        Multi-layered geospatial visualization of FRA implementation + scheme convergence
                    </p>
                </div>
                <div className="flex items-center gap-2 no-print">
                    <button className="flex items-center gap-2 text-xs px-3 py-1.5 border border-gray-200 rounded-lg hover:bg-gray-50">
                        <Download size={13} /> Export Map
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-5">
                {/* Left Sidebar — Layer Control */}
                <div className="space-y-4">
                    {/* Filters */}
                    <div className="tribal-card p-4">
                        <h3 className="font-bold text-[#1a3c2e] text-sm mb-3 flex items-center gap-2">
                            <Filter size={14} /> Filters
                        </h3>
                        <div className="space-y-3">
                            <div>
                                <label className="form-label">State</label>
                                <select
                                    value={selectedState}
                                    onChange={(e) => setSelectedState(e.target.value)}
                                    className="form-input text-xs"
                                >
                                    <option value="all">All States</option>
                                    {states.map((s) => (
                                        <option key={s.id} value={s.id}>{s.name}</option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label className="form-label">Map View</label>
                                <div className="flex gap-1">
                                    {["india", "state", "district"].map((v) => (
                                        <button
                                            key={v}
                                            onClick={() => setMapView(v as typeof mapView)}
                                            className={`flex-1 px-2 py-1.5 rounded text-xs font-medium capitalize ${mapView === v
                                                ? "bg-primary text-white shadow-md"
                                                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                                                }`}
                                        >
                                            {v}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Layers */}
                    <div className="tribal-card p-4">
                        <h3 className="font-bold text-[#1a3c2e] text-sm mb-3 flex items-center gap-2">
                            <Layers size={14} /> Map Layers
                        </h3>
                        <div className="space-y-2">
                            {layers.map((layer) => (
                                <button
                                    key={layer.id}
                                    onClick={() => toggleLayer(layer.id)}
                                    className={`w-full flex items-center justify-between p-2 rounded-lg transition-all text-left ${activeLayers.includes(layer.id)
                                        ? "bg-primary-50 border-2 border-accent"
                                        : "bg-gray-50 hover:bg-gray-100"
                                        }`}
                                >
                                    <div className="flex items-center gap-2">
                                        <div style={{ color: layer.color }}>{layer.icon}</div>
                                        <span className="text-xs font-medium text-primary">{layer.label}</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <Badge variant="neutral" size="sm">{layer.count}</Badge>
                                        {activeLayers.includes(layer.id) ? (
                                            <Eye size={12} className="text-accent" />
                                        ) : (
                                            <EyeOff size={12} className="text-gray-300" />
                                        )}
                                    </div>
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Legend */}
                    <div className="tribal-card p-4">
                        <h3 className="font-bold text-primary text-sm mb-3">Legend</h3>
                        <div className="space-y-2 text-xs">
                            <div className="flex items-center gap-2">
                                <div className="w-3 h-3 rounded-full bg-emerald-500" />
                                <span className="text-gray-600">Granted Claims</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <div className="w-3 h-3 rounded-full bg-amber-500" />
                                <span className="text-gray-600">Pending Claims</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <div className="w-3 h-3 rounded-full bg-red-500" />
                                <span className="text-gray-600">Rejected Claims</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <div className="w-3 h-3 rounded-full bg-blue-500" />
                                <span className="text-gray-600">Village Boundary</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <div className="w-3 h-3 bg-red-500 animate-pulse" />
                                <span className="text-gray-600">Active Fire Alert</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Map Canvas */}
                <div className="lg:col-span-3 space-y-4">
                    {/* Map Container */}
                    <div className="tribal-card overflow-hidden h-[600px] relative">
                        {isMounted ? (
                            <MapContainer
                                center={[23.5, 78.0]}
                                zoom={5}
                                style={{ height: "100%", width: "100%" }}
                                scrollWheelZoom={true}
                            >
                                <TileLayer
                                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                                />
                                {activeLayers.includes("villages") &&
                                    claims.slice(0, 10).map((c, i) => (
                                        <Marker key={c.id} position={[22.048 + i * 0.1, 80.381 + i * 0.05]}>
                                            <Popup>
                                                <div className="text-xs">
                                                    <p className="font-bold text-primary">{c.villageName || "N/A"}</p>
                                                    <p className="text-gray-500">{c.district || "N/A"}</p>
                                                    <p className="mt-1">Claim ID: <b>{c.id}</b></p>
                                                    <p>Area: <b>{c.areaAcres || 0} acres</b></p>
                                                </div>
                                            </Popup>
                                        </Marker>
                                    ))}
                                {activeLayers.includes("fire-alerts") &&
                                    fireAlerts.filter((f) => f.status === "active").slice(0, 5).map((f, i) => (
                                        <Marker key={f.id} position={[22.2 + i * 0.15, 80.5 + i * 0.08]}>
                                            <Popup>
                                                <div className="text-xs">
                                                    <p className="font-bold text-red-600">🔥 Fire Alert</p>
                                                    <p className="font-semibold">{f.villageName || "N/A"}</p>
                                                    <p>Area: {f.areaAffectedHa || "Unknown"} ha</p>
                                                </div>
                                            </Popup>
                                        </Marker>
                                    ))}
                            </MapContainer>
                        ) : (
                            <div className="h-full flex items-center justify-center bg-gray-100">
                                <p className="text-gray-400">Loading map...</p>
                            </div>
                        )}
                    </div>

                    {/* State Summary Cards */}
                    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
                        {loading ? (
                            <StatCardSkeleton count={4} />
                        ) : error ? (
                            <ErrorDisplay title="Failed to Load States" message={error} showRetry={false} />
                        ) : states.length > 0 ? (
                            states.map((s) => (
                                <div key={s.id} className="tribal-card p-3">
                                    <div className="flex items-center justify-between mb-1">
                                        <span className="text-xs font-bold px-2 py-0.5 rounded-full text-white bg-primary">
                                            {s.id}
                                        </span>
                                        <span className="text-xs text-gray-400">State</span>
                                    </div>
                                    <p className="text-sm font-semibold text-primary">{s.name}</p>
                                    <div className="mt-2 space-y-1 text-xs">
                                        <div className="flex justify-between">
                                            <span className="text-gray-500">Claims:</span>
                                            <span className="font-bold">{claims.filter((c) => c.state === s.id).length}</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-gray-500">Granted:</span>
                                            <span className="font-bold text-emerald-600">{claims.filter((c) => c.state === s.id && c.status === "APPROVED").length}</span>
                                        </div>
                                    </div>
                                </div>
                            ))
                        ) : (
                            <p className="col-span-full text-center text-gray-400 text-sm">No state data available</p>
                        )}
                    </div>
                </div>

                {/* Village Search */}
                <div className="tribal-card p-4">
                    <div className="flex items-center gap-2 mb-3">
                        <Search size={14} className="text-gray-400" />
                        <h3 className="font-bold text-primary text-sm">Search Villages</h3>
                    </div>
                    <div className="relative mb-3">
                        <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Search village name, code, or GPS coordinates..."
                            className="w-full pl-9 pr-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:border-primary"
                        />
                    </div>
                    <div className="space-y-2">
                        {claims.slice(0, 5).map((v) => (
                            <div key={v.id} className="flex items-center justify-between p-2 rounded-lg hover:bg-gray-50 cursor-pointer">
                                <div>
                                    <p className="text-sm font-semibold text-primary">{v.villageName || "N/A"}</p>
                                    <p className="text-xs text-gray-500">{v.district || "N/A"}</p>
                                </div>
                                <div className="flex items-center gap-2">
                                    <Badge variant="success" size="sm">{v.grantedClaims}</Badge>
                                    <ChevronRight size={14} className="text-gray-300" />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
        </DashboardLayout >
    );
}

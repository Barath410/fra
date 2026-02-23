"use client";
import React, { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";
import {
    Layers,
    Plus,
    Minus,
    Maximize2,
    Download,
    Filter,
    Eye,
    EyeOff,
    Info,
    X,
    Map as MapIcon,
    FlameIcon,
    Droplets,
    Trees,
    Home,
    ZoomIn,
    Navigation,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Progress, SaturationRing } from "@/components/ui/progress";
import type { MapLayer } from "@/types";

// Default map layers
const DEFAULT_LAYERS: MapLayer[] = [
    { id: "admin-boundaries", name: "Administrative Boundaries", category: "administrative", enabled: true, opacity: 0.8, color: "#6b7280", description: "State, district, block, village boundaries", source: "Census 2011 / LGD" },
    { id: "ifr-boundaries", name: "IFR Patta Boundaries", category: "fra", enabled: true, opacity: 0.7, color: "#4f46e5", description: "Individual Forest Rights granted areas", source: "State FRA Cells" },
    { id: "cfr-boundaries", name: "CFR Boundaries", category: "fra", enabled: true, opacity: 0.6, color: "#16a34a", description: "Community Forest Resource Rights", source: "State FRA Cells" },
    { id: "cr-boundaries", name: "Community Rights", category: "fra", enabled: false, opacity: 0.6, color: "#d97706", description: "Community Rights areas", source: "State FRA Cells" },
    { id: "fsi-forest-cover", name: "Forest Cover (FSI)", category: "environment", enabled: true, opacity: 0.5, color: "#15803d", description: "Forest Survey of India biennial forest cover", source: "FSI 2023" },
    { id: "ndvi-health", name: "NDVI Vegetation Health", category: "environment", enabled: false, opacity: 0.6, color: "#84cc16", description: "Sentinel-2 derived NDVI — quarterly", source: "ESA Sentinel-2" },
    { id: "water-bodies", name: "Water Bodies (AI-detected)", category: "assets", enabled: true, opacity: 0.7, color: "#0ea5e9", description: "AI-detected ponds, streams, water sources", source: "Satellite CV" },
    { id: "farmland", name: "Agricultural Land", category: "assets", enabled: false, opacity: 0.6, color: "#ca8a04", description: "AI-detected agricultural areas in FRA villages", source: "Satellite CV" },
    { id: "groundwater", name: "Groundwater Depth", category: "assets", enabled: false, opacity: 0.5, color: "#0284c7", description: "CGWB district-level depth to water table", source: "CGWB" },
    { id: "css-pmkisan", name: "PM-KISAN Coverage", category: "schemes", enabled: false, opacity: 0.6, color: "#22c55e", description: "PM-KISAN enrollment saturation", source: "MoA API" },
    { id: "css-jjm", name: "JJM Coverage", category: "schemes", enabled: false, opacity: 0.6, color: "#0ea5e9", description: "Jal Jeevan Mission household connections", source: "JJM IMIS" },
    { id: "dajgua-saturation", name: "DA-JGUA Saturation", category: "schemes", enabled: false, opacity: 0.6, color: "#e87722", description: "Dharti Aaba Janjatiya Gram Utkarsh Abhiyan", source: "MoTA" },
    { id: "gati-shakti-infra", name: "PM GatiShakti Infra", category: "schemes", enabled: false, opacity: 0.5, color: "#7c3aed", description: "Infrastructure layers from PM GatiShakti", source: "PM GatiShakti NMP" },
    { id: "fire-alerts", name: "Forest Fire Alerts", category: "alerts", enabled: true, opacity: 1.0, color: "#ef4444", description: "Real-time fire alerts from ISRO FIRMS / VIIRS", source: "ISRO FIRMS" },
];

const CATEGORY_LABELS: Record<string, string> = {
    administrative: "Administrative",
    fra: "FRA Boundaries",
    assets: "Village Assets",
    schemes: "CSS Schemes",
    environment: "Environment",
    alerts: "Alerts",
};

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
    administrative: <MapIcon size={13} />,
    fra: <Trees size={13} />,
    assets: <Home size={13} />,
    schemes: <Navigation size={13} />,
    environment: <Trees size={13} />,
    alerts: <FlameIcon size={13} />,
};

interface VillagePopupData {
    name: string;
    district: string;
    state: string;
    totalClaims: number;
    grantedClaims: number;
    saturationScore: number;
    ndvi?: number;
    waterBodies?: number;
}

interface FRAAtlasProps {
    height?: string;
    showLayerPanel?: boolean;
    showFilterPanel?: boolean;
    showVillagePopup?: boolean;
    initialCenter?: [number, number];
    initialZoom?: number;
    filterState?: string;
    filterDistrict?: string;
    className?: string;
    onVillageClick?: (village: VillagePopupData) => void;
}

export function FRAAtlas({
    height = "h-full",
    showLayerPanel = true,
    showFilterPanel = false,
    initialCenter = [21.5, 82.5],
    initialZoom = 5,
    filterState,
    filterDistrict,
    className,
    onVillageClick,
}: FRAAtlasProps) {
    const mapRef = useRef<HTMLDivElement>(null);
    const leafletMapRef = useRef<unknown>(null);
    const [layers, setLayers] = useState<MapLayer[]>(DEFAULT_LAYERS);
    const [layerPanelOpen, setLayerPanelOpen] = useState(showLayerPanel);
    const [selectedVillage, setSelectedVillage] = useState<VillagePopupData | null>(null);
    const [mapLoaded, setMapLoaded] = useState(false);
    const [activeBaseMap, setActiveBaseMap] = useState<"bhuvan" | "osm" | "satellite">("bhuvan");
    const [zoom, setZoom] = useState(initialZoom);

    useEffect(() => {
        if (typeof window === "undefined" || !mapRef.current || leafletMapRef.current) return;

        // Dynamic import for SSR safety
        import("leaflet").then((L) => {
            // Fix default icon paths
            delete (L.Icon.Default.prototype as unknown as Record<string, unknown>)._getIconUrl;
            L.Icon.Default.mergeOptions({
                iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",
                iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",
                shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
            });

            const map = L.map(mapRef.current!, {
                center: initialCenter,
                zoom: initialZoom,
                zoomControl: false,
                attributionControl: true,
            });

            // Base tile layer (OSM as default accessible option)
            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                attribution: "© OpenStreetMap | NIC | ISRO Bhuvan",
                maxZoom: 18,
            }).addTo(map);

            // Add village markers from API (or default empty if no villages)
            const villages = leafletMapRef.current ? (leafletMapRef.current as any).villages || [] : [];
            villages.forEach((v: any) => {
                const gpsLat = v.latitude || v.gpsCenter?.lat || 22.5;
                const gpsLng = v.longitude || v.gpsCenter?.lng || 82.5;
                const saturationScore = v.saturationScore || 0;
                const color = saturationScore >= 70 ? "#22c55e" : saturationScore >= 50 ? "#f59e0b" : "#ef4444";
                const icon = L.divIcon({
                    html: `<div style="width:10px;height:10px;border-radius:50%;background:${color};border:2px solid white;box-shadow:0 1px 4px rgba(0,0,0,0.3)"></div>`,
                    className: "",
                    iconSize: [10, 10],
                    iconAnchor: [5, 5],
                });

                const marker = L.marker([gpsLat, gpsLng], { icon });
                marker.bindPopup(
                    `<div style="font-family:Noto Sans,sans-serif;min-width:200px">
            <div style="background:#13382e;color:white;padding:8px 12px;margin:-14px -14px 10px;border-radius:4px 4px 0 0">
              <strong style="font-size:13px">${v.name}</strong><br/>
              <span style="font-size:10px;opacity:0.7">${v.block}, ${v.district}</span>
            </div>
            <div style="padding:0 4px">
              <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                <span style="font-size:11px;color:#6b7280">Total Claims</span>
                <strong style="font-size:11px">${v.totalClaims}</strong>
              </div>
              <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                <span style="font-size:11px;color:#6b7280">Granted</span>
                <strong style="font-size:11px;color:#16a34a">${v.grantedClaims}</strong>
              </div>
              <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                <span style="font-size:11px;color:#6b7280">Saturation</span>
                <strong style="font-size:11px;color:${color}">${v.saturationScore}%</strong>
              </div>
              <div style="background:#f3f4f6;border-radius:4px;height:6px;overflow:hidden">
                <div style="width:${v.saturationScore}%;height:100%;background:${color};border-radius:4px"></div>
              </div>
            </div>
          </div>`
                );
                marker.on("click", () => {
                    setSelectedVillage({
                        name: v.name,
                        district: v.district,
                        state: v.state,
                        totalClaims: v.totalClaims,
                        grantedClaims: v.grantedClaims,
                        saturationScore: v.saturationScore,
                        ndvi: v.assets.ndviScore,
                        waterBodies: v.assets.waterBodiesCount,
                    });
                    onVillageClick?.({
                        name: v.name,
                        district: v.district,
                        state: v.state,
                        totalClaims: v.totalClaims,
                        grantedClaims: v.grantedClaims,
                        saturationScore: v.saturationScore,
                    });
                });
                marker.addTo(map);
            });

            // Zoom event
            map.on("zoomend", () => setZoom(map.getZoom()));

            leafletMapRef.current = map;
            setMapLoaded(true);
        });

        return () => {
            if (leafletMapRef.current) {
                (leafletMapRef.current as { remove: () => void }).remove();
                leafletMapRef.current = null;
            }
        };
    }, []);

    const toggleLayer = (layerId: string) => {
        setLayers((prev) =>
            prev.map((l) => (l.id === layerId ? { ...l, enabled: !l.enabled } : l))
        );
    };

    const groupedLayers = layers.reduce<Record<string, MapLayer[]>>((acc, l) => {
        if (!acc[l.category]) acc[l.category] = [];
        acc[l.category].push(l);
        return acc;
    }, {});

    const enabledCount = layers.filter((l) => l.enabled).length;

    return (
        <div className={cn("relative flex overflow-hidden rounded-xl border border-gray-200 bg-white", height, className)}>
            {/* Map */}
            <div
                ref={mapRef}
                className="flex-1 h-full"
                aria-label="FRA Interactive Atlas Map"
            />

            {/* Loading overlay */}
            {!mapLoaded && (
                <div className="absolute inset-0 flex items-center justify-center bg-forest-50 z-20">
                    <div className="text-center">
                        <div className="w-12 h-12 border-3 border-forest-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
                        <p className="text-sm text-forest-600 font-medium">Loading FRA Atlas...</p>
                        <p className="text-xs text-gray-400 mt-1">Initializing spatial layers</p>
                    </div>
                </div>
            )}

            {/* Map Controls — top right */}
            <div className="absolute top-3 right-3 z-10 flex flex-col gap-1.5">
                {/* Layer toggle */}
                <button
                    onClick={() => setLayerPanelOpen(!layerPanelOpen)}
                    className={cn(
                        "w-8 h-8 bg-white rounded-lg shadow-card-sm border border-gray-200 flex items-center justify-center text-gray-600 hover:text-forest-700 hover:border-forest-300 transition-all",
                        layerPanelOpen && "bg-forest-800 text-white border-forest-800"
                    )}
                    title="Toggle layer panel"
                >
                    <Layers size={15} />
                </button>

                {/* Zoom controls */}
                <button
                    onClick={() => (leafletMapRef.current as { zoomIn: () => void } | null)?.zoomIn()}
                    className="w-8 h-8 bg-white rounded-t-lg rounded-b-none shadow-sm border border-gray-200 flex items-center justify-center text-gray-600 hover:text-forest-700 transition-colors"
                    title="Zoom in"
                >
                    <Plus size={14} />
                </button>
                <button
                    onClick={() => (leafletMapRef.current as { zoomOut: () => void } | null)?.zoomOut()}
                    className="w-8 h-8 bg-white rounded-b-lg rounded-t-none shadow-sm border-l border-r border-b border-gray-200 flex items-center justify-center text-gray-600 hover:text-forest-700 transition-colors"
                    title="Zoom out"
                >
                    <Minus size={14} />
                </button>

                {/* Fullscreen */}
                <button
                    className="w-8 h-8 bg-white rounded-lg shadow-card-sm border border-gray-200 flex items-center justify-center text-gray-600 hover:text-forest-700 transition-colors mt-1"
                    title="Fullscreen"
                >
                    <Maximize2 size={14} />
                </button>

                {/* Download */}
                <button
                    className="w-8 h-8 bg-white rounded-lg shadow-card-sm border border-gray-200 flex items-center justify-center text-gray-600 hover:text-forest-700 transition-colors"
                    title="Export map"
                >
                    <Download size={14} />
                </button>
            </div>

            {/* Base map switcher — bottom left */}
            <div className="absolute bottom-6 left-3 z-10 flex gap-1">
                {(["bhuvan", "osm", "satellite"] as const).map((bm) => (
                    <button
                        key={bm}
                        onClick={() => setActiveBaseMap(bm)}
                        className={cn(
                            "px-2 py-1 text-[10px] font-semibold rounded border transition-all",
                            activeBaseMap === bm
                                ? "bg-forest-800 text-white border-forest-800"
                                : "bg-white text-gray-600 border-gray-200 hover:border-forest-300"
                        )}
                    >
                        {bm === "bhuvan" ? "Bhuvan" : bm === "osm" ? "OSM" : "Satellite"}
                    </button>
                ))}
            </div>

            {/* Scale + Zoom indicator */}
            <div className="absolute bottom-3 right-3 z-10 flex items-center gap-2">
                <div className="bg-white/90 backdrop-blur-sm rounded-md px-2 py-1 text-[10px] text-gray-500 border border-gray-200">
                    Zoom: {zoom}
                </div>
                <div className="bg-white/90 backdrop-blur-sm rounded-md px-2 py-1 text-[10px] text-gray-500 border border-gray-200">
                    {enabledCount} layers active
                </div>
            </div>

            {/* Layer Panel */}
            {layerPanelOpen && (
                <div className="absolute top-3 left-3 z-20 w-64 bg-white rounded-xl shadow-card-lg border border-gray-200 overflow-hidden animate-fade-up max-h-[calc(100%-1.5rem)] flex flex-col">
                    <div className="flex items-center justify-between px-3 py-2.5 bg-forest-900">
                        <div className="flex items-center gap-2">
                            <Layers size={14} className="text-white" />
                            <span className="text-white text-xs font-semibold">Map Layers</span>
                            <span className="text-white/50 text-[10px]">({enabledCount} on)</span>
                        </div>
                        <button
                            onClick={() => setLayerPanelOpen(false)}
                            className="text-white/60 hover:text-white"
                        >
                            <X size={13} />
                        </button>
                    </div>

                    <div className="overflow-y-auto flex-1 py-1">
                        {Object.entries(groupedLayers).map(([cat, catLayers]) => (
                            <div key={cat} className="mb-1">
                                <div className="flex items-center gap-1.5 px-3 py-1.5 bg-gray-50 border-y border-gray-100">
                                    <span className="text-gray-500">{CATEGORY_ICONS[cat]}</span>
                                    <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">
                                        {CATEGORY_LABELS[cat]}
                                    </span>
                                </div>
                                {catLayers.map((layer) => (
                                    <button
                                        key={layer.id}
                                        onClick={() => toggleLayer(layer.id)}
                                        className="w-full flex items-center gap-2.5 px-3 py-2 hover:bg-gray-50 transition-colors text-left"
                                        title={layer.description}
                                    >
                                        <div
                                            className={cn(
                                                "w-4 h-4 rounded border-2 flex items-center justify-center shrink-0 transition-all",
                                                layer.enabled
                                                    ? "border-transparent"
                                                    : "border-gray-300 bg-white"
                                            )}
                                            style={layer.enabled ? { background: layer.color } : {}}
                                        >
                                            {layer.enabled && (
                                                <svg viewBox="0 0 10 8" className="w-2.5 h-2 fill-white">
                                                    <path d="M1 4l3 3 5-6" stroke="white" strokeWidth="1.5" fill="none" strokeLinecap="round" strokeLinejoin="round" />
                                                </svg>
                                            )}
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <p className={cn(
                                                "text-xs leading-tight",
                                                layer.enabled ? "text-gray-800 font-medium" : "text-gray-400"
                                            )}>
                                                {layer.name}
                                            </p>
                                            <p className="text-[9px] text-gray-400">{layer.source}</p>
                                        </div>
                                        <div
                                            className="w-3 h-3 rounded-sm shrink-0 opacity-60"
                                            style={{ background: layer.color }}
                                        />
                                    </button>
                                ))}
                            </div>
                        ))}
                    </div>

                    <div className="px-3 py-2 border-t border-gray-100 bg-gray-50 flex gap-2">
                        <button
                            onClick={() => setLayers((prev) => prev.map((l) => ({ ...l, enabled: true })))}
                            className="flex-1 text-[10px] font-semibold text-forest-600 hover:text-forest-800 text-center py-1 rounded border border-forest-200 hover:bg-forest-50 transition-colors"
                        >
                            Show All
                        </button>
                        <button
                            onClick={() => setLayers((prev) => prev.map((l) => ({ ...l, enabled: false })))}
                            className="flex-1 text-[10px] font-semibold text-gray-500 hover:text-gray-700 text-center py-1 rounded border border-gray-200 hover:bg-gray-100 transition-colors"
                        >
                            Hide All
                        </button>
                    </div>
                </div>
            )}

            {/* Village info popup */}
            {selectedVillage && (
                <div className="absolute bottom-16 right-3 z-20 w-56 bg-white rounded-xl shadow-card-lg border border-gray-200 overflow-hidden animate-fade-up">
                    <div className="flex items-center justify-between px-3 py-2 bg-forest-900">
                        <span className="text-white text-xs font-semibold truncate">{selectedVillage.name}</span>
                        <button
                            onClick={() => setSelectedVillage(null)}
                            className="text-white/60 hover:text-white ml-2 shrink-0"
                        >
                            <X size={13} />
                        </button>
                    </div>
                    <div className="p-3 space-y-2">
                        <p className="text-[10px] text-gray-500">{selectedVillage.district}, {selectedVillage.state}</p>
                        <div className="grid grid-cols-2 gap-2">
                            <div className="bg-gray-50 rounded-lg p-1.5 text-center">
                                <p className="text-[18px] font-bold text-forest-700 tabular-nums">{selectedVillage.grantedClaims}</p>
                                <p className="text-[9px] text-gray-500">Claims Granted</p>
                            </div>
                            <div className="bg-gray-50 rounded-lg p-1.5 text-center">
                                <p className="text-[18px] font-bold text-amber-600 tabular-nums">{selectedVillage.totalClaims - selectedVillage.grantedClaims}</p>
                                <p className="text-[9px] text-gray-500">Pending</p>
                            </div>
                        </div>
                        <div>
                            <div className="flex justify-between items-center mb-1">
                                <span className="text-[10px] text-gray-500">Scheme Saturation</span>
                                <span className="text-[10px] font-bold text-forest-700">{selectedVillage.saturationScore}%</span>
                            </div>
                            <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                                <div
                                    className="h-full rounded-full transition-all"
                                    style={{
                                        width: `${selectedVillage.saturationScore}%`,
                                        background: selectedVillage.saturationScore >= 70 ? "#22c55e" : selectedVillage.saturationScore >= 50 ? "#f59e0b" : "#ef4444",
                                    }}
                                />
                            </div>
                        </div>
                        {selectedVillage.ndvi !== undefined && (
                            <div className="flex items-center justify-between">
                                <span className="text-[10px] text-gray-500 flex items-center gap-1">
                                    <Trees className="w-3 h-3 text-green-500" />
                                    NDVI Score
                                </span>
                                <span className="text-[10px] font-bold text-green-600">{selectedVillage.ndvi.toFixed(2)}</span>
                            </div>
                        )}
                        <Button size="sm" variant="outline" fullWidth className="mt-1 text-[10px]">
                            View Full Profile →
                        </Button>
                    </div>
                </div>
            )}

            {/* Legend */}
            <div className="absolute bottom-16 left-3 z-10 bg-white/90 backdrop-blur-sm rounded-lg border border-gray-200 p-2">
                <p className="text-[9px] font-bold text-gray-500 uppercase mb-1.5">Saturation Legend</p>
                <div className="space-y-1">
                    {[
                        { color: "#22c55e", label: "High (≥70%)" },
                        { color: "#f59e0b", label: "Medium (50–70%)" },
                        { color: "#ef4444", label: "Low (<50%)" },
                    ].map((item) => (
                        <div key={item.label} className="flex items-center gap-1.5">
                            <div className="w-2.5 h-2.5 rounded-full shrink-0" style={{ background: item.color }} />
                            <span className="text-[9px] text-gray-600">{item.label}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

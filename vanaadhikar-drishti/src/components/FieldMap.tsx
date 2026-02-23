"use client";

import { useState, useRef, useCallback } from "react";
import Map, { NavigationControl, FullscreenControl, Source, Layer, MapRef } from "react-map-gl";
import { Search, Layers, Compass, Locate, Plus, Minus, MapPin, Globe, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";

// Mapbox token comes from the environment so it never lands in source control
const MAPBOX_TOKEN = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || "";

// Mock GeoJSON for a village boundary (Barwani District example area)
const VILLAGE_BOUNDARY_GEOJSON = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: { name: "Barwani Forest Area", type: "forest" },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [74.902, 22.071],
            [74.908, 22.071],
            [74.908, 22.078],
            [74.902, 22.078],
            [74.902, 22.071]
          ]
        ]
      }
    }
  ]
};

// Mock GeoJSON for a specific claim boundary
const CLAIM_BOUNDARY_GEOJSON = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: { id: "CLA-2024-001", status: "pending" },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [74.904, 22.073],
            [74.906, 22.073],
            [74.906, 22.075],
            [74.904, 22.075],
            [74.904, 22.073]
          ]
        ]
      }
    }
  ]
};

export default function FieldMap() {
  const mapRef = useRef<MapRef>(null);
  const [mapStyle, setMapStyle] = useState("mapbox://styles/mapbox/satellite-streets-v12");
  const [viewState, setViewState] = useState({
    latitude: 22.074,
    longitude: 74.905,
    zoom: 14
  });
  const [isSearching, setIsSearching] = useState(false);
  const [showClaim, setShowClaim] = useState(false);

  // Toggle between Satellite and Street view
  const toggleMapStyle = () => {
    setMapStyle(prev => 
      prev === "mapbox://styles/mapbox/satellite-streets-v12" 
        ? "mapbox://styles/mapbox/streets-v12" 
        : "mapbox://styles/mapbox/satellite-streets-v12"
    );
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSearching(true);
    // Simulate API search delay
    setTimeout(() => {
      setIsSearching(false);
      setShowClaim(true);
      // Fly to the claim location
      mapRef.current?.flyTo({
        center: [74.905, 22.074],
        zoom: 16,
        duration: 2000
      });
    }, 1500);
  };

  const resetView = () => {
    setShowClaim(false);
    mapRef.current?.flyTo({
      center: [74.905, 22.074],
      zoom: 14,
      duration: 1500
    });
  };

  return (
    <div className="relative w-full h-full overflow-hidden">
      
      <Map
        ref={mapRef}
        initialViewState={viewState}
        onMove={evt => setViewState(evt.viewState)}
        style={{ width: "100%", height: "100%" }}
        mapStyle={mapStyle}
        mapboxAccessToken={MAPBOX_TOKEN}
        attributionControl={false}
      >
        <NavigationControl position="bottom-right" />
        <FullscreenControl position="top-right" />

        {/* Village Boundary Layer (Green Outline) */}
        <Source id="village-boundary" type="geojson" data={VILLAGE_BOUNDARY_GEOJSON as any}>
          <Layer
            id="village-boundary-fill"
            type="fill"
            paint={{
              "fill-color": "#10B981",
              "fill-opacity": 0.1
            }}
          />
          <Layer
            id="village-boundary-line"
            type="line"
            paint={{
              "line-color": "#10B981",
              "line-width": 2,
              "line-dasharray": [2, 1]
            }}
          />
        </Source>

        {/* Specific Claim Layer (Orange Outline) - Shown on search */}
        {showClaim && (
          <Source id="claim-boundary" type="geojson" data={CLAIM_BOUNDARY_GEOJSON as any}>
            <Layer
              id="claim-boundary-fill"
              type="fill"
              paint={{
                "fill-color": "#F59E0B",
                "fill-opacity": 0.3
              }}
            />
            <Layer
              id="claim-boundary-line"
              type="line"
              paint={{
                "line-color": "#F59E0B",
                "line-width": 3
              }}
            />
            {/* Outline Glow Effect */}
            <Layer
              id="claim-boundary-glow"
              type="line"
              paint={{
                "line-color": "#F59E0B",
                "line-width": 8,
                "line-opacity": 0.3,
                "line-blur": 4
              }}
            />
          </Source>
        )}

      </Map>

      {/* Floating Search Bar */}
      <div className="absolute top-4 left-4 z-10 w-96 max-w-[calc(100vw-2rem)] bg-white shadow-xl rounded-lg border border-gray-200 overflow-hidden">
        <form onSubmit={handleSearch} className="relative">
          <input 
            type="text" 
            className="w-full px-4 py-3 pr-12 text-sm border-b outline-none placeholder-gray-500 text-gray-900" 
            placeholder="Search Claim ID (e.g. CLA-2024-001)..." 
          />
          <button type="submit" className="absolute right-0 top-0 h-full w-12 flex items-center justify-center hover:bg-gray-50 text-blue-600">
            {isSearching ? <Loader2 className="h-5 w-5 animate-spin" /> : <Search className="h-5 w-5" />}
          </button>
        </form>
        
        {/* Results / List */}
        {!isSearching && !showClaim && (
          <div className="max-h-60 overflow-y-auto bg-white/95 backdrop-blur-sm">
             <div className="px-4 py-2 text-xs font-semibold text-gray-400 bg-gray-50 border-b">SUGGESTED</div>
             <div onClick={handleSearch} className="p-3 hover:bg-blue-50 cursor-pointer flex items-center gap-3 border-b border-gray-100 transition-colors">
                 <div className="bg-orange-100 p-2 rounded-full text-orange-600"><MapPin className="h-4 w-4" /></div>
                 <div>
                    <div className="text-sm font-medium text-gray-900">Claim #CLA-2024-001</div>
                    <div className="text-xs text-gray-500">Pending Verification • Barwani</div>
                 </div>
             </div>
             <div className="p-3 hover:bg-gray-50 cursor-pointer flex items-center gap-3 transition-colors opacity-60">
                 <div className="bg-green-100 p-2 rounded-full text-green-600"><Globe className="h-4 w-4" /></div>
                 <div>
                    <div className="text-sm font-medium text-gray-900">Barwani Forest Range</div>
                    <div className="text-xs text-gray-500">Official Boundary</div>
                 </div>
             </div>
          </div>
        )}

        {/* Selected Claim Details Card */}
        {showClaim && (
           <div className="p-4 bg-white animate-in slide-in-from-top-2 fade-in">
              <div className="flex items-start justify-between mb-3">
                 <div>
                    <h3 className="font-bold text-gray-900 text-lg">Claim #CLA-2024-001</h3>
                    <p className="text-sm text-gray-500">Applicant: Rameshwar Singh</p>
                 </div>
                 <span className="px-2 py-1 bg-orange-100 text-orange-700 text-xs font-bold rounded">PENDING</span>
              </div>
              
              <div className="grid grid-cols-2 gap-2 text-xs text-gray-600 mb-4 bg-gray-50 p-3 rounded-lg border border-dashed">
                 <div><span className="block font-semibold">Area:</span> 2.5 Acres</div>
                 <div><span className="block font-semibold">Coords:</span> 22.074, 74.905</div>
                 <div><span className="block font-semibold">Type:</span> Individual (IFR)</div>
                 <div><span className="block font-semibold">Boundary:</span> 5 Points</div>
              </div>

              <div className="flex gap-2">
                 <Button size="sm" className="w-full bg-blue-600 hover:bg-blue-700" onClick={() => alert("Starting survey...")}>
                    Start Verification
                 </Button>
                 <Button size="sm" variant="outline" className="w-full border-gray-300 text-gray-700" onClick={resetView}>
                    Clear
                 </Button>
              </div>
           </div>
        )}
      </div>

       {/* Map Controls */}
       <div className="absolute top-4 right-12 z-10 flex flex-col gap-2"> {/* Shifted left to avoid overlap with Fullscreen */}
           <button 
              onClick={toggleMapStyle}
              className="bg-white p-2 rounded-md shadow-md border hover:bg-gray-50 group relative hover:bg-blue-50" 
              title="Toggle Satellite/Street"
           >
               <Layers className="h-5 w-5 text-gray-700 group-hover:text-blue-600" />
               <span className="absolute right-full mr-3 top-1/2 -translate-y-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                  {mapStyle.includes('satellite') ? "Switch to Streets" : "Switch to Satellite"}
               </span>
           </button>
       </div>

       <div className="absolute bottom-8 left-8 z-10 bg-white/90 backdrop-blur-sm px-3 py-1.5 rounded shadow text-xs font-mono text-gray-600 border border-gray-200">
           {viewState.latitude.toFixed(4)}° N, {viewState.longitude.toFixed(4)}° E | Zoom: {viewState.zoom.toFixed(1)}
       </div>

       <div className="absolute bottom-8 right-12 z-10 bg-white p-3 rounded-lg shadow-lg border w-56">
           <h4 className="font-semibold text-xs uppercase text-gray-500 mb-2 tracking-wider">Legend</h4>
           <div className="space-y-1.5">
               <div className="flex items-center gap-2 text-xs text-gray-700 font-medium"><span className="w-3 h-3 rounded-sm bg-green-500/20 border border-green-500 border-dashed"></span> Village Boundary</div>
               <div className="flex items-center gap-2 text-xs text-gray-700 font-medium"><span className="w-3 h-3 rounded-sm bg-orange-500/40 border-2 border-orange-500"></span> Selected Claim</div>
               <div className="flex items-center gap-2 text-xs text-gray-700 font-medium"><span className="w-3 h-3 rounded-full bg-blue-500 border border-blue-600"></span> My Location</div>
           </div>
       </div>

    </div>
  );
}

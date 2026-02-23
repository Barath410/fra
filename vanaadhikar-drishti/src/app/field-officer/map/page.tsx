"use client";

import dynamic from "next/dynamic";
import { Loader2 } from "lucide-react";

// Dynamically import the map component with SSR disabled
const FieldMap = dynamic(() => import("@/components/FieldMap"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-screen flex flex-col items-center justify-center bg-gray-100 text-gray-500">
      <Loader2 className="h-8 w-8 animate-spin text-blue-600 mb-2" />
      <p className="text-sm font-medium">Loading Map...</p>
    </div>
  ),
});

export default function FieldMapPage() {
  return (
    <div className="w-full h-full min-h-screen bg-gray-100">
      <FieldMap />
    </div>
  );
}

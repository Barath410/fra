"use client";

import React from "react";
import Link from "next/link";
import { LucideIcon, FileText, Map as MapIcon, LayoutDashboard, ClipboardList, BarChart3, ArrowRight } from "lucide-react";
import { useDashboardData } from "@/lib/use-dashboard-data";
import { StatCard } from "@/components/ui/stat-card";
import { formatNumber } from "@/lib/utils";

interface PlaceholderPageProps {
  title: string;
  description?: string;
  type?: "dashboard" | "map" | "list" | "form" | "content";
}

export function PlaceholderPage({ title, description = "Live data preview for this module.", type = "content" }: PlaceholderPageProps) {
  const getIcon = (): LucideIcon => {
    switch (type) {
      case "dashboard":
        return LayoutDashboard;
      case "map":
        return MapIcon;
      case "list":
        return ClipboardList;
      case "form":
        return FileText;
      default:
        return BarChart3;
    }
  };

  const Icon = getIcon();
  const { data, loading, error } = useDashboardData();
  const national = data?.nationalStats;
  const claims = data?.claims?.slice(0, 5) ?? [];
  const villages = data?.villages?.slice(0, 4) ?? [];

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">{title}</h1>
          <p className="text-gray-500 mt-1">{description}</p>
        </div>
        <div className="p-2 bg-blue-50 rounded-lg">
          <Icon className="w-6 h-6 text-blue-600" />
        </div>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Total Claims" value={national?.totalClaims ?? 0} icon={<FileText size={18} />} accentColor="#2563EB" />
        <StatCard title="Granted" value={national?.totalGranted ?? 0} icon={<LayoutDashboard size={18} />} accentColor="#10B981" />
        <StatCard title="Pending" value={national?.totalPending ?? 0} icon={<ClipboardList size={18} />} accentColor="#F59E0B" />
        <StatCard title="Villages" value={national?.totalVillagesCovered ?? villages.length} icon={<MapIcon size={18} />} accentColor="#8B5CF6" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="tribal-card p-5">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold text-primary">Recent Claims</h3>
            <Link href="/sdlc/dashboard" className="text-xs text-accent hover:underline flex items-center gap-1">
              Manage Claims <ArrowRight size={12} />
            </Link>
          </div>
          {loading && <p className="text-xs text-gray-500">Loading claims…</p>}
          {error && <p className="text-xs text-red-600">{error}</p>}
          <div className="space-y-2">
            {claims.map((c) => (
              <div key={c.id} className="flex items-center justify-between text-xs border-b last:border-0 pb-2 last:pb-0">
                <div>
                  <p className="font-semibold text-primary">{c.claimantName}</p>
                  <p className="text-gray-500">{c.villageName}, {c.state}</p>
                </div>
                <div className="text-right">
                  <p className="font-medium">{c.claimType}</p>
                  <p className="text-gray-400">{c.status.replace(/-/g, " ")}</p>
                </div>
              </div>
            ))}
            {claims.length === 0 && !loading && <p className="text-xs text-gray-500">No claims found in the database.</p>}
          </div>
        </div>

        <div className="tribal-card p-5">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold text-primary">Villages Snapshot</h3>
            <Link href="/atlas" className="text-xs text-accent hover:underline flex items-center gap-1">
              Open Atlas <ArrowRight size={12} />
            </Link>
          </div>
          <div className="space-y-2">
            {villages.map((v) => (
              <div key={v.code} className="flex items-center justify-between text-xs border-b last:border-0 pb-2 last:pb-0">
                <div>
                  <p className="font-semibold text-primary">{v.name}</p>
                  <p className="text-gray-500">{v.block}, {v.district}</p>
                </div>
                <div className="text-right">
                  <p className="font-medium">{formatNumber(v.grantedClaims)}/{formatNumber(v.totalClaims)}</p>
                  <p className="text-gray-400">Sat. {v.saturationScore}%</p>
                </div>
              </div>
            ))}
            {villages.length === 0 && <p className="text-xs text-gray-500">No villages synced yet.</p>}
          </div>
        </div>
      </div>

      <div className="flex flex-wrap gap-3">
        <Link href="/national-dashboard" className="text-xs px-3 py-2 bg-primary text-white rounded-lg hover:bg-primary-600 transition-all">
          Go to National Dashboard
        </Link>
        <Link href="/grievances" className="text-xs px-3 py-2 bg-accent text-white rounded-lg hover:bg-accent/90 transition-all">
          Open Grievances
        </Link>
      </div>
    </div>
  );
}

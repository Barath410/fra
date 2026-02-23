"use client";
import React from "react";
import {
    AreaChart,
    Area,
    BarChart,
    Bar,
    LineChart,
    Line,
    PieChart,
    Pie,
    Cell,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
    RadarChart,
    Radar,
    PolarGrid,
    PolarAngleAxis,
    PolarRadiusAxis,
    ComposedChart,
} from "recharts";

// ── Colors ────────────────────────────────────────────────────────────────────
const PRIMARY = "#2563EB";
const SUCCESS = "#10B981";
const WARNING = "#F59E0B";
const DANGER = "#EF4444";
const BLUE = "#2563EB";
const AMBER = "#F59E0B";
const PURPLE = "#8b5cf6";
const EMERALD = "#10B981";
const RED = "#EF4444";

// ── Custom Tooltip ─────────────────────────────────────────────────────────────
const CustomTooltip = ({ active, payload, label }: { active?: boolean; payload?: Array<{ name: string; value: number; color: string }>; label?: string }) => {
    if (!active || !payload?.length) return null;
    return (
        <div className="bg-white border border-gray-200 rounded-xl shadow-lg p-3 text-xs">
            <p className="font-semibold text-forest-800 mb-2 border-b border-gray-100 pb-1.5">{label}</p>
            {payload.map((p, i) => (
                <div key={i} className="flex items-center gap-2 mt-1">
                    <div className="w-2 h-2 rounded-full shrink-0" style={{ background: p.color }} />
                    <span className="text-gray-500">{p.name}:</span>
                    <span className="font-bold tabular-nums" style={{ color: p.color }}>
                        {typeof p.value === "number" && p.value > 1000
                            ? p.value.toLocaleString("en-IN")
                            : p.value}
                    </span>
                </div>
            ))}
        </div>
    );
};

// ── Monthly Claims Progress Chart ─────────────────────────────────────────────
export function MonthlyProgressChart({ data }: { data: Array<{ month: string; claimsReceived: number; claimsGranted: number; claimsRejected: number }> }) {
    return (
        <ResponsiveContainer width="100%" height={220}>
            <ComposedChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
                <CartesianGrid strokeDasharray="4 2" stroke="#f3f4f6" />
                <XAxis dataKey="month" tick={{ fontSize: 10, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 10, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "12px" }} />
                <Bar dataKey="claimsReceived" name="Received" fill={BLUE} radius={[3, 3, 0, 0]} opacity={0.7} />
                <Bar dataKey="claimsGranted" name="Granted" fill={EMERALD} radius={[3, 3, 0, 0]} />
                <Bar dataKey="claimsRejected" name="Rejected" fill={RED} radius={[3, 3, 0, 0]} opacity={0.6} />
                <Line dataKey="claimsGranted" name="" dot={false} stroke={EMERALD} strokeWidth={2} legendType="none" />
            </ComposedChart>
        </ResponsiveContainer>
    );
}

// ── State Saturation Bar Chart ─────────────────────────────────────────────────
export function StateSaturationChart({ data }: { data: Array<{ name: string; saturationPct: number; color: string }> }) {
    return (
        <ResponsiveContainer width="100%" height={180}>
            <BarChart data={data} layout="vertical" margin={{ top: 4, right: 32, bottom: 4, left: 8 }}>
                <CartesianGrid strokeDasharray="4 2" stroke="#f3f4f6" horizontal={false} />
                <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 10, fill: "#9ca3af" }} axisLine={false} tickLine={false} tickFormatter={(v) => `${v}%`} />
                <YAxis dataKey="name" type="category" tick={{ fontSize: 11, fill: "#374151" }} axisLine={false} tickLine={false} width={80} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="saturationPct" name="Saturation %" radius={[0, 4, 4, 0]} minPointSize={2}>
                    {data.map((entry, i) => (
                        <Cell key={i} fill={entry.color ?? PRIMARY} />
                    ))}
                </Bar>
            </BarChart>
        </ResponsiveContainer>
    );
}

// ── Claims Pipeline Funnel ─────────────────────────────────────────────────────
export function ClaimsPipelineChart({ data }: { data: Array<{ id: string; label: string; count: number; color: string }> }) {
    const max = Math.max(...data.map((d) => d.count));
    return (
        <div className="space-y-2">
            {data.map((stage) => (
                <div key={stage.id} className="flex items-center gap-3">
                    <div className="w-24 text-right shrink-0">
                        <span className="text-[11px] font-medium text-gray-600 leading-tight">{stage.label}</span>
                    </div>
                    <div className="flex-1 bg-gray-100 rounded-full overflow-hidden h-6 relative">
                        <div
                            className="h-full rounded-full flex items-center justify-end pr-2 transition-all duration-700"
                            style={{
                                width: `${(stage.count / max) * 100}%`,
                                background: stage.color,
                                minWidth: "2rem",
                            }}
                        >
                            <span className="text-white text-[10px] font-bold tabular-nums">
                                {stage.count.toLocaleString("en-IN")}
                            </span>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}

// ── Claim Type Donut ───────────────────────────────────────────────────────────
export function ClaimTypeDonut({ ifr, cfr, cr }: { ifr: number; cfr: number; cr: number }) {
    const data = [
        { name: "IFR", value: ifr, color: "#4f46e5" },
        { name: "CFR", value: cfr, color: "#16a34a" },
        { name: "CR", value: cr, color: "#d97706" },
    ];
    const total = ifr + cfr + cr;

    return (
        <div className="flex items-center gap-4">
            <div className="relative" style={{ width: 100, height: 100 }}>
                <ResponsiveContainer width={100} height={100}>
                    <PieChart>
                        <Pie
                            data={data}
                            cx={45}
                            cy={45}
                            innerRadius={28}
                            outerRadius={45}
                            paddingAngle={2}
                            dataKey="value"
                            stroke="none"
                        >
                            {data.map((entry, index) => (
                                <Cell key={index} fill={entry.color} />
                            ))}
                        </Pie>
                    </PieChart>
                </ResponsiveContainer>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-xs font-bold text-gray-700 tabular-nums">{total.toLocaleString("en-IN")}</span>
                    <span className="text-[8px] text-gray-400">Total</span>
                </div>
            </div>
            <div className="flex-1 space-y-2">
                {data.map((d) => (
                    <div key={d.name} className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <div className="w-2.5 h-2.5 rounded-full shrink-0" style={{ background: d.color }} />
                            <span className="text-xs text-gray-600">{d.name}</span>
                        </div>
                        <span className="text-xs font-bold tabular-nums" style={{ color: d.color }}>
                            {d.value.toLocaleString("en-IN")}
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
}

// ── NDVI Trend Line Chart ──────────────────────────────────────────────────────
export function NDVITrendChart({ data }: { data: Array<{ quarter: string;[key: string]: string | number }> }) {
    const villages = Object.keys(data[0] ?? {}).filter((k) => k !== "quarter");
    const colors = [PRIMARY, SUCCESS, WARNING, PURPLE];

    return (
        <ResponsiveContainer width="100%" height={200}>
            <LineChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -20 }}>
                <CartesianGrid strokeDasharray="4 2" stroke="#f3f4f6" />
                <XAxis dataKey="quarter" tick={{ fontSize: 9, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
                <YAxis domain={[0.5, 0.9]} tick={{ fontSize: 9, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ fontSize: "10px", paddingTop: "8px" }} />
                {villages.map((v, i) => (
                    <Line
                        key={v}
                        dataKey={v}
                        name={v.charAt(0).toUpperCase() + v.slice(1)}
                        stroke={colors[i % colors.length]}
                        strokeWidth={2}
                        dot={{ r: 3, fill: colors[i % colors.length], strokeWidth: 0 }}
                        activeDot={{ r: 5 }}
                    />
                ))}
            </LineChart>
        </ResponsiveContainer>
    );
}

// ── Scheme Saturation Radar ────────────────────────────────────────────────────
export function SchemeSaturationRadar({ data }: { data: Array<{ scheme: string; saturation: number; target: number }> }) {
    return (
        <ResponsiveContainer width="100%" height={220}>
            <RadarChart data={data}>
                <PolarGrid stroke="#e5e7eb" />
                <PolarAngleAxis dataKey="scheme" tick={{ fontSize: 9, fill: "#6b7280" }} />
                <PolarRadiusAxis domain={[0, 100]} tick={{ fontSize: 8, fill: "#9ca3af" }} />
                <Radar name="Current" dataKey="saturation" stroke={PRIMARY} fill={PRIMARY} fillOpacity={0.3} />
                <Radar name="Target" dataKey="target" stroke={WARNING} fill={WARNING} fillOpacity={0.1} strokeDasharray="4 2" />
                <Legend wrapperStyle={{ fontSize: "10px" }} />
                <Tooltip content={<CustomTooltip />} />
            </RadarChart>
        </ResponsiveContainer>
    );
}

// ── Budget Utilization Area Chart ─────────────────────────────────────────────
export function BudgetUtilizationChart({ data }: { data: Array<{ name: string; allocated: number; utilized: number }> }) {
    return (
        <ResponsiveContainer width="100%" height={180}>
            <BarChart data={data} margin={{ top: 4, right: 8, bottom: 0, left: -16 }}>
                <CartesianGrid strokeDasharray="4 2" stroke="#f3f4f6" />
                <XAxis dataKey="name" tick={{ fontSize: 9, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 9, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ fontSize: "10px", paddingTop: "8px" }} />
                <Bar dataKey="allocated" name="Allocated (Cr)" fill={BLUE} radius={[3, 3, 0, 0]} opacity={0.5} />
                <Bar dataKey="utilized" name="Utilized (Cr)" fill={SUCCESS} radius={[3, 3, 0, 0]} />
            </BarChart>
        </ResponsiveContainer>
    );
}

// ── DSS Priority Distribution ─────────────────────────────────────────────────
export function DSSPriorityChart({ critical, high, medium, low }: { critical: number; high: number; medium: number; low: number }) {
    const data = [
        { name: "Critical", value: critical, color: "#ef4444" },
        { name: "High", value: high, color: "#f97316" },
        { name: "Medium", value: medium, color: "#f59e0b" },
        { name: "Low", value: low, color: "#22c55e" },
    ];

    return (
        <ResponsiveContainer width="100%" height={160}>
            <PieChart>
                <Pie
                    data={data}
                    cx="50%"
                    cy="50%"
                    outerRadius={60}
                    dataKey="value"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
                >
                    {data.map((d, i) => <Cell key={i} fill={d.color} stroke="none" />)}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
            </PieChart>
        </ResponsiveContainer>
    );
}

// ── Generic Chart Wrappers ─────────────────────────────────────────────────────
export function AreaChartWrapper({ data, height = 220, lines }: { data: Array<Record<string, any>>; height?: number; lines?: Array<{ key: string; color: string }> }) {
    if (!data || data.length === 0) return null;
    const keys = Object.keys(data[0] || {}).filter(k => typeof data[0][k] === 'number');

    return (
        <ResponsiveContainer width="100%" height={height}>
            <AreaChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
                <CartesianGrid strokeDasharray="4 2" stroke="#f3f4f6" />
                <XAxis dataKey={Object.keys(data[0] || {})[0]} tick={{ fontSize: 10, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 10, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "12px" }} />
                {keys.map((key, i) => (
                    <Area key={key} type="monotone" dataKey={key} stroke={[PRIMARY, SUCCESS, WARNING, BLUE][i % 4]} fill={[PRIMARY, SUCCESS, WARNING, BLUE][i % 4]} fillOpacity={0.3} />
                ))}
            </AreaChart>
        </ResponsiveContainer>
    );
}

export function BarChartWrapper({ data, height = 220, bars }: { data: Array<Record<string, any>>; height?: number; bars?: Array<{ key: string; color: string; name?: string }> }) {
    if (!data || data.length === 0) return null;
    const keys = Object.keys(data[0] || {}).filter(k => typeof data[0][k] === 'number');

    return (
        <ResponsiveContainer width="100%" height={height}>
            <BarChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
                <CartesianGrid strokeDasharray="4 2" stroke="#f3f4f6" />
                <XAxis dataKey={Object.keys(data[0] || {})[0]} tick={{ fontSize: 10, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 10, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "12px" }} />
                {keys.map((key, i) => (
                    <Bar key={key} dataKey={key} fill={[PRIMARY, SUCCESS, WARNING, BLUE][i % 4]} radius={[3, 3, 0, 0]} />
                ))}
            </BarChart>
        </ResponsiveContainer>
    );
}

export function PieChartWrapper({ data, height = 200, innerRadius = 0 }: { data: Array<{ name: string; value: number; color?: string }>; height?: number; innerRadius?: number }) {
    if (!data || data.length === 0) return null;

    return (
        <ResponsiveContainer width="100%" height={height}>
            <PieChart>
                <Pie
                    data={data}
                    cx="50%"
                    cy="50%"
                    innerRadius={innerRadius}
                    outerRadius={Math.min(height * 0.4, 80)}
                    dataKey="value"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
                >
                    {data.map((entry, i) => (
                        <Cell key={i} fill={entry.color || [PRIMARY, SUCCESS, WARNING, BLUE, AMBER, PURPLE][i % 6]} />
                    ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{ fontSize: "10px" }} />
            </PieChart>
        </ResponsiveContainer>
    );
}

export function RadialChartWrapper({ data, height = 200, value, label, color }: { data?: Array<{ name: string; value: number; fill?: string }>; height?: number; value?: number; label?: string; color?: string }) {
    // Support both array data and single value
    const chartData = data || (value !== undefined ? [{ name: label || "Value", value, fill: color }] : []);
    if (!chartData || chartData.length === 0) return null;

    return (
        <ResponsiveContainer width="100%" height={height}>
            <RadarChart data={chartData}>
                <PolarGrid stroke="#e5e7eb" />
                <PolarAngleAxis dataKey="name" tick={{ fontSize: 9, fill: "#6b7280" }} />
                <PolarRadiusAxis tick={{ fontSize: 8, fill: "#9ca3af" }} />
                <Radar dataKey="value" stroke={PRIMARY} fill={PRIMARY} fillOpacity={0.3} />
                <Tooltip content={<CustomTooltip />} />
            </RadarChart>
        </ResponsiveContainer>
    );
}

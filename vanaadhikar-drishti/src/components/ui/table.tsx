import * as React from "react";
import { cn } from "@/lib/utils";
import { ChevronUp, ChevronDown, ChevronsUpDown, Search } from "lucide-react";

// ── Column Definition ─────────────────────────────────────────────────────────
export interface Column<T> {
    key: keyof T | string;
    header: string;
    width?: string;
    sortable?: boolean;
    render?: (value: unknown, row: T, index: number) => React.ReactNode;
    align?: "left" | "center" | "right";
}

export interface TableProps<T> {
    data: T[];
    columns: Column<T>[];
    loading?: boolean;
    emptyMessage?: string;
    emptyIcon?: React.ReactNode;
    stickyHeader?: boolean;
    striped?: boolean;
    compact?: boolean;
    onRowClick?: (row: T) => void;
    highlightRow?: (row: T) => boolean;
    keyField?: keyof T;
    searchQuery?: string;
    defaultSortKey?: string;
    defaultSortDir?: "asc" | "desc";
    className?: string;
}

type SortDirection = "asc" | "desc";

export function DataTable<T extends object>({
    data,
    columns,
    loading,
    emptyMessage = "No data available",
    emptyIcon,
    stickyHeader = true,
    striped = true,
    compact = false,
    onRowClick,
    highlightRow,
    keyField,
    searchQuery,
    defaultSortKey,
    defaultSortDir = "asc",
    className,
}: TableProps<T>) {
    const [sortKey, setSortKey] = React.useState<string | null>(defaultSortKey ?? null);
    const [sortDir, setSortDir] = React.useState<SortDirection>(defaultSortDir);

    const handleSort = (key: string) => {
        if (sortKey === key) {
            setSortDir((d) => (d === "asc" ? "desc" : "asc"));
        } else {
            setSortKey(key);
            setSortDir("asc");
        }
    };

    const sortedData = React.useMemo(() => {
        if (!sortKey) return data;
        return [...data].sort((a, b) => {
            const av = (a as Record<string, unknown>)[sortKey];
            const bv = (b as Record<string, unknown>)[sortKey];
            if (av == null) return 1;
            if (bv == null) return -1;
            if (typeof av === "number" && typeof bv === "number") {
                return sortDir === "asc" ? av - bv : bv - av;
            }
            return sortDir === "asc"
                ? String(av).localeCompare(String(bv))
                : String(bv).localeCompare(String(av));
        });
    }, [data, sortKey, sortDir]);

    const cellPad = compact ? "px-3 py-1.5" : "px-4 py-3";

    return (
        <div className={cn("overflow-x-auto rounded-xl border border-gray-200 bg-white", className)}>
            <table className="data-table min-w-full text-sm">
                <thead className={cn(stickyHeader && "sticky top-0 z-10")}>
                    <tr className="bg-gray-50 border-b border-gray-200">
                        {columns.map((col) => (
                            <th
                                key={String(col.key)}
                                className={cn(
                                    cellPad,
                                    "text-xs font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap select-none",
                                    col.align === "center" && "text-center",
                                    col.align === "right" && "text-right",
                                    col.sortable && "cursor-pointer hover:text-forest-700 hover:bg-gray-100 transition-colors",
                                    col.width && `w-[${col.width}]`
                                )}
                                onClick={() => col.sortable && handleSort(String(col.key))}
                            >
                                <div className={cn("flex items-center gap-1", col.align === "center" && "justify-center", col.align === "right" && "justify-end")}>
                                    {col.header}
                                    {col.sortable && (
                                        <span className="text-gray-300">
                                            {sortKey === String(col.key) ? (
                                                sortDir === "asc" ? <ChevronUp size={12} className="text-forest-500" /> : <ChevronDown size={12} className="text-forest-500" />
                                            ) : (
                                                <ChevronsUpDown size={12} />
                                            )}
                                        </span>
                                    )}
                                </div>
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {loading ? (
                        Array.from({ length: 5 }).map((_, i) => (
                            <tr key={i} className="border-b border-gray-100">
                                {columns.map((col) => (
                                    <td key={String(col.key)} className={cellPad}>
                                        <div className="skeleton h-4 rounded w-3/4" />
                                    </td>
                                ))}
                            </tr>
                        ))
                    ) : sortedData.length === 0 ? (
                        <tr>
                            <td colSpan={columns.length} className="text-center py-16 text-gray-400">
                                <div className="flex flex-col items-center gap-2">
                                    {emptyIcon ?? (
                                        <Search size={32} className="text-gray-200" />
                                    )}
                                    <p className="text-sm">{emptyMessage}</p>
                                </div>
                            </td>
                        </tr>
                    ) : (
                        sortedData.map((row, i) => {
                            const highlighted = highlightRow?.(row);
                            const key = keyField ? String((row as Record<string, unknown>)[keyField as string]) : i;
                            return (
                                <tr
                                    key={key}
                                    onClick={() => onRowClick?.(row)}
                                    className={cn(
                                        "border-b border-gray-50 transition-colors",
                                        striped && i % 2 === 0 ? "bg-white" : "bg-gray-50/50",
                                        onRowClick && "cursor-pointer hover:bg-forest-50",
                                        highlighted && "bg-amber-50 hover:bg-amber-100"
                                    )}
                                >
                                    {columns.map((col) => {
                                        const rawValue = (row as Record<string, unknown>)[String(col.key)];
                                        const rendered = col.render ? col.render(rawValue, row, i) : rawValue != null ? String(rawValue) : "—";
                                        return (
                                            <td
                                                key={String(col.key)}
                                                className={cn(
                                                    cellPad,
                                                    "text-sm text-gray-700 whitespace-nowrap",
                                                    col.align === "center" && "text-center",
                                                    col.align === "right" && "text-right tabular-nums"
                                                )}
                                            >
                                                {rendered as React.ReactNode}
                                            </td>
                                        );
                                    })}
                                </tr>
                            );
                        })
                    )}
                </tbody>
            </table>
        </div>
    );
}

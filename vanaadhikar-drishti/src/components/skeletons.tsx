/**
 * Loading skeleton components
 */

export function DataTableSkeleton({ rows = 5 }: { rows?: number }) {
    return (
        <div className="space-y-4">
            {Array.from({ length: rows }).map((_, i) => (
                <div key={i} className="flex gap-4 h-12 bg-slate-200 rounded animate-pulse" />
            ))}
        </div>
    );
}

export function StatCardSkeleton({ count = 4 }: { count?: number }) {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {Array.from({ length: count }).map((_, i) => (
                <div key={i} className="p-6 bg-slate-200 rounded-lg animate-pulse h-24" />
            ))}
        </div>
    );
}

export function ChartSkeleton() {
    return <div className="w-full h-64 bg-slate-200 rounded-lg animate-pulse" />;
}

export function MapSkeleton() {
    return <div className="w-full h-96 bg-slate-200 rounded-lg animate-pulse" />;
}

export function ListSkeleton({ items = 10 }: { items?: number }) {
    return (
        <div className="space-y-2">
            {Array.from({ length: items }).map((_, i) => (
                <div key={i} className="h-10 bg-slate-200 rounded animate-pulse" />
            ))}
        </div>
    );
}

export function CardSkeleton() {
    return (
        <div className="w-full bg-slate-200 rounded-lg p-4 animate-pulse">
            <div className="h-8 bg-slate-300 rounded w-1/2 mb-4" />
            <div className="space-y-2">
                {Array.from({ length: 3 }).map((_, i) => (
                    <div key={i} className="h-4 bg-slate-300 rounded w-full" />
                ))}
            </div>
        </div>
    );
}

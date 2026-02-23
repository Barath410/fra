"use client";
import * as React from "react";
import { cn } from "@/lib/utils";
import { ChevronDown } from "lucide-react";

interface AccordionItem { id: string; title: string; subtitle?: string; icon?: React.ReactNode; badge?: React.ReactNode; children: React.ReactNode; defaultOpen?: boolean }

interface AccordionProps { items: AccordionItem[]; allowMultiple?: boolean; variant?: "default" | "bordered" | "flush"; className?: string }

export function Accordion({ items, allowMultiple = false, variant = "default", className }: AccordionProps) {
    const [openIds, setOpenIds] = React.useState<Set<string>>(
        () => new Set(items.filter((i) => i.defaultOpen).map((i) => i.id))
    );

    const toggle = (id: string) => {
        setOpenIds((prev) => {
            const next = new Set(prev);
            if (next.has(id)) {
                next.delete(id);
            } else {
                if (!allowMultiple) next.clear();
                next.add(id);
            }
            return next;
        });
    };

    return (
        <div className={cn(
            "divide-y divide-gray-100",
            variant === "bordered" && "border border-gray-200 rounded-xl overflow-hidden",
            variant === "flush" && "",
            className
        )}>
            {items.map((item) => {
                const isOpen = openIds.has(item.id);
                return (
                    <div key={item.id} className={cn(variant === "default" && "bg-white rounded-xl border border-gray-200 mb-2 overflow-hidden last:mb-0")}>
                        <button
                            onClick={() => toggle(item.id)}
                            className={cn(
                                "w-full flex items-center gap-3 px-4 py-3.5 text-left transition-colors",
                                isOpen ? "bg-forest-50" : "bg-white hover:bg-gray-50"
                            )}
                            aria-expanded={isOpen}
                        >
                            {item.icon && <span className="text-forest-600 shrink-0">{item.icon}</span>}
                            <div className="flex-1 min-w-0">
                                <p className={cn("text-sm font-semibold", isOpen ? "text-forest-800" : "text-gray-800")}>{item.title}</p>
                                {item.subtitle && <p className="text-xs text-gray-400 mt-0.5">{item.subtitle}</p>}
                            </div>
                            {item.badge && <span className="mr-2">{item.badge}</span>}
                            <ChevronDown
                                size={16}
                                className={cn(
                                    "shrink-0 text-gray-400 transition-transform duration-200",
                                    isOpen && "rotate-180 text-forest-600"
                                )}
                            />
                        </button>
                        <div className={cn(
                            "overflow-hidden transition-all duration-300",
                            isOpen ? "max-h-[2000px] opacity-100" : "max-h-0 opacity-0"
                        )}>
                            <div className="px-4 py-3 border-t border-gray-100 bg-white">
                                {item.children}
                            </div>
                        </div>
                    </div>
                );
            })}
        </div>
    );
}

// ── Section Separator ─────────────────────────────────────────────────────────
export function Separator({ label, className }: { label?: string; className?: string }) {
    if (!label) return <hr className={cn("border-t border-gray-200", className)} />;
    return (
        <div className={cn("flex items-center gap-3", className)}>
            <hr className="flex-1 border-t border-gray-200" />
            <span className="text-xs text-gray-400 font-medium whitespace-nowrap uppercase tracking-widest">{label}</span>
            <hr className="flex-1 border-t border-gray-200" />
        </div>
    );
}

"use client";
import * as React from "react";
import { cn } from "@/lib/utils";

/* ── Card ──────────────────────────────────────────────────────────────── */
interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
    variant?: "default" | "tribal" | "elevated" | "outline" | "alert";
    hover?: boolean;
    padding?: "none" | "sm" | "md" | "lg";
}

const cardVariants: Record<string, string> = {
    default: "bg-white border border-border rounded-xl shadow-sm",
    tribal: "tribal-card",
    elevated: "bg-white border border-border rounded-xl shadow-kpi",
    outline: "bg-transparent border border-border rounded-xl",
    alert: "bg-warning/5 border border-warning/20 rounded-xl",
};

const paddingVariants: Record<string, string> = {
    none: "",
    sm: "p-3",
    md: "p-5",
    lg: "p-7",
};

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
    ({ variant = "tribal", hover = false, padding = "none", className, children, ...props }, ref) => (
        <div
            ref={ref}
            className={cn(
                cardVariants[variant],
                hover && "transition-all duration-200 hover:-translate-y-1 hover:shadow-hover cursor-pointer",
                paddingVariants[padding],
                className
            )}
            {...props}
        >
            {children}
        </div>
    )
);
Card.displayName = "Card";

/* ── CardHeader ─────────────────────────────────────────────────────────── */
export function CardHeader({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
    return (
        <div
            className={cn("flex flex-col space-y-1.5 p-6", className)}
            {...props}
        >
            {children}
        </div>
    );
}

/* ── CardTitle ──────────────────────────────────────────────────────────── */
export const CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
    ({ className, ...props }, ref) => (
        <h3
            ref={ref}
            className={cn("text-2xl font-semibold leading-none tracking-tight", className)}
            {...props}
        />
    )
);
CardTitle.displayName = "CardTitle";


/* ── CardDescription ────────────────────────────────────────────────────── */
export const CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
    ({ className, ...props }, ref) => (
        <p
            ref={ref}
            className={cn("text-sm text-muted-foreground", className)}
            {...props}
        />
    )
);
CardDescription.displayName = "CardDescription";


/* ── CardContent ────────────────────────────────────────────────────────── */
export const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
    ({ className, ...props }, ref) => (
        <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
    )
);
CardContent.displayName = "CardContent";


/* ── CardFooter ─────────────────────────────────────────────────────────── */
export const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
    ({ className, ...props }, ref) => (
        <div
            ref={ref}
            className={cn("flex items-center p-6 pt-0", className)}
            {...props}
        />
    )
);
CardFooter.displayName = "CardFooter";

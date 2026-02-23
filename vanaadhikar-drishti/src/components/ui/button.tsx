"use client";
import * as React from "react";
import { cn } from "@/lib/utils";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?:
    | "primary"
    | "secondary"
    | "outline"
    | "ghost"
    | "danger"
    | "accent"
    | "default"
    | "white";
    size?: "sm" | "md" | "lg" | "icon";
    loading?: boolean;
    leftIcon?: React.ReactNode;
    rightIcon?: React.ReactNode;
    fullWidth?: boolean;
    asChild?: boolean;
}

const variantStyles: Record<string, string> = {
    primary: "bg-primary text-white hover:bg-primary-600 active:bg-primary-700 border-transparent shadow-md hover:shadow-lg hover:-translate-y-0.5",
    secondary: "bg-white text-text hover:bg-gray-50 border-border shadow-sm hover:shadow-md",
    outline: "bg-transparent text-primary hover:bg-primary/5 border-primary/30 hover:border-primary",
    ghost: "bg-transparent text-text hover:bg-gray-100 border-transparent",
    danger: "bg-danger text-white hover:bg-danger/90 border-transparent shadow-md hover:shadow-lg",
    accent: "bg-success text-white hover:bg-success/90 active:bg-success/80 border-transparent shadow-md hover:shadow-lg hover:-translate-y-0.5",
    default: "bg-gray-100 text-text hover:bg-gray-200 border-transparent shadow-sm",
    white: "bg-white text-text hover:bg-gray-50 border-border shadow-sm",
};

const sizeStyles: Record<string, string> = {
    sm: "text-xs px-3 py-1.5 h-7 rounded-md gap-1.5",
    md: "text-sm px-4 py-2 h-9 rounded-lg gap-2",
    lg: "text-base px-6 py-2.5 h-11 rounded-lg gap-2",
    icon: "w-9 h-9 p-0 rounded-lg justify-center",
};

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
    (
        {
            variant = "primary",
            size = "md",
            loading,
            leftIcon,
            rightIcon,
            fullWidth,
            className,
            children,
            disabled,
            ...props
        },
        ref
    ) => {
        return (
            <button
                ref={ref}
                disabled={disabled || loading}
                className={cn(
                    "inline-flex items-center justify-center font-semibold border transition-all duration-200 cursor-pointer select-none",
                    "disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none",
                    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/20 focus-visible:ring-offset-2",
                    variantStyles[variant],
                    sizeStyles[size],
                    fullWidth && "w-full",
                    className
                )}
                {...props}
            >
                {loading ? (
                    <svg
                        className="animate-spin h-4 w-4"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                    >
                        <circle
                            className="opacity-25"
                            cx="12" cy="12" r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                        />
                        <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                        />
                    </svg>
                ) : (
                    leftIcon
                )}
                {size !== "icon" && children}
                {!loading && rightIcon}
            </button>
        );
    }
);

Button.displayName = "Button";

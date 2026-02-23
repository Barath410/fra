import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
    hint?: string;
    leftIcon?: React.ReactNode;
    rightIcon?: React.ReactNode;
    loading?: boolean;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
    ({ className, type = "text", label, error, hint, leftIcon, rightIcon, loading, disabled, ...props }, ref) => {
        return (
            <div className="w-full">
                {label && (
                    <label className="block text-xs font-semibold text-text mb-1.5" htmlFor={props.id}>
                        {label}
                        {props.required && <span className="text-danger ml-1">*</span>}
                    </label>
                )}
                <div className="relative">
                    {leftIcon && (
                        <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none">
                            {leftIcon}
                        </div>
                    )}
                    <input
                        type={type}
                        ref={ref}
                        disabled={disabled || loading}
                        className={cn(
                            "form-input w-full rounded-lg border border-border bg-white px-3 py-2.5 text-sm text-text",
                            "placeholder:text-text-muted",
                            "focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary",
                            "disabled:bg-gray-50 disabled:text-text-muted disabled:cursor-not-allowed",
                            "transition-all duration-200",
                            error && "border-danger/50 focus:ring-danger/10 focus:border-danger",
                            leftIcon && "pl-9",
                            (rightIcon || loading) && "pr-9",
                            className
                        )}
                        {...props}
                    />
                    {(rightIcon || loading) && (
                        <div className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                            {loading ? (
                                <div className="w-4 h-4 border-2 border-gray-300 border-t-primary rounded-full animate-spin" />
                            ) : (
                                rightIcon
                            )}
                        </div>
                    )}
                </div>
                {error && <p className="mt-1 text-xs text-danger">{error}</p>}
                {hint && !error && <p className="mt-1 text-xs text-text-muted">{hint}</p>}
            </div>
        );
    }
);
Input.displayName = "Input";

// ── Textarea ──────────────────────────────────────────────────────────────────
export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
    label?: string;
    error?: string;
    hint?: string;
}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
    ({ className, label, error, hint, ...props }, ref) => (
        <div className="w-full">
            {label && (
                <label className="block text-xs font-semibold text-gray-700 mb-1.5">
                    {label}
                    {props.required && <span className="text-red-500 ml-1">*</span>}
                </label>
            )}
            <textarea
                ref={ref}
                className={cn(
                    "form-input w-full rounded-lg border border-border bg-white px-3 py-2.5 text-sm text-text resize-none",
                    "placeholder:text-text-muted min-h-[80px]",
                    "focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary",
                    "disabled:bg-gray-50 disabled:text-text-muted disabled:cursor-not-allowed",
                    error && "border-danger/50 focus:ring-danger/10",
                    className
                )}
                {...props}
            />
            {error && <p className="mt-1 text-xs text-danger">{error}</p>}
            {hint && !error && <p className="mt-1 text-xs text-text-muted">{hint}</p>}
        </div>
    )
);
Textarea.displayName = "Textarea";

// ── Select ────────────────────────────────────────────────────────────────────
export interface SelectOption { value: string; label: string; disabled?: boolean }
export interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
    label?: string;
    error?: string;
    hint?: string;
    options: SelectOption[];
    placeholder?: string;
}

const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
    ({ className, label, error, hint, options, placeholder, ...props }, ref) => (
        <div className="w-full">
            {label && (
                <label className="block text-xs font-semibold text-gray-700 mb-1.5">
                    {label}
                    {props.required && <span className="text-red-500 ml-1">*</span>}
                </label>
            )}
            <div className="relative">
                <select
                    ref={ref}
                    className={cn(
                        "form-input w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 appearance-none pr-8",
                        "focus:outline-none focus:ring-2 focus:ring-forest-500 focus:border-forest-500",
                        "disabled:bg-gray-50 disabled:text-gray-400 disabled:cursor-not-allowed",
                        error && "border-red-400 focus:ring-red-300",
                        className
                    )}
                    {...props}
                >
                    {placeholder && <option value="">{placeholder}</option>}
                    {options.map((o) => (
                        <option key={o.value} value={o.value} disabled={o.disabled}>
                            {o.label}
                        </option>
                    ))}
                </select>
                <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400">
                    <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
                        <path fillRule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.09 1.03l-4.25 4.5a.75.75 0 01-1.09 0l-4.25-4.5a.75.75 0 01.02-1.06z" clipRule="evenodd" />
                    </svg>
                </div>
            </div>
            {error && <p className="mt-1 text-xs text-red-500">{error}</p>}
            {hint && !error && <p className="mt-1 text-xs text-gray-400">{hint}</p>}
        </div>
    )
);
Select.displayName = "Select";

export { Input, Textarea, Select };

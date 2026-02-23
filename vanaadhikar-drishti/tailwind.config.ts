import type { Config } from "tailwindcss";

const config: Config = {
    darkMode: "class",
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                // Modern Gov-Tech Data Platform Theme
                primary: {
                    DEFAULT: "#2563EB",
                    50: "#EFF6FF",
                    100: "#DBEAFE",
                    200: "#BFDBFE",
                    300: "#93C5FD",
                    400: "#60A5FA",
                    500: "#2563EB",
                    600: "#1D4ED8",
                    700: "#1E40AF",
                    800: "#1E3A8A",
                    900: "#1E293B",
                },
                success: {
                    DEFAULT: "#10B981",
                    50: "#ECFDF5",
                    100: "#D1FAE5",
                    200: "#A7F3D0",
                    300: "#6EE7B7",
                    400: "#34D399",
                    500: "#10B981",
                    600: "#059669",
                    700: "#047857",
                    800: "#065F46",
                    900: "#064E3B",
                },
                warning: {
                    DEFAULT: "#F59E0B",
                    50: "#FFFBEB",
                    100: "#FEF3C7",
                    200: "#FDE68A",
                    300: "#FCD34D",
                    400: "#FBBF24",
                    500: "#F59E0B",
                    600: "#D97706",
                    700: "#B45309",
                    800: "#92400E",
                    900: "#78350F",
                },
                danger: {
                    DEFAULT: "#EF4444",
                    50: "#FEF2F2",
                    100: "#FEE2E2",
                    200: "#FECACA",
                    300: "#FCA5A5",
                    400: "#F87171",
                    500: "#EF4444",
                    600: "#DC2626",
                    700: "#B91C1C",
                    800: "#991B1B",
                    900: "#7F1D1D",
                },
                // Sidebar colors
                sidebar: {
                    DEFAULT: "#0F172A",
                    active: "#1E293B",
                    hover: "#111827",
                    icon: "#94A3B8",
                    text: "#E5E7EB",
                },
                // Background & Surface
                background: "#F5F7FB",
                surface: "#FFFFFF",
                border: "#E5E7EB",
                // Text colors
                text: {
                    DEFAULT: "#111827",
                    muted: "#6B7280",
                    light: "#9CA3AF",
                },
                // Keep legacy colors for backwards compatibility
                forest: {
                    50: "#f0f7f4",
                    100: "#d9ede5",
                    200: "#b3dbca",
                    300: "#7ec0a8",
                    400: "#49a082",
                    500: "#2d8566",
                    600: "#1f6b51",
                    700: "#1a5542",
                    800: "#174437",
                    900: "#13382e",
                    950: "#0a1f19",
                },
                saffron: {
                    50: "#fff8f0",
                    100: "#ffecd5",
                    200: "#ffd6a8",
                    300: "#ffb870",
                    400: "#ff9032",
                    500: "#e87722",
                    600: "#d1601a",
                    700: "#b04a14",
                    800: "#8d3c14",
                    900: "#733213",
                    DEFAULT: "#e87722",
                },
                terracotta: {
                    50: "#fdf4f0",
                    100: "#fce7de",
                    200: "#f8ccbc",
                    300: "#f3a48d",
                    400: "#eb7256",
                    500: "#e05533",
                    600: "#b5541a",
                    700: "#9a4517",
                    800: "#7d3a18",
                    900: "#67321a",
                    DEFAULT: "#b5541a",
                },
                parchment: {
                    50: "#fdfaf7",
                    100: "#f9f0e5",
                    200: "#f4e8d4",
                    300: "#edd8bb",
                    400: "#e3c499",
                    500: "#d9ae79",
                    DEFAULT: "#f4ede3",
                },
                // State-specific (keep for compatibility)
                "mp-orange": "#F59E0B",
                "od-maroon": "#BE3144",
                "tr-green": "#10B981",
                "tg-teal": "#0D9488",
                // Status colors (aligned with semantic palette)
                "status-granted": "#10B981",
                "status-pending": "#F59E0B",
                "status-rejected": "#EF4444",
                "status-received": "#2563EB",
                "status-verified": "#6366F1",
            },
            fontFamily: {
                sans: ["var(--font-noto-sans)", "Noto Sans Devanagari", "sans-serif"],
                serif: ["var(--font-noto-serif)", "Noto Serif Devanagari", "serif"],
                mono: ["JetBrains Mono", "Courier New", "monospace"],
            },
            borderRadius: {
                lg: "var(--radius)",
                md: "calc(var(--radius) - 2px)",
                sm: "calc(var(--radius) - 4px)",
            },
            backgroundImage: {
                "gond-pattern":
                    "url(\"data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Ccircle cx='30' cy='30' r='4' stroke='%232563EB' stroke-width='0.5' opacity='0.06'/%3E%3Ccircle cx='10' cy='10' r='2' stroke='%232563EB' stroke-width='0.5' opacity='0.04'/%3E%3Ccircle cx='50' cy='10' r='2' stroke='%232563EB' stroke-width='0.5' opacity='0.04'/%3E%3Ccircle cx='10' cy='50' r='2' stroke='%232563EB' stroke-width='0.5' opacity='0.04'/%3E%3Ccircle cx='50' cy='50' r='2' stroke='%232563EB' stroke-width='0.5' opacity='0.04'/%3E%3Cline x1='30' y1='10' x2='30' y2='50' stroke='%232563EB' stroke-width='0.3' opacity='0.03'/%3E%3Cline x1='10' y1='30' x2='50' y2='30' stroke='%232563EB' stroke-width='0.3' opacity='0.03'/%3E%3C/g%3E%3C/svg%3E\")",
                "warli-dots":
                    "radial-gradient(circle, rgba(37,99,235,0.05) 1px, transparent 1px)",
                "primary-gradient": "linear-gradient(135deg, #2563EB 0%, #1E40AF 100%)",
                "sidebar-gradient": "linear-gradient(180deg, #0F172A 0%, #1E293B 100%)",
                "surface-gradient": "linear-gradient(180deg, #FFFFFF 0%, #F9FAFB 100%)",
            },
            backgroundSize: {
                "warli-sm": "20px 20px",
                "warli-md": "30px 30px",
            },
            boxShadow: {
                "card-sm": "0 1px 3px 0 rgba(0,0,0,0.05), 0 1px 2px -1px rgba(0,0,0,0.03)",
                "card-md": "0 4px 6px -1px rgba(0,0,0,0.06), 0 2px 4px -2px rgba(0,0,0,0.04)",
                "card-lg": "0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.05)",
                "nav": "0 2px 8px 0 rgba(0,0,0,0.08)",
                "map": "inset 0 0 30px rgba(0,0,0,0.05)",
                "glow": "0 0 20px rgba(37,99,235,0.2)",
                "kpi": "0 8px 30px rgba(0,0,0,0.05)",
                "hover": "0 12px 40px rgba(0,0,0,0.08)",
            },
            keyframes: {
                "accordion-down": {
                    from: { height: "0" },
                    to: { height: "var(--radix-accordion-content-height)" },
                },
                "accordion-up": {
                    from: { height: "var(--radix-accordion-content-height)" },
                    to: { height: "0" },
                },
                "pulse-ring": {
                    "0%": { transform: "scale(0.95)", boxShadow: "0 0 0 0 rgba(37,99,235,0.4)" },
                    "70%": { transform: "scale(1)", boxShadow: "0 0 0 10px rgba(37,99,235,0)" },
                    "100%": { transform: "scale(0.95)", boxShadow: "0 0 0 0 rgba(37,99,235,0)" },
                },
                "slide-in-left": {
                    from: { transform: "translateX(-100%)", opacity: "0" },
                    to: { transform: "translateX(0)", opacity: "1" },
                },
                "fade-up": {
                    from: { transform: "translateY(16px)", opacity: "0" },
                    to: { transform: "translateY(0)", opacity: "1" },
                },
                shimmer: {
                    "100%": { transform: "translateX(100%)" },
                },
            },
            animation: {
                "accordion-down": "accordion-down 0.2s ease-out",
                "accordion-up": "accordion-up 0.2s ease-out",
                "pulse-ring": "pulse-ring 2s cubic-bezier(0.455, 0.03, 0.515, 0.955) infinite",
                "slide-in-left": "slide-in-left 0.3s ease-out",
                "fade-up": "fade-up 0.4s ease-out",
                shimmer: "shimmer 2s infinite",
            },
            typography: {
                DEFAULT: {
                    css: {
                        color: "#1C1C1C",
                        headings: { fontFamily: "var(--font-noto-serif)" },
                    },
                },
            },
        },
    },
    plugins: [],
};

export default config;

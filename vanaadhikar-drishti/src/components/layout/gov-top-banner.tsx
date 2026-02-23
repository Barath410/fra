"use client";
import React from "react";

const LANGUAGES = [
    { code: "en", label: "EN", name: "English" },
    { code: "hi", label: "हि", name: "Hindi" },
    { code: "or", label: "ଓ", name: "Odia" },
    { code: "te", label: "తె", name: "Telugu" },
    { code: "kok", label: "KK", name: "Kokborok" },
];

export function GovTopBanner() {
    return (
        <div className="gov-header-band no-print">
            <div className="max-w-screen-2xl mx-auto px-4 h-8 flex items-center justify-between">
                {/* Left — GOI identity */}
                <div className="flex items-center gap-3">
                    {/* Ashoka Emblem (text fallback) */}
                    <span className="text-amber-400 text-xs font-bold tracking-widest hidden sm:inline">
                        भारत सरकार | GOVERNMENT OF INDIA
                    </span>
                    <span className="text-amber-400 text-xs font-bold tracking-widest sm:hidden">
                        Govt. of India
                    </span>
                    <span className="text-white/30">•</span>
                    <span className="text-white/70 text-xs hidden md:inline">
                        Ministry of Tribal Affairs
                    </span>
                </div>

                {/* Center — GIGW accessibility */}
                <div className="hidden lg:flex items-center gap-2">
                    <span className="text-white/50 text-[10px]">Text Size:</span>
                    {["A-", "A", "A+"].map((s) => (
                        <button
                            key={s}
                            className="lang-btn text-[10px] px-1 py-0.5"
                            aria-label={`Text size ${s}`}
                        >
                            {s}
                        </button>
                    ))}
                    <span className="text-white/30 mx-1">|</span>
                    <button className="lang-btn text-[10px]" aria-label="High contrast mode">
                        High Contrast
                    </button>
                </div>

                {/* Right — language selector */}
                <div className="flex items-center gap-1.5">
                    {LANGUAGES.map((lang) => (
                        <button
                            key={lang.code}
                            className="lang-btn"
                            lang={lang.code}
                            aria-label={`Switch to ${lang.name}`}
                        >
                            {lang.label}
                        </button>
                    ))}
                    <span className="text-white/30 mx-1 hidden sm:inline">|</span>
                    <a
                        href="/sitemap"
                        className="hidden sm:inline text-white/60 hover:text-white text-[10px] transition-colors"
                    >
                        Sitemap
                    </a>
                </div>
            </div>
        </div>
    );
}

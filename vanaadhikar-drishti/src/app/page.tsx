"use client";
import React, { useState } from "react";
import Link from "next/link";
import {
    TreePine, Map, Cpu, FileSearch, Users, Shield,
    ArrowRight, Globe, Layers, BarChart3,
    CheckCircle, Download
} from "lucide-react";
import { formatNumber } from "@/lib/utils";
import { useDashboardData } from "@/lib/use-dashboard-data";
import type { StateStat } from "@/types";
import { Swiper, SwiperSlide } from "swiper/react";
import { Autoplay, Pagination, Navigation, EffectFade } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import "swiper/css/effect-fade";

// High-quality Unsplash images for the project
const HERO_BG = "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?q=80&w=2074&auto=format&fit=crop"; // Forest top view

const FEATURE_SLIDES = [
    {
        src: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop", // Satellite view
        alt: "Nationwide FRA WebGIS overview map",
        kicker: "FRA Atlas • WebGIS",
        title: "See FRA coverage on a live national atlas.",
        caption: "Interactive WebGIS with IFR/CFR boundaries, satellite layers and real-time FRA saturation metrics.",
    },
    {
        src: "https://images.unsplash.com/photo-1596386461350-326ea7750550?q=80&w=2070&auto=format&fit=crop", // Indian village meeting
        alt: "Village-level FRA claim clusters and NDVI backdrop",
        kicker: "Village insights",
        title: "Zoom into each village and Gram Sabha.",
        caption: "Track claims, pattas, NDVI trends and forest alerts for every FRA village and hamlet.",
    },
    {
        src: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070&auto=format&fit=crop", // Data analysis
        alt: "Decision support dashboards for convergence planning",
        kicker: "DSS + benefits",
        title: "Plan schemes and benefits scientifically.",
        caption: "AI-assisted decision support that links patta holders with DA-JGUA schemes and tracks outcomes.",
    },
    {
        src: "https://images.unsplash.com/photo-1627920769857-797775531d04?q=80&w=2070&auto=format&fit=crop", // Indian Farmer
        alt: "Real-time satellite alerts",
        kicker: "Real-time Monitoring",
        title: "Satellite Integration & Alerts",
        caption: "Live tracking of forest fires, encroachment alerts, and vegetation health indices.",
    },
];

const ROLES = [
    {
        id: "mota-nodal",
        title: "MoTA National Officer",
        titleHi: "राष्ट्रीय नोडल अधिकारी",
        description: "National-level monitoring, policy formulation, DA-JGUA convergence",
        href: "/national-dashboard",
        icon: <Shield size={28} />,
        color: "#007BFF",
        gradient: "from-blue-600 to-blue-800",
    },
    {
        id: "state-commissioner",
        title: "State Commissioner",
        titleHi: "राज्य आयुक्त",
        description: "State-level FRA monitoring, district performance, scheme saturation",
        href: "/state/MP/dashboard",
        icon: <BarChart3 size={28} />,
        color: "#F59E0B",
        gradient: "from-amber-500 to-amber-700",
    },
    {
        id: "district-collector",
        title: "District Collector / DRDA",
        titleHi: "जिला कलेक्टर",
        description: "District FRA atlas, DSS interventions, claim queues",
        href: "/district/MP-MAN/dashboard",
        icon: <Map size={28} />,
        color: "#059669",
        gradient: "from-emerald-600 to-emerald-800",
    },
    {
        id: "sdlc-officer",
        title: "SDLC / DLC Officer",
        titleHi: "SDLC / DLC अधिकारी",
        description: "Claim adjudication, patta issuance, field verification management",
        href: "/sdlc/dashboard",
        icon: <FileSearch size={28} />,
        color: "#7C3AED",
        gradient: "from-violet-600 to-violet-800",
    },
    {
        id: "range-officer",
        title: "Range Forest Officer",
        titleHi: "रेंज वन अधिकारी",
        description: "Field verification app, GPS boundary walk, visit reports",
        href: "/field-officer/dashboard",
        icon: <TreePine size={28} />,
        color: "#16A34A",
        gradient: "from-green-600 to-green-800",
    },
    {
        id: "gram-sabha",
        title: "Gram Sabha / FRC",
        titleHi: "ग्राम सभा / FRC",
        description: "Claim submission, status tracking, village FRA map",
        href: "/gram-sabha/dashboard",
        icon: <Users size={28} />,
        color: "#EA580C",
        gradient: "from-orange-600 to-orange-800",
    },
    {
        id: "ngo-researcher",
        title: "NGO / Researcher",
        titleHi: "NGO / शोधकर्ता",
        description: "Open FRA atlas analytics, data export, spatial analysis tools",
        href: "/analytics",
        icon: <Layers size={28} />,
        color: "#0284C7",
        gradient: "from-sky-600 to-sky-800",
    },
    {
        id: "citizen",
        title: "FRA Patta Holder",
        titleHi: "FRA पट्टाधारक",
        description: "Check claim status, download patta, apply for schemes",
        href: "/mera-patta",
        icon: <Globe size={28} />,
        color: "#DB2777",
        gradient: "from-pink-600 to-pink-800",
    },
];

export default function HomePage() {
    const [hovered, setHovered] = useState<string | null>(null);
    const { data, loading, error } = useDashboardData();
    const nationalStats = data?.nationalStats;
    const stateStats = (data?.stateStats as StateStat[]) ?? [];

    return (
        <div className="min-h-screen bg-slate-50 font-sans">
            {/* Gradient Background Overlay - Light blue/white transparency */}
            <div className="fixed inset-0 pointer-events-none z-0 bg-gradient-to-b from-blue-50/50 via-white to-blue-50/30" />

            {/* Skip Navigation */}
            <a href="#main" className="skip-nav relative z-50">Skip to main content</a>

            {/* Top Government Banner */}
            <div className="relative z-40 bg-white border-b border-border shadow-sm">
                <div className="max-w-7xl mx-auto px-4 py-1.5 flex items-center justify-between">
                    <div className="flex items-center gap-3 text-xs text-text-muted">
                        <div className="flex items-center gap-2">
                            <div className="w-8 h-8 rounded-full border border-gray-200 flex items-center justify-center bg-white p-0.5 shadow-sm">
                                <img
                                    src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Emblem_of_India.svg/1024px-Emblem_of_India.svg.png"
                                    alt="Emblem"
                                    className="w-full h-full object-contain"
                                />
                            </div>
                            <div>
                                <span className="block font-bold text-gray-800 text-[10px] leading-tight uppercase tracking-wide">भारत सरकार</span>
                                <span className="block font-bold text-gray-800 text-[10px] leading-tight uppercase tracking-wide">Government of India</span>
                            </div>
                            <div className="h-6 w-px bg-gray-300 mx-1"></div>
                            <div>
                                <span className="block font-semibold text-gray-600 text-[10px] leading-tight">जनजातीय कार्य मंत्रालय</span>
                                <span className="block font-semibold text-gray-600 text-[10px] leading-tight">Ministry of Tribal Affairs</span>
                            </div>
                        </div>
                    </div>
                    <div className="flex items-center gap-3">
                        <span className="text-text-muted text-xs hidden sm:inline">Text Size</span>
                        <div className="flex border border-gray-200 rounded overflow-hidden">
                            <button className="px-2 py-0.5 text-xs hover:bg-gray-100">A-</button>
                            <button className="px-2 py-0.5 text-xs hover:bg-gray-100 border-l border-r border-gray-200">A</button>
                            <button className="px-2 py-0.5 text-xs hover:bg-gray-100">A+</button>
                        </div>
                        <span className="text-text-muted hidden sm:inline">|</span>
                        <div className="flex gap-1">
                            <button className="px-2 py-0.5 text-xs font-bold bg-blue-600 text-white rounded shadow-sm">EN</button>
                            <button className="px-2 py-0.5 text-xs font-medium text-gray-600 hover:bg-gray-100 rounded transition-colors">हि</button>
                        </div>
                    </div>
                </div>
            </div>

            {/* 1. HERO SECTION */}
            <section className="relative z-10 w-full overflow-visible pb-16">
                {/* Hero Background with shape divider */}
                <div className="relative h-[650px] w-full overflow-hidden rounded-b-[3rem] shadow-2xl">
                    <div
                        className="absolute inset-0 bg-cover bg-center transition-transform duration-[20s] hover:scale-105"
                        style={{ backgroundImage: `url('${HERO_BG}')` }}
                    />
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-900/90 via-blue-800/75 to-transparent" />

                    {/* Hero Content */}
                    <div className="relative z-10 container mx-auto px-4 h-full flex flex-col justify-center text-white pb-16">
                        <div className="max-w-3xl">
                            <div className="flex items-center gap-4 mb-8 animate-fade-in-up">
                                <div className="p-3 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 shadow-inner">
                                    <TreePine className="text-emerald-300" size={36} />
                                </div>
                                <div className="h-10 w-px bg-white/30"></div>
                                <div>
                                    <p className="text-sm tracking-[0.2em] text-blue-200 font-bold uppercase">Official FRA Portal</p>
                                    <p className="text-xs text-blue-100/70">Rights • Dignity • Prosperity</p>
                                </div>
                            </div>

                            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight drop-shadow-sm" style={{ fontFamily: "var(--font-noto-serif)" }}>
                                VanAdhikar <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-300 to-teal-200">Drishti</span>
                            </h1>

                            <p className="text-xl md:text-2xl text-blue-100/90 leading-relaxed mb-10 max-w-2xl font-light">
                                Empowering tribal communities through AI-driven Forest Rights Act implementation, real-time monitoring, and seamless claim processing.
                            </p>

                            <div className="flex flex-wrap gap-4">
                                <Link
                                    href="/national-dashboard"
                                    className="group relative px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-white rounded-xl shadow-[0_10px_20px_-10px_rgba(16,185,129,0.5)] transition-all hover:-translate-y-1 overflow-hidden"
                                >
                                    <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-100%] group-hover:animate-shimmer" />
                                    <div className="flex items-center gap-3 font-bold text-lg">
                                        Enter Platform <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
                                    </div>
                                </Link>
                                <Link
                                    href="/mera-patta"
                                    className="px-8 py-4 bg-white/5 hover:bg-white/10 border border-white/20 hover:border-white/40 backdrop-blur-sm text-white rounded-xl font-semibold text-lg transition-all hover:shadow-lg flex items-center gap-3"
                                >
                                    <Download size={20} /> Citizen Services
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Floating Stats Cards - Reduced Size */}
                <div className="relative z-20 mt-[-50px] container mx-auto px-4 max-w-6xl">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
                        {[
                            { label: "Total Claims Filed", value: nationalStats ? formatNumber(nationalStats.totalClaims) : "—", sub: "Across India", icon: <FileSearch size={18} className="text-blue-500" />, color: "border-l-blue-500" },
                            { label: "IFR Area (Acres)", value: nationalStats ? formatNumber(nationalStats.ifrAreaAcres) : "—", sub: "Land Recognized", icon: <Map size={18} className="text-emerald-500" />, color: "border-l-emerald-500" },
                            { label: "Villages Covered", value: nationalStats ? formatNumber(nationalStats.totalVillagesCovered) : "—", sub: "Mapped Digitally", icon: <TreePine size={18} className="text-amber-500" />, color: "border-l-amber-500" },
                            { label: "Saturation", value: nationalStats ? `${nationalStats.saturationPct}%` : "—", sub: "Nationwide", icon: <Cpu size={18} className="text-purple-500" />, color: "border-l-purple-500" },
                        ].map((stat, i) => (
                            <div key={i} className={`bg-white/95 backdrop-blur-xl border border-white/40 shadow-lg rounded-xl p-3 flex flex-col items-start gap-1 hover:transform hover:-translate-y-1 transition-all duration-300 border-l-4 ${stat.color}`}>
                                <div className="w-full flex justify-between items-start">
                                    <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">{stat.label}</span>
                                    <div className="p-1 bg-white rounded-lg shadow-sm border border-gray-100">{stat.icon}</div>
                                </div>
                                <div className="text-xl font-bold text-gray-800">{stat.value}</div>
                                <div className="text-[10px] font-medium text-gray-500 bg-gray-50 px-1.5 py-0.5 rounded-md">{stat.sub}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* 2. FEATURE SLIDER SECTION */}
            <section className="relative z-10 py-12">
                <div className="container mx-auto px-4">
                    <div className="grid md:grid-cols-12 gap-12 items-center mb-16">
                        <div className="md:col-span-12 lg:col-span-4 xl:col-span-5">
                            {/* Feature Text Container - Added Light Blue Outline Card Style */}
                            <div className="bg-white rounded-2xl p-8 border border-blue-100 shadow-[0_2px_15px_-3px_rgba(0,0,0,0.07),0_10px_20px_-2px_rgba(0,0,0,0.04)] ring-1 ring-blue-50">
                                <span className="text-blue-600 font-bold tracking-wider text-sm uppercase mb-2 block">Platform Highlights</span>
                                <h2 className="text-3xl md:text-3xl font-bold text-gray-900 mb-6 leading-tight">Advanced Intelligence for <br /> <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-emerald-600">Forest Rights</span></h2>
                                <p className="text-gray-600 text-base leading-relaxed mb-6">
                                    The VanAdhikar Drishti platform integrates satellite imagery, AI-powered digitization, and ground-level feedback to ensure transparency and speed in the FRA process.
                                </p>
                                <div className="flex flex-col gap-4">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-full bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600 shrink-0"><Map size={20} /></div>
                                        <div><p className="font-bold text-gray-800 text-sm">Geospatial Validation</p><p className="text-xs text-gray-500">Verify claims with 30-year satellite data</p></div>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-full bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600 shrink-0"><Cpu size={20} /></div>
                                        <div><p className="font-bold text-gray-800 text-sm">AI Claim Parsing</p><p className="text-xs text-gray-500">Automated extraction from handwritten forms</p></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="md:col-span-12 lg:col-span-8 xl:col-span-7">
                            <div className="rounded-2xl overflow-hidden shadow-2xl ring-4 ring-white/50 transform hover:scale-[1.01] transition-transform duration-500">
                                <Swiper
                                    modules={[Autoplay, Pagination, Navigation, EffectFade]}
                                    autoplay={{ delay: 5000, disableOnInteraction: false }}
                                    loop
                                    pagination={{ clickable: true }}
                                    effect="fade"
                                    speed={800}
                                    className="h-[400px] md:h-[500px] w-full"
                                >
                                    {FEATURE_SLIDES.map((slide, index) => (
                                        <SwiperSlide key={slide.src}>
                                            <div className="relative w-full h-full group">
                                                <img
                                                    src={slide.src}
                                                    alt={slide.alt}
                                                    className="absolute inset-0 w-full h-full object-cover"
                                                />
                                                <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-gray-900/40 to-transparent" />
                                                <div className="absolute bottom-0 left-0 w-full p-8 md:p-12">
                                                    <span className="inline-block px-3 py-1 bg-emerald-500 text-white text-xs font-bold rounded-full mb-3 shadow-lg uppercase tracking-wider">
                                                        {slide.kicker}
                                                    </span>
                                                    <h3 className="text-2xl md:text-3xl font-bold text-white mb-3">{slide.title}</h3>
                                                    <p className="text-gray-300 text-sm md:text-base max-w-lg leading-relaxed">
                                                        {slide.caption}
                                                    </p>
                                                </div>
                                            </div>
                                        </SwiperSlide>
                                    ))}
                                </Swiper>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Main Content Areas */}
            <main id="main" className="relative z-10 max-w-7xl mx-auto px-4 py-8">

                {/* Role Selection Grid - Redesigned Cards */}
                <section className="mb-20">
                    <div className="text-center mb-10">
                        <span className="px-4 py-1.5 rounded-full bg-blue-50 text-blue-600 font-semibold text-sm mb-4 inline-block border border-blue-100">Portal Access</span>
                        <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Select Your Role</h2>
                        <p className="text-gray-500 text-lg max-w-2xl mx-auto">Access specialized dashboards tailored to your administrative or functional role.</p>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                        {ROLES.map((role) => (
                            <Link
                                key={role.id}
                                href={role.href}
                                onMouseEnter={() => setHovered(role.id)}
                                onMouseLeave={() => setHovered(null)}
                                className="group relative bg-white border border-blue-100 rounded-2xl p-6 shadow-[0_2px_15px_-3px_rgba(0,0,0,0.07),0_10px_20px_-2px_rgba(0,0,0,0.04)] hover:shadow-xl transition-all duration-300 hover:-translate-y-2 overflow-hidden hover:border-blue-300 ring-1 ring-blue-50/50"
                            >
                                <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${role.gradient} opacity-[0.08] rounded-bl-full group-hover:opacity-[0.15] transition-opacity`} />

                                <div
                                    className={`w-14 h-14 rounded-2xl mb-5 flex items-center justify-center shadow-lg transform group-hover:scale-110 transition-transform duration-300 bg-gradient-to-br ${role.gradient} text-white`}
                                >
                                    {role.icon}
                                </div>
                                <h3 className="font-bold text-gray-900 text-lg mb-1 group-hover:text-blue-600 transition-colors">{role.title}</h3>
                                <p className="text-xs font-semibold text-emerald-600 mb-3">{role.titleHi}</p>
                                <p className="text-gray-500 text-sm leading-relaxed mb-6 min-h-[60px]">{role.description}</p>

                                <div className="flex items-center text-sm font-bold text-blue-600 group-hover:translate-x-2 transition-transform">
                                    Login <ArrowRight size={16} className="ml-2" />
                                </div>
                            </Link>
                        ))}
                    </div>
                </section>

                {/* State Stats Redesigned */}
                <section className="mb-20">
                    <div className="flex items-end justify-between mb-8 border-b border-gray-200 pb-4">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-900">Focus States Performance</h2>
                            <p className="text-gray-500 mt-1">High-priority states monitoring</p>
                        </div>
                        <Link href="/atlas" className="text-blue-600 font-semibold hover:bg-blue-50 px-4 py-2 rounded-lg transition-colors flex items-center gap-2">
                            View National Atlas <ArrowRight size={18} />
                        </Link>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                        {stateStats.map((s) => {
                            const pct = Math.round((s.granted / s.totalClaims) * 100);
                            return (
                                <Link
                                    key={s.id}
                                    href={`/state/${s.slug}/dashboard`}
                                    className="bg-white rounded-xl p-5 shadow-[0_2px_15px_-3px_rgba(0,0,0,0.07),0_10px_20px_-2px_rgba(0,0,0,0.04)] border border-blue-100 ring-1 ring-blue-50 hover:shadow-lg hover:border-blue-300 transition-all group"
                                >
                                    <div className="flex justify-between items-start mb-4">
                                        <div className="w-10 h-10 rounded-lg flex items-center justify-center font-bold text-white shadow-md text-sm" style={{ background: s.color }}>
                                            {s.id}
                                        </div>
                                        <div className="text-right">
                                            <p className="text-xs text-gray-400 font-semibold uppercase tracking-wider">Pattas</p>
                                            <p className="text-xl font-bold text-gray-800" style={{ fontFamily: "var(--font-noto-serif)" }}>{formatNumber(s.granted)}</p>
                                        </div>
                                    </div>

                                    <h4 className="font-bold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors">{s.name}</h4>

                                    <div className="w-full bg-gray-100 rounded-full h-2 mb-2 overflow-hidden">
                                        <div className="h-full rounded-full transition-all duration-1000" style={{ width: `${pct}%`, background: s.color }} />
                                    </div>
                                    <div className="flex justify-between text-xs text-gray-500 mb-4">
                                        <span>Grant Rate</span>
                                        <span className="font-bold text-gray-700">{pct}%</span>
                                    </div>

                                    {s.fireAlerts > 0 && (
                                        <div className="bg-red-50 text-red-600 px-3 py-2 rounded-lg text-xs font-semibold flex items-center gap-2">
                                            <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
                                            {s.fireAlerts} Active Fire Alerts
                                        </div>
                                    )}
                                </Link>
                            );
                        })}
                    </div>
                </section>

                {/* Compliance Footer Strip */}
                <div className="flex flex-wrap gap-6 items-center justify-center text-xs text-gray-500 border-t border-gray-200 pt-10 pb-4">
                    {[
                        "GIGW 3.0 Compliant",
                        "WCAG 2.1 AA",
                        "MeghRaj NIC Cloud Hosted",
                        "Jan Parichay SSO",
                        "STQC Certified Architecture",
                    ].map((t) => (
                        <span key={t} className="flex items-center gap-2 px-4 py-1.5 bg-white/80 rounded-full border border-gray-200 shadow-sm">
                            <CheckCircle size={12} className="text-emerald-500" />
                            {t}
                        </span>
                    ))}
                </div>
            </main>

            {/* Footer */}
            <footer className="bg-slate-900 text-white/70 mt-12 relative z-10">
                <div className="max-w-7xl mx-auto px-4 py-12">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-sm mb-12">
                        <div>
                            <p className="font-bold text-white mb-6 text-base border-l-4 border-blue-500 pl-3">Platform</p>
                            <ul className="space-y-3">
                                {["FRA Atlas", "DSS Engine", "Digitization", "Analytics"].map((l) => (
                                    <li key={l}><a href="#" className="hover:text-blue-400 transition-colors flex items-center gap-2"><div className="w-1 h-1 bg-white/30 rounded-full" /> {l}</a></li>
                                ))}
                            </ul>
                        </div>
                        <div>
                            <p className="font-bold text-white mb-6 text-base border-l-4 border-emerald-500 pl-3">Resources</p>
                            <ul className="space-y-3">
                                {["FRA Act 2006", "Rules & Guidelines", "FAQ", "State Reports"].map((l) => (
                                    <li key={l}><a href="#" className="hover:text-emerald-400 transition-colors flex items-center gap-2"><div className="w-1 h-1 bg-white/30 rounded-full" /> {l}</a></li>
                                ))}
                            </ul>
                        </div>
                        <div>
                            <p className="font-bold text-white mb-6 text-base border-l-4 border-amber-500 pl-3">Support</p>
                            <ul className="space-y-3">
                                {["Helpline: 011-23340513", "fra-tribal@gov.in", "Public Grievances", "RTI"].map((l) => (
                                    <li key={l}><a href="#" className="hover:text-amber-400 transition-colors flex items-center gap-2"><div className="w-1 h-1 bg-white/30 rounded-full" /> {l}</a></li>
                                ))}
                            </ul>
                        </div>
                        <div>
                            <div className="bg-white/5 p-4 rounded-xl border border-white/10">
                                <p className="font-bold text-white mb-2">Connect with MoTA</p>
                                <p className="text-xs mb-4">Shastri Bhawan, New Delhi - 110001</p>
                                <div className="flex gap-3">
                                    <div className="w-8 h-8 rounded bg-blue-600 flex items-center justify-center text-white font-bold cursor-pointer hover:bg-blue-500">f</div>
                                    <div className="w-8 h-8 rounded bg-sky-500 flex items-center justify-center text-white font-bold cursor-pointer hover:bg-sky-400">t</div>
                                    <div className="w-8 h-8 rounded bg-red-600 flex items-center justify-center text-white font-bold cursor-pointer hover:bg-red-500">y</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="border-t border-white/10 pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-white/40">
                        <div className="flex items-center gap-4">
                            <span className="text-emerald-400 font-bold">VanAdhikar Drishti</span>
                            <span>© 2026 Ministry of Tribal Affairs. All rights reserved.</span>
                        </div>
                        <p className="flex items-center gap-2">
                            Designed &amp; Hosted by <span className="text-white/60 font-semibold">NIC — National Informatics Centre</span>
                        </p>
                    </div>
                </div>
            </footer>
        </div>
    );
}


"use client";
import Link from "next/link";
import { ArrowLeft, Home, BarChart3, Map, Brain, MessageSquare, FileText, Users, MapPin } from "lucide-react";

export default function SitemapPage() {
    const sections = [
        {
            title: "Main Pages",
            icon: <Home size={20} />,
            links: [
                { name: "Home", href: "/" },
                { name: "Help & Support", href: "/help" },
                { name: "User Profile", href: "/profile" },
                { name: "Settings", href: "/settings" },
                { name: "Notifications", href: "/notifications" },
            ],
        },
        {
            title: "Dashboards",
            icon: <BarChart3 size={20} />,
            links: [
                { name: "National Dashboard", href: "/national-dashboard" },
                { name: "State Dashboards", href: "/state/MP/dashboard" },
                { name: "District Dashboards", href: "/district/MP-BAL/dashboard" },
                { name: "SDLC Dashboard", href: "/sdlc/dashboard" },
                { name: "Field Officer Dashboard", href: "/field-officer/dashboard" },
                { name: "Gram Sabha Dashboard", href: "/gram-sabha/dashboard" },
            ],
        },
        {
            title: "Feature Modules",
            icon: <FileText size={20} />,
            links: [
                { name: "Analytics Portal", href: "/analytics" },
                { name: "Mera Patta (Claim Search)", href: "/mera-patta" },
                { name: "WebGIS Atlas", href: "/atlas" },
                { name: "Decision Support System (DSS)", href: "/dss" },
                { name: "Grievance Redressal", href: "/grievances" },
                { name: "OCR Digitization", href: "/digitization" },
            ],
        },
    ];

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-gradient-to-br from-primary-700 via-primary-800 to-primary-900 text-white p-6">
                <div className="max-w-6xl mx-auto">
                    <Link href="/" className="inline-flex items-center gap-2 text-sm mb-4 hover:underline">
                        <ArrowLeft size={16} /> Back to Home
                    </Link>
                    <h1 className="text-3xl font-bold mb-2">Sitemap</h1>
                    <p className="text-primary-100">Complete navigation map of Vanaadhikar Drishti</p>
                </div>
            </div>

            {/* Content */}
            <div className="max-w-6xl mx-auto p-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {sections.map((section, i) => (
                        <div key={i} className="tribal-card p-6">
                            <div className="flex items-center gap-3 mb-4">
                                <div className="w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center text-primary">
                                    {section.icon}
                                </div>
                                <h2 className="text-xl font-bold text-primary">{section.title}</h2>
                            </div>
                            <ul className="space-y-2">
                                {section.links.map((link, j) => (
                                    <li key={j}>
                                        <Link
                                            href={link.href}
                                            className="text-sm text-gray-700 hover:text-accent hover:underline transition-colors"
                                        >
                                            {link.name}
                                        </Link>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>

                {/* Additional Info */}
                <div className="tribal-card p-6 mt-6">
                    <h2 className="text-xl font-bold text-primary mb-4">About This System</h2>
                    <p className="text-gray-700 mb-4">
                        Vanaadhikar Drishti is a comprehensive Forest Rights Act (FRA) monitoring and decision support
                        system developed for the Ministry of Tribal Affairs, Government of India.
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                        <div>
                            <p className="font-semibold text-primary mb-1">Total Claims</p>
                            <p className="text-2xl font-bold text-accent">24.2 Lakh+</p>
                        </div>
                        <div>
                            <p className="font-semibold text-primary mb-1">States Covered</p>
                            <p className="text-2xl font-bold text-accent">28</p>
                        </div>
                        <div>
                            <p className="font-semibold text-primary mb-1">Helpline</p>
                            <p className="text-2xl font-bold text-accent">1800-11-0130</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

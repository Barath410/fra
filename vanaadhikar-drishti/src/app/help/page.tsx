"use client";
import Link from "next/link";
import { ArrowLeft, HelpCircle, Book, Phone, Mail, MapPin } from "lucide-react";

export default function HelpPage() {
    return (
        <div className="min-h-screen bg-white">
            {/* Header */}
            <div className="bg-gradient-to-br from-primary-700 via-primary-800 to-primary-900 text-white p-6">
                <div className="max-w-4xl mx-auto">
                    <Link href="/" className="inline-flex items-center gap-2 text-sm mb-4 hover:underline">
                        <ArrowLeft size={16} /> Back to Home
                    </Link>
                    <h1 className="text-3xl font-bold mb-2">Help & Support</h1>
                    <p className="text-primary-100">Vanaadhikar Drishti - FRA Monitoring System</p>
                </div>
            </div>

            {/* Content */}
            <div className="max-w-4xl mx-auto p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                    {/* User Guides */}
                    <div className="tribal-card p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="w-12 h-12 rounded-full bg-primary-100 flex items-center justify-center">
                                <Book className="text-primary" size={24} />
                            </div>
                            <h2 className="text-xl font-bold text-primary">User Guides</h2>
                        </div>
                        <ul className="space-y-3">
                            <li>
                                <Link href="/help/getting-started" className="text-accent hover:underline font-semibold">
                                    Getting Started with FRA System
                                </Link>
                            </li>
                            <li>
                                <Link href="/help/claim-process" className="text-accent hover:underline font-semibold">
                                    How to File a Claim
                                </Link>
                            </li>
                            <li>
                                <Link href="/help/dashboard-guide" className="text-accent hover:underline font-semibold">
                                    Dashboard Navigation Guide
                                </Link>
                            </li>
                            <li>
                                <Link href="/help/sdlc-workflow" className="text-accent hover:underline font-semibold">
                                    SDLC Officer Workflow
                                </Link>
                            </li>
                        </ul>
                    </div>

                    {/* Contact Support */}
                    <div className="tribal-card p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="w-12 h-12 rounded-full bg-accent/10 flex items-center justify-center">
                                <HelpCircle className="text-accent" size={24} />
                            </div>
                            <h2 className="text-xl font-bold text-primary">Contact Support</h2>
                        </div>
                        <div className="space-y-4">
                            <div className="flex items-start gap-3">
                                <Phone className="text-accent flex-shrink-0 mt-1" size={18} />
                                <div>
                                    <p className="text-sm font-semibold text-gray-700">Helpline (Toll-Free)</p>
                                    <a href="tel:1800-11-0130" className="text-lg font-bold text-accent">1800-11-0130</a>
                                    <p className="text-xs text-gray-500 mt-1">Mon-Sat, 9 AM - 5 PM</p>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <Mail className="text-accent flex-shrink-0 mt-1" size={18} />
                                <div>
                                    <p className="text-sm font-semibold text-gray-700">Email Support</p>
                                    <a href="mailto:support@fra.gov.in" className="text-accent hover:underline">support@fra.gov.in</a>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <MapPin className="text-accent flex-shrink-0 mt-1" size={18} />
                                <div>
                                    <p className="text-sm font-semibold text-gray-700">Ministry of Tribal Affairs</p>
                                    <p className="text-xs text-gray-600">Shastri Bhawan, New Delhi - 110001</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* FAQ Section */}
                <div className="tribal-card p-6">
                    <h2 className="text-xl font-bold text-primary mb-4">Frequently Asked Questions</h2>
                    <div className="space-y-4">
                        {[
                            { q: "What is the Forest Rights Act (FRA)?", a: "The Scheduled Tribes and Other Traditional Forest Dwellers (Recognition of Forest Rights) Act, 2006 recognizes the rights of forest-dwelling tribal communities and other traditional forest dwellers." },
                            { q: "Who can file an FRA claim?", a: "Members of Scheduled Tribes and Other Traditional Forest Dwellers who have been residing in forest areas for at least 75 years can file claims." },
                            { q: "How long does the claim process take?", a: "The average processing time is approximately 127 days, subject to proper documentation and committee meetings." },
                            { q: "What documents are required?", a: "Proof of residence (75 years), Aadhaar card, community certificate, and evidence of forest dependence are required." },
                        ].map((faq, i) => (
                            <div key={i} className="border-l-4 border-primary pl-4">
                                <h3 className="font-bold text-primary text-sm mb-1">{faq.q}</h3>
                                <p className="text-sm text-gray-600">{faq.a}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

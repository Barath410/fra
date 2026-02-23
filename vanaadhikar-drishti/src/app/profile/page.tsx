"use client";
import Link from "next/link";
import { ArrowLeft, User, Mail, Phone, MapPin, Shield, Bell } from "lucide-react";

export default function ProfilePage() {
    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-gradient-to-br from-primary-700 via-primary-800 to-primary-900 text-white p-6">
                <div className="max-w-4xl mx-auto">
                    <Link href="/" className="inline-flex items-center gap-2 text-sm mb-4 hover:underline">
                        <ArrowLeft size={16} /> Back to Dashboard
                    </Link>
                    <h1 className="text-3xl font-bold mb-2">User Profile</h1>
                    <p className="text-primary-100">Manage your account settings and preferences</p>
                </div>
            </div>

            {/* Content */}
            <div className="max-w-4xl mx-auto p-6">
                <div className="tribal-card p-6 mb-6">
                    <div className="flex items-center gap-4 mb-6">
                        <div className="w-20 h-20 rounded-full bg-gradient-to-br from-primary to-primary-600 flex items-center justify-center text-white text-2xl font-bold">
                            UD
                        </div>
                        <div>
                            <h2 className="text-2xl font-bold text-primary">User Demo</h2>
                            <p className="text-gray-600">SDLC Officer - Madhya Pradesh</p>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="form-label">Full Name</label>
                            <input type="text" className="form-input" defaultValue="User Demo" />
                        </div>
                        <div>
                            <label className="form-label">Email Address</label>
                            <input type="email" className="form-input" defaultValue="user.demo@fra.gov.in" />
                        </div>
                        <div>
                            <label className="form-label">Mobile Number</label>
                            <input type="tel" className="form-input" defaultValue="+91 98765 43210" />
                        </div>
                        <div>
                            <label className="form-label">Designation</label>
                            <input type="text" className="form-input" defaultValue="SDLC Officer" disabled />
                        </div>
                        <div>
                            <label className="form-label">State</label>
                            <select className="form-input">
                                <option>Madhya Pradesh</option>
                                <option>Maharashtra</option>
                                <option>Chhattisgarh</option>
                            </select>
                        </div>
                        <div>
                            <label className="form-label">District</label>
                            <input type="text" className="form-input" defaultValue="Balaghat" />
                        </div>
                    </div>

                    <div className="flex gap-3 mt-6">
                        <button className="px-6 py-2 bg-primary text-white rounded-lg font-semibold shadow-md hover:shadow-lg transition-all">
                            Save Changes
                        </button>
                        <button className="px-6 py-2 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-all">
                            Cancel
                        </button>
                    </div>
                </div>

                {/* Additional Sections */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="tribal-card p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <Shield className="text-primary" size={24} />
                            <h3 className="text-lg font-bold text-primary">Security</h3>
                        </div>
                        <Link href="/settings/change-password" className="text-accent hover:underline font-semibold text-sm">
                            Change Password
                        </Link>
                    </div>

                    <div className="tribal-card p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <Bell className="text-primary" size={24} />
                            <h3 className="text-lg font-bold text-primary">Notifications</h3>
                        </div>
                        <Link href="/notifications" className="text-accent hover:underline font-semibold text-sm">
                            Manage Notification Preferences
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}

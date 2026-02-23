"use client";
import Link from "next/link";
import { ArrowLeft, Settings as SettingsIcon, Bell, Lock, Globe, Palette, Database } from "lucide-react";

export default function SettingsPage() {
    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-gradient-to-br from-primary-700 via-primary-800 to-primary-900 text-white p-6">
                <div className="max-w-4xl mx-auto">
                    <Link href="/" className="inline-flex items-center gap-2 text-sm mb-4 hover:underline">
                        <ArrowLeft size={16} /> Back to Dashboard
                    </Link>
                    <h1 className="text-3xl font-bold mb-2">Settings</h1>
                    <p className="text-primary-100">Manage your application preferences</p>
                </div>
            </div>

            {/* Content */}
            <div className="max-w-4xl mx-auto p-6 space-y-6">
                {/* Notification Settings */}
                <div className="tribal-card p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <Bell className="text-primary" size={24} />
                        <h2 className="text-xl font-bold text-primary">Notification Preferences</h2>
                    </div>
                    <div className="space-y-3">
                        {[
                            { label: "Email notifications for new claims", enabled: true },
                            { label: "SMS alerts for urgent grievances", enabled: true },
                            { label: "Push notifications for meetings", enabled: false },
                            { label: "Weekly summary reports", enabled: true },
                        ].map((setting, i) => (
                            <div key={i} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <span className="text-sm text-gray-700">{setting.label}</span>
                                <label className="relative inline-flex items-center cursor-pointer">
                                    <input type="checkbox" className="sr-only peer" defaultChecked={setting.enabled} />
                                    <div className="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-primary rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                                </label>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Language & Region */}
                <div className="tribal-card p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <Globe className="text-primary" size={24} />
                        <h2 className="text-xl font-bold text-primary">Language & Region</h2>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="form-label">Interface Language</label>
                            <select className="form-input">
                                <option>English</option>
                                <option>हिंदी (Hindi)</option>
                            </select>
                        </div>
                        <div>
                            <label className="form-label">Date Format</label>
                            <select className="form-input">
                                <option>DD/MM/YYYY</option>
                                <option>MM/DD/YYYY</option>
                                <option>YYYY-MM-DD</option>
                            </select>
                        </div>
                    </div>
                </div>

                {/* Display Settings */}
                <div className="tribal-card p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <Palette className="text-primary" size={24} />
                        <h2 className="text-xl font-bold text-primary">Display Settings</h2>
                    </div>
                    <div className="space-y-4">
                        <div>
                            <label className="form-label">Dashboard Layout</label>
                            <select className="form-input">
                                <option>Compact</option>
                                <option>Standard</option>
                                <option>Detailed</option>
                            </select>
                        </div>
                        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                            <span className="text-sm text-gray-700">Show map by default</span>
                            <label className="relative inline-flex items-center cursor-pointer">
                                <input type="checkbox" className="sr-only peer" defaultChecked />
                                <div className="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-primary rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                            </label>
                        </div>
                    </div>
                </div>

                {/* Security */}
                <div className="tribal-card p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <Lock className="text-primary" size={24} />
                        <h2 className="text-xl font-bold text-primary">Security & Privacy</h2>
                    </div>
                    <div className="space-y-3">
                        <Link href="/settings/change-password" className="block p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-all">
                            <span className="text-sm font-semibold text-primary">Change Password</span>
                        </Link>
                        <Link href="/settings/two-factor" className="block p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-all">
                            <span className="text-sm font-semibold text-primary">Two-Factor Authentication</span>
                        </Link>
                        <Link href="/settings/sessions" className="block p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-all">
                            <span className="text-sm font-semibold text-primary">Active Sessions</span>
                        </Link>
                    </div>
                </div>

                {/* Save Button */}
                <div className="flex gap-3">
                    <button className="px-6 py-3 bg-primary text-white rounded-lg font-semibold shadow-md hover:shadow-lg transition-all">
                        Save All Changes
                    </button>
                    <button className="px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-all">
                        Reset to Defaults
                    </button>
                </div>
            </div>
        </div>
    );
}

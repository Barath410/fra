"use client";
import Link from "next/link";
import { ArrowLeft, Bell, AlertCircle, CheckCircle, Info, Calendar } from "lucide-react";

export default function NotificationsPage() {
    const notifications = [
        {
            id: 1,
            type: "urgent",
            icon: <AlertCircle size={20} />,
            title: "SDLC Meeting Scheduled",
            message: "Convergence meeting scheduled for Feb 22, 2026 at 10:00 AM",
            time: "2 hours ago",
            read: false,
        },
        {
            id: 2,
            type: "success",
            icon: <CheckCircle size={20} />,
            title: "Claim Approved",
            message: "Claim FRA-2026-MP-00342 has been approved by DLC",
            time: "5 hours ago",
            read: false,
        },
        {
            id: 3,
            type: "info",
            icon: <Info size={20} />,
            title: "System Update",
            message: "DSS Engine v2.3 deployed with improved accuracy",
            time: "1 day ago",
            read: true,
        },
        {
            id: 4,
            type: "urgent",
            icon: <AlertCircle size={20} />,
            title: "Grievance Assigned",
            message: "New grievance GRV-2026-MP-0234 assigned to you",
            time: "1 day ago",
            read: true,
        },
        {
            id: 5,
            type: "info",
            icon: <Calendar size={20} />,
            title: "Monthly Report Due",
            message: "January 2026 progress report submission deadline: Feb 25",
            time: "2 days ago",
            read: true,
        },
    ];

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-gradient-to-br from-primary-700 via-primary-800 to-primary-900 text-white p-6">
                <div className="max-w-4xl mx-auto">
                    <Link href="/" className="inline-flex items-center gap-2 text-sm mb-4 hover:underline">
                        <ArrowLeft size={16} /> Back to Dashboard
                    </Link>
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-3xl font-bold mb-2">Notifications</h1>
                            <p className="text-primary-100">Stay updated with important alerts and updates</p>
                        </div>
                        <button className="px-4 py-2 bg-white/10 backdrop-blur-sm rounded-lg text-sm font-semibold hover:bg-white/20 transition-all">
                            Mark All as Read
                        </button>
                    </div>
                </div>
            </div>

            {/* Content */}
            <div className="max-w-4xl mx-auto p-6">
                {/* Filter Tabs */}
                <div className="flex gap-2 mb-6">
                    {["All", "Unread", "Urgent", "System"].map((tab) => (
                        <button
                            key={tab}
                            className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${tab === "All"
                                    ? "bg-primary text-white shadow-md"
                                    : "bg-white text-gray-600 hover:bg-gray-100"
                                }`}
                        >
                            {tab}
                        </button>
                    ))}
                </div>

                {/* Notifications List */}
                <div className="space-y-3">
                    {notifications.map((notif) => (
                        <div
                            key={notif.id}
                            className={`tribal-card p-4 transition-all hover:shadow-md cursor-pointer ${!notif.read ? "border-l-4 border-accent" : ""
                                }`}
                        >
                            <div className="flex items-start gap-4">
                                <div
                                    className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${notif.type === "urgent"
                                            ? "bg-red-100 text-red-600"
                                            : notif.type === "success"
                                                ? "bg-emerald-100 text-emerald-600"
                                                : "bg-blue-100 text-blue-600"
                                        }`}
                                >
                                    {notif.icon}
                                </div>
                                <div className="flex-1">
                                    <div className="flex items-start justify-between mb-1">
                                        <h3 className="font-bold text-primary">{notif.title}</h3>
                                        {!notif.read && (
                                            <span className="w-2 h-2 rounded-full bg-accent flex-shrink-0 mt-1.5"></span>
                                        )}
                                    </div>
                                    <p className="text-sm text-gray-600 mb-2">{notif.message}</p>
                                    <p className="text-xs text-gray-400">{notif.time}</p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Empty State (if needed) */}
                {notifications.length === 0 && (
                    <div className="tribal-card p-12 text-center">
                        <Bell className="mx-auto text-gray-300 mb-4" size={48} />
                        <h3 className="text-xl font-bold text-gray-400 mb-2">No Notifications</h3>
                        <p className="text-gray-500">You're all caught up!</p>
                    </div>
                )}
            </div>
        </div>
    );
}

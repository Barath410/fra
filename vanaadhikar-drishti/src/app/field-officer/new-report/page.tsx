'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardPageContainer } from '@/components/dashboard-components';
import { CheckCircle } from 'lucide-react';

export default function NewFieldReportPage() {
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState({ claimId: '', findings: '', gpsLocation: '' });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 3000);
  };

  return (
    <DashboardLayout role="field-officer" title="Field Officer" titleHi="क्षेत्र अधिकारी">
      <DashboardPageContainer title="Submit Field Report">
        <div className="max-w-2xl bg-white rounded-lg shadow-sm p-6">
          {submitted && <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-2"><CheckCircle size={20} className="text-green-600" /><span>Report submitted</span></div>}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div><label className="block text-sm font-medium mb-1">Claim ID</label><input type="text" placeholder="Enter claim ID" className="w-full px-3 py-2 border rounded-lg" value={formData.claimId} onChange={(e) => setFormData(p => ({ ...p, claimId: e.target.value }))} required /></div>
            <div><label className="block text-sm font-medium mb-1">Findings</label><textarea placeholder="Document verification findings" className="w-full px-3 py-2 border rounded-lg h-24" value={formData.findings} onChange={(e) => setFormData(p => ({ ...p, findings: e.target.value }))} required /></div>
            <div><label className="block text-sm font-medium mb-1">GPS Coordinates</label><input type="text" placeholder="Lat,Lon" className="w-full px-3 py-2 border rounded-lg" value={formData.gpsLocation} onChange={(e) => setFormData(p => ({ ...p, gpsLocation: e.target.value }))} /></div>
            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded-lg">Submit Report</button>
          </form>
        </div>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

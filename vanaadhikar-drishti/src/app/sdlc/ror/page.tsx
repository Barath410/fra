'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardPageContainer } from '@/components/dashboard-components';
import { CheckCircle } from 'lucide-react';

export default function RORPage() {
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState({ districtId: '', claimId: '', rorData: '' });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    setFormData({ districtId: '', claimId: '', rorData: '' });
    setTimeout(() => setSubmitted(false), 3000);
  };

  return (
    <DashboardLayout role="sdlc-officer" title="SDLC Officer" titleHi="SDLC अधिकारी">
      <DashboardPageContainer title="Record of Rights (RoR)">
        <div className="max-w-2xl bg-white rounded-lg shadow-sm p-6">
          {submitted && <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-2"><CheckCircle size={20} className="text-green-600" /><span>RoR submitted successfully</span></div>}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div><label className="block text-sm font-medium mb-1">District ID</label><input type="text" placeholder="Enter district ID" className="w-full px-3 py-2 border rounded-lg" value={formData.districtId} onChange={(e) => setFormData(p => ({ ...p, districtId: e.target.value }))} required /></div>
            <div><label className="block text-sm font-medium mb-1">Claim ID</label><input type="text" placeholder="Enter claim ID" className="w-full px-3 py-2 border rounded-lg" value={formData.claimId} onChange={(e) => setFormData(p => ({ ...p, claimId: e.target.value }))} required /></div>
            <div><label className="block text-sm font-medium mb-1">RoR Data</label><textarea placeholder="Enter RoR data" className="w-full px-3 py-2 border rounded-lg h-20" value={formData.rorData} onChange={(e) => setFormData(p => ({ ...p, rorData: e.target.value }))} required /></div>
            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded-lg">Submit RoR</button>
          </form>
        </div>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

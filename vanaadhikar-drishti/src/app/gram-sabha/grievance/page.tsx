'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { DashboardPageContainer } from '@/components/dashboard-components';
import { CheckCircle } from 'lucide-react';

export default function GramSabhaGrievancePage() {
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState({ type: '', description: '' });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    setFormData({ type: '', description: '' });
    setTimeout(() => setSubmitted(false), 3000);
  };

  return (
    <DashboardLayout role="gram-sabha" title="Gram Sabha" titleHi="ग्रां सभा">
      <DashboardPageContainer title="Lodge Grievance">
        <div className="max-w-2xl bg-white rounded-lg shadow-sm p-6">
          {submitted && <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-2"><CheckCircle size={20} className="text-green-600" /><span>Grievance submitted successfully</span></div>}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div><label className="block text-sm font-medium mb-1">Grievance Type</label><select className="w-full px-3 py-2 border rounded-lg" value={formData.type} onChange={(e) => setFormData(p => ({ ...p, type: e.target.value }))} required><option>Select type</option><option>Delay</option><option>Document</option></select></div>
            <div><label className="block text-sm font-medium mb-1">Description</label><textarea placeholder="Describe the issue" className="w-full px-3 py-2 border rounded-lg h-24" value={formData.description} onChange={(e) => setFormData(p => ({ ...p, description: e.target.value }))} required /></div>
            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded-lg">Submit Grievance</button>
          </form>
        </div>
      </DashboardPageContainer>
    </DashboardLayout>
  );
}

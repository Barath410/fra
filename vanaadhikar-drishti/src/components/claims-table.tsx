// src/components/claims-table.tsx
import React, { useState } from 'react';
import { 
  Search, Filter, MoreHorizontal, Eye, FileSignature, AlertCircle, CheckCircle, Clock
} from 'lucide-react';
import { 
  DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger 
} from "@/components/ui/dropdown-menu"; // Assuming you have shadcn/ui or simple custom version
// If not using shadcn/ui actually, I will simulate pure tailwind dropdown or keep it simple.
// I'll stick to pure tailwind to minimize dependency assumptions within this file if shadcn components aren't fully set up.
// Retrying with pure React for maximum compatibility.

export type ClaimStatus = 'Approved' | 'Rejected' | 'Pending' | 'In Review';
export type ClaimType = 'IFR' | 'CFR' | 'Habitat';

export interface Claim {
  id: string;
  claimantName: string;
  village: string;
  claimType: ClaimType;
  submissionDate: string;
  status: ClaimStatus;
  area: string;
}

interface ClaimsTableProps {
  claims: Claim[];
  title?: string;
  onView?: (id: string) => void;
  onApprove?: (id: string) => void;
  onReject?: (id: string) => void;
}

const statusStyles : Record<ClaimStatus, string> = {
  'Approved': 'bg-green-100 text-green-800 border-green-200',
  'Rejected': 'bg-red-100 text-red-800 border-red-200',
  'Pending': 'bg-yellow-100 text-yellow-800 border-yellow-200',
  'In Review': 'bg-blue-100 text-blue-800 border-blue-200',
};

const statusIcons: Record<ClaimStatus, React.ReactNode> = {
  'Approved': <CheckCircle className="w-3 h-3 mr-1" />,
  'Rejected': <AlertCircle className="w-3 h-3 mr-1" />,
  'Pending': <Clock className="w-3 h-3 mr-1" />,
  'In Review': <Eye className="w-3 h-3 mr-1" />,
};

export default function ClaimsTable({ claims, title = "Claims List", onView }: ClaimsTableProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<string>('All');

  const filteredClaims = claims.filter(claim => {
    const matchesSearch = 
      claim.claimantName.toLowerCase().includes(searchTerm.toLowerCase()) || 
      claim.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      claim.village.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFilter = filterStatus === 'All' || claim.status === filterStatus;
    
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      {/* Table Header Controls */}
      <div className="p-5 border-b border-gray-100 flex flex-col md:flex-row justify-between md:items-center gap-4">
        <h2 className="text-lg font-semibold text-gray-800">{title} <span className="text-gray-400 text-sm font-normal">({claims.length})</span></h2>
        
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input 
              type="text" 
              placeholder="Search claims..." 
              className="pl-9 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-full sm:w-64"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="flex items-center space-x-2">
            <select 
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
            >
              <option value="All">All Status</option>
              <option value="Approved">Approved</option>
              <option value="Pending">Pending</option>
              <option value="Rejected">Rejected</option>
              <option value="In Review">In Review</option>
            </select>
            
            <button className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-gray-600">
               <Filter className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Table Content */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Claim ID</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Claimant / Village</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type & Area</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredClaims.length > 0 ? (
              filteredClaims.map((claim) => (
                <tr key={claim.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">
                    {claim.id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{claim.claimantName}</div>
                    <div className="text-sm text-gray-500">{claim.village}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{claim.claimType}</div>
                    <div className="text-xs text-gray-500">{claim.area} Acres</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {claim.submissionDate}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full items-center border ${statusStyles[claim.status]}`}>
                      {statusIcons[claim.status]}
                      {claim.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex justify-end gap-2">
                       <button 
                         onClick={() => onView && onView(claim.id)}
                         className="text-blue-600 hover:text-blue-900 bg-blue-50 p-1.5 rounded-md transition-colors"
                         title="View Details"
                        >
                         <Eye className="w-4 h-4" />
                       </button>
                       <button className="text-gray-400 hover:text-gray-600 p-1.5 rounded-md hover:bg-gray-100">
                         <MoreHorizontal className="w-4 h-4" />
                       </button>
                    </div>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={6} className="px-6 py-10 text-center text-gray-500">
                  <div className="flex flex-col items-center justify-center">
                    <FileSignature className="w-10 h-10 text-gray-300 mb-2" />
                    <p>No claims found matching your filters.</p>
                  </div>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      
      {/* Pagination Footer */}
      <div className="px-6 py-3 flex items-center justify-between border-t border-gray-200 bg-gray-50">
        <div className="text-sm text-gray-500">
          Showing <span className="font-medium">{filteredClaims.length > 0 ? 1 : 0}</span> to <span className="font-medium">{Math.min(10, filteredClaims.length)}</span> of <span className="font-medium">{filteredClaims.length}</span> results
        </div>
        <div className="flex gap-2">
           <button className="px-3 py-1 border border-gray-300 rounded-md text-sm bg-white hover:bg-gray-50 disabled:opacity-50" disabled>Previous</button>
           <button className="px-3 py-1 border border-gray-300 rounded-md text-sm bg-white hover:bg-gray-50">Next</button>
        </div>
      </div>
    </div>
  );
}

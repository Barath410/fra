"use client";

import { File, Download, CloudDownload, FileCheck, Search, Filter } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const DOCUMENTS = [
  { id: 1, title: "FRA Act 2006 (English)", type: "Act", date: "2006-12-29", size: "2.4 MB" },
  { id: 2, title: "FRA Rules 2012 (Amendment)", type: "Rules", date: "2012-09-06", size: "1.8 MB" },
  { id: 3, title: "Ministry Guidelines on CFR", type: "Guideline", date: "2015-04-12", size: "3.2 MB" },
  { id: 4, title: "FAQs on Forest Rights Act", type: "FAQ", date: "2023-01-10", size: "0.5 MB" },
  { id: 5, title: "Supreme Court Order 2019", type: "Order", date: "2019-02-13", size: "1.1 MB" },
  { id: 6, title: "Tribal Welfare Policy Note", type: "Policy", date: "2024-03-01", size: "4.5 MB" },
];

export default function DocumentsPage() {
  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900">Document Repository</h1>
        <p className="text-gray-500">Access acts, rules, guidelines, and important circulars.</p>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 justify-between bg-white p-4 rounded-lg shadow-sm border">
        <div className="relative w-full sm:w-96">
          <Input placeholder="Search documents..." className="pl-10" />
          <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
        </div>
        <div className="flex gap-2">
            <Select defaultValue="all">
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Filter by Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                <SelectItem value="act">Acts & Rules</SelectItem>
                <SelectItem value="guideline">Guidelines</SelectItem>
              </SelectContent>
            </Select>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {DOCUMENTS.map((doc) => (
          <div key={doc.id} className="group relative flex flex-col justify-between rounded-lg border bg-white p-6 shadow-sm transition-all hover:shadow-md">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className={`rounded-full p-2 ${doc.type === 'Act' ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'}`}>
                  {doc.type === 'Act' ? <FileCheck className="h-6 w-6" /> : <File className="h-6 w-6" />}
                </div>
                <span className="text-xs font-medium text-gray-500 border px-2 py-1 rounded-md">{doc.type}</span>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 line-clamp-2">{doc.title}</h3>
                <p className="text-sm text-gray-500 mt-1">Uploaded: {doc.date}</p>
              </div>
            </div>
            <div className="mt-6 pt-4 border-t flex items-center justify-between">
              <span className="text-xs text-gray-400">{doc.size}</span>
              <Button size="sm" variant="outline" className="gap-2 group-hover:bg-blue-50 group-hover:text-blue-700 group-hover:border-blue-200">
                <Download className="h-4 w-4" />
                Download
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

"use client";

import { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { User, Users, MapPin, FileUp, ArrowRight, Loader2 } from "lucide-react";
import { uploadDocumentRequest, DocumentUploadResult } from "@/lib/document-upload";

export default function NewClaimPage() {
  const [loading, setLoading] = useState(false);
  const [claimType, setClaimType] = useState("Individual");
  const [evidenceFiles, setEvidenceFiles] = useState<File[]>([]);
  const [evidenceStatus, setEvidenceStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
  const [evidenceMessage, setEvidenceMessage] = useState<string | null>(null);
  const [evidenceResults, setEvidenceResults] = useState<DocumentUploadResult[]>([]);
  const evidenceInputRef = useRef<HTMLInputElement | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    if (evidenceFiles.length === 0) {
      alert("Please attach at least one supporting document before submitting.");
      setLoading(false);
      return;
    }
    setEvidenceStatus("uploading");
    setEvidenceMessage(null);
    try {
      const results: DocumentUploadResult[] = [];
      for (const file of evidenceFiles) {
        const result = await uploadDocumentRequest({
          file,
          documentType: claimType === "Community" ? "CFR" : "IFR",
        });
        results.push(result);
      }
      setEvidenceResults(results);
      setEvidenceStatus("success");
      setEvidenceMessage(`Uploaded ${results.length} document${results.length > 1 ? "s" : ""} successfully.`);
      alert("Claim submitted and documents uploaded successfully!");
    } catch (error) {
      setEvidenceStatus("error");
      const message = error instanceof Error ? error.message : "Upload failed";
      setEvidenceMessage(message);
      alert(message);
    } finally {
      setLoading(false);
    }
  };

  const handleEvidenceFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setEvidenceFiles(Array.from(event.target.files));
      setEvidenceStatus("idle");
      setEvidenceMessage(null);
      setEvidenceResults([]);
    }
  };

  return (
    <div className="p-6 max-w-3xl mx-auto space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900">File New Claim</h1>
        <p className="text-gray-500">Submit a new Forest Rights claim (Form A or Form B) for processing.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Claimant Details</CardTitle>
          <CardDescription>Enter the personal details of the claimant or the community representative.</CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-6">
            <div className="space-y-3">
              <Label>Claim Type</Label>
              <RadioGroup defaultValue="Individual" onValueChange={setClaimType} className="flex gap-4">
                <div className="flex items-center space-x-2 border p-3 rounded-lg w-full cursor-pointer hover:bg-gray-50">
                  <RadioGroupItem value="Individual" id="individual" />
                  <Label htmlFor="individual" className="flex items-center gap-2 cursor-pointer">
                    <User className="h-4 w-4" /> Individual Forest Rights (IFR)
                  </Label>
                </div>
                <div className="flex items-center space-x-2 border p-3 rounded-lg w-full cursor-pointer hover:bg-gray-50">
                  <RadioGroupItem value="Community" id="community" />
                  <Label htmlFor="community" className="flex items-center gap-2 cursor-pointer">
                    <Users className="h-4 w-4" /> Community Forest Rights (CFR)
                  </Label>
                </div>
              </RadioGroup>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="name">Full Name of Claimant *</Label>
                <Input id="name" placeholder="As per Aadhar/Voter ID" required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="spouse">Spouse Name</Label>
                <Input id="spouse" placeholder="If applicable" />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="caste">Scheduled Tribe / OTFD *</Label>
                <Select defaultValue="st">
                  <SelectTrigger>
                    <SelectValue placeholder="Select Category" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="st">Scheduled Tribe (ST)</SelectItem>
                    <SelectItem value="otfd">Other Traditional Forest Dweller (OTFD)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="mobile">Mobile Number *</Label>
                <Input id="mobile" placeholder="10 Digit Number" type="tel" required />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="address">Address / Village *</Label>
              <Textarea id="address" placeholder="Village, Panchayat, Block, District" required />
            </div>

            <div className="space-y-4 pt-4 border-t">
              <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                <MapPin className="h-4 w-4" /> Land Details
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="khasra">Khasra No. / Compartment No.</Label>
                  <Input id="khasra" placeholder="e.g. 124/2" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="area">Approx. Area (in acres)</Label>
                  <Input id="area" placeholder="e.g. 2.5" type="number" step="0.01" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="boundary">Boundary Description</Label>
                  <Input id="boundary" placeholder="North: River, South: Tree..." />
                </div>
              </div>
            </div>

            <div className="space-y-4 pt-4 border-t">
              <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                <FileUp className="h-4 w-4" /> Evidence Documents
              </h3>
              <input
                ref={evidenceInputRef}
                className="hidden"
                type="file"
                multiple
                accept="application/pdf,image/*"
                onChange={handleEvidenceFileSelect}
              />
              <div
                className="grid grid-cols-1 gap-4 p-4 border-2 border-dashed rounded-lg bg-gray-50 justify-center text-center cursor-pointer hover:bg-gray-100 transition-colors"
                onClick={() => evidenceInputRef.current?.click()}
              >
                <div className="text-sm text-gray-500">
                  <span className="font-semibold text-blue-600">Click to upload</span> or drag and drop
                  <br />
                  Voter ID, Ration Card, House Tax Receipt, etc.
                </div>
                {evidenceFiles.length > 0 && (
                  <div className="text-xs text-gray-600 space-y-1">
                    {evidenceFiles.map((file) => (
                      <div key={file.name} className="flex items-center justify-between bg-white px-3 py-1.5 rounded-lg border">
                        <span className="truncate pr-2">{file.name}</span>
                        <span className="text-gray-400">{(file.size / (1024 * 1024)).toFixed(1)} MB</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
              {evidenceMessage && (
                <p className={`text-xs ${evidenceStatus === "success" ? "text-emerald-600" : evidenceStatus === "error" ? "text-red-500" : "text-gray-500"}`}>
                  {evidenceMessage}
                </p>
              )}
              {evidenceResults.length > 0 && (
                <div className="rounded-lg bg-emerald-50 p-3 text-xs text-emerald-700 space-y-1">
                  {evidenceResults.map((result) => (
                    <p key={result.document_id}>ID #{result.document_id} · {result.document_type ?? "N/A"} · {result.processing_status}</p>
                  ))}
                </div>
              )}
              <div className="flex items-center space-x-2">
                <Checkbox id="terms" required />
                <label
                  htmlFor="terms"
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                  I certify that the information provided above is true to the best of my knowledge.
                </label>
              </div>
            </div>

          </CardContent>
          <CardFooter className="flex justify-end gap-2 border-t pt-4">
            <Button variant="outline" type="button">Save Draft</Button>
            <Button type="submit" disabled={loading}>
              {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Submit Claim
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}

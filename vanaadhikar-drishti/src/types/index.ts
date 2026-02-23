// ─── Core FRA Domain Types ─────────────────────────────────────────────────

export type ClaimType = "IFR" | "CFR" | "CR";
export type ClaimStatus =
    | "received"
    | "frc-verified"
    | "sdlc-approved"
    | "dlc-approved"
    | "granted"
    | "rejected"
    | "pending"
    | "pending-docs"
    | "under-appeal";

export type StateCode = "MP" | "OD" | "TR" | "TG";

export interface NationalStats {
    totalClaims: number;
    totalGranted: number;
    totalPending: number;
    totalRejected: number;
    totalIFR: number;
    totalCFR: number;
    totalCR: number;
    ifrAreaAcres: number;
    cfrAreaAcres: number;
    crAreaAcres: number;
    totalVillagesCovered: number;
    totalPattas: number;
    totalFRCActive: number;
    saturationPct: number;
}

export interface StateStat {
    id: StateCode;
    name: string;
    slug: string;
    color: string;
    totalClaims: number;
    granted: number;
    pending: number;
    rejected: number;
    ifrArea: number;
    cfrArea: number;
    saturationPct: number;
    districts: number;
    villagesCovered: number;
    tribalGroups: string[];
    pvtgCount: number;
    fireAlerts: number;
    dajguaSaturation: number;
    totalCR?: number;
}

export interface DistrictStat {
    id: string;
    name: string;
    grants: number;
    pending: number;
    rejected: number;
    saturation: number;
}

export interface FRAClaim {
    id: string;
    claimantName: string;
    claimantAadhaar?: string;
    villageName: string;
    villageCode: string;
    gramPanchayat: string;
    block: string;
    district: string;
    state: StateCode;
    claimType: ClaimType;
    formNumber: string; // Form A / B / C
    areaAcres: number;
    surveyKhasraNo?: string;
    claimDate: string;
    verificationDate?: string;
    decisionDate?: string;
    status: ClaimStatus;
    patteNumber?: string;
    patteIssuedDate?: string;
    rejectionReason?: string;
    gpsCoordinates?: { lat: number; lng: number };
    boundaryShapefile?: string; // URL to GeoJSON
    scannedDocUrl?: string;
    ocrExtractedData?: OcrExtraction;
    assignedOfficerId?: string;
    lastUpdated: string;
    tribalGroup?: string;
    isPVTG: boolean;
    notes?: string;
    documents?: Array<{ id: string; name: string; type: string; url: string; fileSize?: string; isVerified?: boolean }>;
    ocrData?: {
        status: string;
        confidence: number;
        extractedFields: Record<string, any>;
        nerEntities?: Array<{ type: string; text: string; confidence: number; verified?: boolean }>;
        flags?: string[];
    };
}

export interface OcrExtraction {
    rawText: string;
    entities: NerEntity[];
    confidence: number;
    modelVersion: string;
    processedAt: string;
    needsHumanReview: boolean;
}

export interface NerEntity {
    type:
    | "CLAIMANT_NAME"
    | "VILLAGE_NAME"
    | "DISTRICT_NAME"
    | "KHASRA_NO"
    | "AREA"
    | "DATE"
    | "CLAIM_ID"
    | "COORDINATES"
    | "STATUS";
    value: string;
    confidence: number;
    startPos: number;
    endPos: number;
}

export interface Village {
    code: string;
    name: string;
    gramPanchayat: string;
    block: string;
    district: string;
    state: StateCode;
    population?: number;
    stPopulation?: number;
    totalHouseholds?: number;
    pvtgPresent: boolean;
    tribalGroups: string[];
    totalClaims: number;
    grantedClaims: number;
    pendingClaims: number;
    rejectedClaims: number;
    ifrGrantedArea: number;
    cfrGrantedArea: number;
    crGrantedArea: number;
    saturationScore: number;
    gpsCenter: { lat: number; lng: number };
    assets: VillageAssets;
    schemeEnrollments: SchemeEnrollment[];
    lastSatelliteUpdate?: string;
}

export interface VillageAssets {
    agriculturalLandAcres: number;
    forestCoverAcres: number;
    waterBodiesCount: number;
    waterBodiesAreaAcres: number;
    homesteadsCount: number;
    ndviScore: number; // 0-1
    ndviTrend: "improving" | "stable" | "declining";
    groundwaterDepthM: number;
    lastUpdated: string;
}

export interface SchemeEnrollment {
    schemeId: string;
    eligibleCount: number;
    enrolledCount: number;
    gapCount: number;
    saturationPct: number;
    lastSynced: string;
}

export interface DSSRecommendation {
    villageCode: string;
    villageName: string;
    district?: string;
    block?: string;
    schemeId: string;
    schemeName: string;
    ministry: string;
    priority: "critical" | "high" | "medium" | "low";
    triggerCondition: string;
    trigger?: string;
    eligibleBeneficiaries: number;
    currentlyEnrolled: number;
    gap: number;
    aiScore: number; // 0-100
    actionRequired: string;
    responsibleOfficer?: string;
    deadline?: string;
}

export interface Officer {
    id: string;
    name: string;
    designation:
    | "mota-nodal"
    | "state-commissioner"
    | "district-collector"
    | "sdlc-officer"
    | "dlc-officer"
    | "range-officer"
    | "frc-member"
    | "ngo-researcher";
    state?: StateCode;
    district?: string;
    block?: string;
    mobile: string;
    email: string;
    lastActive: string;
    totalClaimsHandled: number;
    pendingActions: number;
    gpsLocation?: { lat: number; lng: number };
}

export interface FieldVisitReport {
    id: string;
    claimId: string;
    officerId: string;
    villageName: string;
    visitDate: string;
    gpsLocation: { lat: number; lng: number };
    gpsBoundary?: Array<{ lat: number; lng: number }>;
    gpsVerified?: boolean;
    photos: string[];
    photosUploaded?: boolean;
    notes: string;
    observations?: string;
    communityConsentObtained?: boolean;
    voiceNoteUrl?: string;
    verificationStatus: "confirmed" | "discrepancy" | "not-found" | "pending";
    discrepancyDetails?: string;
    submittedAt: string;
    syncedAt?: string;
}

export interface GrievanceTicket {
    id: string;
    claimantName: string;
    claimId?: string;
    villageName: string;
    village?: string;
    block?: string;
    district: string;
    state: StateCode;
    category:
    | "rejection-dispute"
    | "delay"
    | "document-issue"
    | "officer-conduct"
    | "scheme-non-enrollment"
    | "boundary-dispute"
    | "other";
    description: string;
    status: "open" | "in-review" | "in-progress" | "escalated" | "resolved" | "closed";
    priority: "urgent" | "high" | "medium" | "normal" | "low";
    assignedOfficerId?: string;
    assignedTo?: string;
    createdAt: string;
    filedDate?: string;
    lastUpdated: string;
    daysOpen: number;
    resolution?: string;
    channel: "portal" | "whatsapp" | "helpline" | "email";
    source?: string;
    mobile?: string;
}

export interface DAJGUAIntervention {
    id: string;
    name: string;
    ministry: string;
    targetVillages: number;
    completedVillages: number;
    inProgressVillages: number;
    budgetAllocatedCr: number;
    budgetUtilizedCr: number;
    saturationPct: number;
    state: StateCode;
}

export interface DashboardSummary {
    nationalStats: NationalStats;
    stateStats: StateStat[];
    districtStats: Record<string, DistrictStat[]>;
    claims: FRAClaim[];
    villages: Village[];
    officers: Officer[];
    grievances: GrievanceTicket[];
    datasets: {
        dajguaInterventions: DAJGUAIntervention[];
        dssRecommendations: DSSRecommendation[];
        monthlyProgress: MonthlyProgressReport[];
        forestFireAlerts: ForestFireAlert[];
        fieldVisitReports: FieldVisitReport[];
        ndviTrend: Array<Record<string, number | string>>;
        claimPipeline: Array<{ id: string; label: string; color: string; count: number; labelHi: string }>
    };
}

export interface MonthlyProgressReport {
    month: string;
    year: number;
    state: StateCode;
    claimsReceived: number;
    claimsVerified: number;
    claimsGranted: number;
    claimsRejected: number;
    claimsPending?: number;
    totalPattas: number;
    ifrPattas: number;
    cfrPattas: number;
    crPattas: number;
    ifrAreaAcres: number;
    cfrAreaAcres: number;
    schemesSaturated: number;
}

export interface ForestFireAlert {
    id: string;
    villageName: string;
    district: string;
    state: StateCode;
    isCFRZone: boolean;
    detectedAt: string;
    coordinates: { lat: number; lng: number };
    confidencePct: number;
    areaAffectedHa: number;
    status: "active" | "controlled" | "extinguished";
    alertLevel: "critical" | "high" | "moderate";
    source: "ISRO-FIRMS" | "VIIRS" | "MODIS";
}

export interface MapLayer {
    id: string;
    name: string;
    category: "administrative" | "fra" | "assets" | "schemes" | "alerts" | "environment";
    enabled: boolean;
    opacity: number;
    color?: string;
    description: string;
    source: string;
    lastUpdated?: string;
}

export interface FilterState {
    state?: StateCode;
    district?: string;
    block?: string;
    village?: string;
    claimType?: ClaimType | "all";
    claimStatus?: ClaimStatus | "all";
    tribalGroup?: string;
    dateFrom?: string;
    dateTo?: string;
    isPVTG?: boolean;
}

export interface KPICard {
    title: string;
    value: string | number;
    subtitle?: string;
    change?: number;
    changeLabel?: string;
    icon?: string;
    color?: string;
}

export interface NavigationItem {
    label: string;
    labelHi?: string;
    href: string;
    icon: string;
    badge?: number;
    children?: NavigationItem[];
}

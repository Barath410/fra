export type DocumentUploadResult = {
    document_id: number;
    document_type: string | null;
    processing_status: string;
    template_id: string | null;
    created_at: string;
};

const rawBackendUrl = process.env.NEXT_PUBLIC_BACKEND_URL?.trim();
const normalizedBaseUrl = rawBackendUrl?.replace(/\/$/, "");
export const BACKEND_BASE_URL = normalizedBaseUrl && normalizedBaseUrl.length > 0
    ? normalizedBaseUrl
    : "http://localhost:8000";

export type UploadDocumentParams = {
    file: File;
    documentType?: string;
    language?: string;
    signal?: AbortSignal;
};

const DEFAULT_ERROR_MESSAGE = "Unable to upload document";

export async function uploadDocumentRequest({
    file,
    documentType,
    language,
    signal,
}: UploadDocumentParams): Promise<DocumentUploadResult> {
    const formData = new FormData();
    formData.append("file", file);
    if (documentType) {
        formData.append("document_type", documentType);
    }
    if (language) {
        formData.append("language", language);
    }

    const response = await fetch(`${BACKEND_BASE_URL}/api/documents/upload-document`, {
        method: "POST",
        body: formData,
        signal,
    });

    if (!response.ok) {
        throw new Error(await extractErrorMessage(response));
    }

    return response.json();
}

async function extractErrorMessage(response: Response): Promise<string> {
    try {
        const textPayload = await response.text();
        if (!textPayload) {
            return DEFAULT_ERROR_MESSAGE;
        }
        try {
            const parsed = JSON.parse(textPayload);
            if (parsed?.detail) {
                return typeof parsed.detail === "string" ? parsed.detail : JSON.stringify(parsed.detail);
            }
        } catch {
            // continue and fallback to raw text
        }
        return textPayload;
    } catch {
        return DEFAULT_ERROR_MESSAGE;
    }
}

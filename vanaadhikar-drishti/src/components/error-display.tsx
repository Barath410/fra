/**
 * Error display component
 */

import { AlertTriangle, RefreshCw } from 'lucide-react';

interface ErrorDisplayProps {
    title?: string;
    message: string;
    onRetry?: () => void;
    showRetry?: boolean;
}

export function ErrorDisplay({
    title = 'Error Loading Data',
    message,
    onRetry,
    showRetry = true,
}: ErrorDisplayProps) {
    return (
        <div className="flex flex-col items-center justify-center p-8 bg-red-50 border border-red-200 rounded-lg">
            <AlertTriangle className="w-12 h-12 text-red-600 mb-4" />
            <h3 className="text-lg font-semibold text-red-900 mb-2">{title}</h3>
            <p className="text-red-700 text-center mb-4">{message}</p>
            {showRetry && onRetry && (
                <button
                    onClick={onRetry}
                    className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
                >
                    <RefreshCw size={16} />
                    Retry
                </button>
            )}
        </div>
    );
}

export function ErrorBoundary({
    error,
    onRetry,
}: {
    error: Error | null;
    onRetry?: () => void;
}) {
    if (!error) return null;

    return (
        <ErrorDisplay
            title="Something went wrong"
            message={error.message || 'An unexpected error occurred'}
            onRetry={onRetry}
            showRetry={!!onRetry}
        />
    );
}

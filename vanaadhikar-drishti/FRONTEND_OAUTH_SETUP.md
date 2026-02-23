"""
Frontend OAuth Integration Guide

Complete setup for integrating Google OAuth with Next.js frontend
"""

# =============================================================================
# 1. ENVIRONMENT VARIABLES (.env.local in vanaadhikar-drishti folder)
# =============================================================================

# .env.local
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_API_V1_PREFIX=/api/v1
NEXT_PUBLIC_APP_ENV=development


# =============================================================================
# 2. API CLIENT UTILITY (lib/api-client.ts)
# =============================================================================

# Example implementation:

"""
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
const API_V1 = `${API_BASE_URL}/api/v1`;

const apiClient = axios.create({
  baseURL: API_V1,
  withCredentials: true, // Important: sends cookies automatically
});

// Add JWT token to requests if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  // Get Google login URL
  getLoginUrl: async () => {
    const response = await apiClient.get('/auth/google/login');
    return response.data.auth_url;
  },

  // Get current user profile (requires token)
  getCurrentUser: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  // Logout
  logout: async () => {
    await apiClient.post('/auth/logout');
    localStorage.removeItem('auth_token');
  },
};

export const claimsAPI = {
  // Get all claims (public)
  getClaims: async (state?: string, status?: string) => {
    const response = await apiClient.get('/claims', {
      params: { state, status },
    });
    return response.data;
  },

  // Get single claim (public)
  getClaim: async (claimId: string) => {
    const response = await apiClient.get(`/claims/${claimId}`);
    return response.data;
  },

  // Create claim (requires authentication)
  createClaim: async (data: any) => {
    const response = await apiClient.post('/claims', data);
    return response.data;
  },
};
"""


# =============================================================================
# 3. LOGIN COMPONENT (app/auth/login.tsx)
# =============================================================================

"""
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authAPI } from '@/lib/api-client';

export default function LoginPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGoogleLogin = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Step 1: Get Google login URL from backend
      const loginUrl = await authAPI.getLoginUrl();
      
      // Step 2: Redirect user to Google OAuth
      window.location.href = loginUrl;
    } catch (err) {
      setError('Failed to initiate login');
      console.error(err);
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div className="w-full max-w-md">
        <h1 className="text-3xl font-bold mb-8">Vanaadhikar Drishti</h1>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <button
          onClick={handleGoogleLogin}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          {loading ? 'Signing in...' : 'Sign in with Google'}
        </button>
      </div>
    </div>
  );
}
"""


# =============================================================================
# 4. OAUTH CALLBACK HANDLER (app/auth/callback.tsx)
# =============================================================================

"""
'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

export default function OAuthCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // Backend handles the actual OAuth callback at:
        // GET /api/v1/auth/google/callback?code=<google_code>
        
        // When user authorizes in Google, they're redirected to backend callback
        // Backend returns: { token, user: {...} }
        // Backend also sets auth_token cookie
        
        // If redirected here through frontend route, check for token in localStorage
        const token = localStorage.getItem('auth_token');
        if (token) {
          // User is authenticated
          router.push('/dashboard');
        } else {
          // Frontend redirect without token - shouldn't happen
          setError('Authentication failed');
        }
      } catch (err) {
        setError('Callback processing failed');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    handleCallback();
  }, [router]);

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Processing login...</div>;
  }

  if (error) {
    return <div className="flex items-center justify-center min-h-screen text-red-600">{error}</div>;
  }

  return null;
}
"""


# =============================================================================
# 5. AUTH CONTEXT (lib/auth-context.tsx)
# =============================================================================

"""
'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { authAPI } from '@/lib/api-client';

interface User {
  id: number;
  email: string;
  name: string;
  picture: string | null;
  provider: string;
  last_login: string | null;
  created_at: string;
  updated_at: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Try to get current user on mount
    const fetchUser = async () => {
      try {
        const currentUser = await authAPI.getCurrentUser();
        setUser(currentUser);
      } catch (err) {
        // User not authenticated or token invalid
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  const logout = async () => {
    try {
      await authAPI.logout();
      setUser(null);
    } catch (err) {
      setError('Logout failed');
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, error, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
"""


# =============================================================================
# 6. PROTECTED ROUTE WRAPPER (component/protected-route.tsx)
# =============================================================================

"""
'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth-context';
import { useEffect } from 'react';

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { user, loading, isAuthenticated } = useAuth();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/auth/login');
    }
  }, [loading, isAuthenticated, router]);

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (!isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}

// Usage in page.tsx:
// export default function DashboardPage() {
//   return (
//     <ProtectedRoute>
//       <Dashboard />
//     </ProtectedRoute>
//   );
// }
"""


# =============================================================================
# 7. GOOGLE OAUTH CONFIGURATION
# =============================================================================

"""
IMPORTANT: Configure redirect URI in Google Cloud Console

1. Go to https://console.cloud.google.com
2. Select your project
3. Go to APIs & Services > OAuth 2.0 Client IDs > Web application
4. Add Authorized redirect URIs:
   - http://localhost:8000/api/v1/auth/google/callback (development)
   - https://yourdomain.com/api/v1/auth/google/callback (production)

NOTE: Backend handles the OAuth callback, not the frontend.
The callback URL must point to the backend /api/v1/auth/google/callback endpoint.

Backend will:
1. Exchange authorization code for access token
2. Fetch user profile from Google
3. Create/update user in database
4. Generate JWT token
5. Set auth_token cookie
6. Return token + user data

Frontend then:
1. Gets redirected to callback page OR receives token in response
2. Stores token in localStorage (if not using cookie)
3. Redirects to dashboard
"""


# =============================================================================
# 8. AUTHENTICATION FLOW DIAGRAM
# =============================================================================

"""
┌─────────────────────────────────────────────────────────────────────────┐
│                         GOOGLE OAUTH FLOW                               │
└─────────────────────────────────────────────────────────────────────────┘

1. USER CLICKS "SIGN IN WITH GOOGLE"
   ┌──────────┐
   │ Frontend │─── GET /api/v1/auth/google/login ───┐
   └──────────┘                                      │
                                                     ▼
                                            ┌─────────────────┐
                                            │    Backend      │
                                            │ Returns auth_url│
                                            └─────────────────┘
                                                     │
   ┌──────────┐◀─── Redirect to Google OAuth ─────┐
   │ Frontend │
   └──────────┘

2. GOOGLE AUTHORIZATION
   ┌──────────┐
   │ Frontend │─── User logs in to Google ───┐
   └──────────┘                               │
                                              ▼
                                    Google OAuth Server
                                    User authorizes app
                                              │
   ┌──────────┐◀─── Redirect with code ────┐
   │ Backend  │    /callback?code=XXX
   └──────────┘

3. TOKEN EXCHANGE & USER CREATION
   ┌──────────┐
   │ Backend  │
   └──────────┘
       │
       ├─ Exchange code for Google access token
       ├─ Fetch user profile (email, name, picture)
       ├─ Query/create user in database
       ├─ Generate JWT token
       ├─ Set auth_token cookie
       └─ Return { token, user }

4. FRONTEND RECEIVES TOKEN
   ┌──────────┐
   │ Frontend │◀─── { token, user } ────┐
   └──────────┘                          │
       │                                  │
       ├─ Store token in localStorage
       ├─ Set auth_token cookie (if via backend)
       └─ Redirect to /dashboard

5. SUBSEQUENT API REQUESTS
   ┌──────────┐
   │ Frontend │─── Authorization: Bearer {token} ───┐
   └──────────┘                                     │
                                                    ▼
                                           ┌─────────────────┐
                                           │    Backend      │
                                           │ Verify token    │
                                           │ Fetch user data │
                                           │ Return response │
                                           └─────────────────┘
"""


# =============================================================================
# 9. TESTING THE OAUTH FLOW
# =============================================================================

"""
MANUAL TESTING:

1. Start backend:
   cd backend
   python -m uvicorn app.main:app --reload --port 8000

2. Start frontend:
   cd vanaadhikar-drishti
   npm run dev

3. Visit login page:
   http://localhost:3000/auth/login

4. Click "Sign in with Google"
   - Gets redirected to Google OAuth
   - User authorizes
   - Redirected back to backend callback
   - Backend creates/updates user and returns token
   - Redirected to dashboard

5. Verify in database:
   mysql -u root -pLakpra849@ -h localhost
   USE fra_documents;
   SELECT id, email, name, provider, last_login FROM users;

6. Test protected endpoint with token:
   curl -H "Authorization: Bearer {token}" \\
        http://localhost:8000/api/v1/auth/me

EXPECTED RESPONSE:
{
  "id": 1,
  "email": "user@gmail.com",
  "name": "User Name",
  "picture": "https://lh3.googleusercontent.com/...",
  "provider": "google",
  "last_login": "2026-02-23T10:30:00Z",
  "created_at": "2026-02-23T10:25:00Z",
  "updated_at": "2026-02-23T10:30:00Z"
}
"""

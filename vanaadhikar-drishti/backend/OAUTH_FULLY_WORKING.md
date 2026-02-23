"""
GOOGLE OAUTH - FULLY WORKING IMPLEMENTATION

═════════════════════════════════════════════════════════════════════════════

CREDENTIALS CONFIGURED
─────────────────────────────────────────────────────────────────────────────
✓ Google Client ID: provided via backend/.env (GOOGLE_CLIENT_ID)
✓ Google Client Secret: provided via backend/.env (GOOGLE_CLIENT_SECRET)
✓ Redirect URI: http://localhost:8000/api/v1/auth/google/callback
✓ Database: defined by backend/.env (DATABASE_URL, e.g. mysql+pymysql://user:pass@host:3306/db)
✓ JWT Secret: configured in backend/.env (JWT_SECRET_KEY)

═════════════════════════════════════════════════════════════════════════════

QUICK START
─────────────────────────────────────────────────────────────────────────────

1. START BACKEND:
   cd backend
   python -m uvicorn app.main:app --reload --port 8000
   
   OR
   
   python scripts/start_oauth.py

2. VERIFY SETUP:
   python scripts/check_oauth.py

3. TEST ENDPOINTS:
   curl http://localhost:8000/health
   curl http://localhost:8000/api/v1/auth/google/login
   curl http://localhost:8000/docs  (Swagger UI in browser)

═════════════════════════════════════════════════════════════════════════════

OAUTH FLOW (STEP-BY-STEP)
─────────────────────────────────────────────────────────────────────────────

STEP 1: Get Login URL
───────────────────
GET /api/v1/auth/google/login

Response:
{
  "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=437990075904-...&redirect_uri=http://localhost:8000/api/v1/auth/google/callback&..."
}

STEP 2: User Visits auth_url
──────────────────────────
User is redirected to Google login page
User enters credentials and authorizes app
Google redirects back to: http://localhost:8000/api/v1/auth/google/callback?code=<AUTH_CODE>

STEP 3: Backend Processes Callback
──────────────────────────────────
Endpoint: GET /api/v1/auth/google/callback?code=<code>

Backend:
1. Exchanges code for Google access token
2. Fetches user profile (email, name, picture)
3. Creates new user if first login: INSERT into users table
4. Updates last_login if returning user: UPDATE users SET last_login = NOW()
5. Generates JWT token (12-hour expiration)
6. Sets auth_token cookie (HttpOnly, expires 12 hours)
7. Returns response with token + user data

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@gmail.com",
    "name": "User Name",
    "picture": "https://lh3.googleusercontent.com/..."
  }
}

STEP 4: Use Token for Protected Endpoints
──────────────────────────────────────────

GET /api/v1/auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Response:
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

═════════════════════════════════════════════════════════════════════════════

API ENDPOINTS
─────────────────────────────────────────────────────────────────────────────

PUBLIC ENDPOINTS:
├─ GET  /api/v1/auth/google/login
│  └─ Returns Google OAuth login URL
│
├─ GET  /api/v1/auth/google/callback?code=<code>
│  ├─ Called by Google after user authorization
│  ├─ Creates/updates user in database
│  ├─ Returns JWT token
│  └─ Sets auth_token cookie
│
└─ GET  /api/v1/health
   └─ Backend health check

PROTECTED ENDPOINTS (require JWT token):
├─ GET  /api/v1/auth/me
│  └─ Get current user profile
│
├─ POST /api/v1/auth/logout
│  └─ Logout and clear cookie
│
├─ GET  /api/v1/protected-example/profile
│  ├─ Get user profile (example protected route)
│  └─ Requires authentication
│
├─ GET  /api/v1/protected-example/user-claims
│  ├─ Get user's claims (example protected route)
│  └─ Requires authentication
│
└─ POST /api/v1/claims
   └─ Create new claim (requires authentication)

═════════════════════════════════════════════════════════════════════════════

TESTING
─────────────────────────────────────────────────────────────────────────────

MANUAL TEST WITH CURL:

1. Get login URL:
   curl http://localhost:8000/api/v1/auth/google/login

2. Copy auth_url from response, open in browser:
   (User will be redirected after authorizing)

3. From browser console or response, get the token and use it:
   
   Replace <TOKEN> with actual token from step 2
   
   curl -H "Authorization: Bearer <TOKEN>" \\
        http://localhost:8000/api/v1/auth/me

4. Verify user in database:
   mysql -u root -p<YOUR_DB_PASSWORD> -h localhost -e \\
   "USE fra_documents; SELECT id, email, name, provider, last_login FROM users;"

5. Test protected endpoint:
   curl -H "Authorization: Bearer <TOKEN>" \\
        http://localhost:8000/api/v1/protected-example/profile

TEST WITH SWAGGER UI:
   1. Go to http://localhost:8000/docs
   2. Click "Try it out" on any endpoint
   3. For protected endpoints, click "Authorize" button and paste token

═════════════════════════════════════════════════════════════════════════════

TOKEN AUTHENTICATION METHODS
─────────────────────────────────────────────────────────────────────────────

METHOD 1: Authorization Header (API clients)
─────────────────────────────────────────────
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/auth/me

METHOD 2: Cookie (Browsers automatically)
───────────────────────────────────────────
curl -b "auth_token=<token>" http://localhost:8000/api/v1/auth/me

Both methods supported simultaneously.

═════════════════════════════════════════════════════════════════════════════

DATABASE OPERATIONS
─────────────────────────────────────────────────────────────────────────────

FIRST LOGIN:
1. Google OAuth code → access token exchange ✓
2. GET https://www.googleapis.com/oauth2/v2/userinfo ✓
3. SELECT * FROM users WHERE email = ? → NULL (new user)
4. INSERT INTO users (email, name, picture, provider, last_login) VALUES (...)
   → Creates new user with last_login = NOW()
5. Generate JWT token ✓
6. Return token + user data ✓

SUBSEQUENT LOGIN:
1. Google OAuth code → access token exchange ✓
2. GET user profile from Google ✓
3. SELECT * FROM users WHERE email = ? → Returns user (exists)
4. UPDATE users SET last_login = NOW() WHERE id = ? 
   → Updates last_login timestamp (tracks user activity)
5. Generate new JWT token ✓
6. Return token + updated user data ✓

PROTECTED API REQUEST:
1. Extract token from: Authorization header OR auth_token cookie
2. Decode JWT using settings.jwt_secret_key
3. Extract user_id from JWT payload: payload["sub"]
4. SELECT * FROM users WHERE id = ? → Get user from database
5. Return 401 if user not found
6. Proceed with request using user context ✓

═════════════════════════════════════════════════════════════════════════════

SECURITY FEATURES
─────────────────────────────────────────────────────────────────────────────

✓ JWT Tokens
  - Signed with 256-bit secret key
  - Algorithm: HS256 (HMAC SHA-256)
  - Expiration: 12 hours
  - Invalid after expiration

✓ Cookies
  - HttpOnly: Cannot be accessed by JavaScript (XSS protection)
  - Secure: Only sent over HTTPS (in production)
  - SameSite=Lax: CSRF protection
  - MaxAge: 12 hours

✓ Token Validation
  - Every protected request requires valid JWT
  - User verified in database on each request
  - Invalid tokens rejected with 401

✓ Google OAuth
  - No passwords stored locally
  - Uses industry-standard OAuth 2.0
  - Users control account in Google

✓ Database
  - User email is UNIQUE
  - Passwords never stored
  - All fields properly indexed

═════════════════════════════════════════════════════════════════════════════

CONFIGURATION FILES
─────────────────────────────────────────────────────────────────────────────

.env file (backend/):
- GOOGLE_CLIENT_ID: <your Google OAuth client ID> (set in Google Cloud console)
- GOOGLE_CLIENT_SECRET: <your Google OAuth client secret> (store securely)
- GOOGLE_REDIRECT_URI: http://localhost:8000/api/v1/auth/google/callback
- JWT_SECRET_KEY: <strong random value for signing JWTs>
- DATABASE_URL: mysql+pymysql://<user>:<password>@<host>:3306/<database>

app/core/config.py:
- Loads from .env file
- Settings class with all OAuth configuration

requirements.txt:
- python-jose: JWT token generation and verification
- cryptography: Encryption for JWT
- email-validator: Email validation in schemas
- httpx: HTTP client for Google API calls

═════════════════════════════════════════════════════════════════════════════

FRONTEND INTEGRATION
─────────────────────────────────────────────────────────────────────────────

See: FRONTEND_OAUTH_SETUP.md for complete Next.js integration guide

Quick summary:
1. Call GET /api/v1/auth/google/login to get auth_url
2. Redirect user to auth_url
3. After authorization, user is redirected back to your app
4. Store token in localStorage or cookie
5. Use token in Authorization header for subsequent API calls
6. Implement auth context and protected routes

═════════════════════════════════════════════════════════════════════════════

TROUBLESHOOTING
─────────────────────────────────────────────────────────────────────────────

Problem: "Invalid auth code" error
Solution: Code expired or already used. Request new code from /auth/google/login

Problem: "Missing email in Google profile"
Solution: User didn't grant email permission. Check Google OAuth scopes.

Problem: User created but last_login not updating
Solution: Ensure UPDATE query is executing. Check database permissions.

Problem: Token works for /auth/me but fails for protected endpoints
Solution: Token might be expired. Request new token via OAuth callback.

Problem: "Cannot find user" error  
Solution: User table doesn't exist or token user_id is invalid.
Check: mysql -e "USE fra_documents; SELECT * FROM users LIMIT 1;"

Problem: Backend can't connect to Google
Solution: firewall/proxy blocking googleapis.com. Check network.

═════════════════════════════════════════════════════════════════════════════

FILES CREATED/MODIFIED
─────────────────────────────────────────────────────────────────────────────

CREATED:
✓ app/schemas/auth.py — JWT and response schemas
✓ app/services/auth_service.py — Auth business logic
✓ app/api/dependencies.py — Auth middleware
✓ app/api/endpoints/protected_example.py — Protected route examples
✓ scripts/check_oauth.py — OAuth configuration checker
✓ scripts/start_oauth.py — Start backend with OAuth
✓ scripts/verify_oauth.py — Full OAuth verification
✓ AUTH_IMPLEMENTATION.md — Detailed auth documentation
✓ FRONTEND_OAUTH_SETUP.md — Frontend integration guide

MODIFIED:
✓ .env — Added Google credentials & JWT secret
✓ app/core/config.py — Defaults for OAuth settings
✓ app/api/endpoints/auth.py — Full OAuth implementation
✓ app/api/endpoints/claims.py — Example protected routes
✓ requirements.txt — Added OAuth dependencies

═════════════════════════════════════════════════════════════════════════════

DEPLOYMENT CHECKLIST
─────────────────────────────────────────────────────────────────────────────

Before going to production:

[ ] Change JWT_SECRET_KEY to strong random value
[ ] Set APP_ENV=production in .env
[ ] Update Google OAuth redirect_uri to production domain
[ ] Add production domain to Google OAuth authorized redirects
[ ] Enable HTTPS (Secure flag on cookies)
[ ] Test OAuth flow end-to-end
[ ] Test protected endpoints with valid token
[ ] Test protected endpoints without token (should get 401)
[ ] Monitor user creation in database
[ ] Check last_login updates on repeat logins
[ ] Set up logging for OAuth errors
[ ] Monitor database connections

═════════════════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(__doc__)

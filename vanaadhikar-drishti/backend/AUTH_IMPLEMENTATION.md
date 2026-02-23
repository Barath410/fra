"""
GOOGLE OAUTH PRODUCTION FLOW - IMPLEMENTATION SUMMARY

Files Created/Modified:
1. app/schemas/auth.py - JWT and response schemas
2. app/services/auth_service.py - Auth business logic
3. app/api/dependencies.py - Auth middleware/dependencies
4. app/api/endpoints/auth.py - OAuth endpoints (updated)
5. app/api/endpoints/protected_example.py - Protected route examples

ENDPOINTS:
"""

# =============================================================================
# 1. OAuth FLOW ENDPOINTS
# =============================================================================

"""
GET /api/v1/auth/google/login
Response: {"auth_url": "https://accounts.google.com/o/oauth2/v2/auth?..."}

GET /api/v1/auth/google/callback?code=<google_auth_code>
Response: {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "name": "User Name",
        "picture": "https://..."
    }
}
Side Effect: Sets auth_token cookie (HttpOnly, max_age=12hrs)

POST /api/v1/auth/logout
Response: {"message": "Logout successful"}
Side Effect: Clears auth_token cookie
"""

# =============================================================================
# 2. PROTECTED ENDPOINTS (REQUIRE AUTHENTICATION)
# =============================================================================

"""
GET /api/v1/auth/me
Authorization: Bearer <jwt_token>
OR
Cookie: auth_token=<jwt_token>

Response: {
    "id": 1,
    "email": "user@example.com",
    "name": "User Name",
    "picture": "https://...",
    "provider": "google",
    "last_login": "2026-02-23T10:30:00Z",
    "created_at": "2026-02-20T08:15:00Z",
    "updated_at": "2026-02-23T10:30:00Z"
}
"""

# =============================================================================
# 3. USAGE IN PROTECTED ROUTES
# =============================================================================

"""
from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from app.api.dependencies import CurrentUser
from app.db.session import get_db

router = APIRouter()

@router.get("/my-data")
def get_my_data(
    current_user: CurrentUser,  # Automatically validates JWT token
    db: Annotated[Session, Depends(get_db)],
):
    # current_user is UserResponse with: id, email, name, picture, provider, last_login, created_at, updated_at
    return {
        "user_id": current_user.id,
        "user_email": current_user.email,
        "your_data": []
    }

@router.post("/create-something")
def create_something(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
    payload: SomeSchema,
):
    # Only authenticated users can access
    return {"created_by": current_user.id, "data": payload}
"""

# =============================================================================
# 4. REQUEST EXAMPLES
# =============================================================================

"""
STEP 1: Get login URL
curl -X GET http://localhost:8000/api/v1/auth/google/login

STEP 2: User authorizes via Google, redirect to callback with code
(Happens in browser)

STEP 3: Exchange code for token
curl -X GET "http://localhost:8000/api/v1/auth/google/callback?code=<code>"
Returns: token + user data + sets auth_token cookie

STEP 4: Use token in subsequent requests
Option A - Authorization header:
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/auth/me

Option B - Cookie (automatic from browser):
curl -b "auth_token=<token>" http://localhost:8000/api/v1/auth/me

Option C - Protected endpoint:
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/protected-example/profile

STEP 5: Logout
curl -X POST http://localhost:8000/api/v1/auth/logout
"""

# =============================================================================
# 5. TOKEN VERIFICATION FLOW
# =============================================================================

"""
Token Extraction (app/api/dependencies.py):
1. Check Authorization header for "Bearer <token>"
2. Fallback to auth_token cookie
3. Raise 401 if no token found

Token Validation (app/services/auth_service.py):
1. Decode JWT using settings.jwt_secret_key
2. Extract user_id from payload["sub"]
3. Query User from database
4. Return user or raise 401

Both mechanisms (header + cookie) are supported for flexibility:
- Browser clients: Cookie (automatic)
- API clients: Authorization header
"""

# =============================================================================
# 6. DATABASE OPERATIONS
# =============================================================================

"""
FIRST LOGIN:
- User submits Google auth code
- Code exchanged for Google access token
- Google profile fetched (email, name, picture)
- db.query(User).filter(User.email == email).first() returns None
- New User record created with: email, name, picture, provider='google', last_login=NOW()
- JWT token generated
- Set cookie

SUBSEQUENT LOGINS:
- User submits Google auth code
- db.query(User).filter(User.email == email).first() returns existing User
- User.last_login updated to NOW()
- JWT token generated
- Set cookie

GET /auth/me:
- Extract token from header/cookie
- Decode JWT
- db.query(User).filter(User.id == decoded_user_id).first()
- Return UserResponse with all fields
"""

# =============================================================================
# 7. SECURITY FEATURES
# =============================================================================

"""
✓ JWT tokens signed with settings.jwt_secret_key (HS256)
✓ Token expiration: 12 hours
✓ HttpOnly cookies prevent XSS access
✓ Secure flag in production (controlled by app_env)
✓ SameSite=Lax prevents CSRF attacks
✓ Token validation on every protected endpoint
✓ User existence verified on each request
✓ last_login timestamp tracks activity
✓ Google OAuth reduces password management burden
"""

# =============================================================================
# 8. CONFIGURATION REQUIRED
# =============================================================================

"""
In .env file:
GOOGLE_CLIENT_ID=<from Google Cloud Console>
GOOGLE_CLIENT_SECRET=<from Google Cloud Console>
JWT_SECRET_KEY=<strong random string>
APP_ENV=production (or development)

In backend/app/core/config.py (already set):
- google_redirect_uri: http://localhost:8000/api/v1/auth/google/callback
- jwt_algorithm: HS256
- jwt defaults to 12-hour expiration
"""

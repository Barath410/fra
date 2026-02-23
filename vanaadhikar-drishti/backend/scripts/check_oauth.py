#!/usr/bin/env python
"""Quick OAuth Configuration Check"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings

print("\n" + "="*70)
print("OAUTH CONFIGURATION")
print("="*70)

print(f"\n✓ Google Client ID: {settings.google_client_id[:30]}...")
print(f"✓ Google Client Secret: {settings.google_client_secret[:10]}...{settings.google_client_secret[-5:]}")
print(f"✓ Redirect URI: {settings.google_redirect_uri}")
print(f"✓ JWT Secret Key: {settings.jwt_secret_key[:20]}...")
print(f"✓ JWT Algorithm: {settings.jwt_algorithm}")
print(f"✓ Database URL: {settings.database_url.split('@')[1]}")

print("\n✓ All OAuth credentials loaded successfully!")
print("\n" + "="*70)
print("NEXT STEPS")
print("="*70)

print("""
1. Start the backend:
   cd backend
   python -m uvicorn app.main:app --reload --port 8000

2. You should see OAuth endpoints:
   GET  /api/v1/auth/google/login
   GET  /api/v1/auth/google/callback
   GET  /api/v1/auth/me
   POST /api/v1/auth/logout

3. Test the endpoints:
   curl http://localhost:8000/api/v1/auth/google/login
   
   Should return:
   {
     "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=437990075904-...",
     ...
   }

4. Click the auth_url or use Google OAuth:
   - User will be redirected to Google login
   - After authorization, redirected to /api/v1/auth/google/callback?code=XXX
   - Backend exchanges code for token
   - User created in database (fra_documents.users table)
   - JWT token returned + auth_token cookie set

5. Use token to access protected endpoints:
   curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/auth/me
   
   Should return user profile with all fields

6. Check database for created user:
   mysql -u root -pLakpra849@ -h localhost -e "USE fra_documents; SELECT id, email, name, last_login FROM users;"
""")

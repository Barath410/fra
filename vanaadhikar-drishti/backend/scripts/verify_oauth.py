"""
OAuth Setup Verification Script

Test that Google OAuth is properly configured and working.
Run this after starting the backend: python scripts/verify_oauth.py
"""

import os
import sys
import httpx
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.services.auth_service import AuthService
from app.models.user import User


def test_configuration():
    """Verify OAuth configuration is loaded."""
    print("\n" + "="*70)
    print("OAUTH CONFIGURATION VERIFICATION")
    print("="*70)

    checks = {
        "Google Client ID": settings.google_client_id,
        "Google Client Secret": settings.google_client_secret[:10] + "***" if settings.google_client_secret else None,
        "Google Redirect URI": settings.google_redirect_uri,
        "JWT Secret Key": settings.jwt_secret_key[:10] + "***" if settings.jwt_secret_key else None,
        "JWT Algorithm": settings.jwt_algorithm,
        "Database URL": settings.database_url.replace(settings.database_url.split("@")[0].split("://")[1], "***"),
    }

    for key, value in checks.items():
        status = "✓" if value and value != "None***" else "✗"
        print(f"{status} {key:.<40} {value}")

    required_fields = [settings.google_client_id, settings.google_client_secret, settings.jwt_secret_key]
    if all(required_fields):
        print("\n✓ All configuration fields are set")
        return True
    else:
        print("\n✗ Missing required configuration fields")
        return False


def test_jwt_token_generation():
    """Verify JWT token generation works."""
    print("\n" + "="*70)
    print("JWT TOKEN GENERATION TEST")
    print("="*70)

    try:
        # Create a mock user object
        class MockUser:
            id = 1
            email = "test@example.com"
            name = "Test User"

        user = MockUser()
        token, expires_in = AuthService.generate_access_token(user)

        print(f"✓ Token generated successfully")
        print(f"  Token (first 50 chars): {token[:50]}...")
        print(f"  Expiration: {expires_in} seconds ({expires_in / 3600} hours)")

        # Test token verification
        payload = AuthService.verify_token(token)
        print(f"✓ Token verified successfully")
        print(f"  Payload: {json.dumps(payload, indent=2, default=str)}")

        return True
    except Exception as e:
        print(f"✗ JWT token generation failed: {str(e)}")
        return False


def test_backend_connectivity():
    """Test that backend is running and accessible."""
    print("\n" + "="*70)
    print("BACKEND CONNECTIVITY TEST")
    print("="*70)

    try:
        with httpx.Client(timeout=5) as client:
            response = client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("✓ Backend is running and responsive")
                print(f"  Health check response: {response.json()}")
                return True
            else:
                print(f"✗ Backend returned status {response.status_code}")
                return False
    except Exception as e:
        print(f"✗ Cannot connect to backend: {str(e)}")
        print("  Make sure backend is running: cd backend && python -m uvicorn app.main:app --reload --port 8000")
        return False


def test_oauth_endpoints():
    """Test OAuth endpoints are accessible."""
    print("\n" + "="*70)
    print("OAUTH ENDPOINTS TEST")
    print("="*70)

    try:
        with httpx.Client(timeout=5) as client:
            # Test login URL generation
            response = client.get("http://localhost:8000/api/v1/auth/google/login")
            if response.status_code == 200:
                data = response.json()
                if "auth_url" in data:
                    print("✓ GET /api/v1/auth/google/login is working")
                    print(f"  Auth URL: {data['auth_url'][:60]}...")
                else:
                    print("✗ Login URL endpoint returned unexpected response")
                    return False
            else:
                print(f"✗ Login URL endpoint returned status {response.status_code}")
                return False

            # Test /me endpoint without token (should fail)
            response = client.get("http://localhost:8000/api/v1/auth/me")
            if response.status_code == 401:
                print("✓ GET /api/v1/auth/me correctly requires authentication")
                print(f"  Error message: {response.json()['detail']}")
            else:
                print(f"✗ /me endpoint should require auth but returned {response.status_code}")
                return False

        return True
    except Exception as e:
        print(f"✗ OAuth endpoints test failed: {str(e)}")
        return False


def print_next_steps():
    """Print instructions for next steps."""
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("""
1. AUTHENTICATE WITH GOOGLE:
   - Visit: http://localhost:3000/auth/login (or navigate in frontend)
   - Or directly: GET http://localhost:8000/api/v1/auth/google/login
   - Copy the auth_url and open in browser
   - Authorize with your Google account

2. GOOGLE WILL REDIRECT TO:
   http://localhost:8000/api/v1/auth/google/callback?code=<AUTH_CODE>
   
   This endpoint will:
   ✓ Get user profile from Google
   ✓ Create/update user in database (fra_documents.users table)
   ✓ Generate JWT token
   ✓ Set auth_token cookie
   ✓ Redirect or return token + user data

3. USE TOKEN IN SUBSEQUENT REQUESTS:
   
   Option A - Authorization header:
   curl -H "Authorization: Bearer <token>" \\
        http://localhost:8000/api/v1/auth/me
   
   Option B - With cookie:
   curl -b "auth_token=<token>" \\
        http://localhost:8000/api/v1/auth/me

4. VERIFY USER CREATED IN DATABASE:
   mysql -u root -pLakpra849@ -h localhost -e \\
   "USE fra_documents; SELECT id, email, name, last_login FROM users;"

5. TEST PROTECTED ENDPOINTS:
   curl -H "Authorization: Bearer <token>" \\
        http://localhost:8000/api/v1/protected-example/profile
        
   Returns current user profile with all fields.
""")


def main():
    """Run all verification tests."""
    print("\n" * 2)
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "VANAADHIKAR DRISHTI - OAUTH SETUP VERIFICATION" + " "*7 + "║")
    print("╚" + "="*68 + "╝")

    results = {
        "Configuration": test_configuration(),
        "JWT Token Generation": test_jwt_token_generation(),
        "Backend Connectivity": test_backend_connectivity(),
        "OAuth Endpoints": test_oauth_endpoints(),
    }

    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:.<50} {test_name}")

    if all(results.values()):
        print("\n✓ All tests passed! OAuth is fully configured and ready.")
        print_next_steps()
        return 0
    else:
        print("\n✗ Some tests failed. Check configuration and try again.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

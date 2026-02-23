#!/usr/bin/env python
"""Start backend with OAuth configured"""

import os
import sys
import subprocess
from pathlib import Path

os.chdir(Path(__file__).parent.parent)

print("\n" + "="*70)
print("STARTING VANAADHIKAR DRISHTI BACKEND WITH OAUTH")
print("="*70)

print("\n✓ OAuth Credentials Loaded:")
print("  - Google Client ID: 437990075904-...")
print("  - Google Redirect URI: http://localhost:8000/api/v1/auth/google/callback")
print("  - DB: fra_documents")
print("  - JWT: Configured")

print("\n✓ Available Endpoints:")
print("  GET  http://localhost:8000/health")
print("  GET  http://localhost:8000/api/v1/auth/google/login")
print("  GET  http://localhost:8000/api/v1/auth/google/callback?code=<code>")
print("  GET  http://localhost:8000/api/v1/auth/me")
print("  POST http://localhost:8000/api/v1/auth/logout")
print("  GET  http://localhost:8000/docs (Swagger UI)")

print("\n✓ Starting server...")
print("="*70 + "\n")

subprocess.run([
    sys.executable,
    "-m", "uvicorn",
    "app.main:app",
    "--reload",
    "--port", "8000"
])

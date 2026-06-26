"""
Security Configuration for Flask Server
This file contains security settings to control network access
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Network Security Configuration
NETWORK_SECURITY = {
    # Set to 'true' to allow external network access (NOT RECOMMENDED for development)
    'allow_external_access': os.environ.get('ALLOW_EXTERNAL_ACCESS', 'false').lower() == 'true',
    
    # Allowed hosts (localhost variants)
    'allowed_hosts': [
        '127.0.0.1',      # IPv4 localhost
        'localhost',      # Hostname localhost
        '::1',           # IPv6 localhost
    ],
    
    # Blocked IP addresses (add IPs to block here)
    'blocked_ips': set(),
    
    # Require HTTPS (set to 'true' in production)
    'require_https': os.environ.get('REQUIRE_HTTPS', 'false').lower() == 'true',
    
    # Server binding configuration
    'host': '127.0.0.1',  # Only bind to localhost
    'port': 5000,         # Default port
    
    # CORS origins — configurable via CORS_ORIGINS env var (comma-separated)
    'allowed_origins': [
        origin.strip()
        for origin in os.environ.get(
            'CORS_ORIGINS',
            'http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000'
        ).split(',')
        if origin.strip()
    ]
}

# Security Headers
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains' if NETWORK_SECURITY['require_https'] else None,
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
}

def get_server_config():
    """Get server configuration based on environment"""
    if NETWORK_SECURITY['allow_external_access']:
        print("⚠️  WARNING: External access is enabled. This is not recommended for development.")
        return {
            'host': '0.0.0.0',
            'port': NETWORK_SECURITY['port']
        }
    else:
        print("✅ Server configured for localhost-only access")
        return {
            'host': NETWORK_SECURITY['host'],
            'port': NETWORK_SECURITY['port']
        }

def print_security_status():
    """Print current security configuration"""
    print("\n🔒 Security Configuration:")
    print(f"   External Access: {'❌ BLOCKED' if not NETWORK_SECURITY['allow_external_access'] else '⚠️  ALLOWED'}")
    print(f"   Server Host: {NETWORK_SECURITY['host']}")
    print(f"   Server Port: {NETWORK_SECURITY['port']}")
    print(f"   HTTPS Required: {'✅ Yes' if NETWORK_SECURITY['require_https'] else '❌ No'}")
    print(f"   Allowed Origins: {NETWORK_SECURITY['allowed_origins']}")
    print() 
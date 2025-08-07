# Security Configuration for Flask Server

## Overview
This Flask server has been configured with security measures to prevent unauthorized access from external networks while allowing local development.

## Security Features Implemented

### 1. Localhost-Only Access
- **Default Configuration**: Server only binds to `127.0.0.1` (localhost)
- **External Access**: Blocked by default
- **Network Isolation**: Prevents access from other devices on the same network

### 2. Environment-Based Configuration
You can control security settings using environment variables:

```bash
# Block external access (default - RECOMMENDED)
ALLOW_EXTERNAL_ACCESS=false

# Allow external access (NOT RECOMMENDED for development)
ALLOW_EXTERNAL_ACCESS=true

# Require HTTPS (set to true in production)
REQUIRE_HTTPS=false
```

### 3. CORS Protection
- Only allows requests from localhost origins:
  - `http://localhost:5173`
  - `http://127.0.0.1:5173`
  - `http://localhost:3000`
  - `http://127.0.0.1:3000`

### 4. Request Filtering
- All requests are checked for localhost origin
- External requests are blocked with 403 Forbidden response
- Detailed logging of blocked attempts

## How to Use

### For Development (Recommended)
```bash
# Start server with default security (localhost only)
python app.py
```

The server will:
- Bind to `127.0.0.1:5000`
- Only accept connections from localhost
- Block all external network access
- Display security status on startup

### For Production (If External Access Needed)
```bash
# Set environment variable to allow external access
export ALLOW_EXTERNAL_ACCESS=true
python app.py
```

**⚠️ WARNING**: Only enable external access if absolutely necessary and ensure proper firewall rules are in place.

## Security Status Display
When you start the server, you'll see a security status like this:
```
🔒 Security Configuration:
   External Access: ❌ BLOCKED
   Server Host: 127.0.0.1
   Server Port: 5000
   HTTPS Required: ❌ No
   Allowed Origins: ['http://localhost:5173', 'http://127.0.0.1:5173', ...]

🚀 Starting Flask server on 127.0.0.1:5000
🔒 Access URL: http://localhost:5000
```

## Network Access Control

### What's Blocked
- All external IP addresses
- Requests from other devices on the same network
- Requests with non-localhost Host headers

### What's Allowed
- Localhost connections (`127.0.0.1`)
- Localhost hostname (`localhost`)
- IPv6 localhost (`::1`)

## Additional Security Measures

### 1. Rate Limiting
- Built-in rate limiting to prevent abuse
- Configurable limits per IP address

### 2. File Upload Security
- File size limits
- File type validation
- Secure filename handling

### 3. Authentication
- JWT token-based authentication
- Token expiration and revocation
- User session management

## Troubleshooting

### If You Can't Access the Server
1. Make sure you're using `http://localhost:5000` (not your IP address)
2. Check that the server is running on `127.0.0.1:5000`
3. Verify no firewall is blocking localhost connections

### If You Need External Access (Advanced)
1. Set `ALLOW_EXTERNAL_ACCESS=true` in environment
2. Configure your firewall to allow port 5000
3. Use a reverse proxy (nginx) for additional security
4. Enable HTTPS with `REQUIRE_HTTPS=true`

## Best Practices

1. **Always use localhost-only access for development**
2. **Never expose development servers to the internet**
3. **Use environment variables for configuration**
4. **Regularly update dependencies**
5. **Monitor server logs for security events**
6. **Use HTTPS in production**

## Emergency Override
If you need to temporarily allow external access for testing:

```python
# In app.py, temporarily change:
app.run(host='0.0.0.0', port=5000, debug=True)

# Remember to change it back to:
app.run(host='127.0.0.1', port=5000, debug=True)
```

**⚠️ Remember to revert this change immediately after testing!** 
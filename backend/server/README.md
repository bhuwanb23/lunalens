# LunaLens Backend Server

This is the Flask backend server for the LunaLens application, providing authentication and API endpoints.

## Features

- **JWT Authentication**: Secure token-based authentication
- **Multiple User Support**: Demo users with different roles and permissions
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Configuration Management**: Environment-based configuration
- **Security**: Token validation and session management

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the environment template and configure your settings:

```bash
cp env_template.txt .env
```

Edit `.env` file with your configuration:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Security Keys (CHANGE THESE IN PRODUCTION!)
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 3. Run the Server

```bash
cd server
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Authentication

#### POST `/login`
Login with mission credentials.

**Request:**
```json
{
  "missionId": "isro123",
  "accessCode": "moon@2024"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful!",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "missionId": "isro123",
    "name": "ISRO Mission Control",
    "role": "admin",
    "permissions": ["dashboard", "analytics", "settings"]
  }
}
```

#### POST `/logout`
Logout and invalidate token.

**Request:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Logout successful!"
}
```

#### POST `/verify-token`
Verify if a token is valid.

**Request:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:**
```json
{
  "valid": true,
  "user": {
    "missionId": "isro123",
    "name": "ISRO Mission Control",
    "role": "admin",
    "permissions": ["dashboard", "analytics", "settings"]
  }
}
```

## Demo Users

The system includes demo users for testing:

| Mission ID | Access Code | Name | Role | Permissions |
|------------|-------------|------|------|-------------|
| `isro123` | `moon@2024` | ISRO Mission Control | admin | dashboard, analytics, settings |
| `mission001` | `lunar@2024` | Lunar Mission Team | user | dashboard, analytics |
| `research002` | `research@2024` | Research Team | researcher | dashboard, analytics, data_export |

## Configuration

### Development
- Debug mode enabled
- CORS allows all origins
- Detailed error messages

### Production
- Debug mode disabled
- Secure session cookies
- Environment variables for secrets
- Restricted CORS origins

## Security Features

- **JWT Tokens**: Secure, time-limited authentication tokens
- **Token Revocation**: Active token tracking for logout
- **CORS Protection**: Controlled cross-origin access
- **Environment Variables**: Secure credential management
- **Session Security**: HTTP-only, secure cookies

## File Structure

```
server/
├── app.py              # Main Flask application
├── config.py           # Configuration management
├── env_template.txt    # Environment variables template
├── README.md          # This file
└── uploads/           # File upload directory (auto-created)
```

## Future Enhancements

- Database integration for user management
- Role-based access control
- Rate limiting
- File upload endpoints
- Lunar data analysis APIs
- Real-time WebSocket connections

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure frontend URL is in CORS_ORIGINS
2. **Token Expired**: Tokens expire after 24 hours
3. **Invalid Credentials**: Check demo user credentials
4. **Port Already in Use**: Change port in app.py or kill existing process

### Logs

Check console output for detailed error messages and request logs. 
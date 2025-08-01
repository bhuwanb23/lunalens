# 🚀 LunaLens Backend - Quick Start

## 📋 Login Credentials

| Mission ID | Access Code | Name | Role |
|------------|-------------|------|------|
| `isro123` | `moon@2024` | ISRO Mission Control | Admin |
| `mission001` | `lunar@2024` | Lunar Mission Team | User |
| `research002` | `research@2024` | Research Team | Researcher |
| `test001` | `test@2024` | Test User | User |

## 🛠️ Setup Instructions

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup Environment (Optional)
```bash
cd server
cp env_template.txt .env
```

### 3. Run the Server
```bash
cd server
python app.py
```

## 🌐 Access Points

- **Backend Homepage**: http://localhost:5000
- **API Endpoints**: 
  - POST http://localhost:5000/login
  - POST http://localhost:5000/logout
  - POST http://localhost:5000/verify-token

## 🧪 Test the API

### Test Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"missionId": "isro123", "accessCode": "moon@2024"}'
```

### Expected Response
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

## 📁 File Structure

```
server/
├── app.py              # Main Flask application (single file)
├── templates/
│   └── home.html      # Backend homepage template
├── env_template.txt    # Environment variables template (optional)
├── QUICK_START.md     # This file
└── README.md          # Detailed documentation
```

## 🔧 Troubleshooting

### Common Issues

1. **Port 5000 already in use**
   ```bash
   # Kill existing process
   lsof -ti:5000 | xargs kill -9
   ```

2. **Missing dependencies**
   ```bash
   pip install flask flask-cors PyJWT python-dotenv
   ```

3. **Environment file missing**
   ```bash
   cp env_template.txt .env
   ```

4. **CORS errors from frontend**
   - Ensure frontend is running on http://localhost:5173
   - Check CORS_ORIGINS in .env file

## 🎯 Next Steps

1. Start the backend server
2. Start the frontend server (`cd frontend/website && npm run dev`)
3. Navigate to http://localhost:5173
4. Login with any of the credentials above
5. Explore the dashboard!

## 📞 Support

If you encounter issues:
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure .env file is properly configured
4. Check that ports 5000 and 5173 are available 
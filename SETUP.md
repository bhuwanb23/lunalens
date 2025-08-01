# LunaLens Setup Guide

This guide will help you set up the complete LunaLens application with authentication and dashboard functionality.

## Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- npm or yarn

## Quick Start

### 1. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend/website

# Install dependencies
npm install

# Install React Router (if not already installed)
npm install react-router-dom

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Navigate to server directory
cd server

# Start the backend server
python app.py
```

The backend will be available at `http://localhost:5000`

## Authentication Flow

### Demo Credentials

Use these credentials to test the application:

| Mission ID | Access Code | Role |
|------------|-------------|------|
| `isro123` | `moon@2024` | Admin |
| `mission001` | `lunar@2024` | User |
| `research002` | `research@2024` | Researcher |

### How It Works

1. **Login Page**: User enters Mission ID and Access Code
2. **Authentication**: Backend validates credentials and returns JWT token
3. **Dashboard Access**: Frontend stores token and redirects to dashboard
4. **Protected Routes**: Dashboard is only accessible with valid token
5. **Logout**: Token is invalidated and user is redirected to login

## File Structure

```
lunalens/
├── frontend/
│   └── website/
│       ├── src/
│       │   ├── pages/
│       │   │   ├── login/          # Login page components
│       │   │   └── dashboard/      # Dashboard components
│       │   └── App.jsx            # Main app with routing
│       └── package.json
├── backend/
│   ├── server/
│   │   ├── app.py                 # Flask backend (single file)
│   │   ├── templates/
│   │   │   └── home.html         # Backend homepage
│   │   └── env_template.txt      # Environment template (optional)
│   └── requirements.txt
└── SETUP.md                       # This file
```

## Features

### Frontend
- ✅ React + Vite setup
- ✅ Tailwind CSS styling
- ✅ React Router for navigation
- ✅ Protected routes
- ✅ Login form with validation
- ✅ Dashboard with lunar analysis UI
- ✅ Responsive design
- ✅ Dark space theme

### Backend
- ✅ Flask API server
- ✅ JWT authentication
- ✅ Multiple user support
- ✅ CORS configuration
- ✅ Environment-based config
- ✅ Token validation
- ✅ Secure logout

## Development

### Frontend Development

```bash
cd frontend/website
npm run dev
```

### Backend Development

```bash
cd backend/server
python run.py
```

### Environment Variables

Create a `.env` file in `backend/server/` with:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
CORS_ORIGINS=http://localhost:5173
```

## Testing the Application

1. **Start both servers** (frontend and backend)
2. **Navigate to** `http://localhost:5173`
3. **Login** with demo credentials
4. **Explore** the dashboard features
5. **Test logout** functionality

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure backend is running on port 5000
   - Check CORS_ORIGINS in backend config

2. **Login Fails**
   - Verify backend is running
   - Check demo credentials
   - Check browser console for errors

3. **Dashboard Not Loading**
   - Check if token is stored in localStorage
   - Verify authentication state

4. **Port Conflicts**
   - Frontend: Change port in vite.config.js
   - Backend: Change port in run.py

### Debug Mode

Enable debug mode for detailed error messages:

```bash
# Frontend
npm run dev

# Backend
FLASK_DEBUG=True python run.py
```

## Production Deployment

### Frontend
- Build with `npm run build`
- Deploy to static hosting (Netlify, Vercel, etc.)
- Update API endpoints to production URLs

### Backend
- Use production WSGI server (Gunicorn)
- Set environment variables for secrets
- Use production database
- Enable HTTPS

## Security Notes

- Change default secrets in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Implement rate limiting
- Add input validation
- Use secure session management

## Next Steps

- [ ] Add database integration
- [ ] Implement real lunar data APIs
- [ ] Add file upload functionality
- [ ] Create user management system
- [ ] Add real-time features
- [ ] Implement role-based access control 
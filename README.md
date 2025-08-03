# 🌙 LunaLens - Lunar Analysis Platform

<div align="center">

![LunaLens](https://img.shields.io/badge/LunaLens-Lunar%20Analysis-blue?style=for-the-badge&logo=moon)
![React](https://img.shields.io/badge/React-18+-blue?style=for-the-badge&logo=react)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-API-red?style=for-the-badge&logo=flask)
![Vite](https://img.shields.io/badge/Vite-Build-orange?style=for-the-badge&logo=vite)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-38B2AC?style=for-the-badge&logo=tailwind-css)

<br>

<div style="background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 20px; margin: 25px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">

# 🚀 **Advanced Lunar Analysis & Detection Platform**

*A comprehensive full-stack application for lunar terrain analysis, boulder detection, and geospatial processing with advanced authentication and real-time dashboard capabilities.*

</div>

<br>

[![Stars](https://img.shields.io/github/stars/your-repo/lunalens?style=social)](https://github.com/your-repo/lunalens)
[![Forks](https://img.shields.io/github/forks/your-repo/lunalens?style=social)](https://github.com/your-repo/lunalens)
[![Issues](https://img.shields.io/github/issues/your-repo/lunalens)](https://github.com/your-repo/lunalens/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/your-repo/lunalens)](https://github.com/your-repo/lunalens/pulls)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🌟 **Platform Overview**

<div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🎯 **Core Capabilities**

<table>
<tr>
<td align="center" width="50%">

#### 🌙 **Lunar Analysis**
- 🗺️ **QGIS Integration**: Advanced geospatial processing
- 🔍 **Boulder Detection**: AI-powered object detection
- 📊 **Terrain Analysis**: Comprehensive lunar mapping
- 🎨 **Visualization**: Real-time data visualization

</td>
<td align="center" width="50%">

#### 🔐 **Authentication System**
- 🛡️ **JWT Security**: Secure token-based authentication
- 👥 **Multi-User Support**: Role-based access control
- 🔄 **Session Management**: Persistent user sessions
- 🚪 **Protected Routes**: Secure dashboard access

</td>
</tr>
<tr>
<td align="center" width="50%">

#### 💻 **Modern Frontend**
- ⚡ **React 18+**: Latest React features
- 🎨 **Tailwind CSS**: Beautiful responsive design
- 🚀 **Vite Build**: Lightning-fast development
- 📱 **Mobile Responsive**: Perfect on all devices

</td>
<td align="center" width="50%">

#### 🔧 **Robust Backend**
- 🐍 **Python Flask**: RESTful API server
- 🔌 **CORS Support**: Cross-origin resource sharing
- 📊 **Data Processing**: Real-time analysis
- 🛡️ **Security**: Production-ready security

</td>
</tr>
</table>

</div>

---

## 🚀 **Quick Start Guide**

<div style="background: linear-gradient(45deg, #ff6b35, #f7931e); padding: 20px; border-radius: 15px; margin: 20px 0;">

### ⚡ **Prerequisites**

- 🖥️ **Node.js** (v16 or higher)
- 🐍 **Python** (v3.8 or higher)
- 📦 **npm** or **yarn**

</div>

### 🎯 **Step 1: Frontend Setup**

<div style="background: linear-gradient(45deg, #4facfe, #00f2fe); padding: 15px; border-radius: 10px; margin: 10px 0;">

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

🌐 **Frontend will be available at**: `http://localhost:5173`

</div>

### 🔧 **Step 2: Backend Setup**

<div style="background: linear-gradient(45deg, #a8edea, #fed6e3); padding: 15px; border-radius: 10px; margin: 10px 0;">

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

🔌 **Backend will be available at**: `http://localhost:5000`

</div>

---

## 🔐 **Authentication System**

<div style="background: linear-gradient(45deg, #ff9a9e, #fecfef); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🎯 **Demo Credentials**

<table>
<tr>
<th>🚀 Mission ID</th>
<th>🔑 Access Code</th>
<th>👤 Role</th>
<th>🎯 Access Level</th>
</tr>
<tr>
<td><code>isro123</code></td>
<td><code>moon@2024</code></td>
<td>👑 Admin</td>
<td>🟢 Full Access</td>
</tr>
<tr>
<td><code>mission001</code></td>
<td><code>lunar@2024</code></td>
<td>👤 User</td>
<td>🟡 Standard Access</td>
</tr>
<tr>
<td><code>research002</code></td>
<td><code>research@2024</code></td>
<td>🔬 Researcher</td>
<td>🔵 Research Access</td>
</tr>
</table>

### 🔄 **Authentication Flow**

<div style="background: linear-gradient(45deg, #667eea, #764ba2); padding: 15px; border-radius: 10px; margin: 10px 0;">

1. 🚪 **Login Page**: User enters Mission ID and Access Code
2. 🔐 **Authentication**: Backend validates credentials and returns JWT token
3. 🎯 **Dashboard Access**: Frontend stores token and redirects to dashboard
4. 🛡️ **Protected Routes**: Dashboard is only accessible with valid token
5. 🚪 **Logout**: Token is invalidated and user is redirected to login

</div>

</div>

---

## 📁 **Project Architecture**

<div style="background: linear-gradient(45deg, #ffecd2, #fcb69f); padding: 20px; border-radius: 15px; margin: 20px 0;">

```
🌙 lunalens/
├── 🎨 frontend/
│   └── 🌐 website/
│       ├── 📁 src/
│       │   ├── 📁 pages/
│       │   │   ├── 🚪 login/          # Login page components
│       │   │   └── 📊 dashboard/      # Dashboard components
│       │   └── 🚀 App.jsx            # Main app with routing
│       └── 📦 package.json
├── 🔧 backend/
│   ├── 🗺️ detection_qgis/           # QGIS lunar analysis
│   │   └── 📁 processed/             # Analysis modules
│   ├── 🪨 boulder_detection/         # AI boulder detection
│   │   ├── 🎯 detector.py           # Main detection logic
│   │   ├── 👁️ gradcam.py           # Grad-CAM visualization
│   │   ├── 🤖 ml_models.py          # Model loading
│   │   └── 🧠 vit_model.pth         # Vision Transformer model
│   ├── 🖥️ server/
│   │   ├── 🚀 app.py                # Flask backend
│   │   ├── 📄 templates/
│   │   │   └── 🏠 home.html         # Backend homepage
│   │   └── 📝 env_template.txt      # Environment template
│   └── 📋 requirements.txt
└── 📖 README.md                     # This documentation
```

</div>

---

## ✨ **Features**

<div style="background: linear-gradient(45deg, #a8edea, #fed6e3); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🎨 **Frontend Features**

<table>
<tr>
<td align="center" width="50%">

#### ⚡ **Modern Technology Stack**
- ✅ **React 18+**: Latest React features and hooks
- ✅ **Vite Build**: Lightning-fast development server
- ✅ **Tailwind CSS**: Beautiful responsive design
- ✅ **React Router**: Seamless navigation

</td>
<td align="center" width="50%">

#### 🎯 **User Experience**
- ✅ **Protected Routes**: Secure dashboard access
- ✅ **Login Form**: Validation and error handling
- ✅ **Responsive Design**: Perfect on all devices
- ✅ **Dark Space Theme**: Beautiful lunar aesthetic

</td>
</tr>
</table>

### 🔧 **Backend Features**

<table>
<tr>
<td align="center" width="50%">

#### 🛡️ **Security & Authentication**
- ✅ **JWT Authentication**: Secure token-based auth
- ✅ **Multi-User Support**: Role-based access control
- ✅ **CORS Configuration**: Cross-origin support
- ✅ **Environment Config**: Flexible deployment

</td>
<td align="center" width="50%">

#### 🌙 **Lunar Analysis**
- ✅ **QGIS Integration**: Advanced geospatial processing
- ✅ **Boulder Detection**: AI-powered object detection
- ✅ **Real-time Processing**: Live data analysis
- ✅ **Data Visualization**: Interactive charts and maps

</td>
</tr>
</table>

</div>

---

## 🛠️ **Development Guide**

<div style="background: linear-gradient(45deg, #667eea, #764ba2); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🎨 **Frontend Development**

```bash
cd frontend/website
npm run dev
```

**Features:**
- ⚡ **Hot Reload**: Instant code updates
- 🎨 **Tailwind CSS**: Utility-first styling
- 📱 **Responsive Design**: Mobile-first approach
- 🔍 **Dev Tools**: React Developer Tools integration

### 🔧 **Backend Development**

```bash
cd backend/server
python run.py
```

**Features:**
- 🔄 **Auto-reload**: Flask development server
- 🐛 **Debug Mode**: Detailed error messages
- 📊 **API Testing**: Built-in testing endpoints
- 🔍 **Logging**: Comprehensive request logging

### ⚙️ **Environment Configuration**

Create a `.env` file in `backend/server/` with:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
CORS_ORIGINS=http://localhost:5173
```

</div>

---

## 🧪 **Testing the Application**

<div style="background: linear-gradient(45deg, #ff9a9e, #fecfef); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🚀 **Step-by-Step Testing**

1. **🚀 Start Both Servers**
   ```bash
   # Terminal 1: Frontend
   cd frontend/website && npm run dev
   
   # Terminal 2: Backend
   cd backend/server && python app.py
   ```

2. **🌐 Navigate to Application**
   - Open browser to `http://localhost:5173`

3. **🔐 Login with Demo Credentials**
   - Use any of the provided demo accounts
   - Test different user roles

4. **📊 Explore Dashboard Features**
   - Navigate through different sections
   - Test responsive design
   - Check authentication state

5. **🚪 Test Logout Functionality**
   - Verify token invalidation
   - Test protected route access

### 🎯 **Testing Checklist**

- ✅ **Authentication Flow**: Login/logout works correctly
- ✅ **Protected Routes**: Dashboard only accessible with valid token
- ✅ **Responsive Design**: Works on mobile and desktop
- ✅ **API Integration**: Backend communication functional
- ✅ **Error Handling**: Graceful error display
- ✅ **Session Management**: Persistent login state

</div>

---

## 🔧 **Troubleshooting**

<div style="background: linear-gradient(45deg, #ff6b6b, #ee5a24); padding: 20px; border-radius: 15px; margin: 20px 0;">

### ❌ **Common Issues & Solutions**

#### 🌐 **CORS Errors**
- **Problem**: Frontend can't connect to backend
- **Solution**: Ensure backend is running on port 5000
- **Check**: CORS_ORIGINS configuration in backend

#### 🔐 **Login Failures**
- **Problem**: Authentication not working
- **Solution**: Verify backend is running and credentials are correct
- **Check**: Browser console for error messages

#### 📊 **Dashboard Issues**
- **Problem**: Dashboard not loading after login
- **Solution**: Check localStorage for JWT token
- **Check**: Authentication state management

#### 🔌 **Port Conflicts**
- **Problem**: Ports already in use
- **Solution**: Change ports in configuration files
- **Frontend**: Modify `vite.config.js`
- **Backend**: Modify `run.py`

### 🐛 **Debug Mode**

Enable detailed debugging:

```bash
# Frontend Debug
npm run dev

# Backend Debug
FLASK_DEBUG=True python run.py
```

### 📊 **Performance Monitoring**

- 🔍 **Frontend**: React Developer Tools
- 📊 **Backend**: Flask debug mode
- 🌐 **Network**: Browser Network tab
- 🗄️ **Storage**: Browser Application tab

</div>

---

## 🚀 **Production Deployment**

<div style="background: linear-gradient(45deg, #4facfe, #00f2fe); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🎨 **Frontend Deployment**

```bash
# Build for production
npm run build

# Deploy to static hosting
# - Netlify
# - Vercel
# - GitHub Pages
# - AWS S3
```

**Configuration:**
- 📝 **Environment Variables**: Set production API endpoints
- 🔒 **HTTPS**: Enable secure connections
- 📊 **Analytics**: Add monitoring tools
- 🚀 **CDN**: Use content delivery network

### 🔧 **Backend Deployment**

```bash
# Production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Configuration:**
- 🔐 **Environment Variables**: Set production secrets
- 🛡️ **HTTPS**: Enable SSL/TLS
- 📊 **Database**: Use production database
- 🔄 **Load Balancing**: Multiple server instances

### 🛡️ **Security Checklist**

- ✅ **Change Default Secrets**: Update all default passwords
- ✅ **Environment Variables**: Use secure secret management
- ✅ **HTTPS Only**: Enable SSL/TLS encryption
- ✅ **Rate Limiting**: Implement API rate limiting
- ✅ **Input Validation**: Sanitize all user inputs
- ✅ **Session Security**: Secure session management

</div>

---

## 🔮 **Future Roadmap**

<div style="background: linear-gradient(45deg, #a8edea, #fed6e3); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🎯 **Planned Features**

<table>
<tr>
<td align="center" width="50%">

#### 📊 **Data & Analytics**
- [ ] **Database Integration**: PostgreSQL/MongoDB
- [ ] **Real Lunar APIs**: NASA/ESA data integration
- [ ] **File Upload**: Bulk data processing
- [ ] **Real-time Features**: WebSocket integration

</td>
<td align="center" width="50%">

#### 👥 **User Management**
- [ ] **User Registration**: Self-service signup
- [ ] **Role Management**: Advanced access control
- [ ] **Profile Management**: User preferences
- [ ] **Team Collaboration**: Multi-user projects

</td>
</tr>
<tr>
<td align="center" width="50%">

#### 🌙 **Lunar Analysis**
- [ ] **3D Visualization**: Three.js integration
- [ ] **Advanced AI**: More detection models
- [ ] **Historical Data**: Temporal analysis
- [ ] **Export Features**: PDF/Excel reports

</td>
<td align="center" width="50%">

#### 🚀 **Performance**
- [ ] **Caching**: Redis integration
- [ ] **CDN**: Global content delivery
- [ ] **Optimization**: Code splitting and lazy loading
- [ ] **Monitoring**: Application performance monitoring

</td>
</tr>
</table>

</div>

---

## 🤝 **Contributing**

<div style="background: linear-gradient(45deg, #ff9a9e, #fecfef); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🚀 **How to Contribute**

1. 🍴 **Fork the repository**
2. 🌿 **Create a feature branch**
3. 🔧 **Make your changes**
4. 🧪 **Add tests if applicable**
5. 📝 **Update documentation**
6. 🔄 **Submit a pull request**

### 📋 **Development Guidelines**

- 📝 **Code Style**: Follow project conventions
- 🧪 **Testing**: Add tests for new features
- 📚 **Documentation**: Update README and comments
- 🔍 **Code Review**: All changes require review
- 🚀 **Performance**: Optimize for speed and efficiency

### 🎯 **Areas for Contribution**

- 🌙 **Lunar Analysis**: QGIS and geospatial features
- 🤖 **AI/ML**: Boulder detection and analysis
- 🎨 **Frontend**: React components and UI/UX
- 🔧 **Backend**: API development and optimization
- 📊 **Data**: Database and data processing
- 🧪 **Testing**: Unit and integration tests

</div>

---

## 📄 **License**

<div style="background: linear-gradient(45deg, #667eea, #764ba2); padding: 15px; border-radius: 10px; margin: 10px 0;">

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🙏 **Acknowledgments**

<div style="background: linear-gradient(45deg, #ffecd2, #fcb69f); padding: 20px; border-radius: 15px; margin: 20px 0;">

### 🛠️ **Core Technologies**
- 🎨 **React** by Meta for frontend framework
- 🐍 **Python** for backend development
- 🔥 **Flask** for API server
- ⚡ **Vite** for build tooling
- 🎨 **Tailwind CSS** for styling

### 🌙 **Lunar Science**
- 🚀 **NASA** for lunar data and research
- 🌍 **ESA** for space exploration initiatives
- 🔬 **Academic researchers** for lunar geology studies
- 🗺️ **QGIS** for geospatial processing

### 🤖 **AI/ML Technologies**
- 🎯 **YOLO** by Ultralytics for object detection
- 🧠 **Vision Transformer** by Google Research
- 👁️ **Grad-CAM** for model interpretability
- 🔥 **PyTorch** for deep learning

</div>

---

<div align="center">

## 🌙 **Happy Lunar Analysis!** 🚀

*LunaLens provides comprehensive lunar terrain analysis and detection capabilities using advanced AI/ML techniques and modern web technologies.*

<br>

[![Made with Love](https://img.shields.io/badge/Made%20with-Love-red?style=for-the-badge)](https://github.com/your-repo/lunalens)
[![Powered by React](https://img.shields.io/badge/Powered%20by-React-blue?style=for-the-badge)](https://reactjs.org/)
[![Lunar Science](https://img.shields.io/badge/Lunar-Science-purple?style=for-the-badge)](https://github.com/your-repo/lunalens)

</div>

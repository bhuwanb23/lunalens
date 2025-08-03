# 🌙 LunaLens

<div align="center">

![LunaLens](https://img.shields.io/badge/LunaLens-Lunar%20Analysis-blue?style=for-the-badge&logo=moon)
![React](https://img.shields.io/badge/React-18+-blue?style=for-the-badge&logo=react)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-API-red?style=for-the-badge&logo=flask)
![Vite](https://img.shields.io/badge/Vite-Build-orange?style=for-the-badge&logo=vite)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-38B2AC?style=for-the-badge&logo=tailwind-css)

<br>

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 25px; margin: 30px 0; box-shadow: 0 15px 35px rgba(0,0,0,0.3);">

# 🚀 **Advanced Lunar Analysis Platform**

*A comprehensive full-stack application for lunar terrain analysis, boulder detection, and geospatial processing with advanced authentication and real-time dashboard capabilities.*

</div>

<br>

[![Stars](https://img.shields.io/github/stars/your-repo/lunalens?style=social)](https://github.com/your-repo/lunalens)
[![Forks](https://img.shields.io/github/forks/your-repo/lunalens?style=social)](https://github.com/your-repo/lunalens)
[![Issues](https://img.shields.io/github/issues/your-repo/lunalens)](https://github.com/your-repo/lunalens/issues)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🌟 **What is LunaLens?**

<div style="background: linear-gradient(45deg, #667eea, #764ba2); padding: 25px; border-radius: 20px; margin: 25px 0;">

LunaLens is a **comprehensive lunar analysis platform** that combines advanced AI/ML techniques with modern web technologies to provide real-time lunar surface analysis, boulder detection, and geospatial processing capabilities.

### 🎯 **Key Features**
- 🌙 **Lunar Terrain Analysis** - Advanced QGIS integration
- 🤖 **AI-Powered Detection** - Boulder and crater detection
- 🔐 **Secure Authentication** - JWT-based user management
- 📊 **Real-time Dashboard** - Interactive analytics and visualization
- 📱 **Responsive Design** - Perfect on all devices

</div>

---

## 🚀 **Quick Start**

<div style="background: linear-gradient(45deg, #ff6b35, #f7931e); padding: 25px; border-radius: 20px; margin: 25px 0;">

### ⚡ **Prerequisites**
- 🖥️ **Node.js** (v16+)
- 🐍 **Python** (v3.8+)
- 📦 **npm** or **yarn**

### 🎯 **Installation**

```bash
# Clone the repository
git clone https://github.com/your-repo/lunalens.git
cd lunalens

# Frontend Setup
cd frontend/website
npm install
npm run dev

# Backend Setup (in new terminal)
cd backend/server
pip install -r requirements.txt
python setup_database.py
python app.py
```

🌐 **Frontend**: `http://localhost:5173` | 🔌 **Backend**: `http://localhost:5000`

</div>

---

## 🔐 **Demo Access**

<div style="background: linear-gradient(45deg, #ff9a9e, #fecfef); padding: 25px; border-radius: 20px; margin: 25px 0;">

| 🚀 Mission ID | 🔑 Access Code | 👤 Role |
|---------------|----------------|---------|
| `isro123` | `moon@2024` | 👑 Admin |
| `mission001` | `lunar@2024` | 👤 User |
| `research002` | `research@2024` | 🔬 Researcher |

</div>

---

## 🏗️ **Architecture**

<div style="background: linear-gradient(45deg, #4facfe, #00f2fe); padding: 25px; border-radius: 20px; margin: 25px 0;">

### 🎨 **Frontend**
- ⚛️ **React 18+** with modern hooks
- ⚡ **Vite** for lightning-fast builds
- 🎨 **Tailwind CSS** for beautiful styling
- 📱 **Responsive** design for all devices

### 🔧 **Backend**
- 🐍 **Python Flask** RESTful API
- 🗄️ **SQLAlchemy** ORM with SQLite
- 🔐 **JWT Authentication** system
- 🤖 **AI/ML** integration for detection

### 🌙 **Analysis**
- 🗺️ **QGIS** geospatial processing
- 🎯 **YOLO** object detection
- 🧠 **Vision Transformer** validation
- 📊 **Real-time** analytics

</div>

---

## 📊 **Features Overview**

<div style="background: linear-gradient(45deg, #a8edea, #fed6e3); padding: 25px; border-radius: 20px; margin: 25px 0;">

<table>
<tr>
<td align="center" width="50%">

### 🔐 **Authentication**
- 🛡️ JWT-based security
- 👥 Multi-user support
- 🔄 Session management
- 🚪 Protected routes

</td>
<td align="center" width="50%">

### 🌙 **Lunar Analysis**
- 🗺️ QGIS integration
- 🔍 Boulder detection
- 📊 Terrain mapping
- 🎨 Data visualization

</td>
</tr>
<tr>
<td align="center" width="50%">

### 📱 **User Experience**
- 🎨 Dark space theme
- 📱 Mobile responsive
- ⚡ Fast loading
- 🎯 Intuitive UI

</td>
<td align="center" width="50%">

### 🔧 **Development**
- ⚡ Hot reload
- 🐛 Debug tools
- 📦 Easy deployment
- 🧪 Testing support

</td>
</tr>
</table>

</div>

---

## 🚀 **Deployment**

<div style="background: linear-gradient(45deg, #ffecd2, #fcb69f); padding: 25px; border-radius: 20px; margin: 25px 0;">

### 🎨 **Frontend**
```bash
npm run build
# Deploy to Netlify, Vercel, or GitHub Pages
```

### 🔧 **Backend**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 🐳 **Docker**
```dockerfile
# Frontend
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 80
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "80"]
```

</div>

---

## 🔧 **Troubleshooting**

<div style="background: linear-gradient(45deg, #ff6b6b, #ee5a24); padding: 25px; border-radius: 20px; margin: 25px 0;">

### ❌ **Common Issues**

| Problem | Solution |
|---------|----------|
| 🌐 CORS Errors | Check backend port 5000 |
| 🔐 Login Fails | Verify demo credentials |
| 📊 Dashboard Issues | Check JWT token |
| 🔌 Port Conflicts | Change ports in config |

### 🐛 **Debug Mode**
```bash
# Frontend
npm run dev

# Backend
FLASK_DEBUG=True python app.py
```

</div>

---

## 🤝 **Contributing**

<div style="background: linear-gradient(45deg, #667eea, #764ba2); padding: 25px; border-radius: 20px; margin: 25px 0;">

1. 🍴 **Fork the repository**
2. 🌿 **Create a feature branch**
3. 🔧 **Make your changes**
4. 🧪 **Add tests**
5. 📝 **Update documentation**
6. 🔄 **Submit a pull request**

### 🎯 **Areas for Contribution**
- 🌙 **Lunar Analysis** - QGIS and geospatial features
- 🤖 **AI/ML** - Boulder detection and analysis
- 🎨 **Frontend** - React components and UI/UX
- 🔧 **Backend** - API development and optimization

</div>

---

## 📄 **License**

<div style="background: linear-gradient(45deg, #ff9a9e, #fecfef); padding: 20px; border-radius: 15px; margin: 20px 0;">

This project is licensed under the **MIT License**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🙏 **Acknowledgments**

<div style="background: linear-gradient(45deg, #ffecd2, #fcb69f); padding: 25px; border-radius: 20px; margin: 25px 0;">

- 🎨 **React** by Meta
- 🐍 **Python** & **Flask**
- 🗺️ **QGIS** for geospatial processing
- 🎯 **YOLO** by Ultralytics
- 🧠 **Vision Transformer** by Google Research
- 🚀 **NASA** & **ESA** for lunar data

</div>

---

<div align="center">

## 🌙 **Happy Lunar Analysis!** 🚀

*LunaLens - Advanced lunar terrain analysis with AI-powered detection and modern web technologies.*

<br>

[![Made with Love](https://img.shields.io/badge/Made%20with-Love-red?style=for-the-badge)](https://github.com/your-repo/lunalens)
[![Powered by React](https://img.shields.io/badge/Powered%20by-React-blue?style=for-the-badge)](https://reactjs.org/)
[![Lunar Science](https://img.shields.io/badge/Lunar-Science-purple?style=for-the-badge)](https://github.com/your-repo/lunalens)

</div>

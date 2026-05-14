# 🌙 LunaLens - Advanced Lunar Analysis Platform

<div align="center">

![LunaLens](https://img.shields.io/badge/LunaLens-Lunar%20Analysis-blue?style=for-the-badge&logo=moon)
![React](https://img.shields.io/badge/React-18+-blue?style=for-the-badge&logo=react)
![Python](https://img.shields.io/badge/Python-3.9+-green?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-API-red?style=for-the-badge&logo=flask)
![YOLO](https://img.shields.io/badge/YOLO-v8-red?style=for-the-badge&logo=yolo)
![QGIS](https://img.shields.io/badge/QGIS-Geospatial-3ba63c?style=for-the-badge&logo=qgis)

<br>

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 25px; margin: 30px 0; box-shadow: 0 15px 35px rgba(0,0,0,0.3);">

# 🚀 **Comprehensive Lunar Surface Analysis Platform**

*A full-stack application combining AI-powered boulder detection, QGIS-based terrain risk analysis, and modern web technologies for lunar exploration and research.*

</div>

<br>

[![Stars](https://img.shields.io/github/stars/bhuwanb23/lunalens?style=social)](https://github.com/bhuwanb23/lunalens)
[![Forks](https://img.shields.io/github/forks/bhuwanb23/lunalens?style=social)](https://github.com/bhuwanb23/lunalens)
[![Issues](https://img.shields.io/github/issues/bhuwanb23/lunalens)](https://github.com/bhuwanb23/lunalens/issues)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

</div>

---

## 🌟 **What is LunaLens?**

<div style="background: linear-gradient(45deg, #667eea, #764ba2); padding: 25px; border-radius: 20px; margin: 25px 0;">

LunaLens is a **comprehensive lunar analysis platform** that integrates advanced AI/ML techniques with geospatial processing to provide real-time lunar surface analysis capabilities.

### 🎯 **Core Capabilities**
- 🤖 **AI-Powered Boulder Detection** - YOLOv8 + Vision Transformer with enhanced sensitivity
- 🗺️ **QGIS Terrain Risk Analysis** - Multi-parameter risk assessment (slope, aspect, roughness, etc.)
- 🔐 **Secure Authentication** - JWT-based user management with role-based access
- 📊 **Real-time Dashboard** - Interactive analytics and visualization
- 📱 **Modern Web Interface** - React frontend with responsive design
- 🎨 **Clean Visualizations** - Publication-ready detection overlays

</div>

---

## 🏗️ **Architecture Overview**

<div style="background: linear-gradient(45deg, #4facfe, #00f2fe); padding: 25px; border-radius: 20px; margin: 25px 0;">

### 🎨 **Frontend** (`frontend/website/`)
- ⚛️ **React 18+** with modern hooks and routing
- ⚡ **Vite** for lightning-fast development
- 🎨 **Tailwind CSS** for beautiful styling
- 📱 **Responsive design** for all devices
- 🔐 **Protected routes** with JWT authentication

### 🔧 **Backend** (`backend/server/`)
- 🐍 **Python Flask** RESTful API
- 🗄️ **SQLAlchemy ORM** with SQLite database
- 🔐 **JWT Authentication** system
- 📁 **File upload/management** with secure serving
- 📝 **Comprehensive logging** and analytics

### 🪨 **Boulder Detection** (`backend/boulder_detection/`)
- 🎯 **YOLOv8** primary detection with enhanced multi-threshold pipeline
- 🧠 **Vision Transformer** fallback for low-confidence detections
- 📏 **Physical measurements** (diameter, volume, circularity, elongation)
- 🎨 **Grad-CAM visualization** for interpretability
- 🔍 **Small-object recovery** for improved recall
- 📊 **Built-in evaluation** tools and metrics

### 🌙 **QGIS Analysis** (`detection_qgis/`)
- 🗺️ **QGIS integration** for geospatial processing
- 📊 **Multi-parameter risk analysis** (slope, aspect, hillshade, roughness, etc.)
- 🧮 **Weighted composite risk** scoring (0-100 scale)
- 📈 **Real-time expressions** for QGIS Raster Calculator
- 📄 **Comprehensive reporting** (JSON + human-readable)

</div>

## ISRO BAH 2025 Final Selected PPT
Click the link to download the PPT 
[View the PDF](./Bharatiya%20Antariksh%20Hackathon%202025%20Idea%20Submission.pdf)

---

## 🚀 **Quick Start**

<div style="background: linear-gradient(45deg, #ff6b35, #f7931e); padding: 25px; border-radius: 20px; margin: 25px 0;">

### ⚡ **Prerequisites**
- 🖥️ **Node.js** (v16+)
- 🐍 **Python** (v3.9+)
- 🗺️ **QGIS 3.x** (optional, for terrain analysis)
- 📦 **npm** or **yarn**

### 🎯 **Installation**

```bash
# 1) Clone the repository
git clone https://github.com/bhuwanb23/lunalens.git
cd lunalens

# 2) Frontend setup
cd frontend/website
cp .env.example .env          # adjust VITE_API_URL if your backend isn't on :5000
npm install
npm run dev

# 3) Backend setup (in a new terminal, from the repo root)
cd backend
pip install -r requirements.txt
cd server
cp env.example .env           # set SECRET_KEY / JWT_SECRET_KEY before deploying
python setup_database.py      # creates SQLite DB and seeds demo users
python app.py
```

🌐 **Frontend**: `http://localhost:5173` | 🔌 **Backend**: `http://localhost:5000`

> **Note:** Boulder detection requires two model files (`best.pt`, `vit_model.pth`) that are *not* committed to the repo — see the [Model Files](#-model-files) section below. The server will still start and the QGIS / analytics endpoints will work without them; only `/api/boulder/*` will return `503` until the models are present.

### 🔐 **Demo Access**
| 🚀 Mission ID | 🔑 Access Code | 👤 Role |
|---------------|----------------|---------|
| `isro123` | `isro123@2024` | 👑 Admin |
| `mission001` | `mission001@2024` | 👤 User |
| `research002` | `research002@2024` | 🔬 Researcher |
| `test001` | `test001@2024` | 🧪 Test User |

> Access codes follow the pattern `<missionId>@2024`. Change them before deploying — see [backend/server/database.py](backend/server/database.py) and [backend/server/app.py](backend/server/app.py).

</div>

---

## 📦 **Model Files**

The boulder-detection pipeline needs two model artefacts that are **not** stored in git (they're large and gitignored):

| File | Path | Purpose |
|------|------|---------|
| `best.pt` | `backend/boulder_detection/best.pt` | YOLOv8 weights (primary detector) |
| `vit_model.pth` | `backend/boulder_detection/vit_model.pth` | Vision Transformer weights (fallback validator) |

You have three options:

1. **Train from scratch** — see [`backend/boulder_detection/lunalena_yolo_train.py`](backend/boulder_detection/lunalena_yolo_train.py). Set `ROBOFLOW_API_KEY` in your environment before running.
2. **Download the pre-trained release artefacts** from this repo's GitHub Releases page (once published) and drop them into `backend/boulder_detection/`.
3. **Skip them** — the rest of the platform (QGIS terrain risk, analytics, dashboards) works without the boulder models. `/api/boulder/status` will report `models_loaded: false`.

---

## 🪨 **Boulder Detection Features**

<div style="background: linear-gradient(45deg, #a8edea, #fed6e3); padding: 25px; border-radius: 20px; margin: 25px 0;">

### 🤖 **AI Models**
- **YOLOv8**: Primary detection with enhanced multi-threshold pipeline
- **Vision Transformer**: Fallback validation for low-confidence detections
- **Enhanced Sensitivity**: Combines multiple confidence/IoU thresholds with NMS
- **Small Object Recovery**: Specialized detection for very small boulders

### 📏 **Physical Measurements**
- **Diameter**: Real-world size estimation
- **Volume**: 3D volume calculation
- **Circularity**: Shape analysis
- **Elongation**: Aspect ratio analysis
- **Density**: Spatial distribution analysis

### 🎨 **Visualizations**
- **Clean Bounding Boxes**: Publication-ready overlays (no cluttering labels)
- **Grad-CAM**: Attention heatmaps for interpretability
- **Multiple Formats**: PNG, JPG, GIF support

### 📊 **Analysis Types**
- **Basic**: Standard YOLO detection
- **Advanced**: YOLO + ViT fallback
- **Depth**: Shadow-based depth estimation (experimental)
- **Grad-CAM**: Attention visualization analysis

</div>

---

## 🌙 **QGIS Terrain Risk Analysis**

<div style="background: linear-gradient(45deg, #ff9a9e, #fecfef); padding: 25px; border-radius: 20px; margin: 25px 0;">

### 🧮 **Risk Components & Weights**
- **Slope**: 30% (terrain steepness)
- **Aspect**: 15% (solar exposure)
- **Hillshade**: 15% (illumination)
- **Contour Density**: 10% (terrain complexity)
- **Profile Gradient**: 10% (elevation change)
- **Crater Ratio**: 5% (impact features)
- **Roughness (TRI)**: 10% (terrain ruggedness)
- **Elevation**: 5% (altitude factors)

### 📊 **Risk Levels**
- **0-20**: LOW RISK
- **20-40**: MODERATE RISK
- **40-60**: HIGH RISK
- **60-80**: VERY HIGH RISK
- **80-100**: EXTREME RISK

### 🗺️ **QGIS Integration**
- **Raster Calculator Expressions**: Ready-to-use formulas
- **Real-time Analysis**: Live risk assessment
- **Comprehensive Reports**: JSON + human-readable summaries
- **Multi-format Outputs**: GeoTIFF, reports, visualizations

</div>

---

## 🔌 **API Endpoints**

<div style="background: linear-gradient(45deg, #667eea, #764ba2); padding: 25px; border-radius: 20px; margin: 25px 0;">

### 🔐 **Authentication**
- `POST /login` → JWT token generation
- `POST /logout` → Token invalidation
- `POST /verify-token` → Token validation

### 🪨 **Boulder Detection**
- `POST /api/boulder/upload` → Image upload
- `POST /api/boulder/analyze` → Detection analysis
- `GET /api/boulder/status` → System status
- `GET /uploads/<filename>` → File serving

### 📊 **Analytics**
- `GET /api/analytics/summary` → Dashboard metrics
- `GET /api/analyses` → Analysis history
- `GET /api/analyses/<id>` → Specific analysis

### 🌙 **QGIS Analysis**
- `POST /api/lunar-analysis` → Terrain risk analysis
- `GET /api/lunar-analysis/progress` → Progress tracking

### 🛠️ **Utilities**
- `GET /api/test/files` → File listing
- `GET /api/test/image/<filename>` → Image serving

</div>

---

## 📁 **Project Structure**

<div style="background: linear-gradient(45deg, #ffecd2, #fcb69f); padding: 25px; border-radius: 20px; margin: 25px 0;">

```
🌙 lunalens/
├── 📁 frontend/website/           # React frontend
│   ├── 📁 src/
│   │   ├── 📁 pages/             # Route components
│   │   │   ├── 🚪 login/         # Authentication
│   │   │   ├── 📊 dashboard/     # Main dashboard
│   │   │   ├── 📈 analytics/     # Analytics page
│   │   │   ├── 🪨 boulder/       # Boulder detection
│   │   │   └── 🌙 landslide/     # Landslide analysis
│   │   ├── 📁 components/        # Reusable components
│   │   └── 🚀 App.jsx            # Main app with routing
│   └── 📦 package.json
├── 📁 backend/
│   ├── 📁 server/                # Flask API server
│   │   ├── 🚀 app.py             # Main Flask app
│   │   ├── 📊 models.py          # Database models
│   │   ├── 🔐 security_config.py # Security settings
│   │   └── 📁 uploads/           # File storage
│   └── 📁 boulder_detection/     # AI detection system
│       ├── 🎯 detector.py        # Main detection logic
│       ├── 🧠 ml_models.py       # Model loading
│       ├── 🎨 gradcam.py         # Visualization
│       ├── 📏 measurements.py    # Physical metrics
│       └── 🧪 test_*.py          # Evaluation scripts
└── 📁 detection_qgis/            # QGIS analysis
    ├── 📁 Parameters/            # Risk formulas & expressions
    └── 📁 processed/             # Analysis outputs
```

</div>

---

## 🛠️ **Development**

<div style="background: linear-gradient(45deg, #4facfe, #00f2fe); padding: 25px; border-radius: 20px; margin: 25px 0;">

### 🎨 **Frontend Development**
```bash
cd frontend/website
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

### 🔧 **Backend Development**
```bash
cd backend/server
python app.py                    # Start Flask server
python setup_database.py         # Initialize database
python test_server.py            # Run tests
```

### 🪨 **Boulder Detection Testing**
```bash
cd backend/boulder_detection
python quick_metrics.py          # Quick model metrics
python model_evaluation.py       # Comprehensive evaluation
python test_enhanced_detection.py # Compare detection methods
```

### 🌙 **QGIS Analysis**
```bash
cd detection_qgis/Parameters
python qgis_lunar_risk_expressions.py  # Generate QGIS expressions
python lunar_risk_analysis.py          # Run risk analysis
```

</div>

---

## 🔒 **Security Features**

<div style="background: linear-gradient(45deg, #ff6b6b, #ee5a24); padding: 25px; border-radius: 20px; margin: 25px 0;">

### 🛡️ **Default Security**
- **Localhost-only**: Server binds to `127.0.0.1:5000` by default
- **CORS Protection**: Limited to localhost origins
- **JWT Authentication**: Secure token-based auth
- **File Validation**: Secure file upload handling

### 🔧 **Production Configuration**
- Set `ALLOW_EXTERNAL_ACCESS=true` for external access
- Configure `SECRET_KEY` and `JWT_SECRET_KEY`
- Enable HTTPS with `REQUIRE_HTTPS=true`
- Customize `allowed_origins` for CORS

### 📝 **Environment Variables**
```bash
FLASK_CONFIG=production
ALLOW_EXTERNAL_ACCESS=true
REQUIRE_HTTPS=true
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

</div>

---

## 📊 **Performance & Optimization**

<div style="background: linear-gradient(45deg, #a8edea, #fed6e3); padding: 25px; border-radius: 20px; margin: 25px 0;">

### ⚡ **Detection Performance**
- **GPU Acceleration**: CUDA support for YOLOv8 and ViT
- **Enhanced Pipeline**: Multi-threshold detection for higher recall
- **Memory Optimization**: Efficient model loading and inference
- **Batch Processing**: Support for multiple images

### 🗺️ **QGIS Processing**
- **Large File Support**: Handles multi-GB DEM files
- **Streaming Processing**: Efficient memory usage
- **Parallel Processing**: Multi-core analysis capabilities
- **Progress Tracking**: Real-time analysis status

### 📱 **Frontend Performance**
- **Code Splitting**: Lazy loading of components
- **Image Optimization**: Compressed visualizations
- **Caching**: Efficient data caching
- **Responsive Design**: Mobile-first approach

</div>

---

## 🧪 **Testing & Evaluation**

<div style="background: linear-gradient(45deg, #667eea, #764ba2); padding: 25px; border-radius: 20px; margin: 25px 0;">

### 🪨 **Boulder Detection Tests**
- **Model Evaluation**: Precision, recall, F1-score metrics
- **Performance Testing**: Speed, memory, detection counts
- **Visualization Tests**: Clean bounding box verification
- **Enhanced Detection**: Comparison with standard methods

### 🔧 **Backend Tests**
- **API Testing**: Endpoint functionality and responses
- **Authentication**: JWT token validation
- **File Handling**: Upload and serving tests
- **Database**: CRUD operations and integrity

### 🌙 **QGIS Analysis Tests**
- **Expression Validation**: Risk formula accuracy
- **Output Verification**: Report generation and format
- **Performance**: Large file processing capabilities
- **Integration**: Backend API connectivity

</div>

---

## 🚀 **Deployment**

<div style="background: linear-gradient(45deg, #ff9a9e, #fecfef); padding: 25px; border-radius: 20px; margin: 25px 0;">

### 🎨 **Frontend Deployment**
```bash
cd frontend/website
npm run build
# Deploy dist/ folder to:
# - Netlify (drag & drop)
# - Vercel (git-based)
# - GitHub Pages
# - AWS S3
```

### 🔧 **Backend Deployment**
```bash
cd backend/server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 🐳 **Docker Deployment**
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

# Backend
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

</div>

---

## 🔧 **Troubleshooting**

<div style="background: linear-gradient(45deg, #ffecd2, #fcb69f); padding: 25px; border-radius: 20px; margin: 25px 0;">

### ❌ **Common Issues**

| Problem | Solution |
|---------|----------|
| 🔐 Login fails | Verify demo credentials or check backend |
| 🪨 Detection fails | Ensure `best.pt` and `vit_model.pth` exist |
| 🌐 CORS errors | Check backend port and CORS settings |
| 📊 Dashboard issues | Verify JWT token in localStorage |
| 🗺️ QGIS analysis fails | Check QGIS installation and paths |
| 🔌 Port conflicts | Change ports in configuration |

### 🐛 **Debug Mode**
```bash
# Frontend
npm run dev

# Backend
FLASK_DEBUG=True python app.py

# Boulder Detection
python -m boulder_detection.main --debug
```

### 📝 **Logs & Monitoring**
- Backend logs: `backend/server/logs/`
- Database: SQLite with SQLAlchemy
- Performance: Built-in metrics and evaluation tools

</div>

## Contributors

| Name        | Role          | GitHub Profile              |
|-------------|---------------|-----------------------------|
| Bhuwan B    | Project Lead  | [@bhuwanb23](https://github.com/bhuwanb23)       |
| Nishanth P  | ML Architect  | _add GitHub handle_   |
| Avinash A   | QGIS Expertise   | _add GitHub handle_     |
| Mukesh V    | Researcher and Developer   | _add GitHub handle_       |
| Padmanaban G  | Developer   | _add GitHub handle_   |
| Dhanush KB   | Data Analyst   | _add GitHub handle_     |

---


---

## 🤝 **Contributing**

<div style="background: linear-gradient(45deg, #667eea, #764ba2); padding: 25px; border-radius: 20px; margin: 25px 0;">

### 🚀 **How to Contribute**
1. 🍴 **Fork the repository**
2. 🌿 **Create a feature branch**
3. 🔧 **Make your changes**
4. 🧪 **Add tests if applicable**
5. 📝 **Update documentation**
6. 🔄 **Submit a pull request**

### 🎯 **Areas for Contribution**
- 🌙 **Lunar Analysis**: QGIS expressions and geospatial features
- 🤖 **AI/ML**: Boulder detection and model improvements
- 🎨 **Frontend**: React components and UI/UX enhancements
- 🔧 **Backend**: API development and optimization
- 📊 **Analytics**: Data visualization and reporting
- 🧪 **Testing**: Unit and integration tests

### 📋 **Development Guidelines**
- 📝 **Code Style**: Follow ESLint rules and Python PEP 8
- 🧪 **Testing**: Add tests for new features
- 📚 **Documentation**: Update README and code comments
- 🔍 **Code Review**: All changes require review
- 🚀 **Performance**: Optimize for speed and efficiency

</div>

---

## 📄 **License**

<div style="background: linear-gradient(45deg, #ff9a9e, #fecfef); padding: 20px; border-radius: 15px; margin: 20px 0;">

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🙏 **Acknowledgments**

<div style="background: linear-gradient(45deg, #ffecd2, #fcb69f); padding: 25px; border-radius: 20px; margin: 25px 0;">

### 🛠️ **Core Technologies**
- ⚛️ **React** by Meta for frontend framework
- 🐍 **Python** & **Flask** for backend API
- 🎯 **YOLOv8** by Ultralytics for object detection
- 🧠 **Vision Transformer** by Google Research
- 🗺️ **QGIS** for geospatial processing
- 🎨 **Tailwind CSS** for styling

### 🚀 **Research & Data**
- 🌙 **NASA** & **ESA** for lunar data and research
- 🗺️ **Open Source Geospatial** community
- 🤖 **AI/ML** research community
- 📊 **Scientific Computing** tools and libraries

### 🎨 **Design & UI**
- 🌙 **Lunar Theme**: Space-inspired design
- 📱 **Responsive Design**: Mobile-first approach
- 🎨 **Modern UI**: Clean and intuitive interface
- ⭐ **Space Elements**: Beautiful space imagery

</div>

---

<div align="center">

## 🌙 **Happy Lunar Analysis!** 🚀

*LunaLens - Advanced lunar terrain analysis with AI-powered detection and modern web technologies.*

<br>

[![Made with Love](https://img.shields.io/badge/Made%20with-Love-red?style=for-the-badge)](https://github.com/bhuwanb23/lunalens)
[![Powered by React](https://img.shields.io/badge/Powered%20by-React-blue?style=for-the-badge)](https://reactjs.org/)
[![Lunar Science](https://img.shields.io/badge/Lunar-Science-purple?style=for-the-badge)](https://github.com/bhuwanb23/lunalens)

</div>

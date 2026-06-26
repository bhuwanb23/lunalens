# LunaLens

**Advanced Lunar Surface Analysis Platform with AI-Powered Detection**

[![CI](https://img.shields.io/github/actions/workflow/status/bhuwanb23/lunalens/ci.yml?label=CI&style=flat)](https://github.com/bhuwanb23/lunalens/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/bhuwanb23/lunalens?style=social)](https://github.com/bhuwanb23/lunalens)

> **ISRO Bharatiya Antariksh Hackathon 2025 -- Finalist**
> Selected for the finals of the Indian Space Research Organisation's national hackathon for lunar exploration and research.
> [View the submission (PDF)](./Bharatiya%20Antariksh%20Hackathon%202025%20Idea%20Submission.pdf)

---

## About

LunaLens is a full-stack web application that combines AI-powered boulder detection, QGIS-based terrain risk analysis, and a modern React frontend for lunar surface research. It is designed to support mission planners and researchers in identifying hazards and assessing terrain risk on the lunar surface.

The platform uses YOLOv8 with a Vision Transformer fallback for boulder detection, multi-parameter composite risk scoring for terrain analysis, and provides real-time dashboards and analytics for tracking results.

## Key Features

- **AI-Powered Boulder Detection** -- YOLOv8 primary detector with Vision Transformer fallback for low-confidence detections. Physical measurements (diameter, volume, circularity, elongation) and Grad-CAM visualizations for interpretability.
- **Terrain Risk Analysis** -- QGIS-based multi-parameter risk assessment covering slope, aspect, hillshade, contour density, roughness, and elevation. Weighted composite scoring on a 0-100 scale with configurable risk levels.
- **Interactive Dashboard** -- Real-time analytics, scan history, and quick-action navigation across detection modules.
- **Secure Authentication** -- JWT-based user management with role-based access control (admin, researcher, user).
- **Docker Deployment** -- Containerized setup with Docker Compose for local and production deployment.
- **REST API** -- Full API for boulder detection, terrain analysis, analytics, and file management.

## Architecture

| Component | Technology | Location |
|-----------|------------|----------|
| Frontend | React 19, Vite, Tailwind CSS | `frontend/website/` |
| Backend API | Python Flask, SQLAlchemy, JWT | `backend/server/` |
| Boulder Detection | YOLOv8, Vision Transformer, Grad-CAM | `backend/boulder_detection/` |
| Terrain Risk Analysis | QGIS, Raster Calculator | `detection_qgis/` |

## Quick Start

### Prerequisites

- Node.js v18+
- Python 3.11+
- QGIS 3.x (optional, for terrain analysis)

### Local Development

```bash
git clone https://github.com/bhuwanb23/lunalens.git
cd lunalens

# Backend
cd backend
pip install -r requirements.txt
cd server
cp env.example .env
python setup_database.py
python app.py

# Frontend (new terminal)
cd frontend/website
cp .env.example .env
npm install
npm run dev
```

Frontend: `http://localhost:5173` | Backend: `http://localhost:5000`

### Docker

```bash
git clone https://github.com/bhuwanb23/lunalens.git
cd lunalens

export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
export JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

docker-compose up --build
```

Frontend: `http://localhost` | Backend: `http://localhost:5000`

> Boulder detection requires model files (`best.pt`, `vit_model.pth`) that are not committed to the repo. The platform works without them -- only `/api/boulder/*` endpoints will return 503. See [Model Files](#model-files) for options.

### Demo Credentials

| Mission ID | Access Code | Role |
|------------|-------------|------|
| `isro123` | `isro123@2024` | Admin |
| `mission001` | `mission001@2024` | User |
| `research002` | `research002@2024` | Researcher |
| `test001` | `test001@2024` | Test User |

Access codes follow the pattern `<missionId>@2024`. Change them before deploying -- see `backend/server/database.py`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/login` | JWT token generation |
| `POST` | `/logout` | Token invalidation |
| `POST` | `/verify-token` | Token validation |
| `POST` | `/api/boulder/upload` | Upload image for boulder detection |
| `POST` | `/api/boulder/analyze` | Run boulder detection analysis |
| `GET` | `/api/boulder/status` | Detection system status |
| `GET` | `/api/analytics/summary` | Dashboard metrics |
| `GET` | `/api/analyses` | Analysis history (paginated) |
| `GET` | `/api/analyses/<id>` | Specific analysis details |
| `POST` | `/api/lunar-analysis` | Terrain risk analysis |
| `GET` | `/api/lunar-analysis/progress` | Analysis progress tracking |

## Project Structure

```
lunalens/
├── frontend/website/           # React frontend
│   └── src/
│       ├── pages/              # Route components
│       │   ├── login/          # Authentication
│       │   ├── dashboard/      # Main dashboard
│       │   ├── analytics/      # Analytics page
│       │   ├── boulder/        # Boulder detection
│       │   └── landslide/      # Terrain risk analysis
│       └── components/         # Shared components
├── backend/
│   ├── server/                 # Flask API server
│   │   ├── app.py              # Main application
│   │   ├── models.py           # Database models
│   │   └── security_config.py  # Security settings
│   └── boulder_detection/      # AI detection system
│       ├── detector.py         # Detection logic
│       ├── ml_models.py        # Model loading
│       ├── gradcam.py          # Visualization
│       └── measurements.py     # Physical metrics
├── detection_qgis/             # QGIS terrain analysis
│   ├── Parameters/             # Risk formulas
│   └── processed/              # Analysis outputs
├── docker-compose.yml          # Docker orchestration
└── Procfile                    # PaaS deployment
```

## Model Files

The boulder detection pipeline requires two model artifacts not stored in git:

| File | Path | Purpose |
|------|------|---------|
| `best.pt` | `backend/boulder_detection/best.pt` | YOLOv8 weights |
| `vit_model.pth` | `backend/boulder_detection/vit_model.pth` | Vision Transformer weights |

Options:
1. **Train from scratch** -- see `backend/boulder_detection/lunalena_yolo_train.py`. Set `ROBOFLOW_API_KEY` in your environment.
2. **Download from GitHub Releases** (once published) and place in `backend/boulder_detection/`.
3. **Skip** -- the rest of the platform works without the boulder models.

## Development

```bash
# Frontend
cd frontend/website
npm run dev          # Start dev server
npm run build        # Production build
npm run lint         # Run ESLint

# Backend
cd backend/server
python app.py                    # Start Flask server
python setup_database.py         # Initialize database

# Linting
ruff check backend/              # Python linting
```

## Security

- Server binds to `127.0.0.1:5000` by default (localhost only)
- CORS restricted to configured origins via `CORS_ORIGINS` env var
- JWT authentication with hashed passwords (werkzeug)
- Secrets (`SECRET_KEY`, `JWT_SECRET_KEY`) required via environment variables in production
- Set `ALLOW_EXTERNAL_ACCESS=true` and `REQUIRE_HTTPS=true` for production deployment

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, branch conventions, and PR guidelines.

## Team

| Name | Role |
|------|------|
| Bhuwan B | Project Lead |
| Nishanth P | ML Architect |
| Avinash A | QGIS Expertise |
| Mukesh V | Researcher and Developer |
| Padmanaban G | Developer |
| Dhanush KB | Data Analyst |

## License

This project is licensed under the MIT License -- see [LICENSE](LICENSE) for details.

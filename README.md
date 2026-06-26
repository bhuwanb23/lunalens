# LunaLens

**AI-Powered Lunar Surface Analysis Platform**

[![CI](https://img.shields.io/github/actions/workflow/status/bhuwanb23/lunalens/ci.yml?label=CI&style=flat)](https://github.com/bhuwanb23/lunalens/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/bhuwanb23/lunalens?style=social)](https://github.com/bhuwanb23/lunalens)

> **ISRO Bharatiya Antariksh Hackathon 2025 -- Finalist**
> Selected for the finals of India's national hackathon for lunar exploration and research.
> [View the submission (PDF)](./Bharatiya%20Antariksh%20Hackathon%202025%20Idea%20Submission.pdf)

---

## About

LunaLens is a full-stack web application that combines AI-powered boulder detection, QGIS-based terrain risk analysis, and a modern React frontend for lunar surface research. It supports mission planners and researchers in identifying hazards and assessing terrain risk on the lunar surface.

The platform uses YOLOv8 with a Vision Transformer fallback for boulder detection, multi-parameter composite risk scoring for terrain analysis, and provides real-time dashboards and analytics for tracking results.

## How It Works

1. **Upload** -- Users upload lunar surface imagery (DEM files or photographs) through the web interface.
2. **Detect** -- The AI pipeline runs YOLOv8 for boulder detection, with a Vision Transformer validating low-confidence results. Physical measurements (diameter, volume, circularity) are computed for each detected object.
3. **Analyze** -- QGIS-based terrain risk analysis processes DEM data across multiple parameters (slope, aspect, hillshade, roughness, elevation) to produce a weighted composite risk score.
4. **Visualize** -- Results are displayed through interactive dashboards with Grad-CAM attention maps, detection overlays, and analytics.

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

> Boulder detection requires model files (`best.pt`, `vit_model.pth`) not committed to the repo. The platform works without them -- only `/api/boulder/*` endpoints return 503. See [Contributing](#contributing) for model setup.

### Demo Credentials

| Mission ID | Access Code | Role |
|------------|-------------|------|
| `isro123` | `isro123@2024` | Admin |
| `mission001` | `mission001@2024` | User |
| `research002` | `research002@2024` | Researcher |
| `test001` | `test001@2024` | Test User |

## How to Deploy

### Docker (Recommended)

```bash
docker-compose up --build -d
```

Set `SECRET_KEY` and `JWT_SECRET_KEY` as environment variables before starting. The `docker-compose.yml` handles frontend (nginx) and backend (gunicorn) services with persistent volumes for uploads and the database.

### PaaS (Render, Railway, Heroku)

The project includes a `Procfile` for PaaS deployment:

```
web: cd backend/server && gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 app:app
```

Set the following environment variables in your PaaS dashboard:
- `SECRET_KEY` -- Random hex string for session signing
- `JWT_SECRET_KEY` -- Random hex string for JWT tokens
- `FLASK_CONFIG=production`
- `ALLOW_EXTERNAL_ACCESS=true`

### Manual Deployment

```bash
cd backend/server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

Build the frontend and serve the `dist/` folder with nginx or any static file server.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, branch conventions, and PR guidelines.

### Model Files

The boulder detection pipeline requires two model artifacts:

| File | Path | Purpose |
|------|------|---------|
| `best.pt` | `backend/boulder_detection/best.pt` | YOLOv8 weights |
| `vit_model.pth` | `backend/boulder_detection/vit_model.pth` | Vision Transformer weights |

Options:
1. **Train from scratch** -- see `backend/boulder_detection/lunalena_yolo_train.py`. Requires `ROBOFLOW_API_KEY`.
2. **Download from GitHub Releases** and place in `backend/boulder_detection/`.
3. **Skip** -- the rest of the platform works without the boulder models.

## Releases

See the [Releases page](https://github.com/bhuwanb23/lunalens/releases) for published versions and download links.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

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

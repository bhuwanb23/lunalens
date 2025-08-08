# 🚀 LunaLens Backend Server

<div align="center">

![LunaLens Backend](https://img.shields.io/badge/LunaLens-Backend-blue?style=for-the-badge&logo=server)
![Flask](https://img.shields.io/badge/Flask-API-red?style=for-the-badge&logo=flask)
![Python](https://img.shields.io/badge/Python-3.9%2B-green?style=for-the-badge&logo=python)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-orange?style=for-the-badge&logo=sqlalchemy)
![JWT](https://img.shields.io/badge/JWT-Auth-purple?style=for-the-badge&logo=jwt)
![SQLite](https://img.shields.io/badge/SQLite-Database-yellow?style=for-the-badge&logo=sqlite)

</div>

---

## 🌙 Overview

Secure Flask API for lunar surface analysis with:
- **JWT Authentication & Roles**
- **Boulder Detection** (integrates `backend/boulder_detection`)
- **Uploads & Visualization** under `/uploads/*`
- **Analytics, Logging & DB** (SQLite by default)
- **QGIS-based Lunar Analysis** runner (optional)

By default the server is locked to **localhost-only** for safety. Enable external access via env (see Security).

---

## 📋 Prerequisites

- Python 3.9+
- Windows PowerShell (commands here assume PowerShell)
- Optional: QGIS 3.x for the lunar analysis endpoint

---

## 🛠️ Installation

From project root:

```powershell
cd backend/server
pip install -r ..\requirements.txt
```

Or install a minimal set (Windows-friendly):

```powershell
pip install Flask Flask-CORS Flask-SQLAlchemy Flask-Migrate PyJWT python-dotenv Werkzeug numpy opencv-python Pillow
```

Initialize DB and demo data:

```powershell
python setup_database.py
```

---

## ⚙️ Configuration

```powershell
copy env.example .env
```

Important settings (see `config.py`, `security_config.py`):
- `FLASK_CONFIG`: `development` | `production` | `testing` (default: development)
- `DATABASE_URL`/`DEV_DATABASE_URL`/`TEST_DATABASE_URL` → SQLite by default
- `SECRET_KEY`, `JWT_SECRET_KEY`
- `UPLOAD_FOLDER` (default `uploads` under `backend/server`)
- Security (in `security_config.py`):
  - `ALLOW_EXTERNAL_ACCESS=true` → bind `0.0.0.0` (otherwise `127.0.0.1`)
  - `REQUIRE_HTTPS=true` → HSTS header in production
  - `allowed_origins` → CORS frontends

---

## 🔒 Security Defaults

- Binds to `127.0.0.1:5000` (localhost-only)
- CORS limited to localhost origins
- To expose externally, set `ALLOW_EXTERNAL_ACCESS=true` (not recommended for dev)

On startup the server prints the current security status.

---

## 🏃 Run the Server

```powershell
python app.py
```

- Initializes DB and Boulder Detection
- URL: `http://localhost:5000`

---

## 🪨 Boulder Detection Integration

The server imports `BoulderDetectionController` from `backend/boulder_detection` and expects:
- `backend/boulder_detection/best.pt`
- `backend/boulder_detection/vit_model.pth`

Detection uses an enhanced multi-threshold pipeline for higher recall. Visualizations are generated and served under `/uploads/*`.

Path handling:
- For `/api/boulder/analyze`, `filepath` may be absolute or relative to `backend/server`.
- Files uploaded via `/api/boulder/upload` are stored in `backend/server/uploads`.

---

## 🔌 API Endpoints

### Public pages
- `GET /` → Home HTML
- `GET /credentials` → Demo login page
- `GET /boulder-detection` → Simple HTML UI
- `GET /database` → Simple DB UI

### Authentication
- `POST /login` → `{ missionId, accessCode }` → `{ token, user }`
- `POST /logout` → `{ token }`
- `POST /verify-token` → `{ token }` → `{ valid, user? }`

PowerShell example:
```powershell
$login = Invoke-RestMethod -Method Post -Uri http://localhost:5000/login -ContentType 'application/json' -Body '{"missionId":"test001","accessCode":"test001@2024"}'
$token = $login.token
```

### Analytics
- `GET /api/analytics/summary`
- `GET /api/analyses?page=&per_page=&user_id=`
- `GET /api/analyses/<id>`

### Boulder Detection
- `POST /api/boulder/upload` (multipart form-data `image`) → `{ filename, filepath }`
- `POST /api/boulder/analyze` (JSON body):
  ```json
  { "filepath": "uploads/your_image.png", "analysisType": "basic|advanced|gradcam|full" }
  ```
  - Include `Authorization: Bearer <token>` to associate results and store in DB
  - Returns detected objects, analysis summary, density, and paths such as `/uploads/<viz.png>` and `/uploads/<gradcam.png>`
- `GET /api/boulder/status` → availability flags
- `GET /uploads/<filename>` → serves uploaded/generated files (PNG/JPG/GIF content-type)

Analyze example:
```powershell
$headers = @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/boulder/analyze -ContentType 'application/json' -Headers $headers -Body '{"filepath":"uploads\\test.png","analysisType":"full"}'
```

### Utilities / Diagnostics
- `GET /api/test/files` → list files in `uploads`
- `GET /api/test/image/<filename>` → serve specific image with debug headers

### QGIS Lunar Analysis (optional)
- `POST /api/lunar-analysis`
  - Body: `{ "dem_path": "C:\\path\\to\\your.tif" }` (optional)
  - Uses QGIS launcher path in code: `C:\\Program Files\\QGIS 3.40.9\\bin\\python-qgis-ltr.bat`
  - Aggregates JSON results from `detection_qgis/processed/json_results`
- `GET /api/lunar-analysis/progress` → returns `progress_info.json` if present

---

## 📊 Database Schema (summary)

Tables:
- `users`, `analyses`, `detected_objects`, `density_analysis`, `system_logs`

`python setup_database.py --info` prints DB details.

---

## 📝 Logging

Auth, analysis, errors, performance, and activity events are persisted. See logs/DB entries per config.

---

## 🧪 Testing

```powershell
python test_server.py
python test_image_serving.py
python setup_database.py --check
python setup_database.py --info
```

---

## 🐳 Docker (example)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

---

## 🆘 Troubleshooting

- 5000 in use → change port in `security_config.py`
- Missing models → add `best.pt` and `vit_model.pth` to `backend/boulder_detection`
- External access blocked → set `ALLOW_EXTERNAL_ACCESS=true`
- Analyze: "file not found" → pass absolute path or a `backend/server`-relative path
- QGIS run fails → verify `qgis_python` path and `dem_path`

---

## 📈 Performance Notes

- SQLite is the default and requires no external setup
- Detection benefits from GPU (model side); server may run on CPU
- CORS restricted to localhost by default

---

<div align="center" style="margin-top:16px;">

**🌙 Happy Lunar Analysis!**

</div> 
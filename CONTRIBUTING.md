# Contributing to LunaLens

Thanks for your interest in improving LunaLens! This guide explains how to set up the project locally, the conventions we follow, and what we expect from contributors.

## Code of Conduct

By participating in this project you agree to abide by the [Code of Conduct](./CODE_OF_CONDUCT.md). Please be respectful and constructive.

## Getting set up

LunaLens is a three-part project: a React frontend, a Flask backend, and a QGIS-based terrain pipeline.

### Prerequisites
- Node.js 18+ and npm
- Python 3.10–3.12 (3.13 has dependency issues with some ML libs)
- (Optional) QGIS 3.40+ if you want to run the lunar terrain analysis pipeline
- (Optional) `best.pt` and `vit_model.pth` model files for boulder detection — see the [Model Files](./README.md#-model-files) section in the README

### Local setup

```bash
# 1) Clone and enter the repo
git clone https://github.com/bhuwanb23/lunalens.git
cd lunalens

# 2) Frontend
cd frontend/website
cp .env.example .env
npm install
npm run dev   # http://localhost:5173

# 3) Backend (in a separate terminal, from the repo root)
cd backend
pip install -r requirements.txt
cd server
cp env.example .env
python setup_database.py   # seeds SQLite with demo users
python app.py              # http://localhost:5000
```

## Development workflow

1. **Fork** the repo and create a feature branch off `main`:
   ```bash
   git checkout -b feat/short-description
   ```
   Branch naming: `feat/`, `fix/`, `docs/`, `refactor/`, `chore/`.
2. **Make focused changes** — one logical change per PR. Avoid mixing refactors with bug fixes.
3. **Keep commits clean** — write commit messages that explain *why*, not just *what*.
4. **Run the checks** before opening a PR (see below).
5. **Open a PR** against `main` and fill in the PR template.

## Pre-PR checklist

Before requesting review, make sure:

- [ ] Frontend builds: `cd frontend/website && npm run build`
- [ ] Frontend lints clean: `cd frontend/website && npm run lint`
- [ ] Backend modules compile: `python -m py_compile backend/server/*.py backend/boulder_detection/*.py`
- [ ] No secrets, API keys, personal paths, or `*.db`/`*.pt` files are committed
- [ ] Any new env vars are documented in the relevant `*.env.example` and the README
- [ ] README / docs are updated if you changed setup steps or APIs

GitHub Actions runs the same checks on every PR — see [.github/workflows/ci.yml](./.github/workflows/ci.yml).

## Code style

### Python
- Follow PEP 8 and aim for type hints on new functions.
- Use `os.environ.get` (with a sane default) for any path or secret. **Never** hardcode developer-specific paths or API keys.
- Keep route handlers thin; put business logic in `database.py` / dedicated modules.

### JavaScript / React
- Functional components with hooks; no class components.
- Honour the React rules of hooks (no early returns *before* hook calls).
- Pull the API base URL from [`src/config/api.js`](frontend/website/src/config/api.js) — never hardcode `http://localhost:5000`.
- Run `npm run lint` and fix everything before pushing.

### QGIS / detection_qgis
- Read `QGIS_PREFIX_PATH` and any DEM paths from environment variables / CLI args, not hardcoded `D:\moon extract\…` style paths.

## Reporting bugs / requesting features

Use the [issue templates](./.github/ISSUE_TEMPLATE/) — they prompt you for the info maintainers need to triage quickly.

## Areas that need help

- More robust unit/integration tests (especially for `backend/server/app.py`)
- Cross-platform testing of the QGIS pipeline (macOS / Linux)
- UI/UX polish on the analytics and landslide pages
- Documentation: tutorials, API reference, deployment guides
- Performance: code-splitting the frontend bundle, optimising large-DEM processing

Thanks for contributing!

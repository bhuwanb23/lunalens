# Changelog

All notable changes to LunaLens will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Docker Compose setup for local and production deployment
- Frontend Dockerfile with nginx SPA support
- Backend Dockerfile with gunicorn
- Procfile for PaaS deployment (Render, Railway, Heroku)
- React ErrorBoundary with fallback UI
- 404 route for unmatched paths
- Ruff linting configuration for Python
- Enhanced CI pipeline with linting and dependency auditing
- Password hashing with werkzeug for user authentication
- CORS_ORIGINS environment variable support
- Input validation for login and lunar analysis endpoints

### Fixed
- Removed hardcoded secret key fallbacks (SECRET_KEY and JWT_SECRET_KEY now required)
- Disabled debug mode in production
- Removed error details and tracebacks from API responses
- Fixed credential validation to use hashed passwords instead of plaintext comparison
- Fixed landslide analysis endpoint missing response.ok check
- Removed debug console.log statements from boulder components

### Changed
- Default FLASK_DEBUG from True to False
- README rewritten to professional format
- CODE_OF_CONDUCT updated with GitHub Issues for reporting

## [0.1.0] - 2025

### Added
- Initial release
- AI-powered boulder detection (YOLOv8 + Vision Transformer)
- QGIS terrain risk analysis with multi-parameter scoring
- React frontend with dashboard, analytics, and detection pages
- JWT authentication with role-based access
- REST API for boulder detection, terrain analysis, and analytics
- Grad-CAM visualization for detection interpretability
- Physical measurements (diameter, volume, circularity, elongation)
- ISRO Bharatiya Antariksh Hackathon 2025 finalist submission

# 🌙 LunaLens Frontend

<div align="center">

![LunaLens Frontend](https://img.shields.io/badge/LunaLens-Frontend-blue?style=for-the-badge&logo=react)
![React](https://img.shields.io/badge/React-18%2B-blue?style=for-the-badge&logo=react)
![Vite](https://img.shields.io/badge/Vite-Build-orange?style=for-the-badge&logo=vite)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-38B2AC?style=for-the-badge&logo=tailwind-css)
![ESLint](https://img.shields.io/badge/ESLint-Linting-yellow?style=for-the-badge&logo=eslint)

</div>

---

## 🌟 Overview

Modern React app (Vite + Tailwind) for lunar analysis dashboards and tools. Includes JWT login, protected routes, a dashboard, analytics, boulder detection workflow, and a landslide page stub.

---

## 🚀 Quick Start

```powershell
cd frontend/website
npm install
npm run dev
```

- App: `http://localhost:5173`
- Backend (default): `http://localhost:5000` (proxy `/api` if configured in `vite.config.js`)

Optional installs:
```powershell
npm install react-router-dom
```

---

## 🔐 Authentication

- Token stored in `localStorage` as `lunalens_token`
- On load, if token exists → redirect to `/dashboard`, else `/login`
- Logout clears token

Login flow in `src/App.jsx` protects routes and wraps authenticated pages with a header layout.

---

## 🧭 Routes

Defined in `src/App.jsx`:
- `/login` → Login page (`src/pages/login`)
- `/dashboard` → Dashboard (`src/pages/dashboard`)
- `/analytics` → Analytics (`src/pages/analytics`)
- `/boulder` → Boulder detection (`src/pages/boulder`)
- `/landslide` → Landslide detection stub (`src/pages/landslide`)
- `/` → Redirects to `/dashboard` (if authed) or `/login`

---

## 🪨 Boulder Detection Workflow

Page: `src/pages/boulder/boulder.jsx`
- Upload image → `POST /api/boulder/upload`
- Analyze → `POST /api/boulder/analyze` with `{ filepath, analysisType }`
- Renders clean detection visualization and (if available) Grad‑CAM via `/uploads/...` URLs returned by backend

Notes
- Backend must be running with boulder detection models present
- The page currently uses absolute URLs `http://localhost:5000/...`. You can switch to a Vite proxy (`server.proxy['/api']`) for cleaner calls.

---

## 📊 Dashboard & Analytics

- `src/pages/dashboard/dashboard.jsx` – KPIs, lunar analysis panel, alerts, quick actions, and recent scans
- `src/pages/analytics/` – analytics header, stats, filters, and tables

---

## 🧩 Project Structure (src)

```
src/
├─ App.jsx            # Routes + auth wrapper
├─ main.jsx           # App bootstrap
├─ index.css          # Global styles
├─ components/Header.jsx
└─ pages/
   ├─ login/
   ├─ dashboard/
   ├─ analytics/
   ├─ boulder/
   └─ landslide/
```

---

## 🔌 Backend Integration

Default backend base URL: `http://localhost:5000`.

Recommended Vite proxy (optional):
```js
// vite.config.js
export default defineConfig({
  server: {
    proxy: { '/api': 'http://localhost:5000' }
  }
})
```

Then replace hardcoded `http://localhost:5000` calls with `/api` in pages.

---

## 🛠 Development

```bash
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Lint
```

Tailwind is available via styles and utility classes in components/pages.

---

## ⚠️ Troubleshooting

- Backend CORS/security: backend is localhost-only by default; see backend README to enable external access.
- Upload/Analyze fails: ensure backend `/api/boulder/*` endpoints are up; check console for error JSON.
- Images not visible: use full URL `http://localhost:5000/uploads/...` or configure proxy and prefix.

---

## 📄 License

MIT

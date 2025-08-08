# 🌑 Lunar Terrain Risk Analysis (Parameters)

<div align="center">

![QGIS](https://img.shields.io/badge/QGIS-Raster%20Calc-3ba63c?style=for-the-badge&logo=qgis)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Expressions](https://img.shields.io/badge/Expressions-QGIS-purple?style=for-the-badge)
![Reports](https://img.shields.io/badge/Reports-JSON%2FTXT-orange?style=for-the-badge)

</div>

---

## 📋 Overview

This folder contains reusable formulas, expressions, and scripts to score lunar terrain risk using multiple raster-derived parameters. Outputs include human-readable reports and machine-readable JSON for downstream analysis or serving via the backend API.

- Risk formula weights are standardized and implemented in both QGIS expressions and Python scripts.
- Supports both desktop workflows (QGIS Raster Calculator) and Python-only processing.

---

## 🎯 Risk Components & Weights

The composite risk is a weighted sum of individual component risks scaled to 0–100.

- Slope: 0.30
- Aspect: 0.15
- Hillshade: 0.15
- Contour Density: 0.10
- Profile Gradient: 0.10
- Crater Ratio: 0.05
- Roughness (TRI): 0.10
- Elevation: 0.05

Risk level bands:
- 0–20 LOW, 20–40 MODERATE, 40–60 HIGH, 60–80 VERY HIGH, 80–100 EXTREME

---

## 🧮 Core Formulas

- Slope: `(slope / 60.0) * 100.0`
- Aspect (distance from 315°): `(distance_from_315° / 180.0) * 100.0`
- Hillshade: `(128.0 - hillshade) / 128.0 * 100.0`
- Contour Density: `(density / 10.0) * 100.0`
- Profile Gradient: `(gradient / 50.0) * 100.0`
- Crater Ratio: `(ratio / 30.0) * 100.0`
- Roughness (TRI): `(roughness / 10.0) * 100.0`
- Elevation (bounded):
  - `<1000m → 0`, `>2000m → 100`, else linear `(elev-1000)/1000*100`

Composite risk: `Σ(component_risk × weight)`

---

## 🧰 What’s in this folder

- `qgis_lunar_risk_expressions.py`: Generates ready-to-use QGIS Raster Calculator expressions, a full workflow script, and an expressions guide.
- `lunar_risk_analysis.py`: Parses textual analysis reports and computes composite risk and summaries in Python.
- `convert_json_to_text.py`: Converts JSON results to readable text summaries.
- Reports (examples):
  - `lunar_risk_analysis_results.json`, `lunar_risk_analysis_results.txt`
  - Component reports like `lunar_slope_analysis_report.txt`, `lunar_aspect_analysis_report.txt`, etc.
  - `comprehensive_lunar_risk_report.txt`, `lunar_analysis_summary_report.txt`

---

## 💻 Python Usage

### 1) Generate QGIS expressions, guide, and workflow
```bash
python qgis_lunar_risk_expressions.py
# Outputs:
#  - qgis_lunar_risk_workflow.py
#  - qgis_lunar_risk_expressions_guide.txt
```

### 2) Run the risk analyzer on reports
```bash
python lunar_risk_analysis.py
# Scans available component reports and writes:
#  - lunar_risk_analysis_results.json
#  - comprehensive_lunar_risk_report.txt
```

### 3) Convert JSON → Text (optional)
```bash
python convert_json_to_text.py
```

Notes
- The analyzer attempts robust parsing of report sections (statistics, thresholds, factors).
- Ensure component reports exist (slope, aspect, roughness/TRI, elevation, etc.).

---

## 🗺️ QGIS Desktop Usage

1) Load required raster layers (slope, aspect, hillshade, elevation, TRI, etc.).
2) Open Processing → Raster calculator.
3) Paste expressions from `qgis_lunar_risk_expressions_guide.txt` (generated) or build with `qgis_lunar_risk_expressions.py`.
4) Export each component risk as GeoTIFF.
5) Use the composite expression to produce `composite_risk.tif` (0–100).
6) Optionally classify levels (LOW…EXTREME) with the provided CASE expression.

Requirements
- All rasters should share the same CRS, extent, and resolution.

---

## 🌐 Backend Integration (Optional)

If you are using the LunaLens backend server, you can trigger the QGIS-based pipeline via API:

- `POST /api/lunar-analysis` with optional body `{ "dem_path": "C:\\path\\to\\your.tif" }`
- Results are aggregated from `detection_qgis/processed/json_results` and returned as JSON.

> The backend uses a Windows QGIS launcher path by default:
> `C:\\Program Files\\QGIS 3.40.9\\bin\\python-qgis-ltr.bat`

---

## 📑 Example Outputs (this folder)

- `lunar_risk_analysis_results.json`: Machine-readable scores by component and composite.
- `comprehensive_lunar_risk_report.txt`: Human-readable summary (overall score, breakdown, notes).
- Component summaries: `lunar_*_analysis_report.txt` (slope, aspect, elevation, roughness, curvature, etc.).

Interpretation
- Composite score ~10 → LOW RISK (safe for operations; monitor roughness if high locally)
- Always validate against optical imagery and mission needs.

---

## ⚠️ Notes & Best Practices

- Align raster preprocessing steps (extent, resolution, CRS) before risk calculation.
- Consider temporal analysis to track terrain changes.
- Calibrate thresholds/weights per mission if needed.
- Document assumptions; validate with known benchmarks.

---

## 📞 Support

- Use the generated expression guide for exact QGIS syntax.
- Review the comprehensive and component reports for QA.
- Integrate JSON outputs into dashboards or APIs as needed.

<div align="center" style="margin-top:12px;">

**🌙 Precision risk analytics for lunar terrain.**

</div> 
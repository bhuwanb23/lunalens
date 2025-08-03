# 🌑 LUNAR TERRAIN RISK ANALYSIS SYSTEM
## Comprehensive Real-Time Risk Assessment for Lunar Terrain

### 📋 OVERVIEW
This system provides a complete framework for analyzing lunar terrain risk using multiple parameters and generating real-time risk scores. The system processes any lunar terrain analysis report and applies standardized risk formulas to generate comprehensive risk assessments.

---

## 🎯 RISK SCORING FORMULAS

### 1. SLOPE RISK SCORE
**Formula:** `(slope / 60.0) * 100.0`
- **Input:** Slope angle in degrees (0-90°)
- **Output:** Risk score 0-100
- **Thresholds:**
  - 0-20°: Low risk (0-33.3)
  - 20-40°: Moderate risk (33.3-66.7)
  - 40-60°: High risk (66.7-100)
  - >60°: Extreme risk (100)

### 2. ASPECT RISK SCORE
**Formula:** `(distance_from_315° / 180.0) * 100.0`
- **Input:** Aspect in degrees (0-360°)
- **Output:** Risk score 0-100
- **Logic:** 315° is considered optimal (lowest risk)
- **Calculation:** Circular distance from 315°

### 3. HILLSHADE RISK SCORE
**Formula:** `(128.0 - hillshade) / 128.0 * 100.0`
- **Input:** Hillshade intensity (0-255)
- **Output:** Risk score 0-100
- **Logic:** 128 is neutral, lower values indicate shadows (higher risk)

### 4. CONTOUR DENSITY RISK SCORE
**Formula:** `(density / 10.0) * 100.0`
- **Input:** Contour lines per km²
- **Output:** Risk score 0-100
- **Logic:** Higher density = more complex terrain = higher risk

### 5. PROFILE GRADIENT RISK SCORE
**Formula:** `(gradient / 50.0) * 100.0`
- **Input:** Elevation change per 100m horizontal distance
- **Output:** Risk score 0-100
- **Logic:** Steeper gradients = higher risk

### 6. CRATER RATIO RISK SCORE
**Formula:** `(ratio / 30.0) * 100.0`
- **Input:** Crater depth ratio (depth/rim_elevation * 100%)
- **Output:** Risk score 0-100
- **Logic:** Deeper craters = higher risk

### 7. ROUGHNESS RISK SCORE
**Formula:** `(roughness / 10.0) * 100.0`
- **Input:** Terrain roughness index (TRI)
- **Output:** Risk score 0-100
- **Logic:** Rougher terrain = higher risk

### 8. ELEVATION RISK SCORE
**Formula:** `(elevation - 1000.0) / 1000.0 * 100.0`
- **Input:** Elevation in meters
- **Output:** Risk score 0-100
- **Bounds:**
  - <1000m: 0 risk
  - 1000-2000m: Linear scale
  - >2000m: 100 risk

---

## 📊 COMPOSITE RISK CALCULATION

### WEIGHTED FORMULA
```
Composite_Risk = Σ(Component_Risk × Component_Weight)
```

### WEIGHTS USED
- **Slope:** 0.30 (30%)
- **Aspect:** 0.15 (15%)
- **Hillshade:** 0.15 (15%)
- **Contour Density:** 0.10 (10%)
- **Profile Gradient:** 0.10 (10%)
- **Crater Ratio:** 0.05 (5%)
- **Roughness:** 0.10 (10%)
- **Elevation:** 0.05 (5%)

### COMPLETE FORMULA
```
Final_Risk = 
  0.30 × Risk_slope +
  0.15 × Risk_aspect +
  0.15 × Risk_hillshade +
  0.10 × Risk_contour_density +
  0.10 × Risk_profile_gradient +
  0.05 × Risk_crater_ratio +
  0.10 × Risk_roughness +
  0.05 × Risk_elevation
```

---

## 🎯 RISK LEVEL CLASSIFICATION

| Risk Score | Level | Description | Recommendations |
|------------|-------|-------------|-----------------|
| 0-20 | **LOW** | Safe terrain for lunar operations | Standard safety protocols sufficient |
| 20-40 | **MODERATE** | Moderate terrain challenges | Enhanced monitoring protocols |
| 40-60 | **HIGH** | High risk terrain - caution required | Strict safety measures, consider alternatives |
| 60-80 | **VERY HIGH** | Very high risk - extreme caution | Avoid if possible, emergency protocols |
| 80-100 | **EXTREME** | Extreme risk - avoid if possible | Mission postponement recommended |

---

## 🔧 QGIS EXPRESSIONS

### Individual Risk Expressions

#### 1. Slope Risk
```sql
("slope@1" / 60.0) * 100.0
```

#### 2. Aspect Risk
```sql
(
  (abs("aspect@1" - 315.0) >= 180.0) * (360.0 - abs("aspect@1" - 315.0))
  +
  (abs("aspect@1" - 315.0) < 180.0) * abs("aspect@1" - 315.0)
) / 180.0 * 100.0
```

#### 3. Hillshade Risk
```sql
(128.0 - "hillshade@1") / 128.0 * 100.0
```

#### 4. Elevation Risk
```sql
CASE
  WHEN "elevation@1" < 1000.0 THEN 0.0
  WHEN "elevation@1" > 2000.0 THEN 100.0
  ELSE ("elevation@1" - 1000.0) / 1000.0 * 100.0
END
```

#### 5. Roughness Risk
```sql
("roughness@1" / 10.0) * 100.0
```

### Composite Risk Expression
```sql
(
  0.30 * ("slope@1" / 60.0 * 100.0)
+ 0.15 * (
     (abs("aspect@1" - 315.0) >= 180.0) * (360.0 - abs("aspect@1" - 315.0))
     +
     (abs("aspect@1" - 315.0) < 180.0) * abs("aspect@1" - 315.0)
   ) / 180.0 * 100.0
+ 0.15 * (128.0 - "hillshade@1") / 128.0 * 100.0
+ 0.10 * ("contour_density@1" / 10.0 * 100.0)
+ 0.10 * ("profile_gradient@1" / 50.0 * 100.0)
+ 0.05 * ("crater_ratio@1" / 30.0 * 100.0)
+ 0.10 * ("roughness@1" / 10.0 * 100.0)
+ 0.05 * (("elevation@1" - 1000.0) / 1000.0 * 100.0)
)
```

### Risk Level Classification
```sql
CASE
  WHEN "composite_risk@1" < 20.0 THEN 'LOW'
  WHEN "composite_risk@1" < 40.0 THEN 'MODERATE'
  WHEN "composite_risk@1" < 60.0 THEN 'HIGH'
  WHEN "composite_risk@1" < 80.0 THEN 'VERY_HIGH'
  ELSE 'EXTREME'
END
```

---

## 🚀 USAGE INSTRUCTIONS

### 1. Real-Time Analysis
```bash
python lunar_risk_analysis.py
```
- Processes all available analysis reports
- Generates comprehensive risk assessment
- Outputs detailed report and JSON results

### 2. QGIS Desktop Usage
1. Load raster layers into QGIS
2. Open Raster Calculator
3. Copy appropriate expression
4. Set output path
5. Run calculation
6. Repeat for each component
7. Use composite expression for final assessment

### 3. Custom Analysis
```python
from lunar_risk_analysis import LunarRiskAnalyzer

analyzer = LunarRiskAnalyzer()
results = analyzer.process_analysis_reports(['report1.txt', 'report2.txt'])
```

---

## 📁 GENERATED FILES

### Analysis Results
- `comprehensive_lunar_risk_report.txt` - Human-readable risk report
- `lunar_risk_analysis_results.json` - Detailed JSON results
- `lunar_risk_analysis.py` - Main analysis script

### QGIS Tools
- `qgis_lunar_risk_expressions.py` - Expression generator
- `qgis_lunar_risk_workflow.py` - QGIS workflow script
- `qgis_lunar_risk_expressions_guide.txt` - Expression guide

---

## 📊 CURRENT ANALYSIS RESULTS

Based on your lunar terrain analysis reports:

### Composite Risk Score: **10.13/100** (LOW RISK)

### Individual Component Scores:
- **Slope Risk:** 19.23/100 (Gentle slopes)
- **Aspect Risk:** 0.00/100 (Optimal orientation)
- **Contour Density:** 1.21/100 (Low complexity)
- **Elevation Risk:** 0.00/100 (Safe elevation)
- **Roughness Risk:** 34.96/100 (Moderate terrain variation)
- **Profile Gradient:** 7.43/100 (Low gradient)
- **Hillshade Risk:** 0.00/100 (No data)
- **Crater Ratio:** 0.00/100 (No data)

### Recommendations:
- ✅ Terrain is generally safe for lunar operations
- ✅ Standard safety protocols sufficient
- ⚠️ Monitor terrain roughness for potential challenges

---

## 🔄 REAL-TIME MONITORING

The system can be used for:
1. **Pre-mission planning** - Assess landing site suitability
2. **Real-time monitoring** - Track terrain changes
3. **Risk mitigation** - Identify high-risk areas
4. **Mission optimization** - Select optimal routes

### Integration Points:
- QGIS Desktop for spatial analysis
- Python scripts for batch processing
- JSON output for API integration
- Real-time data feeds for live monitoring

---

## ⚠️ IMPORTANT NOTES

### Data Requirements:
- All input rasters must have same extent and resolution
- Use consistent coordinate reference system
- Validate results against known terrain features
- Consider temporal changes for monitoring

### Limitations:
- Formulas based on lunar-specific parameters
- May need adjustment for different terrain types
- Requires validation with field observations
- Consider local conditions and mission requirements

### Best Practices:
- Always validate results against optical imagery
- Use multiple data sources when available
- Consider temporal analysis for change detection
- Implement quality control procedures
- Document assumptions and limitations

---

## 📞 SUPPORT

For questions or issues:
1. Check the generated expression guide
2. Review the comprehensive risk report
3. Examine the JSON results for detailed data
4. Use the QGIS workflow script for automation

---

*Generated: 2025-08-03*
*System Version: 1.0*
*Lunar Terrain Risk Analysis Framework* 
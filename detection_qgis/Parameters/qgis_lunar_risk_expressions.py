#!/usr/bin/env python3
"""
🌑 QGIS LUNAR TERRAIN RISK EXPRESSIONS
======================================
Complete set of QGIS Raster Calculator expressions for lunar terrain risk analysis
Ready-to-use formulas for real-time risk assessment in QGIS Desktop
"""

class QGISLunarRiskExpressions:
    """
    QGIS Raster Calculator Expressions for Lunar Terrain Risk Analysis
    """
    
    def __init__(self):
        self.risk_weights = {
            'slope': 0.30,
            'aspect': 0.15,
            'hillshade': 0.15,
            'contour_density': 0.10,
            'profile_gradient': 0.10,
            'crater_ratio': 0.05,
            'roughness': 0.10,
            'elevation': 0.05
        }
    
    def get_slope_risk_expression(self, layer_name="slope@1"):
        """
        Slope Risk Expression
        Formula: (slope / 60.0) * 100.0
        """
        return f'("{layer_name}" / 60.0) * 100.0'
    
    def get_aspect_risk_expression(self, layer_name="aspect@1"):
        """
        Aspect Risk Expression
        Complex distance from 315° calculation
        """
        return f'''(
  (abs("{layer_name}" - 315.0) >= 180.0) * (360.0 - abs("{layer_name}" - 315.0))
  +
  (abs("{layer_name}" - 315.0) < 180.0) * abs("{layer_name}" - 315.0)
) / 180.0 * 100.0'''
    
    def get_hillshade_risk_expression(self, layer_name="hillshade@1"):
        """
        Hillshade Risk Expression
        Formula: (128.0 - hillshade) / 128.0 * 100.0
        """
        return f'(128.0 - "{layer_name}") / 128.0 * 100.0'
    
    def get_contour_density_risk_expression(self, layer_name="contour_density@1"):
        """
        Contour Density Risk Expression
        Formula: (density / 10.0) * 100.0
        """
        return f'("{layer_name}" / 10.0) * 100.0'
    
    def get_profile_gradient_risk_expression(self, layer_name="profile_gradient@1"):
        """
        Profile Gradient Risk Expression
        Formula: (gradient / 50.0) * 100.0
        """
        return f'("{layer_name}" / 50.0) * 100.0'
    
    def get_crater_ratio_risk_expression(self, layer_name="crater_ratio@1"):
        """
        Crater Depth Ratio Risk Expression
        Formula: (ratio / 30.0) * 100.0
        """
        return f'("{layer_name}" / 30.0) * 100.0'
    
    def get_roughness_risk_expression(self, layer_name="roughness@1"):
        """
        Terrain Roughness Risk Expression
        Formula: (roughness / 10.0) * 100.0
        """
        return f'("{layer_name}" / 10.0) * 100.0'
    
    def get_elevation_risk_expression(self, layer_name="elevation@1"):
        """
        Elevation Risk Expression with bounds
        Formula: (elevation - 1000.0) / 1000.0 * 100.0
        """
        return f'''CASE
  WHEN "{layer_name}" < 1000.0 THEN 0.0
  WHEN "{layer_name}" > 2000.0 THEN 100.0
  ELSE ("{layer_name}" - 1000.0) / 1000.0 * 100.0
END'''
    
    def get_composite_risk_expression(self, layer_names):
        """
        Complete Composite Risk Expression
        Weighted combination of all risk components
        """
        expressions = []
        
        if 'slope' in layer_names:
            slope_expr = self.get_slope_risk_expression(layer_names['slope'])
            expressions.append(f'{self.risk_weights["slope"]} * ({slope_expr})')
        
        if 'aspect' in layer_names:
            aspect_expr = self.get_aspect_risk_expression(layer_names['aspect'])
            expressions.append(f'{self.risk_weights["aspect"]} * ({aspect_expr})')
        
        if 'hillshade' in layer_names:
            hillshade_expr = self.get_hillshade_risk_expression(layer_names['hillshade'])
            expressions.append(f'{self.risk_weights["hillshade"]} * ({hillshade_expr})')
        
        if 'contour_density' in layer_names:
            contour_expr = self.get_contour_density_risk_expression(layer_names['contour_density'])
            expressions.append(f'{self.risk_weights["contour_density"]} * ({contour_expr})')
        
        if 'profile_gradient' in layer_names:
            gradient_expr = self.get_profile_gradient_risk_expression(layer_names['profile_gradient'])
            expressions.append(f'{self.risk_weights["profile_gradient"]} * ({gradient_expr})')
        
        if 'crater_ratio' in layer_names:
            crater_expr = self.get_crater_ratio_risk_expression(layer_names['crater_ratio'])
            expressions.append(f'{self.risk_weights["crater_ratio"]} * ({crater_expr})')
        
        if 'roughness' in layer_names:
            roughness_expr = self.get_roughness_risk_expression(layer_names['roughness'])
            expressions.append(f'{self.risk_weights["roughness"]} * ({roughness_expr})')
        
        if 'elevation' in layer_names:
            elevation_expr = self.get_elevation_risk_expression(layer_names['elevation'])
            expressions.append(f'{self.risk_weights["elevation"]} * ({elevation_expr})')
        
        return ' + '.join(expressions)
    
    def get_risk_level_expression(self, risk_layer="composite_risk@1"):
        """
        Risk Level Classification Expression
        """
        return f'''CASE
  WHEN "{risk_layer}" < 20.0 THEN 'LOW'
  WHEN "{risk_layer}" < 40.0 THEN 'MODERATE'
  WHEN "{risk_layer}" < 60.0 THEN 'HIGH'
  WHEN "{risk_layer}" < 80.0 THEN 'VERY_HIGH'
  ELSE 'EXTREME'
END'''
    
    def get_risk_category_expression(self, risk_layer="composite_risk@1"):
        """
        Risk Category Expression (1-10 scale)
        """
        return f'''CASE
  WHEN "{risk_layer}" < 10.0 THEN 1
  WHEN "{risk_layer}" < 20.0 THEN 2
  WHEN "{risk_layer}" < 30.0 THEN 3
  WHEN "{risk_layer}" < 40.0 THEN 4
  WHEN "{risk_layer}" < 50.0 THEN 5
  WHEN "{risk_layer}" < 60.0 THEN 6
  WHEN "{risk_layer}" < 70.0 THEN 7
  WHEN "{risk_layer}" < 80.0 THEN 8
  WHEN "{risk_layer}" < 90.0 THEN 9
  ELSE 10
END'''
    
    def generate_qgis_workflow(self, layer_names):
        """
        Generate complete QGIS workflow script
        """
        workflow = f"""# QGIS Lunar Terrain Risk Analysis Workflow
# Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

from qgis.core import QgsRasterLayer, QgsProject
from qgis.analysis import QgsNativeAlgorithms
import processing

# Initialize processing
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

# Layer names for risk calculation
LAYER_NAMES = {layer_names}

def calculate_individual_risks():
    \"\"\"
    Calculate individual risk components
    \"\"\"
    
    # Slope Risk
    slope_expr = r'{self.get_slope_risk_expression(layer_names.get("slope", "slope@1"))}'
    processing.run("qgis:rastercalculator", {{
        'EXPRESSION': slope_expr,
        'LAYERS': [LAYER_NAMES['slope']],
        'OUTPUT': 'slope_risk.tif'
    }})
    print("✅ Slope risk calculated")
    
    # Aspect Risk
    aspect_expr = r'''{self.get_aspect_risk_expression(layer_names.get("aspect", "aspect@1"))}'''
    processing.run("qgis:rastercalculator", {{
        'EXPRESSION': aspect_expr,
        'LAYERS': [LAYER_NAMES['aspect']],
        'OUTPUT': 'aspect_risk.tif'
    }})
    print("✅ Aspect risk calculated")
    
    # Elevation Risk
    elevation_expr = r'''{self.get_elevation_risk_expression(layer_names.get("elevation", "elevation@1"))}'''
    processing.run("qgis:rastercalculator", {{
        'EXPRESSION': elevation_expr,
        'LAYERS': [LAYER_NAMES['elevation']],
        'OUTPUT': 'elevation_risk.tif'
    }})
    print("✅ Elevation risk calculated")
    
    # Roughness Risk
    roughness_expr = r'{self.get_roughness_risk_expression(layer_names.get("roughness", "roughness@1"))}'
    processing.run("qgis:rastercalculator", {{
        'EXPRESSION': roughness_expr,
        'LAYERS': [LAYER_NAMES['roughness']],
        'OUTPUT': 'roughness_risk.tif'
    }})
    print("✅ Roughness risk calculated")

def calculate_composite_risk():
    \"\"\"
    Calculate composite risk score
    \"\"\"
    composite_expr = r'''{self.get_composite_risk_expression(layer_names)}'''
    
    # Collect available risk layers
    risk_layers = []
    for component in ['slope', 'aspect', 'elevation', 'roughness']:
        if component in LAYER_NAMES:
            risk_layers.append(f'{{component}}_risk@1')
    
    processing.run("qgis:rastercalculator", {{
        'EXPRESSION': composite_expr,
        'LAYERS': risk_layers,
        'OUTPUT': 'composite_risk.tif'
    }})
    print("✅ Composite risk calculated")

def classify_risk_levels():
    \"\"\"
    Classify risk levels
    \"\"\"
    risk_level_expr = r'''{self.get_risk_level_expression()}'''
    
    processing.run("qgis:rastercalculator", {{
        'EXPRESSION': risk_level_expr,
        'LAYERS': ['composite_risk@1'],
        'OUTPUT': 'risk_levels.tif'
    }})
    print("✅ Risk levels classified")

def main():
    \"\"\"
    Execute complete workflow
    \"\"\"
    print("🚀 Starting Lunar Terrain Risk Analysis...")
    
    calculate_individual_risks()
    calculate_composite_risk()
    classify_risk_levels()
    
    print("✅ Risk analysis workflow completed!")

if __name__ == "__main__":
    main()
"""
        return workflow
    
    def generate_expression_guide(self):
        """
        Generate comprehensive expression guide
        """
        guide = f"""🌑 QGIS LUNAR TERRAIN RISK EXPRESSIONS GUIDE
============================================================

📊 INDIVIDUAL RISK COMPONENT EXPRESSIONS
----------------------------------------

1. SLOPE RISK
Expression: {self.get_slope_risk_expression()}
Description: Normalizes slope values (0-60°) to risk scale (0-100)
Usage: Apply to slope raster layer

2. ASPECT RISK
Expression: {self.get_aspect_risk_expression()}
Description: Calculates distance from optimal 315° aspect
Usage: Apply to aspect raster layer

3. HILLSHADE RISK
Expression: {self.get_hillshade_risk_expression()}
Description: Inverts hillshade values (0-255) to risk scale
Usage: Apply to hillshade raster layer

4. CONTOUR DENSITY RISK
Expression: {self.get_contour_density_risk_expression()}
Description: Normalizes contour density to risk scale
Usage: Apply to contour density raster layer

5. PROFILE GRADIENT RISK
Expression: {self.get_profile_gradient_risk_expression()}
Description: Normalizes elevation change per 100m to risk scale
Usage: Apply to profile gradient raster layer

6. CRATER RATIO RISK
Expression: {self.get_crater_ratio_risk_expression()}
Description: Normalizes crater depth ratio to risk scale
Usage: Apply to crater ratio raster layer

7. ROUGHNESS RISK
Expression: {self.get_roughness_risk_expression()}
Description: Normalizes terrain roughness to risk scale
Usage: Apply to roughness raster layer

8. ELEVATION RISK
Expression: {self.get_elevation_risk_expression()}
Description: Bounded elevation risk calculation
Usage: Apply to elevation raster layer

📈 COMPOSITE RISK EXPRESSION
-----------------------------
Complete weighted formula for all components:

{self.get_composite_risk_expression({
    'slope': 'slope@1',
    'aspect': 'aspect@1',
    'hillshade': 'hillshade@1',
    'contour_density': 'contour_density@1',
    'profile_gradient': 'profile_gradient@1',
    'crater_ratio': 'crater_ratio@1',
    'roughness': 'roughness@1',
    'elevation': 'elevation@1'
})}

🎯 RISK LEVEL CLASSIFICATION
-----------------------------
Expression: {self.get_risk_level_expression()}

📋 USAGE INSTRUCTIONS
---------------------
1. Load all required raster layers into QGIS
2. Open Raster Calculator (Processing > Toolbox > Raster analysis > Raster calculator)
3. Copy and paste the appropriate expression
4. Set output file path
5. Run calculation
6. Repeat for each component
7. Use composite expression for final risk assessment

⚠️  IMPORTANT NOTES
-------------------
• Ensure all input rasters have the same extent and resolution
• Use consistent coordinate reference system
• Validate results against known terrain features
• Consider temporal changes for monitoring applications
• Risk scores range from 0 (Safe) to 100 (Extreme Risk)

🔧 WEIGHTS USED
----------------
{chr(10).join([f"• {component.replace('_', ' ').title()}: {weight:.2f}" for component, weight in self.risk_weights.items()])}

📊 RISK LEVELS
---------------
• LOW (0-20): Safe terrain for lunar operations
• MODERATE (20-40): Moderate terrain challenges
• HIGH (40-60): High risk terrain - caution required
• VERY HIGH (60-80): Very high risk - extreme caution
• EXTREME (80-100): Extreme risk - avoid if possible
"""
        return guide

def main():
    """
    Generate all QGIS expressions and guides
    """
    from datetime import datetime
    
    expressions = QGISLunarRiskExpressions()
    
    # Example layer names
    example_layers = {
        'slope': 'slope@1',
        'aspect': 'aspect@1',
        'elevation': 'elevation@1',
        'roughness': 'roughness@1'
    }
    
    print("🌙 QGIS Lunar Terrain Risk Expressions Generator")
    print("=" * 50)
    
    # Generate individual expressions
    print("\n📊 Individual Risk Expressions:")
    print(f"Slope: {expressions.get_slope_risk_expression()}")
    print(f"Aspect: {expressions.get_aspect_risk_expression()}")
    print(f"Elevation: {expressions.get_elevation_risk_expression()}")
    print(f"Roughness: {expressions.get_roughness_risk_expression()}")
    
    # Generate composite expression
    print(f"\n📈 Composite Risk Expression:")
    composite_expr = expressions.get_composite_risk_expression(example_layers)
    print(composite_expr)
    
    # Generate risk level classification
    print(f"\n🎯 Risk Level Classification:")
    risk_level_expr = expressions.get_risk_level_expression()
    print(risk_level_expr)
    
    # Generate workflow script
    print(f"\n🔧 Generating QGIS workflow script...")
    workflow = expressions.generate_qgis_workflow(example_layers)
    with open("qgis_lunar_risk_workflow.py", "w", encoding="utf-8") as f:
        f.write(workflow)
    
    # Generate expression guide
    print(f"\n📖 Generating expression guide...")
    guide = expressions.generate_expression_guide()
    with open("qgis_lunar_risk_expressions_guide.txt", "w", encoding="utf-8") as f:
        f.write(guide)
    
    print("\n✅ All expressions and guides generated successfully!")
    print("📁 Generated files:")
    print("   - qgis_lunar_risk_workflow.py")
    print("   - qgis_lunar_risk_expressions_guide.txt")

if __name__ == "__main__":
    main() 
import sys
import os
from typing import Dict, List, Optional

class QGISRiskExpressionGenerator:
    """
    QGIS Raster Calculator Expression Generator for Lunar Terrain Risk Analysis
    Generates QGIS-compatible expressions for real-time risk calculation
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
        
    def generate_slope_risk_expression(self, slope_layer_name: str = "slope@1") -> str:
        """
        Generate QGIS expression for slope risk calculation
        Formula: (slope / 60.0) * 100.0
        """
        return f'("{slope_layer_name}" / 60.0) * 100.0'
    
    def generate_aspect_risk_expression(self, aspect_layer_name: str = "aspect@1") -> str:
        """
        Generate QGIS expression for aspect risk calculation
        Formula: Complex distance from 315° calculation
        """
        return f'''(
  (abs("{aspect_layer_name}" - 315.0) >= 180.0) * (360.0 - abs("{aspect_layer_name}" - 315.0))
  +
  (abs("{aspect_layer_name}" - 315.0) < 180.0) * abs("{aspect_layer_name}" - 315.0)
) / 180.0 * 100.0'''
    
    def generate_hillshade_risk_expression(self, hillshade_layer_name: str = "hillshade@1") -> str:
        """
        Generate QGIS expression for hillshade risk calculation
        Formula: (128.0 - hillshade) / 128.0 * 100.0
        """
        return f'(128.0 - "{hillshade_layer_name}") / 128.0 * 100.0'
    
    def generate_contour_density_risk_expression(self, contour_layer_name: str = "contour_density@1") -> str:
        """
        Generate QGIS expression for contour density risk calculation
        Formula: (density / 10.0) * 100.0
        """
        return f'("{contour_layer_name}" / 10.0) * 100.0'
    
    def generate_profile_gradient_risk_expression(self, gradient_layer_name: str = "profile_gradient@1") -> str:
        """
        Generate QGIS expression for profile gradient risk calculation
        Formula: (gradient / 50.0) * 100.0
        """
        return f'("{gradient_layer_name}" / 50.0) * 100.0'
    
    def generate_crater_ratio_risk_expression(self, crater_layer_name: str = "crater_ratio@1") -> str:
        """
        Generate QGIS expression for crater depth ratio risk calculation
        Formula: (ratio / 30.0) * 100.0
        """
        return f'("{crater_layer_name}" / 30.0) * 100.0'
    
    def generate_roughness_risk_expression(self, roughness_layer_name: str = "roughness@1") -> str:
        """
        Generate QGIS expression for terrain roughness risk calculation
        Formula: (roughness / 10.0) * 100.0
        """
        return f'("{roughness_layer_name}" / 10.0) * 100.0'
    
    def generate_elevation_risk_expression(self, elevation_layer_name: str = "elevation@1") -> str:
        """
        Generate QGIS expression for elevation risk calculation
        Formula: (elevation - 1000.0) / 1000.0 * 100.0 with bounds
        """
        return f'''CASE
  WHEN "{elevation_layer_name}" < 1000.0 THEN 0.0
  WHEN "{elevation_layer_name}" > 2000.0 THEN 100.0
  ELSE ("{elevation_layer_name}" - 1000.0) / 1000.0 * 100.0
END'''
    
    def generate_composite_risk_expression(self, layer_names: Dict[str, str]) -> str:
        """
        Generate complete composite risk expression for QGIS Raster Calculator
        """
        # Generate individual risk expressions
        risk_expressions = {}
        
        if 'slope' in layer_names:
            risk_expressions['slope'] = self.generate_slope_risk_expression(layer_names['slope'])
        
        if 'aspect' in layer_names:
            risk_expressions['aspect'] = self.generate_aspect_risk_expression(layer_names['aspect'])
        
        if 'hillshade' in layer_names:
            risk_expressions['hillshade'] = self.generate_hillshade_risk_expression(layer_names['hillshade'])
        
        if 'contour_density' in layer_names:
            risk_expressions['contour_density'] = self.generate_contour_density_risk_expression(layer_names['contour_density'])
        
        if 'profile_gradient' in layer_names:
            risk_expressions['profile_gradient'] = self.generate_profile_gradient_risk_expression(layer_names['profile_gradient'])
        
        if 'crater_ratio' in layer_names:
            risk_expressions['crater_ratio'] = self.generate_crater_ratio_risk_expression(layer_names['crater_ratio'])
        
        if 'roughness' in layer_names:
            risk_expressions['roughness'] = self.generate_roughness_risk_expression(layer_names['roughness'])
        
        if 'elevation' in layer_names:
            risk_expressions['elevation'] = self.generate_elevation_risk_expression(layer_names['elevation'])
        
        # Build composite expression
        composite_parts = []
        
        for component, expression in risk_expressions.items():
            weight = self.risk_weights.get(component, 0.0)
            weighted_expression = f'{weight} * ({expression})'
            composite_parts.append(weighted_expression)
        
        # Join all parts
        composite_expression = ' + '.join(composite_parts)
        
        return composite_expression
    
    def generate_risk_level_expression(self, risk_score_layer: str = "composite_risk@1") -> str:
        """
        Generate expression to classify risk levels based on composite score
        """
        return f'''CASE
  WHEN "{risk_score_layer}" < 20.0 THEN 'LOW'
  WHEN "{risk_score_layer}" < 40.0 THEN 'MODERATE'
  WHEN "{risk_score_layer}" < 60.0 THEN 'HIGH'
  WHEN "{risk_score_layer}" < 80.0 THEN 'VERY_HIGH'
  ELSE 'EXTREME'
END'''
    
    def generate_risk_category_expression(self, risk_score_layer: str = "composite_risk@1") -> str:
        """
        Generate expression to create risk categories (0-100 scale)
        """
        return f'''CASE
  WHEN "{risk_score_layer}" < 10.0 THEN 1
  WHEN "{risk_score_layer}" < 20.0 THEN 2
  WHEN "{risk_score_layer}" < 30.0 THEN 3
  WHEN "{risk_score_layer}" < 40.0 THEN 4
  WHEN "{risk_score_layer}" < 50.0 THEN 5
  WHEN "{risk_score_layer}" < 60.0 THEN 6
  WHEN "{risk_score_layer}" < 70.0 THEN 7
  WHEN "{risk_score_layer}" < 80.0 THEN 8
  WHEN "{risk_score_layer}" < 90.0 THEN 9
  ELSE 10
END'''
    
    def generate_qgis_workflow_script(self, layer_names: Dict[str, str], output_path: str = None) -> str:
        """
        Generate a complete QGIS Python script for risk analysis workflow
        """
        script_content = f'''# QGIS Lunar Terrain Risk Analysis Workflow
# Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

from qgis.core import QgsRasterLayer, QgsProject
from qgis.analysis import QgsNativeAlgorithms
import processing

# Initialize processing
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

# Layer names for risk calculation
LAYER_NAMES = {layer_names}

# Risk weights
RISK_WEIGHTS = {self.risk_weights}

def calculate_individual_risk_components():
    """
    Calculate individual risk components using Raster Calculator
    """
    project = QgsProject.instance()
    
    # Slope Risk
    if 'slope' in LAYER_NAMES:
        slope_expression = r'{self.generate_slope_risk_expression(layer_names.get("slope", "slope@1"))}'
        processing.run("qgis:rastercalculator", {{
            'EXPRESSION': slope_expression,
            'LAYERS': [LAYER_NAMES['slope']],
            'OUTPUT': 'slope_risk.tif'
        }})
        print("✅ Slope risk calculated")
    
    # Aspect Risk
    if 'aspect' in LAYER_NAMES:
        aspect_expression = r'''{self.generate_aspect_risk_expression(layer_names.get("aspect", "aspect@1"))}'''
        processing.run("qgis:rastercalculator", {{
            'EXPRESSION': aspect_expression,
            'LAYERS': [LAYER_NAMES['aspect']],
            'OUTPUT': 'aspect_risk.tif'
        }})
        print("✅ Aspect risk calculated")
    
    # Hillshade Risk
    if 'hillshade' in LAYER_NAMES:
        hillshade_expression = r'{self.generate_hillshade_risk_expression(layer_names.get("hillshade", "hillshade@1"))}'
        processing.run("qgis:rastercalculator", {{
            'EXPRESSION': hillshade_expression,
            'LAYERS': [LAYER_NAMES['hillshade']],
            'OUTPUT': 'hillshade_risk.tif'
        }})
        print("✅ Hillshade risk calculated")
    
    # Elevation Risk
    if 'elevation' in LAYER_NAMES:
        elevation_expression = r'''{self.generate_elevation_risk_expression(layer_names.get("elevation", "elevation@1"))}'''
        processing.run("qgis:rastercalculator", {{
            'EXPRESSION': elevation_expression,
            'LAYERS': [LAYER_NAMES['elevation']],
            'OUTPUT': 'elevation_risk.tif'
        }})
        print("✅ Elevation risk calculated")
    
    # Roughness Risk
    if 'roughness' in LAYER_NAMES:
        roughness_expression = r'{self.generate_roughness_risk_expression(layer_names.get("roughness", "roughness@1"))}'
        processing.run("qgis:rastercalculator", {{
            'EXPRESSION': roughness_expression,
            'LAYERS': [LAYER_NAMES['roughness']],
            'OUTPUT': 'roughness_risk.tif'
        }})
        print("✅ Roughness risk calculated")

def calculate_composite_risk():
    """
    Calculate composite risk score using weighted formula
    """
    composite_expression = r'''{self.generate_composite_risk_expression(layer_names)}'''
    
    # Collect all available risk layers
    risk_layers = []
    for component in ['slope', 'aspect', 'hillshade', 'elevation', 'roughness']:
        if component in LAYER_NAMES:
            risk_layers.append(f'{{component}}_risk@1')
    
    processing.run("qgis:rastercalculator", {{
        'EXPRESSION': composite_expression,
        'LAYERS': risk_layers,
        'OUTPUT': 'composite_risk.tif'
    }})
    print("✅ Composite risk calculated")

def classify_risk_levels():
    """
    Classify risk levels based on composite score
    """
    risk_level_expression = r'''{self.generate_risk_level_expression()}'''
    
    processing.run("qgis:rastercalculator", {{
        'EXPRESSION': risk_level_expression,
        'LAYERS': ['composite_risk@1'],
        'OUTPUT': 'risk_levels.tif'
    }})
    print("✅ Risk levels classified")

def main():
    """
    Execute complete risk analysis workflow
    """
    print("🚀 Starting Lunar Terrain Risk Analysis...")
    
    # Step 1: Calculate individual risk components
    calculate_individual_risk_components()
    
    # Step 2: Calculate composite risk
    calculate_composite_risk()
    
    # Step 3: Classify risk levels
    classify_risk_levels()
    
    print("✅ Risk analysis workflow completed!")
    print("📁 Output files:")
    print("   - slope_risk.tif")
    print("   - aspect_risk.tif")
    print("   - hillshade_risk.tif")
    print("   - elevation_risk.tif")
    print("   - roughness_risk.tif")
    print("   - composite_risk.tif")
    print("   - risk_levels.tif")

if __name__ == "__main__":
    main()
'''
        
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(script_content)
                print(f"✅ QGIS workflow script saved to: {output_path}")
            except Exception as e:
                print(f"❌ Error saving script: {e}")
        
        return script_content
    
    def generate_expression_guide(self) -> str:
        """
        Generate a comprehensive guide for all risk calculation expressions
        """
        guide_content = """🌑 QGIS LUNAR TERRAIN RISK CALCULATION EXPRESSIONS
============================================================

📊 INDIVIDUAL RISK COMPONENT EXPRESSIONS
----------------------------------------

1. SLOPE RISK
Expression: ("slope@1" / 60.0) * 100.0
Description: Normalizes slope values (0-60°) to risk scale (0-100)
Usage: Apply to slope raster layer

2. ASPECT RISK
Expression: (
  (abs("aspect@1" - 315.0) >= 180.0) * (360.0 - abs("aspect@1" - 315.0))
  +
  (abs("aspect@1" - 315.0) < 180.0) * abs("aspect@1" - 315.0)
) / 180.0 * 100.0
Description: Calculates distance from optimal 315° aspect
Usage: Apply to aspect raster layer

3. HILLSHADE RISK
Expression: (128.0 - "hillshade@1") / 128.0 * 100.0
Description: Inverts hillshade values (0-255) to risk scale
Usage: Apply to hillshade raster layer

4. CONTOUR DENSITY RISK
Expression: ("contour_density@1" / 10.0) * 100.0
Description: Normalizes contour density to risk scale
Usage: Apply to contour density raster layer

5. PROFILE GRADIENT RISK
Expression: ("profile_gradient@1" / 50.0) * 100.0
Description: Normalizes elevation change per 100m to risk scale
Usage: Apply to profile gradient raster layer

6. CRATER RATIO RISK
Expression: ("crater_ratio@1" / 30.0) * 100.0
Description: Normalizes crater depth ratio to risk scale
Usage: Apply to crater ratio raster layer

7. ROUGHNESS RISK
Expression: ("roughness@1" / 10.0) * 100.0
Description: Normalizes terrain roughness to risk scale
Usage: Apply to roughness raster layer

8. ELEVATION RISK
Expression: CASE
  WHEN "elevation@1" < 1000.0 THEN 0.0
  WHEN "elevation@1" > 2000.0 THEN 100.0
  ELSE ("elevation@1" - 1000.0) / 1000.0 * 100.0
END
Description: Bounded elevation risk calculation
Usage: Apply to elevation raster layer

📈 COMPOSITE RISK EXPRESSION
-----------------------------
Complete weighted formula for all components:

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

🎯 RISK LEVEL CLASSIFICATION
-----------------------------
Expression: CASE
  WHEN "composite_risk@1" < 20.0 THEN 'LOW'
  WHEN "composite_risk@1" < 40.0 THEN 'MODERATE'
  WHEN "composite_risk@1" < 60.0 THEN 'HIGH'
  WHEN "composite_risk@1" < 80.0 THEN 'VERY_HIGH'
  ELSE 'EXTREME'
END

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
"""
        
        return guide_content

# Example usage
if __name__ == "__main__":
    from datetime import datetime
    
    generator = QGISRiskExpressionGenerator()
    
    # Example layer names (replace with actual layer names)
    example_layers = {
        'slope': 'slope@1',
        'aspect': 'aspect@1',
        'hillshade': 'hillshade@1',
        'elevation': 'elevation@1',
        'roughness': 'roughness@1'
    }
    
    print("🌙 QGIS Lunar Terrain Risk Expression Generator")
    print("=" * 50)
    
    # Generate individual expressions
    print("\n📊 Individual Risk Expressions:")
    print(f"Slope: {generator.generate_slope_risk_expression()}")
    print(f"Aspect: {generator.generate_aspect_risk_expression()}")
    print(f"Hillshade: {generator.generate_hillshade_risk_expression()}")
    print(f"Elevation: {generator.generate_elevation_risk_expression()}")
    print(f"Roughness: {generator.generate_roughness_risk_expression()}")
    
    # Generate composite expression
    print(f"\n📈 Composite Risk Expression:")
    composite_expr = generator.generate_composite_risk_expression(example_layers)
    print(composite_expr)
    
    # Generate risk level classification
    print(f"\n🎯 Risk Level Classification:")
    risk_level_expr = generator.generate_risk_level_expression()
    print(risk_level_expr)
    
    # Generate workflow script
    print(f"\n🔧 Generating QGIS workflow script...")
    generator.generate_qgis_workflow_script(example_layers, "lunar_risk_workflow.py")
    
    # Generate expression guide
    print(f"\n📖 Generating expression guide...")
    guide = generator.generate_expression_guide()
    with open("qgis_risk_expressions_guide.txt", "w", encoding="utf-8") as f:
        f.write(guide)
    
    print("\n✅ All expressions and guides generated successfully!")
    print("📁 Generated files:")
    print("   - lunar_risk_workflow.py")
    print("   - qgis_risk_expressions_guide.txt") 
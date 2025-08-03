#!/usr/bin/env python3
"""
Convert JSON risk analysis results to readable text format
"""

import json
from datetime import datetime

def convert_json_to_text(json_file_path, output_file_path):
    """
    Convert JSON risk analysis results to readable text format
    """
    try:
        # Read JSON file
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Generate text report
        text_content = f"""🌑 LUNAR TERRAIN RISK ANALYSIS RESULTS
============================================================
Generated: {data['timestamp']}

📊 COMPOSITE RISK ASSESSMENT
------------------------------
• Overall Risk Score: {data['composite_risk_score']:.2f}/100
• Risk Level: {data['risk_level']}
• Risk Description: {data['risk_description']}

📋 INDIVIDUAL RISK COMPONENTS
------------------------------
"""
        
        # Add individual risk scores
        for component, score in data['individual_risk_scores'].items():
            weight = {
                'slope': 0.30,
                'aspect': 0.15,
                'hillshade': 0.15,
                'contour_density': 0.10,
                'profile_gradient': 0.10,
                'crater_ratio': 0.05,
                'roughness': 0.10,
                'elevation': 0.05
            }.get(component, 0.0)
            
            weighted_score = score * weight
            text_content += f"• {component.upper().replace('_', ' ')}:\n"
            text_content += f"  - Risk Score: {score:.2f}/100\n"
            text_content += f"  - Weight: {weight:.2f}\n"
            text_content += f"  - Weighted Contribution: {weighted_score:.2f}\n\n"
        
        # Add analysis summary
        text_content += f"""📈 ANALYSIS SUMMARY
------------------------------
• Total Reports Processed: {data['analysis_summary']['total_reports_processed']}
• Available Components: {', '.join(data['analysis_summary']['available_components'])}
• Missing Components: {', '.join(data['analysis_summary']['missing_components'])}

📊 DETAILED REPORT DATA
------------------------------
"""
        
        # Add detailed parsed reports
        for report_type, report_data in data['parsed_reports'].items():
            text_content += f"\n🔍 {report_type.upper().replace('_', ' ')} ANALYSIS:\n"
            text_content += f"  - Timestamp: {report_data.get('timestamp', 'N/A')}\n"
            text_content += f"  - Layer Name: {report_data.get('layer_name', 'N/A')}\n"
            text_content += f"  - Risk Level: {report_data.get('risk_level', 'N/A')}\n"
            
            if report_data.get('risk_factors'):
                text_content += f"  - Risk Factors: {', '.join(report_data['risk_factors'])}\n"
            
            # Add key statistics
            if report_data.get('statistics'):
                text_content += f"  - Key Statistics:\n"
                stats = report_data['statistics']
                key_stats = ['min', 'max', 'mean', 'std', 'std_dev']
                for stat in key_stats:
                    if stat in stats:
                        text_content += f"    * {stat.upper()}: {stats[stat]}\n"
                    elif f"{stat}_dev" in stats:
                        text_content += f"    * {stat.upper()}: {stats[f'{stat}_dev']}\n"
            
            text_content += "\n"
        
        # Add risk mitigation recommendations
        risk_score = data['composite_risk_score']
        text_content += f"""🎯 RISK MITIGATION RECOMMENDATIONS
----------------------------------------
"""
        
        if risk_score < 20:
            text_content += "• Terrain is generally safe for lunar operations\n"
            text_content += "• Standard safety protocols sufficient\n"
        elif risk_score < 40:
            text_content += "• Implement enhanced monitoring protocols\n"
            text_content += "• Consider alternative landing sites if available\n"
        elif risk_score < 60:
            text_content += "• High risk terrain - implement strict safety measures\n"
            text_content += "• Consider mission postponement if possible\n"
        elif risk_score < 80:
            text_content += "• Very high risk - avoid this terrain if possible\n"
            text_content += "• Implement emergency protocols\n"
        else:
            text_content += "• EXTREME RISK - AVOID THIS TERRAIN\n"
            text_content += "• Mission should be postponed or redirected\n"
        
        text_content += f"""
🔧 TECHNICAL DETAILS
------------------------------
• Risk Calculation Method: Weighted composite scoring
• Maximum Individual Risk: {max(data['individual_risk_scores'].values()):.2f}
• Minimum Individual Risk: {min(data['individual_risk_scores'].values()):.2f}
• Risk Score Range: 0-100 (0 = Safe, 100 = Extreme Risk)

📝 FORMULA USED
------------------------------
Composite Risk = Σ(Component_Risk × Component_Weight)
Where weights sum to 1.0 and individual risks are normalized to 0-100 scale.

📊 WEIGHTS USED
------------------------------
• Slope: 0.30 (30%)
• Aspect: 0.15 (15%)
• Hillshade: 0.15 (15%)
• Contour Density: 0.10 (10%)
• Profile Gradient: 0.10 (10%)
• Crater Ratio: 0.05 (5%)
• Roughness: 0.10 (10%)
• Elevation: 0.05 (5%)

🎯 RISK LEVELS
------------------------------
• LOW (0-20): Safe terrain for lunar operations
• MODERATE (20-40): Moderate terrain challenges
• HIGH (40-60): High risk terrain - caution required
• VERY HIGH (60-80): Very high risk - extreme caution
• EXTREME (80-100): Extreme risk - avoid if possible

---
Generated from JSON data: {json_file_path}
Converted: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        # Write to text file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        print(f"✅ Successfully converted JSON to text format!")
        print(f"📁 Output saved to: {output_file_path}")
        
        return text_content
        
    except Exception as e:
        print(f"❌ Error converting JSON to text: {e}")
        return None

def main():
    """
    Convert the lunar risk analysis JSON results to text format
    """
    json_file = "lunar_risk_analysis_results.json"
    output_file = "lunar_risk_analysis_results.txt"
    
    print("🔄 Converting JSON risk analysis results to text format...")
    
    result = convert_json_to_text(json_file, output_file)
    
    if result:
        print(f"\n📄 Text report preview (first 500 characters):")
        print("=" * 50)
        print(result[:500] + "..." if len(result) > 500 else result)
        print("=" * 50)
    else:
        print("❌ Failed to convert JSON to text format")

if __name__ == "__main__":
    main() 
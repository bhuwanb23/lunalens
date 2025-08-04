#!/usr/bin/env python3
"""
🌑 LUNAR TERRAIN RISK ANALYSIS SCRIPT
=====================================
Comprehensive risk assessment for lunar terrain analysis reports
Processes any lunar terrain analysis report and generates real-time risk scores
"""

import os
import re
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

class LunarRiskAnalyzer:
    """
    Comprehensive Lunar Terrain Risk Analyzer
    Processes analysis reports and generates real-time risk assessments
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
        self.analysis_results = {}
        
    def parse_report_file(self, report_path: str) -> Dict[str, Any]:
        """
        Parse any lunar terrain analysis report file and extract relevant data
        """
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Initialize data structure
            report_data = {
                'timestamp': None,
                'layer_name': None,
                'risk_level': None,
                'risk_factors': [],
                'statistics': {},
                'thresholds': {},
                'analysis_type': None
            }
            
            # Extract timestamp
            timestamp_match = re.search(r'Generated:\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', content)
            if timestamp_match:
                report_data['timestamp'] = timestamp_match.group(1)
            
            # Extract layer name
            layer_match = re.search(r'Layer:\s*([^\n]+)', content)
            if layer_match:
                report_data['layer_name'] = layer_match.group(1).strip()
            
            # Extract risk level
            risk_match = re.search(r'Risk Level:\s*([^\n]+)', content)
            if risk_match:
                report_data['risk_level'] = risk_match.group(1).strip()
            
            # Extract risk factors
            risk_factors_match = re.search(r'Risk Factors:\s*([^\n]+)', content)
            if risk_factors_match:
                factors = risk_factors_match.group(1).strip()
                report_data['risk_factors'] = [f.strip() for f in factors.split(',')]
            
            # Extract statistics - improved parsing
            stats_section = re.search(r'Statistics:(.*?)(?=\n\n|\n[A-Z]|$)', content, re.DOTALL)
            if stats_section:
                stats_text = stats_section.group(1)
                # Parse various statistics with improved regex
                for line in stats_text.split('\n'):
                    line = line.strip()
                    if ':' in line and not line.startswith('-') and not line.startswith('•'):
                        key, value = line.split(':', 1)
                        key = key.strip().lower().replace(' ', '_').replace('-', '_')
                        value = value.strip()
                        
                        # Try to extract numeric values with improved regex
                        numeric_match = re.search(r'([+-]?\d*\.?\d+)', value)
                        if numeric_match:
                            try:
                                report_data['statistics'][key] = float(numeric_match.group(1))
                            except ValueError:
                                report_data['statistics'][key] = value
                        else:
                            report_data['statistics'][key] = value
            
            # Also look for statistics in bullet point format
            bullet_stats = re.findall(r'•\s*([^:]+):\s*([^\n]+)', content)
            for key, value in bullet_stats:
                key = key.strip().lower().replace(' ', '_').replace('-', '_')
                value = value.strip()
                
                # Try to extract numeric values
                numeric_match = re.search(r'([+-]?\d*\.?\d+)', value)
                if numeric_match:
                    try:
                        report_data['statistics'][key] = float(numeric_match.group(1))
                    except ValueError:
                        report_data['statistics'][key] = value
                else:
                    report_data['statistics'][key] = value
            
            # Parse statistics in dash format (e.g., "  - Min: 0.00")
            dash_stats = re.findall(r'\s*-\s*([^:]+):\s*([^\n]+)', content)
            for key, value in dash_stats:
                key = key.strip().lower().replace(' ', '_').replace('-', '_')
                value = value.strip()
                
                # Try to extract numeric values
                numeric_match = re.search(r'([+-]?\d*\.?\d+)', value)
                if numeric_match:
                    try:
                        report_data['statistics'][key] = float(numeric_match.group(1))
                    except ValueError:
                        report_data['statistics'][key] = value
                else:
                    report_data['statistics'][key] = value
            
            # Extract thresholds
            thresholds_section = re.search(r'Thresholds:(.*?)(?=\n\n|\n[A-Z]|$)', content, re.DOTALL)
            if thresholds_section:
                thresholds_text = thresholds_section.group(1)
                for line in thresholds_text.split('\n'):
                    line = line.strip()
                    if ':' in line and not line.startswith('-'):
                        key, value = line.split(':', 1)
                        key = key.strip().lower().replace(' ', '_')
                        value = value.strip()
                        
                        numeric_match = re.search(r'([+-]?\d*\.?\d+)', value)
                        if numeric_match:
                            try:
                                report_data['thresholds'][key] = float(numeric_match.group(1))
                            except ValueError:
                                report_data['thresholds'][key] = value
                        else:
                            report_data['thresholds'][key] = value
            
            # Determine analysis type based on filename or content
            if 'slope' in report_path.lower():
                report_data['analysis_type'] = 'slope'
            elif 'aspect' in report_path.lower():
                report_data['analysis_type'] = 'aspect'
            elif 'curvature' in report_path.lower():
                report_data['analysis_type'] = 'curvature'
            elif 'elevation' in report_path.lower():
                report_data['analysis_type'] = 'elevation'
            elif 'hillshade' in report_path.lower():
                report_data['analysis_type'] = 'hillshade'
            elif 'contour' in report_path.lower():
                report_data['analysis_type'] = 'contour'
            elif 'tri' in report_path.lower() or 'ruggedness' in report_path.lower():
                report_data['analysis_type'] = 'roughness'
            elif 'crater' in report_path.lower():
                report_data['analysis_type'] = 'crater'
            elif 'landslide' in report_path.lower():
                report_data['analysis_type'] = 'landslide'
            elif 'scarps' in report_path.lower() or 'headwalls' in report_path.lower():
                report_data['analysis_type'] = 'scarps_headwalls'
            
            print(f"✅ Successfully parsed report: {os.path.basename(report_path)}")
            print(f"   - Analysis Type: {report_data['analysis_type']}")
            print(f"   - Risk Level: {report_data['risk_level']}")
            print(f"   - Statistics: {len(report_data['statistics'])} values extracted")
            if report_data['statistics']:
                print(f"   - Sample stats: {list(report_data['statistics'].keys())[:3]}")
            
            return report_data
            
        except Exception as e:
            print(f"❌ Error parsing report file {report_path}: {e}")
            return {}
    
    def calculate_slope_risk_score(self, slope_data: Dict[str, Any]) -> float:
        """
        Calculate slope risk score using the formula: (slope / 60.0) * 100.0
        """
        try:
            # Extract slope values from statistics
            mean_slope = slope_data.get('statistics', {}).get('mean', 0.0)
            max_slope = slope_data.get('statistics', {}).get('max', 0.0)
            
            # Use maximum slope for worst-case scenario
            slope_value = max_slope if max_slope > 0 else mean_slope
            
            # Apply the formula: (slope / 60.0) * 100.0
            risk_score = min((slope_value / 60.0) * 100.0, 100.0)
            
            print(f"🌙 Slope Risk Calculation:")
            print(f"   - Input slope: {slope_value:.2f}°")
            print(f"   - Risk score: {risk_score:.2f}/100")
            
            return risk_score
            
        except Exception as e:
            print(f"❌ Error calculating slope risk: {e}")
            return 0.0
    
    def calculate_aspect_risk_score(self, aspect_data: Dict[str, Any]) -> float:
        """
        Calculate aspect risk score using the complex formula for distance from 315°
        """
        try:
            # Extract aspect values from statistics
            mean_aspect = aspect_data.get('statistics', {}).get('mean', 315.0)
            
            # Calculate distance from 315° (safe direction)
            aspect_diff = abs(mean_aspect - 315.0)
            
            # Handle circular distance (if > 180, use 360 - diff)
            if aspect_diff > 180.0:
                aspect_diff = 360.0 - aspect_diff
            
            # Apply the formula: (distance / 180.0) * 100.0
            risk_score = (aspect_diff / 180.0) * 100.0
            
            print(f"🌙 Aspect Risk Calculation:")
            print(f"   - Input aspect: {mean_aspect:.2f}°")
            print(f"   - Distance from 315°: {aspect_diff:.2f}°")
            print(f"   - Risk score: {risk_score:.2f}/100")
            
            return risk_score
            
        except Exception as e:
            print(f"❌ Error calculating aspect risk: {e}")
            return 0.0
    
    def calculate_hillshade_risk_score(self, hillshade_data: Dict[str, Any]) -> float:
        """
        Calculate hillshade risk score using the formula: (128.0 - hillshade) / 128.0 * 100.0
        """
        try:
            # Extract hillshade values from statistics
            mean_hillshade = hillshade_data.get('statistics', {}).get('mean', 128.0)
            
            # Apply the formula: (128.0 - hillshade) / 128.0 * 100.0
            risk_score = max((128.0 - mean_hillshade) / 128.0 * 100.0, 0.0)
            
            print(f"🌙 Hillshade Risk Calculation:")
            print(f"   - Input hillshade: {mean_hillshade:.2f}")
            print(f"   - Risk score: {risk_score:.2f}/100")
            
            return risk_score
            
        except Exception as e:
            print(f"❌ Error calculating hillshade risk: {e}")
            return 0.0
    
    def calculate_contour_density_risk_score(self, contour_data: Dict[str, Any]) -> float:
        """
        Calculate contour density risk score using the formula: (density / 10.0) * 100.0
        """
        try:
            # Extract contour density from statistics
            contour_density = contour_data.get('statistics', {}).get('contour_density', 0.0)
            
            # Apply the formula: (density / 10.0) * 100.0
            risk_score = min((contour_density / 10.0) * 100.0, 100.0)
            
            print(f"🌙 Contour Density Risk Calculation:")
            print(f"   - Input density: {contour_density:.4f}")
            print(f"   - Risk score: {risk_score:.2f}/100")
            
            return risk_score
            
        except Exception as e:
            print(f"❌ Error calculating contour density risk: {e}")
            return 0.0
    
    def calculate_elevation_risk_score(self, elevation_data: Dict[str, Any]) -> float:
        """
        Calculate elevation risk score using the formula: (elevation - 1000.0) / 1000.0 * 100.0
        """
        try:
            # Extract elevation values from statistics
            mean_elevation = elevation_data.get('statistics', {}).get('mean', 0.0)
            
            # Apply the formula with bounds
            if mean_elevation < 1000.0:
                risk_score = 0.0
            elif mean_elevation > 2000.0:
                risk_score = 100.0
            else:
                risk_score = (mean_elevation - 1000.0) / 1000.0 * 100.0
            
            print(f"🌙 Elevation Risk Calculation:")
            print(f"   - Input elevation: {mean_elevation:.2f} m")
            print(f"   - Risk score: {risk_score:.2f}/100")
            
            return risk_score
            
        except Exception as e:
            print(f"❌ Error calculating elevation risk: {e}")
            return 0.0
    
    def calculate_roughness_risk_score(self, roughness_data: Dict[str, Any]) -> float:
        """
        Calculate terrain roughness risk score using the formula: (roughness / 10.0) * 100.0
        """
        try:
            # Extract roughness values from statistics
            mean_roughness = roughness_data.get('statistics', {}).get('mean', 0.0)
            std_roughness = roughness_data.get('statistics', {}).get('std', 0.0)
            tri_mean = roughness_data.get('statistics', {}).get('mean_tri', 0.0)
            
            # Use the most relevant roughness metric
            roughness_value = 0.0
            if tri_mean > 0:
                roughness_value = tri_mean
            elif std_roughness > 0:
                roughness_value = std_roughness
            elif mean_roughness > 0:
                roughness_value = mean_roughness
            
            # Apply the formula: (roughness / 10.0) * 100.0
            risk_score = min((roughness_value / 10.0) * 100.0, 100.0)
            
            print(f"🌙 Roughness Risk Calculation:")
            print(f"   - Input roughness: {roughness_value:.2f}")
            print(f"   - Risk score: {risk_score:.2f}/100")
            
            return risk_score
            
        except Exception as e:
            print(f"❌ Error calculating roughness risk: {e}")
            return 0.0
    
    def calculate_curvature_risk_score(self, curvature_data: Dict[str, Any]) -> float:
        """
        Calculate curvature risk score using profile gradient approximation
        """
        try:
            # Extract curvature values from statistics
            profile_curvature_std = curvature_data.get('statistics', {}).get('profile_curvature_std', 0.0)
            mean_curvature_std = curvature_data.get('statistics', {}).get('mean_curvature_std', 0.0)
            gaussian_curvature_std = curvature_data.get('statistics', {}).get('gaussian_curvature_std', 0.0)
            
            # Use the most relevant curvature metric
            gradient_value = 0.0
            if profile_curvature_std > 0:
                gradient_value = profile_curvature_std
            elif mean_curvature_std > 0:
                gradient_value = mean_curvature_std
            elif gaussian_curvature_std > 0:
                gradient_value = gaussian_curvature_std / 100.0  # Scale down large values
            
            # Apply the formula: (gradient / 50.0) * 100.0
            risk_score = min((gradient_value / 50.0) * 100.0, 100.0)
            
            print(f"🌙 Curvature Risk Calculation:")
            print(f"   - Input gradient: {gradient_value:.2f}")
            print(f"   - Risk score: {risk_score:.2f}/100")
            
            return risk_score
            
        except Exception as e:
            print(f"❌ Error calculating curvature risk: {e}")
            return 0.0
    
    def calculate_composite_risk_score(self, risk_scores: Dict[str, float]) -> float:
        """
        Calculate the final composite risk score using weighted formula
        """
        try:
            # Apply weights to each risk component
            weighted_risks = {
                'slope': risk_scores.get('slope', 0.0) * self.risk_weights['slope'],
                'aspect': risk_scores.get('aspect', 0.0) * self.risk_weights['aspect'],
                'hillshade': risk_scores.get('hillshade', 0.0) * self.risk_weights['hillshade'],
                'contour_density': risk_scores.get('contour_density', 0.0) * self.risk_weights['contour_density'],
                'profile_gradient': risk_scores.get('profile_gradient', 0.0) * self.risk_weights['profile_gradient'],
                'crater_ratio': risk_scores.get('crater_ratio', 0.0) * self.risk_weights['crater_ratio'],
                'roughness': risk_scores.get('roughness', 0.0) * self.risk_weights['roughness'],
                'elevation': risk_scores.get('elevation', 0.0) * self.risk_weights['elevation']
            }
            
            # Sum all weighted risks
            composite_score = sum(weighted_risks.values())
            
            print(f"🌙 Composite Risk Calculation:")
            for component, weighted_score in weighted_risks.items():
                if weighted_score > 0:
                    print(f"   - {component}: {weighted_score:.2f}")
            print(f"   - Final composite score: {composite_score:.2f}/100")
            
            return composite_score
            
        except Exception as e:
            print(f"❌ Error calculating composite risk: {e}")
            return 0.0
    
    def determine_risk_level(self, risk_score: float) -> Tuple[str, str]:
        """
        Determine risk level and description based on composite score
        """
        if risk_score < 20:
            return "LOW", "Safe terrain for lunar operations"
        elif risk_score < 40:
            return "MODERATE", "Moderate terrain challenges"
        elif risk_score < 60:
            return "HIGH", "High risk terrain - caution required"
        elif risk_score < 80:
            return "VERY HIGH", "Very high risk - extreme caution"
        else:
            return "EXTREME", "Extreme risk - avoid if possible"
    
    def process_analysis_reports(self, report_paths: List[str]) -> Dict[str, Any]:
        """
        Process multiple analysis reports and generate comprehensive risk assessment
        """
        print("🚀 Starting comprehensive lunar terrain risk analysis...")
        
        all_risk_scores = {}
        parsed_reports = {}
        
        # Parse all reports
        for report_path in report_paths:
            report_data = self.parse_report_file(report_path)
            if report_data:
                analysis_type = report_data.get('analysis_type')
                if analysis_type:
                    parsed_reports[analysis_type] = report_data
        
        # Calculate individual risk scores
        if 'slope' in parsed_reports:
            all_risk_scores['slope'] = self.calculate_slope_risk_score(parsed_reports['slope'])
        
        if 'aspect' in parsed_reports:
            all_risk_scores['aspect'] = self.calculate_aspect_risk_score(parsed_reports['aspect'])
        
        if 'hillshade' in parsed_reports:
            all_risk_scores['hillshade'] = self.calculate_hillshade_risk_score(parsed_reports['hillshade'])
        
        if 'contour' in parsed_reports:
            all_risk_scores['contour_density'] = self.calculate_contour_density_risk_score(parsed_reports['contour'])
        
        if 'elevation' in parsed_reports:
            all_risk_scores['elevation'] = self.calculate_elevation_risk_score(parsed_reports['elevation'])
        
        if 'roughness' in parsed_reports:
            all_risk_scores['roughness'] = self.calculate_roughness_risk_score(parsed_reports['roughness'])
        
        if 'curvature' in parsed_reports:
            all_risk_scores['profile_gradient'] = self.calculate_curvature_risk_score(parsed_reports['curvature'])
        
        # Set default values for missing components
        missing_components = set(self.risk_weights.keys()) - set(all_risk_scores.keys())
        for component in missing_components:
            all_risk_scores[component] = 0.0
            print(f"⚠️  No data for {component}, using default risk score: 0.0")
        
        # Calculate composite risk score
        composite_score = self.calculate_composite_risk_score(all_risk_scores)
        risk_level, risk_description = self.determine_risk_level(composite_score)
        
        # Generate comprehensive results
        results = {
            'timestamp': datetime.now().isoformat(),
            'composite_risk_score': composite_score,
            'risk_level': risk_level,
            'risk_description': risk_description,
            'individual_risk_scores': all_risk_scores,
            'parsed_reports': parsed_reports,
            'analysis_summary': {
                'total_reports_processed': len(parsed_reports),
                'available_components': list(all_risk_scores.keys()),
                'missing_components': list(missing_components)
            }
        }
        
        # Store results
        self.analysis_results = results
        
        return results
    
    def generate_risk_report(self, results: Dict[str, Any], output_path: str = None) -> str:
        """
        Generate a comprehensive risk analysis report
        """
        report_content = f"""🌑 LUNAR TERRAIN RISK ANALYSIS REPORT
============================================================
Generated: {results['timestamp']}

📊 COMPOSITE RISK ASSESSMENT
------------------------------
• Overall Risk Score: {results['composite_risk_score']:.2f}/100
• Risk Level: {results['risk_level']}
• Risk Description: {results['risk_description']}

📋 INDIVIDUAL RISK COMPONENTS
------------------------------
"""
        
        for component, score in results['individual_risk_scores'].items():
            weight = self.risk_weights.get(component, 0.0)
            weighted_score = score * weight
            report_content += f"• {component.upper().replace('_', ' ')}:\n"
            report_content += f"  - Risk Score: {score:.2f}/100\n"
            report_content += f"  - Weight: {weight:.2f}\n"
            report_content += f"  - Weighted Contribution: {weighted_score:.2f}\n\n"
        
        report_content += f"""📈 ANALYSIS SUMMARY
------------------------------
• Total Reports Processed: {results['analysis_summary']['total_reports_processed']}
• Available Components: {', '.join(results['analysis_summary']['available_components'])}
• Missing Components: {', '.join(results['analysis_summary']['missing_components'])}

🎯 RISK MITIGATION RECOMMENDATIONS
----------------------------------------
"""
        
        if results['composite_risk_score'] < 20:
            report_content += "• Terrain is generally safe for lunar operations\n"
            report_content += "• Standard safety protocols sufficient\n"
        elif results['composite_risk_score'] < 40:
            report_content += "• Implement enhanced monitoring protocols\n"
            report_content += "• Consider alternative landing sites if available\n"
        elif results['composite_risk_score'] < 60:
            report_content += "• High risk terrain - implement strict safety measures\n"
            report_content += "• Consider mission postponement if possible\n"
        elif results['composite_risk_score'] < 80:
            report_content += "• Very high risk - avoid this terrain if possible\n"
            report_content += "• Implement emergency protocols\n"
        else:
            report_content += "• EXTREME RISK - AVOID THIS TERRAIN\n"
            report_content += "• Mission should be postponed or redirected\n"
        
        report_content += f"""
🔧 TECHNICAL DETAILS
------------------------------
• Risk Calculation Method: Weighted composite scoring
• Maximum Individual Risk: {max(results['individual_risk_scores'].values()):.2f}
• Minimum Individual Risk: {min(results['individual_risk_scores'].values()):.2f}
• Risk Score Range: 0-100 (0 = Safe, 100 = Extreme Risk)

📝 FORMULA USED
------------------------------
Composite Risk = Σ(Component_Risk × Component_Weight)
Where weights sum to 1.0 and individual risks are normalized to 0-100 scale.

"""
        
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                print(f"✅ Risk report saved to: {output_path}")
            except Exception as e:
                print(f"❌ Error saving report: {e}")
        
        return report_content

def main():
    """
    Main function to run lunar terrain risk analysis
    """
    analyzer = LunarRiskAnalyzer()
    
    # List of all available report files
    report_files = [
        "lunar_slope_analysis_report.txt",
        "lunar_aspect_analysis_report.txt",
        "lunar_curvature_analysis_report.txt",
        "lunar_elevation_analysis_report.txt",
        "lunar_contour_analysis_report.txt",
        "terrain_ruggedness_analysis_report.txt",
        "lunar_landslide_analysis_report.txt",
        "scarps_headwalls_analysis_report.txt"
    ]
    
    # Filter to only existing files
    existing_reports = [path for path in report_files if os.path.exists(path)]
    
    if existing_reports:
        print(f"📊 Processing {len(existing_reports)} analysis reports...")
        print("📁 Available reports:")
        for report in existing_reports:
            print(f"   - {report}")
        
        # Process reports and generate risk assessment
        results = analyzer.process_analysis_reports(existing_reports)
        
        # Generate and display report
        report_content = analyzer.generate_risk_report(results, "comprehensive_lunar_risk_report.txt")
        print("\n" + report_content)
        
        # Save detailed results as JSON
        try:
            with open("lunar_risk_analysis_results.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, default=str)
            print("✅ Detailed results saved to: lunar_risk_analysis_results.json")
        except Exception as e:
            print(f"❌ Error saving JSON results: {e}")
        
    else:
        print("❌ No analysis reports found!")
        print("📝 Expected report files:")
        for path in report_files:
            print(f"   - {path}")
        print("\n💡 Please ensure analysis reports exist before running risk assessment")

if __name__ == "__main__":
    main() 
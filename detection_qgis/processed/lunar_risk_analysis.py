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
        
    def _extract_stat(self, data, *keys, default=0.0):
        """
        Try to extract a statistic from multiple possible keys in the data dict, including 'stats', 'statistics', and top-level.
        """
        for key in keys:
            # Try nested 'statistics' dict first
            if 'statistics' in data and key in data['statistics']:
                return data['statistics'][key]
            # Try nested 'stats' dict
            if 'stats' in data and key in data['stats']:
                return data['stats'][key]
            # Try top-level
            if key in data:
                return data[key]
        # Not found, print debug
        print(f"[WARN] Could not find any of {keys} in data. Returning default={default}")
        return default

    def _normalize_analysis_type(self, analysis_type):
        """
        Map various analysis_type strings to canonical risk component names.
        """
        mapping = {
            'slope': 'slope',
            'slope_analysis': 'slope',
            'slope_analysis_results': 'slope',
            'elevation': 'elevation',
            'elevation_statistics': 'elevation',
            'elevation_statistics_results': 'elevation',
            'curvature': 'curvature',
            'curvature_statistics': 'curvature',
            'curvature_statistics_results': 'curvature',
            'terrain_ruggedness_pipeline_summary': 'roughness',
            'ruggedness_analysis_results': 'roughness',
            'tri_raster_calculator_results': 'roughness',
            'roughness': 'roughness',
            'contour': 'contour',
            'contour_analysis': 'contour',
            'contour_analysis_results': 'contour',
            'contour_pipeline_summary': 'contour',
            'hillshade': 'hillshade',
            'hillshade_calculation': 'hillshade',
            'hillshade_calculation_results': 'hillshade',
            'aspect': 'aspect',
            'aspect_analysis': 'aspect',
            'aspect_analysis_results': 'aspect',
            'crater': 'crater',
            'crater_edges': 'crater',
            'crater_edges_analysis': 'crater',
            'crater_walls_analysis': 'crater',
            'debris_flow_pipeline_summary': 'debris_flow',
            'debris_flow_paths_analysis': 'debris_flow',
            'debris_vector_analysis': 'debris_flow',
            'debris_hillshade_analysis': 'debris_flow',
            'debris_slope_analysis': 'debris_flow',
            'tif_loading': None,
            'tif_loading_results': None,
        }
        return mapping.get(analysis_type, analysis_type)

    def parse_json_file(self, json_path: str) -> Dict[str, Any]:
        """
        Load and parse a JSON analysis result file
        """
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Try to infer analysis_type if not present
            if 'analysis_type' not in data:
                for k in ['slope', 'elevation', 'curvature', 'contour', 'hillshade', 'aspect', 'crater', 'roughness', 'debris']:
                    if k in json_path.lower():
                        data['analysis_type'] = k
                        break
            data['source_file'] = os.path.basename(json_path)
            print(f"✅ Loaded JSON: {os.path.basename(json_path)} as {data.get('analysis_type')}")
            return data
        except Exception as e:
            print(f"❌ Error loading JSON file {json_path}: {e}")
            return {}

    def process_analysis_jsons(self, json_paths: List[str]) -> Dict[str, Any]:
        """
        Process multiple analysis JSON files and generate comprehensive risk assessment
        """
        print("🚀 Starting comprehensive lunar terrain risk analysis (JSON mode)...")
        all_risk_scores = {}
        parsed_reports = {}
        # Parse all JSONs
        all_reports = []
        for json_path in json_paths:
            report_data = self.parse_json_file(json_path)
            if report_data:
                analysis_type = report_data.get('analysis_type')
                canonical = self._normalize_analysis_type(analysis_type)
                if canonical:
                    if canonical not in parsed_reports:
                        parsed_reports[canonical] = []
                    parsed_reports[canonical].append(report_data)
                all_reports.append(report_data)
        # Calculate individual risk scores (search all files for each component)
        def find_stat_in_reports(reports, *keys, default=0.0, nested_keys=None):
            for rep in reports:
                # Try direct keys
                val = self._extract_stat(rep, *keys, default=None)
                if val is not None:
                    print(f"[INFO] Found {keys} in {rep.get('source_file', 'unknown')}: {val}")
                    return val
                # Try nested keys if provided
                if nested_keys:
                    for nk in nested_keys:
                        d = rep
                        found = True
                        for k in nk:
                            if isinstance(d, dict) and k in d:
                                d = d[k]
                            else:
                                found = False
                                break
                        if found and d is not None:
                            print(f"[INFO] Found {'.'.join(nk)} in {rep.get('source_file', 'unknown')}: {d}")
                            return d
            print(f"[WARN] Could not find any of {keys}{' or ' + str(nested_keys) if nested_keys else ''} in any report. Returning default={default}")
            return default
        # Slope
        if 'slope' in parsed_reports:
            all_risk_scores['slope'] = self.calculate_slope_risk_score(parsed_reports['slope'][0])
        # Aspect
        if 'aspect' in parsed_reports:
            all_risk_scores['aspect'] = self.calculate_aspect_risk_score(parsed_reports['aspect'][0])
        # Hillshade: check all likely locations
        if 'hillshade' in parsed_reports:
            val = find_stat_in_reports(
                parsed_reports['hillshade'],
                'mean', 'mean_hillshade',
                nested_keys=[['stats', 'mean'], ['statistics', 'mean']]
            )
            all_risk_scores['hillshade'] = max((128.0 - val) / 128.0 * 100.0, 0.0) if val is not None else 0.0
        # Contour density: search all contour reports for contour_density
        if 'contour' in parsed_reports:
            val = find_stat_in_reports(parsed_reports['contour'], 'contour_density', default=0.0)
            if val is not None:
                all_risk_scores['contour_density'] = min((val / 10.0) * 100.0, 100.0)
            else:
                all_risk_scores['contour_density'] = 0.0
        # Elevation: search all elevation reports for mean_elevation
        if 'elevation' in parsed_reports:
            mean_elev = find_stat_in_reports(parsed_reports['elevation'], 'mean', 'mean_elevation', default=None, nested_keys=[['stats', 'mean'], ['statistics', 'mean']])
            if mean_elev is None:
                mean_elev = 0.0
            # Adjusted formula for negative elevations: map min_elev to 100, max_elev to 0
            min_elev = find_stat_in_reports(parsed_reports['elevation'], 'min', 'min_elevation', default=mean_elev, nested_keys=[['stats', 'min'], ['statistics', 'min']])
            max_elev = find_stat_in_reports(parsed_reports['elevation'], 'max', 'max_elevation', default=mean_elev, nested_keys=[['stats', 'max'], ['statistics', 'max']])
            if min_elev == max_elev:
                risk_score = 0.0
            else:
                risk_score = max(0.0, min(100.0, 100.0 * (max_elev - mean_elev) / (max_elev - min_elev)))
            all_risk_scores['elevation'] = risk_score
        # Roughness: check all likely locations
        if 'roughness' in parsed_reports:
            tri_mean = find_stat_in_reports(
                parsed_reports['roughness'],
                'mean_tri', 'mean',
                nested_keys=[['results', 'ruggedness_analysis', 'mean_tri'], ['results', 'tri_calculator', 'stats', 'mean'], ['stats', 'mean'], ['statistics', 'mean']]
            )
            std_roughness = find_stat_in_reports(
                parsed_reports['roughness'],
                'std_tri', 'std',
                nested_keys=[['results', 'ruggedness_analysis', 'std_tri'], ['results', 'tri_calculator', 'stats', 'std'], ['stats', 'std'], ['statistics', 'std']]
            )
            mean_roughness = find_stat_in_reports(parsed_reports['roughness'], 'mean_roughness', default=None)
            # Use std_roughness for normalized risk: std=0 -> 0, std=50 -> 100
            if std_roughness is not None and std_roughness >= 0:
                roughness_value = std_roughness
                risk_score = min(max((roughness_value / 50.0) * 100.0, 0.0), 100.0)
                print(f"[INFO] Roughness std={roughness_value}, risk_score={risk_score}")
            else:
                risk_score = 0.0
            all_risk_scores['roughness'] = risk_score
        # Curvature: search all curvature reports for profile_std, profile_curvature_std, mean_std, mean_curvature_std, gaussian_std, gaussian_curvature_std
        if 'curvature' in parsed_reports:
            profile_std = find_stat_in_reports(parsed_reports['curvature'], 'profile_std', 'profile_curvature_std', default=None)
            mean_std = find_stat_in_reports(parsed_reports['curvature'], 'mean_std', 'mean_curvature_std', default=None)
            gaussian_std = find_stat_in_reports(parsed_reports['curvature'], 'gaussian_std', 'gaussian_curvature_std', default=None)
            gradient_value = 0.0
            if profile_std is not None and profile_std > 0:
                gradient_value = profile_std
            elif mean_std is not None and mean_std > 0:
                gradient_value = mean_std
            elif gaussian_std is not None and gaussian_std > 0:
                gradient_value = gaussian_std / 100.0
            all_risk_scores['profile_gradient'] = min((gradient_value / 50.0) * 100.0, 100.0)
        # Crater ratio: look for 'crater_ratio' in any crater report, else use 'stats.density_percent'
        if 'crater' in parsed_reports:
            crater_ratio = find_stat_in_reports(parsed_reports['crater'], 'crater_ratio', default=None)
            if crater_ratio is None:
                # Try stats.density_percent
                for rep in parsed_reports['crater']:
                    if 'stats' in rep and 'density_percent' in rep['stats']:
                        crater_ratio = rep['stats']['density_percent']
                        print(f"[INFO] Using stats.density_percent from {rep.get('source_file', 'unknown')} as crater_ratio: {crater_ratio}")
                        break
            if crater_ratio is None:
                crater_ratio = 0.0
            all_risk_scores['crater_ratio'] = crater_ratio
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
                'total_reports_processed': sum(len(v) for v in parsed_reports.values()),
                'available_components': list(all_risk_scores.keys()),
                'missing_components': list(missing_components)
            }
        }
        self.analysis_results = results
        return results
    
    def calculate_slope_risk_score(self, slope_data: Dict[str, Any]) -> float:
        """
        Calculate slope risk score using the formula: (slope / 60.0) * 100.0
        """
        try:
            mean_slope = self._extract_stat(slope_data, 'mean', 'mean_value', 'mean_slope', default=0.0)
            max_slope = self._extract_stat(slope_data, 'max', 'max_value', 'max_slope', default=0.0)
            
            # Use maximum slope for worst-case scenario
            slope_value = max_slope if max_slope > 0 else mean_slope
            
            # Apply the formula: (slope / 60.0) * 100.0
            risk_score = min((slope_value / 60.0) * 100.0, 100.0)
            
            print(f"[DEBUG] Slope: mean={mean_slope}, max={max_slope}, used={slope_value}")
            print(f"🌙 Slope Risk Calculation:\n   - Input slope: {slope_value:.2f}°\n   - Risk score: {risk_score:.2f}/100")
            
            return risk_score
            
        except Exception as e:
            print(f"❌ Error calculating slope risk: {e}")
            return 0.0
    
    def calculate_aspect_risk_score(self, aspect_data: Dict[str, Any]) -> float:
        """
        Calculate aspect risk score using the complex formula for distance from 315°
        """
        try:
            mean_aspect = self._extract_stat(aspect_data, 'mean', 'mean_aspect', default=None)
            if mean_aspect is None:
                # Try nested 'stats' dict
                if 'stats' in aspect_data and 'mean' in aspect_data['stats']:
                    mean_aspect = aspect_data['stats']['mean']
            if mean_aspect is None:
                print(f"[WARN] Aspect mean not found in aspect_data. Using default 315.0")
                mean_aspect = 315.0
            # Calculate distance from 315° (safe direction)
            aspect_diff = abs(mean_aspect - 315.0)
            # Handle circular distance (if > 180, use 360 - diff)
            if aspect_diff > 180.0:
                aspect_diff = 360.0 - aspect_diff
            # Apply the formula: (distance / 180.0) * 100.0
            risk_score = (aspect_diff / 180.0) * 100.0
            print(f"[DEBUG] Aspect: mean={mean_aspect}, diff={aspect_diff}")
            print(f"🌙 Aspect Risk Calculation:\n   - Input aspect: {mean_aspect:.2f}°\n   - Distance from 315°: {aspect_diff:.2f}°\n   - Risk score: {risk_score:.2f}/100")
            return risk_score
        except Exception as e:
            print(f"❌ Error calculating aspect risk: {e}")
            return 0.0
    
    def calculate_hillshade_risk_score(self, hillshade_data: Dict[str, Any]) -> float:
        """
        Calculate hillshade risk score using the formula: (128.0 - hillshade) / 128.0 * 100.0
        """
        try:
            mean_hillshade = self._extract_stat(hillshade_data, 'mean', 'mean_hillshade', default=128.0)
            
            # Apply the formula: (128.0 - hillshade) / 128.0 * 100.0
            risk_score = max((128.0 - mean_hillshade) / 128.0 * 100.0, 0.0)
            
            print(f"[DEBUG] Hillshade: mean={mean_hillshade}")
            print(f"🌙 Hillshade Risk Calculation:\n   - Input hillshade: {mean_hillshade:.2f}\n   - Risk score: {risk_score:.2f}/100")
            
            return risk_score
            
        except Exception as e:
            print(f"❌ Error calculating hillshade risk: {e}")
            return 0.0
    
    def calculate_contour_density_risk_score(self, contour_data: Dict[str, Any]) -> float:
        """
        Calculate contour density risk score using the formula: (density / 10.0) * 100.0
        """
        try:
            contour_density = self._extract_stat(contour_data, 'contour_density', default=0.0)
            
            # Apply the formula: (density / 10.0) * 100.0
            risk_score = min((contour_density / 10.0) * 100.0, 100.0)
            
            print(f"[DEBUG] Contour Density: {contour_density}")
            print(f"🌙 Contour Density Risk Calculation:\n   - Input density: {contour_density:.4f}\n   - Risk score: {risk_score:.2f}/100")
            
            return risk_score
            
        except Exception as e:
            print(f"❌ Error calculating contour density risk: {e}")
            return 0.0
    
    def calculate_elevation_risk_score(self, elevation_data: Dict[str, Any]) -> float:
        """
        Calculate elevation risk score using the formula: (elevation - 1000.0) / 1000.0 * 100.0
        """
        try:
            mean_elevation = self._extract_stat(elevation_data, 'mean', 'mean_elevation', default=None)
            if mean_elevation is None:
                # Try nested 'stats' dict
                if 'stats' in elevation_data and 'mean' in elevation_data['stats']:
                    mean_elevation = elevation_data['stats']['mean']
            if mean_elevation is None:
                print(f"[WARN] Elevation mean not found in elevation_data. Using default 0.0")
                mean_elevation = 0.0
            # Apply the formula with bounds
            if mean_elevation < 1000.0:
                risk_score = 0.0
            elif mean_elevation > 2000.0:
                risk_score = 100.0
            else:
                risk_score = (mean_elevation - 1000.0) / 1000.0 * 100.0
            print(f"[DEBUG] Elevation: mean={mean_elevation}")
            print(f"🌙 Elevation Risk Calculation:\n   - Input elevation: {mean_elevation:.2f} m\n   - Risk score: {risk_score:.2f}/100")
            return risk_score
        except Exception as e:
            print(f"❌ Error calculating elevation risk: {e}")
            return 0.0
    
    def _extract_roughness_stat(self, data, *keys, default=0.0):
        # Try top-level first
        for key in keys:
            if key in data:
                return data[key]
            if 'statistics' in data and key in data['statistics']:
                return data['statistics'][key]
            if 'stats' in data and key in data['stats']:
                return data['stats'][key]
        # Try nested in 'results.ruggedness_analysis' and 'results.tri_calculator.stats'
        if 'results' in data:
            rugged = data['results'].get('ruggedness_analysis', {})
            for key in keys:
                if key in rugged:
                    return rugged[key]
            tri_calc = data['results'].get('tri_calculator', {})
            if 'stats' in tri_calc:
                for key in keys:
                    if key in tri_calc['stats']:
                        return tri_calc['stats'][key]
        # Try nested in 'calculation_results.ruggedness_analysis'
        if 'calculation_results' in data:
            rugged = data['calculation_results'].get('ruggedness_analysis', {})
            for key in keys:
                if key in rugged:
                    return rugged[key]
        print(f"[WARN] Could not find any of {keys} in roughness data. Returning default={default}")
        return default
    
    def calculate_roughness_risk_score(self, roughness_data: Dict[str, Any]) -> float:
        """
        Calculate terrain roughness risk score using the formula: (roughness / 10.0) * 100.0
        """
        try:
            # Try TRI mean, std, or other roughness metrics
            tri_mean = self._extract_roughness_stat(roughness_data, 'mean_tri', 'mean', default=0.0)
            std_roughness = self._extract_roughness_stat(roughness_data, 'std_tri', 'std', default=0.0)
            mean_roughness = self._extract_roughness_stat(roughness_data, 'mean_roughness', default=0.0)
            
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
            
            print(f"[DEBUG] Roughness: tri_mean={tri_mean}, std={std_roughness}, mean_roughness={mean_roughness}, used={roughness_value}")
            print(f"🌙 Roughness Risk Calculation:\n   - Input roughness: {roughness_value:.2f}\n   - Risk score: {risk_score:.2f}/100")
            
            return risk_score
            
        except Exception as e:
            print(f"❌ Error calculating roughness risk: {e}")
            return 0.0
    
    def calculate_curvature_risk_score(self, curvature_data: Dict[str, Any]) -> float:
        """
        Calculate curvature risk score using profile gradient approximation
        """
        try:
            # Try all possible std keys for curvature
            profile_curvature_std = self._extract_stat(curvature_data, 'profile_std', 'profile_curvature_std', default=0.0)
            mean_curvature_std = self._extract_stat(curvature_data, 'mean_std', 'mean_curvature_std', default=0.0)
            gaussian_curvature_std = self._extract_stat(curvature_data, 'gaussian_std', 'gaussian_curvature_std', default=0.0)
            
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
            
            print(f"[DEBUG] Curvature: profile_std={profile_curvature_std}, mean_std={mean_curvature_std}, gaussian_std={gaussian_curvature_std}, used={gradient_value}")
            print(f"🌙 Curvature Risk Calculation:\n   - Input gradient: {gradient_value:.2f}\n   - Risk score: {risk_score:.2f}/100")
            
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
    Main function to run lunar terrain risk analysis (JSON mode)
    """
    analyzer = LunarRiskAnalyzer()
    # Dynamically list all JSON files in json_results
    json_dir = os.path.join(os.path.dirname(__file__), 'json_results')
    json_paths = [
        os.path.join(json_dir, f)
        for f in os.listdir(json_dir)
        if f.endswith('.json')
    ]
    if json_paths:
        print(f"📊 Processing {len(json_paths)} analysis JSON files...")
        print("📁 Available JSONs:")
        for path in json_paths:
            print(f"   - {os.path.basename(path)}")
        # Process JSONs and generate risk assessment
        results = analyzer.process_analysis_jsons(json_paths)
        # Show mapping of files to risk components
        print("\n🔎 Mapping of JSON files to risk components:")
        for k, v in results.get('parsed_reports', {}).items():
            if isinstance(v, list):
                for rep in v:
                    print(f"   - {k}: {rep.get('analysis_type', 'unknown')} (from {rep.get('source_file', 'unknown')})")
            else:
                print(f"   - {k}: {v.get('analysis_type', 'unknown')} (from {v.get('source_file', 'unknown')})")
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
        print("❌ No analysis JSON files found!")
        print("📝 Please ensure analysis JSON files exist before running risk assessment")

if __name__ == "__main__":
    main() 
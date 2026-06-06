import React, { useState } from 'react';
import HeroSection from './components/HeroSection';
import ImageUpload from './components/ImageUpload';
import ImagePreview from './components/ImagePreview';
import AnalysisResults from './components/AnalysisResults';
import { apiUrl } from '../../config/api';

// Helper to map backend JSON results to frontend analysisData structure
function mapBackendResultsToAnalysisData(results) {
  // Slope
  const slopeJson = results['slope_analysis_results.json'];
  const slopeStats = slopeJson?.statistics || {};
  const slope = slopeJson ? {
    riskLevel: slopeJson.analysis_results?.risk_level || 'N/A',
    riskFactors: slopeJson.analysis_results?.risk_factors || [],
    statistics: {
      min: slopeStats.min_value ?? slopeStats.min ?? 0,
      max: slopeStats.max_value ?? slopeStats.max ?? 0,
      mean: slopeStats.mean_value ?? slopeStats.mean ?? 0,
      stdDev: slopeStats.std_dev ?? slopeStats.std ?? 0,
    },
    thresholds: slopeJson.thresholds || {},
  } : undefined;

  // Elevation
  const elevJson = results['elevation_statistics_results.json'];
  const elevation = elevJson ? {
    riskLevel: 'N/A',
    riskFactors: [],
    statistics: {
      min: elevJson.min_elevation,
      max: elevJson.max_elevation,
      mean: elevJson.mean_elevation,
      stdDev: elevJson.std_elevation,
      range: elevJson.elevation_range,
    },
    thresholds: {},
    elevationDistribution: {},
  } : undefined;

  // Curvature
  const curvJson = results['curvature_statistics_results.json'];
  const curvature = curvJson ? {
    riskLevel: 'N/A',
    riskFactors: [],
    statistics: {
      profileCurvatureMean: curvJson.profile_mean,
      profileCurvatureStd: curvJson.profile_std,
      planCurvatureMean: curvJson.plan_mean,
      planCurvatureStd: curvJson.plan_std,
      gaussianCurvatureMean: curvJson.gaussian_mean,
      gaussianCurvatureStd: curvJson.gaussian_std,
      meanCurvatureMean: curvJson.mean_mean,
      meanCurvatureStd: curvJson.mean_std,
    },
    thresholds: {},
  } : undefined;

  // Roughness (TRI)
  const triJson = results['terrain_ruggedness_pipeline_summary.json'];
  let triStats = undefined;
  if (triJson?.results?.ruggedness_analysis) {
    triStats = triJson.results.ruggedness_analysis;
  } else if (triJson?.calculation_results?.ruggedness_analysis) {
    triStats = triJson.calculation_results.ruggedness_analysis;
  }
  const roughness = triStats ? {
    riskLevel: triStats.category || 'N/A',
    riskFactors: [triStats.description || ''],
    statistics: {
      min: triStats.min_tri,
      max: triStats.max_tri,
      mean: triStats.mean_tri,
      std: triStats.std_tri,
    },
    percentiles: {},
    terrainDistribution: {},
    categories: {},
  } : undefined;

  // Contours
  const contourJson = results['contour_analysis_results.json'];
  const contours = contourJson ? {
    terrainComplexity: contourJson.terrain_complexity,
    statistics: {
      numberOfContours: contourJson.num_contours,
      numberOfLevels: contourJson.num_levels,
      contourDensity: contourJson.contour_density,
      elevationRange: { min: contourJson.elevation_range?.[0], max: contourJson.elevation_range?.[1] },
    },
    elevationDistribution: contourJson.elevation_distribution,
  } : undefined;

  // Composite (from risk analysis, if available)
  const riskJson = results['lunar_risk_analysis_results.json'];
  const composite = riskJson ? {
    overallRisk: {
      score: riskJson.composite_risk_score,
      level: riskJson.risk_level,
      description: riskJson.risk_description,
    },
    components: (riskJson.individual_risk_scores && Object.entries(riskJson.individual_risk_scores).map(([name, riskScore]) => ({
      name: name.toUpperCase(),
      riskScore,
      weight: riskJson.parsed_reports?.[name]?.weight || 0,
      weightedContribution: (riskScore * (riskJson.parsed_reports?.[name]?.weight || 0)),
    }))) || [],
    weights: riskJson.weights || {},
    analysis: riskJson.analysis_summary || {},
  } : undefined;

  return {
    slope,
    elevation,
    curvature,
    roughness,
    contours,
    composite,
    // Add more mappings as needed
  };
}

const LandslideDetection = () => {
  const [image, setImage] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);
  const [error, setError] = useState(null);

  const handleImageUpload = async (fileData) => {
    setIsUploading(true);
    setShowResults(false);
    await new Promise(resolve => setTimeout(resolve, 2000));
    const mockFile = {
      name: fileData.path.split(/[\\/]/).pop(),
      size: 1024 * 1024 * 50,
      type: 'image/tiff',
      path: fileData.path
    };
    setImage(mockFile);
    setIsUploading(false);
  };

  const startAnalysis = async () => {
    if (!image) return;
    setIsAnalyzing(true);
    setError(null);
    setShowResults(false);
    try {
      const response = await fetch(apiUrl('/api/lunar-analysis'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('lunalens_token')}`
        },
        body: JSON.stringify({ dem_path: image.path })  
      });
      const data = await response.json();
      if (data.success) {
        const mapped = mapBackendResultsToAnalysisData(data.results);
        setAnalysisData(mapped);
        setShowResults(true);
      } else {
        setError(data.error || 'Analysis failed.');
      }
    } catch {
      setError('Error connecting to backend.');
    }
    setIsAnalyzing(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-gray-100 relative overflow-hidden">
            {/* Animated Background Elements */}
            <div className="fixed inset-0 pointer-events-none z-0">
                {/* Floating particles */}
                <div className="absolute top-20 left-20 w-2 h-2 bg-blue-400 rounded-full animate-ping opacity-20" style={{animationDelay: '0s'}}></div>
                <div className="absolute top-40 right-32 w-1 h-1 bg-purple-400 rounded-full animate-ping opacity-30" style={{animationDelay: '1s'}}></div>
                <div className="absolute bottom-32 left-1/4 w-1.5 h-1.5 bg-orange-400 rounded-full animate-ping opacity-25" style={{animationDelay: '2s'}}></div>
                <div className="absolute top-1/2 right-1/4 w-1 h-1 bg-green-400 rounded-full animate-ping opacity-20" style={{animationDelay: '3s'}}></div>
                
                {/* Larger floating orbs */}
                <div className="absolute top-1/3 left-1/3 w-4 h-4 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full animate-bounce opacity-10" style={{animationDelay: '0.5s'}}></div>
                <div className="absolute bottom-1/3 right-1/3 w-3 h-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full animate-bounce opacity-15" style={{animationDelay: '1.5s'}}></div>
                
                {/* Subtle gradient overlays */}
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-purple-500/3 to-orange-500/5 animate-pulse"></div>
                <div className="absolute inset-0 bg-gradient-to-tl from-green-500/3 via-blue-500/2 to-purple-500/3 animate-pulse" style={{animationDelay: '2s'}}></div>
                
                {/* Grid pattern */}
                <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:50px_50px] opacity-20"></div>
                
                {/* Radial gradient */}
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(59,130,246,0.1)_0%,transparent_50%)]"></div>
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(147,51,234,0.1)_0%,transparent_50%)]"></div>
            </div>

            {/* Main Content */}
            <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6 lg:py-8">
        {/* Hero Section */}
        <HeroSection />

        {/* Main Content Layout */}
                <div className="flex flex-col lg:flex-row gap-4 sm:gap-6 lg:gap-8 mt-4 sm:mt-6 lg:mt-8 relative">
                    {/* Animated connection line between columns */}
                    <div className="hidden lg:block absolute left-[calc(50%-1px)] top-0 bottom-0 w-px bg-gradient-to-b from-transparent via-blue-500/30 to-transparent"></div>
                    
          {/* Left Column - Controls and Configuration */}
                    <div className="lg:w-[400px] xl:w-[420px] flex-shrink-0 relative w-full">
            <div className="space-y-6">
              {/* Image Upload */}
              <ImageUpload 
                onImageUpload={handleImageUpload}
                isUploading={isUploading}
              />
                            
                            {/* Analysis Button */}
                            {image && (
                                <button
                                    onClick={startAnalysis}
                                    disabled={isAnalyzing}
                                    className={`w-full px-6 py-4 rounded-xl font-bold text-lg transition-all duration-300 shadow-lg ${
                                        isAnalyzing
                                            ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                                            : 'bg-gradient-to-r from-blue-500 via-purple-500 to-orange-400 hover:from-blue-600 hover:to-orange-500 text-white hover:shadow-2xl hover:scale-105'
                                    }`}
                                >
                                    {isAnalyzing ? (
                                        <div className="flex items-center justify-center space-x-2">
                                            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                                            <span>Analyzing...</span>
            </div>
                                    ) : (
                                        <span>Start Analysis</span>
                                    )}
                                </button>
                            )}

                            {error && (
                                <div className="rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-300">
                                    {error}
                                </div>
                            )}
          </div>

                        {/* Floating accent elements */}
                        <div className="absolute -top-4 -left-4 w-8 h-8 border-l-2 border-t-2 border-blue-500/30 rounded-tl-lg"></div>
                        <div className="absolute -bottom-4 -right-4 w-8 h-8 border-r-2 border-b-2 border-purple-500/30 rounded-br-lg"></div>
                    </div>

                    {/* Right Column - Preview and Results */}
                    <div className="flex-1 min-w-0 relative w-full">
                        <div className="space-y-4 sm:space-y-6">
              {/* Image Preview */}
              {image && (
                                <div className="relative group">
                <ImagePreview
                  image={image}
                  isAnalyzing={isAnalyzing}
                />
                                    {/* Hover glow effect */}
                                    <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-blue-500/0 via-purple-500/0 to-orange-500/0 group-hover:from-blue-500/10 group-hover:via-purple-500/10 group-hover:to-orange-500/10 transition-all duration-500 pointer-events-none"></div>
                                </div>
                            )}

                            {/* Analysis Results */}
                            <AnalysisResults
                                isVisible={showResults}
                                analysisData={analysisData}
              />

              {/* Placeholder for right column when no content */}
              {!image && (
                                <div className="relative group">
                                    <div className="bg-gradient-to-br from-gray-800/90 to-gray-900/90 rounded-2xl p-4 sm:p-6 lg:p-8 border-2 border-gray-700/50 shadow-2xl backdrop-blur-sm relative overflow-hidden">
                                        {/* Animated background pattern */}
                                        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-purple-500/3 to-orange-500/5 animate-pulse"></div>
                                        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(255,255,255,0.05)_0%,transparent_70%)]"></div>
                                        
                                        <div className="relative z-10 text-center">
                                            <div className="w-16 h-16 sm:w-20 sm:h-20 lg:w-24 lg:h-24 mx-auto bg-gradient-to-br from-gray-700 to-gray-600 rounded-full flex items-center justify-center mb-4 sm:mb-6 shadow-lg group-hover:shadow-xl transition-all duration-500 group-hover:scale-110">
                                                <svg className="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12 text-gray-400 group-hover:text-blue-400 transition-colors duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                    </div>
                                            <h3 className="text-lg sm:text-xl lg:text-2xl font-bold text-gray-100 mb-2 sm:mb-4 group-hover:text-blue-200 transition-colors duration-500">
                      Upload a Lunar DEM
                    </h3>
                                            <p className="text-sm sm:text-base lg:text-lg text-gray-400 group-hover:text-gray-300 transition-colors duration-500">
                      Upload a Digital Elevation Model to begin lunar terrain analysis
                    </p>
                  </div>
                                        
                                        {/* Corner decorations */}
                                        <div className="absolute top-2 sm:top-4 left-2 sm:left-4 w-4 h-4 sm:w-6 sm:h-6 border-l-2 border-t-2 border-blue-500/30 rounded-tl-lg"></div>
                                        <div className="absolute top-2 sm:top-4 right-2 sm:right-4 w-4 h-4 sm:w-6 sm:h-6 border-r-2 border-t-2 border-purple-500/30 rounded-tr-lg"></div>
                                        <div className="absolute bottom-2 sm:bottom-4 left-2 sm:left-4 w-4 h-4 sm:w-6 sm:h-6 border-l-2 border-b-2 border-blue-500/30 rounded-bl-lg"></div>
                                        <div className="absolute bottom-2 sm:bottom-4 right-2 sm:right-4 w-4 h-4 sm:w-6 sm:h-6 border-r-2 border-b-2 border-purple-500/30 rounded-br-lg"></div>
                                    </div>
                                    
                                    {/* Hover glow effect */}
                                    <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-blue-500/0 via-purple-500/0 to-orange-500/0 group-hover:from-blue-500/10 group-hover:via-purple-500/10 group-hover:to-orange-500/10 transition-all duration-500 pointer-events-none"></div>
                </div>
              )}
            </div>
                        
                        {/* Floating accent elements */}
                        <div className="absolute -top-4 -right-4 w-8 h-8 border-r-2 border-t-2 border-purple-500/30 rounded-tr-lg"></div>
                        <div className="absolute -bottom-4 -left-4 w-8 h-8 border-l-2 border-b-2 border-blue-500/30 rounded-bl-lg"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandslideDetection;

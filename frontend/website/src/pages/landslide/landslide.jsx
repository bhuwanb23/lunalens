import React, { useState } from 'react';
import HeroSection from './components/HeroSection';
import ImageUpload from './components/ImageUpload';
import ImagePreview from './components/ImagePreview';
import AnalysisResults from './components/AnalysisResults';

const sampleAnalysisData = {
    slope: {
        riskLevel: 'LOW',
        riskFactors: ['Gentle slopes', 'Low slope variability'],
        statistics: { min: 0.00, max: 11.54, mean: 5.01, stdDev: 2.00 },
        thresholds: { gentleSlopes: 3.01, moderateSlopes: 5.01, steepSlopes: 7.01 }
    },
    aspect: {
        statistics: { min: 0.00, max: 359.9999, mean: 189.4721, stdDev: 89.5053 }
    },
    elevation: {
        riskLevel: 'HIGH',
        riskFactors: ['High terrain variability', 'Extreme elevation differences'],
        statistics: { min: -3641.00, max: 205.00, mean: -1977.48, stdDev: 625.98, range: 3846.00 },
        thresholds: {
            lowElevation: -2679.50,
            mediumElevation: -1718.00,
            highElevation: -756.50
        },
        elevationDistribution: {
            low: { pixels: 1000000, percentage: 20.0 },
            medium: { pixels: 3000000, percentage: 60.0 },
            high: { pixels: 1000000, percentage: 20.0 }
        }
    },
    curvature: {
        riskLevel: 'HIGH',
        riskFactors: ['High curvature variability', 'Complex terrain features'],
        statistics: {
            profileCurvatureMean: -0.010725,
            profileCurvatureStd: 3.716956,
            planCurvatureMean: -0.009777,
            planCurvatureStd: 3.628621,
            gaussianCurvatureMean: -0.019519,
            gaussianCurvatureStd: 385.109967,
            meanCurvatureMean: 0.024214,
            meanCurvatureStd: 6.684292
        },
        thresholds: {
            profileCurvatureThreshold: 7.433913,
            planCurvatureThreshold: 7.257242,
            gaussianCurvatureThreshold: 770.219933,
            tangentialCurvatureThreshold: 7.257242,
            meanCurvatureThreshold: 13.368584
        }
    },
    roughness: {
        riskLevel: 'MODERATE',
        riskFactors: ['Moderate terrain complexity'],
        statistics: { min: 0.000000, max: 8.999971, mean: 7.327898, std: 3.496449 },
        percentiles: {
            p25: 3.32,
            p50: 6.71,
            p75: 11.79,
            p90: 20.02,
            p95: 28.04,
            p99: 69.61
        },
        terrainDistribution: {
            low: { pixels: 1062978, percentage: 20.3 },
            moderate: { pixels: 3527883, percentage: 67.5 },
            high: { pixels: 334127, percentage: 6.4 },
            veryHigh: { pixels: 301508, percentage: 5.8 }
        },
        categories: {
            'LOW': { threshold: 0.1, description: 'Smooth terrain with minimal elevation variation' },
            'MODERATE': { threshold: 0.5, description: 'Moderate terrain variation' },
            'HIGH': { threshold: 1.0, description: 'High terrain ruggedness' },
            'VERY HIGH': { threshold: null, description: 'Extreme terrain variation' }
        }
    },
    contours: {
        terrainComplexity: 'HIGH',
        statistics: {
            numberOfContours: 12,
            numberOfLevels: 14,
            contourDensity: 0.1211,
            elevationRange: { min: 0.0, max: 650.0 }
        },
        elevationDistribution: {
            '0-50m': 1,
            '50-100m': 1,
            '100-150m': 1,
            '150-200m': 1,
            '200-250m': 1,
            '250-300m': 1,
            '300-350m': 1,
            '350-400m': 1,
            '400-450m': 1,
            '450-500m': 1,
            '500-550m': 1,
            '550-600m': 1
        }
    },
    scarps: {
        riskLevel: 'LOW',
        riskFactors: ['Limited scarp features'],
        statistics: {
            scarpPixels: 195324.0000,
            densityPercent: 0.0504,
            slopeThreshold: 30.0,
            curvatureThreshold: 0.001,
            triThreshold: 0.5,
            featureCount: 1331731
        },
        parameters: {
            slope: {
                min: 0.0000,
                max: 89.9996,
                mean: 0.2286,
                std: 4.5305
            },
            aspect: {
                min: 0.0000,
                max: 359.9999,
                mean: 189.4721,
                std: 89.5053
            },
            curvature: {
                min: 0.0000,
                max: 89.9996,
                mean: 0.2286,
                std: 4.5305
            },
            tri: {
                min: 0.0000,
                max: 89.9996,
                mean: 0.2286,
                std: 4.5305
            }
        },
        detectionResults: {
            totalPixels: 5227296,
            scarpPixels: 195324,
            densityPercent: 0.0504,
            featureCount: 1331731
        }
    },
    composite: {
        overallRisk: { score: 10.13, level: 'LOW', description: 'Safe terrain for lunar operations' },
        components: [
            { name: 'SLOPE', riskScore: 19.23, weight: 0.30, weightedContribution: 5.77 },
            { name: 'ASPECT', riskScore: 0.00, weight: 0.15, weightedContribution: 0.00 },
            { name: 'CONTOUR_DENSITY', riskScore: 1.21, weight: 0.10, weightedContribution: 0.12 },
            { name: 'ELEVATION', riskScore: 0.00, weight: 0.05, weightedContribution: 0.00 },
            { name: 'ROUGHNESS', riskScore: 34.96, weight: 0.10, weightedContribution: 3.50 },
            { name: 'PROFILE_GRADIENT', riskScore: 7.43, weight: 0.10, weightedContribution: 0.74 },
            { name: 'HILLSHADE', riskScore: 0.00, weight: 0.15, weightedContribution: 0.00 },
            { name: 'CRATER_RATIO', riskScore: 0.00, weight: 0.05, weightedContribution: 0.00 }
        ],
        weights: {
            SLOPE: 0.30,
            ASPECT: 0.15,
            CONTOUR_DENSITY: 0.10,
            ELEVATION: 0.05,
            ROUGHNESS: 0.10,
            PROFILE_GRADIENT: 0.10,
            HILLSHADE: 0.15,
            CRATER_RATIO: 0.05
        },
        analysis: {
            totalReportsProcessed: 9,
            availableComponents: ['SLOPE', 'ASPECT', 'CONTOUR_DENSITY', 'ELEVATION', 'ROUGHNESS', 'PROFILE_GRADIENT', 'HILLSHADE', 'CRATER_RATIO'],
            missingComponents: []
        }
    }
};

const LandslideDetection = () => {
    const [image, setImage] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [showResults, setShowResults] = useState(false);

    const handleImageUpload = async (fileData) => {
        setIsUploading(true);
        setShowResults(false);

        // Simulate upload delay
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Create a mock file object for ImagePreview
        const mockFile = {
            name: fileData.path.split(/[\\/]/).pop(),
            size: 1024 * 1024 * 50, // 50MB mock size
            type: 'image/tiff',
            path: fileData.path
        };

        setImage(mockFile);
        setIsUploading(false);
    };

    const startAnalysis = async () => {
        if (!image) return;

        setIsAnalyzing(true);

        // Simulate analysis processing
        await new Promise(resolve => setTimeout(resolve, 3000));

        setShowResults(true);
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
            <div className="relative z-10 max-w-7xl mx-auto px-4 py-8">
                {/* Hero Section */}
                <HeroSection />

                {/* Main Content Layout */}
                <div className="flex flex-col xl:flex-row gap-8 mt-8 relative">
                    {/* Animated connection line between columns */}
                    <div className="hidden xl:block absolute left-[420px] top-0 bottom-0 w-px bg-gradient-to-b from-transparent via-blue-500/30 to-transparent"></div>
                    
                    {/* Left Column - Controls and Configuration */}
                    <div className="xl:w-[420px] flex-shrink-0 relative">
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
                        </div>
                        
                        {/* Floating accent elements */}
                        <div className="absolute -top-4 -left-4 w-8 h-8 border-l-2 border-t-2 border-blue-500/30 rounded-tl-lg"></div>
                        <div className="absolute -bottom-4 -right-4 w-8 h-8 border-r-2 border-b-2 border-purple-500/30 rounded-br-lg"></div>
                    </div>

                    {/* Right Column - Preview and Results */}
                    <div className="flex-1 min-w-0 relative">
                        <div className="space-y-6">
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
                                analysisData={sampleAnalysisData}
                            />

                            {/* Placeholder for right column when no content */}
                            {!image && (
                                <div className="relative group">
                                    <div className="bg-gradient-to-br from-gray-800/90 to-gray-900/90 rounded-2xl p-8 border-2 border-gray-700/50 shadow-2xl backdrop-blur-sm relative overflow-hidden">
                                        {/* Animated background pattern */}
                                        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-purple-500/3 to-orange-500/5 animate-pulse"></div>
                                        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(255,255,255,0.05)_0%,transparent_70%)]"></div>
                                        
                                        <div className="relative z-10 text-center">
                                            <div className="w-24 h-24 mx-auto bg-gradient-to-br from-gray-700 to-gray-600 rounded-full flex items-center justify-center mb-6 shadow-lg group-hover:shadow-xl transition-all duration-500 group-hover:scale-110">
                                                <svg className="w-12 h-12 text-gray-400 group-hover:text-blue-400 transition-colors duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                                </svg>
                                            </div>
                                            <h3 className="text-2xl font-bold text-gray-100 mb-4 group-hover:text-blue-200 transition-colors duration-500">
                                                Upload a Lunar DEM
                                            </h3>
                                            <p className="text-gray-400 text-lg group-hover:text-gray-300 transition-colors duration-500">
                                                Upload a Digital Elevation Model to begin lunar terrain analysis
                                            </p>
                                        </div>
                                        
                                        {/* Corner decorations */}
                                        <div className="absolute top-4 left-4 w-6 h-6 border-l-2 border-t-2 border-blue-500/30 rounded-tl-lg"></div>
                                        <div className="absolute top-4 right-4 w-6 h-6 border-r-2 border-t-2 border-purple-500/30 rounded-tr-lg"></div>
                                        <div className="absolute bottom-4 left-4 w-6 h-6 border-l-2 border-b-2 border-blue-500/30 rounded-bl-lg"></div>
                                        <div className="absolute bottom-4 right-4 w-6 h-6 border-r-2 border-b-2 border-purple-500/30 rounded-br-lg"></div>
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

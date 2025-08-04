import React from 'react';
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
    statistics: { min: -3641.00, max: 205.00, mean: -1977.48, stdDev: 625.98, range: 3846.00 }
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
    }
  },
  roughness: {
    riskLevel: 'MODERATE',
    riskFactors: ['Moderate terrain complexity'],
    statistics: { min: 0.000000, max: 8.999971, mean: 7.327898, std: 3.496449 },
    terrainDistribution: {
      low: { pixels: 1062978, percentage: 20.3 },
      moderate: { pixels: 3527883, percentage: 67.5 },
      high: { pixels: 334127, percentage: 6.4 },
      veryHigh: { pixels: 301508, percentage: 5.8 }
    }
  },
  contours: {
    terrainComplexity: 'HIGH',
    statistics: {
      numberOfContours: 12,
      numberOfLevels: 14,
      contourDensity: 0.1211,
      elevationRange: { min: 0.0, max: 650.0 }
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
    ]
  }
};

const LandslideDetection = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-gray-100 relative overflow-hidden">
      <div className="max-w-5xl mx-auto py-8">
        <AnalysisResults isVisible={true} analysisData={sampleAnalysisData} />
      </div>
    </div>
  );
};

export default LandslideDetection;

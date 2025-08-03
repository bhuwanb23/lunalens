import React from 'react';
import { LANDSLIDE_CONSTANTS } from '../constants/constants';

const AnalysisResults = ({ results, onExport }) => {
  if (!results) return null;

  const getRiskCategory = (riskScore) => {
    if (riskScore >= LANDSLIDE_CONSTANTS.DETECTION_CATEGORIES.HIGH_RISK.threshold) {
      return LANDSLIDE_CONSTANTS.DETECTION_CATEGORIES.HIGH_RISK;
    } else if (riskScore >= LANDSLIDE_CONSTANTS.DETECTION_CATEGORIES.MEDIUM_RISK.threshold) {
      return LANDSLIDE_CONSTANTS.DETECTION_CATEGORIES.MEDIUM_RISK;
    } else if (riskScore >= LANDSLIDE_CONSTANTS.DETECTION_CATEGORIES.LOW_RISK.threshold) {
      return LANDSLIDE_CONSTANTS.DETECTION_CATEGORIES.LOW_RISK;
    } else {
      return LANDSLIDE_CONSTANTS.DETECTION_CATEGORIES.SAFE;
    }
  };

  const riskCategory = getRiskCategory(results.riskScore);

  const getRiskColor = (color) => {
    const colors = {
      red: 'bg-red-500',
      orange: 'bg-orange-500',
      yellow: 'bg-yellow-500',
      green: 'bg-green-500'
    };
    return colors[color] || 'bg-gray-500';
  };

  const getRiskTextColor = (color) => {
    const colors = {
      red: 'text-red-400',
      orange: 'text-orange-400',
      yellow: 'text-yellow-400',
      green: 'text-green-400'
    };
    return colors[color] || 'text-gray-400';
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <div className="mb-6">
        <h3 className="text-xl font-semibold text-gray-100 mb-2">
          Analysis Results
        </h3>
        <p className="text-gray-400 text-sm">
          Comprehensive landslide detection analysis results
        </p>
      </div>

      {/* Risk Assessment */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h4 className="text-lg font-medium text-gray-200">Risk Assessment</h4>
          <div className={`px-3 py-1 rounded-full ${getRiskColor(riskCategory.color)} text-white text-sm font-medium`}>
            {riskCategory.label}
          </div>
        </div>

        <div className="bg-gray-700 rounded-lg p-4 mb-4">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm text-gray-300">Risk Score</span>
            <span className={`text-lg font-bold ${getRiskTextColor(riskCategory.color)}`}>
              {(results.riskScore * 100).toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-600 rounded-full h-3">
            <div 
              className={`h-3 rounded-full transition-all duration-500 ${getRiskColor(riskCategory.color)}`}
              style={{ width: `${results.riskScore * 100}%` }}
            ></div>
          </div>
          <p className="text-xs text-gray-400 mt-2">{riskCategory.description}</p>
        </div>
      </div>

      {/* Detection Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-gray-700 rounded-lg p-4">
          <h5 className="text-sm font-medium text-gray-300 mb-2">Detection Metrics</h5>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-xs text-gray-400">Confidence</span>
              <span className="text-sm font-medium text-gray-200">
                {(results.confidence * 100).toFixed(1)}%
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-xs text-gray-400">Precision</span>
              <span className="text-sm font-medium text-gray-200">
                {(results.precision * 100).toFixed(1)}%
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-xs text-gray-400">Recall</span>
              <span className="text-sm font-medium text-gray-200">
                {(results.recall * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        </div>

        <div className="bg-gray-700 rounded-lg p-4">
          <h5 className="text-sm font-medium text-gray-300 mb-2">Spatial Analysis</h5>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-xs text-gray-400">Affected Area</span>
              <span className="text-sm font-medium text-gray-200">
                {results.affectedArea} km²
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-xs text-gray-400">Slope Range</span>
              <span className="text-sm font-medium text-gray-200">
                {results.slopeRange.min}° - {results.slopeRange.max}°
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-xs text-gray-400">Elevation Change</span>
              <span className="text-sm font-medium text-gray-200">
                {results.elevationChange} m
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Detected Features */}
      <div className="mb-6">
        <h5 className="text-sm font-medium text-gray-300 mb-3">Detected Features</h5>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {results.detectedFeatures.map((feature, index) => (
            <div key={index} className="bg-gray-700 rounded-lg p-3 text-center">
              <div className="text-lg mb-1">{feature.icon}</div>
              <div className="text-xs font-medium text-gray-200">{feature.name}</div>
              <div className="text-xs text-gray-400">{feature.count} detected</div>
            </div>
          ))}
        </div>
      </div>

      {/* Analysis Summary */}
      <div className="mb-6">
        <h5 className="text-sm font-medium text-gray-300 mb-3">Analysis Summary</h5>
        <div className="bg-gray-700 rounded-lg p-4">
          <p className="text-sm text-gray-300 leading-relaxed">
            {results.summary}
          </p>
        </div>
      </div>

      {/* Recommendations */}
      {results.recommendations && results.recommendations.length > 0 && (
        <div className="mb-6">
          <h5 className="text-sm font-medium text-gray-300 mb-3">Recommendations</h5>
          <div className="space-y-2">
            {results.recommendations.map((recommendation, index) => (
              <div key={index} className="flex items-start space-x-3 p-3 bg-gray-700 rounded-lg">
                <div className="text-orange-400 mt-0.5">•</div>
                <p className="text-sm text-gray-300">{recommendation}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Export Options */}
      <div className="border-t border-gray-700 pt-6">
        <h5 className="text-sm font-medium text-gray-300 mb-3">Export Results</h5>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {LANDSLIDE_CONSTANTS.EXPORT_FORMATS.map((format) => (
            <button
              key={format.value}
              onClick={() => onExport(format.value)}
              className="flex flex-col items-center p-3 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
            >
              <span className="text-lg mb-1">{format.icon}</span>
              <span className="text-xs text-gray-200">{format.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnalysisResults; 
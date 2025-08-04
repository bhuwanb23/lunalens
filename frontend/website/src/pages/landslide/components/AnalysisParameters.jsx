import React from 'react';
import { LANDSLIDE_CONSTANTS } from '../constants/constants';

const AnalysisParameters = ({ parameters, onParameterChange, isAnalyzing }) => {
  const handleSliderChange = (paramKey, value) => {
    onParameterChange(paramKey, parseFloat(value));
  };

  const getRiskColor = (value, paramKey) => {
    const param = LANDSLIDE_CONSTANTS.ANALYSIS_PARAMETERS[paramKey];
    const percentage = (value - param.min) / (param.max - param.min);
    
    if (percentage > 0.7) return 'text-red-400';
    if (percentage > 0.4) return 'text-orange-400';
    if (percentage > 0.2) return 'text-yellow-400';
    return 'text-green-400';
  };

  return (
    <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700 shadow-lg">
      <div className="mb-5">
        <h3 className="text-xl font-bold text-gray-100 mb-3">
          Analysis Parameters
        </h3>
        <p className="text-gray-400 text-sm">
          Adjust detection parameters for optimal landslide analysis
        </p>
      </div>

              <div className="space-y-6">
        {Object.entries(LANDSLIDE_CONSTANTS.ANALYSIS_PARAMETERS).map(([key, param]) => (
          <div key={key} className="space-y-3">
            <div className="flex justify-between items-center">
              <div>
                <label className="text-sm font-medium text-gray-200">
                  {param.name}
                </label>
                <p className="text-xs text-gray-400 mt-1">
                  {param.description}
                </p>
              </div>
              <div className="text-right">
                <div className={`text-lg font-bold ${getRiskColor(parameters[key], key)}`}>
                  {parameters[key]} {param.unit}
                </div>
                <div className="text-xs text-gray-400">
                  {param.min} - {param.max} {param.unit}
                </div>
              </div>
            </div>

            <div className="relative">
              <input
                type="range"
                min={param.min}
                max={param.max}
                step={(param.max - param.min) / 100}
                value={parameters[key]}
                onChange={(e) => handleSliderChange(key, e.target.value)}
                disabled={isAnalyzing}
                className={`w-full h-2 rounded-lg appearance-none cursor-pointer ${
                  isAnalyzing ? 'opacity-50 cursor-not-allowed' : ''
                }`}
                style={{
                  background: `linear-gradient(to right, #ef4444 0%, #f97316 50%, #22c55e 100%)`,
                  outline: 'none'
                }}
              />
              
              {/* Slider thumb styling */}
              <style>{`
                input[type="range"]::-webkit-slider-thumb {
                  appearance: none;
                  height: 20px;
                  width: 20px;
                  border-radius: 50%;
                  background: #f97316;
                  cursor: pointer;
                  border: 2px solid #fff;
                  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                }
                input[type="range"]::-moz-range-thumb {
                  height: 20px;
                  width: 20px;
                  border-radius: 50%;
                  background: #f97316;
                  cursor: pointer;
                  border: 2px solid #fff;
                  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                }
              `}</style>
            </div>

            {/* Parameter indicators */}
            <div className="flex justify-between text-xs text-gray-500">
              <span>Low</span>
              <span>Medium</span>
              <span>High</span>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Presets */}
      <div className="mt-5 pt-5 border-t border-gray-700">
        <h4 className="text-sm font-medium text-gray-200 mb-3">Quick Presets</h4>
        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={() => {
              onParameterChange('SLOPE_THRESHOLD', 25);
              onParameterChange('ELEVATION_CHANGE', 30);
              onParameterChange('SURFACE_ROUGHNESS', 0.2);
              onParameterChange('COHERENCE_THRESHOLD', 0.8);
            }}
            disabled={isAnalyzing}
            className="px-3 py-2 text-xs bg-gray-700 hover:bg-gray-600 text-gray-200 rounded-lg transition-colors disabled:opacity-50"
          >
            Conservative
          </button>
          <button
            onClick={() => {
              onParameterChange('SLOPE_THRESHOLD', 35);
              onParameterChange('ELEVATION_CHANGE', 60);
              onParameterChange('SURFACE_ROUGHNESS', 0.4);
              onParameterChange('COHERENCE_THRESHOLD', 0.6);
            }}
            disabled={isAnalyzing}
            className="px-3 py-2 text-xs bg-gray-700 hover:bg-gray-600 text-gray-200 rounded-lg transition-colors disabled:opacity-50"
          >
            Balanced
          </button>
          <button
            onClick={() => {
              onParameterChange('SLOPE_THRESHOLD', 45);
              onParameterChange('ELEVATION_CHANGE', 80);
              onParameterChange('SURFACE_ROUGHNESS', 0.6);
              onParameterChange('COHERENCE_THRESHOLD', 0.4);
            }}
            disabled={isAnalyzing}
            className="px-3 py-2 text-xs bg-gray-700 hover:bg-gray-600 text-gray-200 rounded-lg transition-colors disabled:opacity-50"
          >
            Sensitive
          </button>
          <button
            onClick={() => {
              onParameterChange('SLOPE_THRESHOLD', 55);
              onParameterChange('ELEVATION_CHANGE', 100);
              onParameterChange('SURFACE_ROUGHNESS', 0.8);
              onParameterChange('COHERENCE_THRESHOLD', 0.3);
            }}
            disabled={isAnalyzing}
            className="px-3 py-2 text-xs bg-gray-700 hover:bg-gray-600 text-gray-200 rounded-lg transition-colors disabled:opacity-50"
          >
            Aggressive
          </button>
        </div>
      </div>

      {/* Analysis Status */}
      {isAnalyzing && (
        <div className="mt-5 p-4 bg-orange-500/10 border border-orange-500/20 rounded-lg">
          <div className="flex items-center space-x-3">
            <div className="w-4 h-4 border-2 border-orange-500 border-t-transparent rounded-full animate-spin"></div>
            <div>
              <p className="text-sm font-medium text-orange-400">Analysis in Progress</p>
              <p className="text-xs text-orange-300">Processing with current parameters...</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalysisParameters; 
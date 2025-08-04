import React from 'react';

const AnalysisConfig = ({ onStartAnalysis, isAnalyzing }) => {
  return (
    <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700 shadow-lg">
      <div className="mb-5">
        <h3 className="text-xl font-bold text-gray-100 mb-3">
          Lunar Analysis Configuration
        </h3>
        <p className="text-gray-400 text-sm">
          Configure lunar terrain analysis parameters and start processing
        </p>
      </div>

      <div className="space-y-4">
        {/* Analysis Type Selection */}
        <div className="bg-gray-700 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-200 mb-3">Analysis Type</h4>
          <div className="grid grid-cols-2 gap-3">
            <button
              className="p-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors text-sm font-medium"
              disabled={isAnalyzing}
            >
              Complete Analysis
            </button>
            <button
              className="p-3 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors text-sm font-medium"
              disabled={isAnalyzing}
            >
              Quick Assessment
            </button>
          </div>
        </div>

        {/* Processing Options */}
        <div className="bg-gray-700 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-200 mb-3">Processing Options</h4>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-300">Slope Analysis</span>
              <div className="w-4 h-4 bg-green-500 rounded-full"></div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-300">Aspect Analysis</span>
              <div className="w-4 h-4 bg-green-500 rounded-full"></div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-300">Curvature Analysis</span>
              <div className="w-4 h-4 bg-green-500 rounded-full"></div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-300">Elevation Analysis</span>
              <div className="w-4 h-4 bg-green-500 rounded-full"></div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-300">Terrain Ruggedness</span>
              <div className="w-4 h-4 bg-green-500 rounded-full"></div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-300">Feature Detection</span>
              <div className="w-4 h-4 bg-green-500 rounded-full"></div>
            </div>
          </div>
        </div>

        {/* Start Analysis Button */}
        <div className="pt-4">
          <button
            onClick={onStartAnalysis}
            disabled={isAnalyzing}
            className={`w-full py-3 px-4 rounded-lg font-medium transition-colors ${
              isAnalyzing
                ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white'
            }`}
          >
            {isAnalyzing ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Processing Lunar Terrain...
              </div>
            ) : (
              'Start Lunar Analysis'
            )}
          </button>
        </div>

        {/* Analysis Status */}
        {isAnalyzing && (
          <div className="mt-4 p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
              <div>
                <p className="text-sm font-medium text-blue-400">Lunar Analysis in Progress</p>
                <p className="text-xs text-blue-300">Processing terrain parameters and generating reports...</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalysisConfig; 
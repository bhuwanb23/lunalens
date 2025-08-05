import React from 'react';

const ElevationAnalysis = ({ data }) => {
  // Default data based on lunar_elevation_analysis_report.txt
  const elevationData = data || {
    riskLevel: 'HIGH',
    riskFactors: ['High terrain variability', 'Extreme elevation differences'],
    statistics: {
      min: -3641.00,
      max: 205.00,
      mean: -1977.48,
      stdDev: 625.98,
      range: 3846.00
    },
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
  };

  const getRiskColor = (level) => {
    const colors = {
      'LOW': 'text-green-400',
      'MODERATE': 'text-yellow-400',
      'HIGH': 'text-orange-400',
      'VERY HIGH': 'text-red-400'
    };
    return colors[level] || 'text-gray-400';
  };

  const getRiskBgColor = (level) => {
    const colors = {
      'LOW': 'bg-green-500',
      'MODERATE': 'bg-yellow-500',
      'HIGH': 'bg-orange-500',
      'VERY HIGH': 'bg-red-500'
    };
    return colors[level] || 'bg-gray-500';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-lg font-bold text-gray-200 flex items-center">
            <span className="mr-2">🏔️</span>
            Elevation Analysis
          </h4>
          <div className={`px-3 py-1 rounded-full ${getRiskBgColor(elevationData.riskLevel)} text-white text-xs font-medium`}>
            {elevationData.riskLevel} RISK
          </div>
        </div>
        <p className="text-gray-400 text-sm">
          Elevation analysis indicates terrain complexity and surface roughness
        </p>
      </div>

      {/* Statistics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-blue-400">{elevationData.statistics.min} m</div>
          <div className="text-sm text-gray-400">Minimum</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-orange-400">{elevationData.statistics.max} m</div>
          <div className="text-sm text-gray-400">Maximum</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-green-400">{elevationData.statistics.mean.toFixed(2)} m</div>
          <div className="text-sm text-gray-400">Mean</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-purple-400">{elevationData.statistics.range} m</div>
          <div className="text-sm text-gray-400">Range</div>
        </div>
      </div>

      {/* Elevation Distribution */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-4">Elevation Distribution</h5>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-lg font-bold text-blue-400">{elevationData.thresholds.lowElevation} m</div>
            <div className="text-sm text-gray-400">Low Elevation</div>
            <div className="text-xs text-blue-400 mt-1">Below Sea Level</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-yellow-400">{elevationData.thresholds.mediumElevation} m</div>
            <div className="text-sm text-gray-400">Medium Elevation</div>
            <div className="text-xs text-yellow-400 mt-1">Mid-Range</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-green-400">{elevationData.thresholds.highElevation} m</div>
            <div className="text-sm text-gray-400">High Elevation</div>
            <div className="text-xs text-green-400 mt-1">Above Sea Level</div>
          </div>
        </div>
      </div>

      {/* Elevation Range Visualization */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Elevation Range</h5>
        <div className="relative">
          <div className="w-full bg-gray-600 rounded-full h-4 mb-2">
            <div 
              className="bg-gradient-to-r from-blue-500 via-yellow-500 to-green-500 h-4 rounded-full"
              style={{ width: '100%' }}
            ></div>
          </div>
          <div className="flex justify-between text-xs text-gray-400">
            <span>{elevationData.statistics.min} m</span>
            <span>{elevationData.statistics.mean.toFixed(0)} m (mean)</span>
            <span>{elevationData.statistics.max} m</span>
          </div>
        </div>
        <div className="mt-3 text-sm text-gray-400">
          <p>• Total elevation range: {elevationData.statistics.range} meters</p>
          <p>• Standard deviation: {elevationData.statistics.stdDev.toFixed(2)} meters</p>
        </div>
      </div>

      {/* Risk Factors */}
      <div className="bg-gradient-to-r from-orange-500/10 to-red-500/10 rounded-xl p-4 border border-orange-500/20">
        <h5 className="text-md font-bold text-orange-400 mb-3 flex items-center">
          <span className="mr-2">⚠️</span>
          Risk Factors
        </h5>
        <ul className="text-gray-300 space-y-1">
          {elevationData.riskFactors.map((factor, index) => (
            <li key={index} className="flex items-center">
              <span className="w-2 h-2 bg-orange-400 rounded-full mr-3"></span>
              {factor}
            </li>
          ))}
        </ul>
      </div>

      {/* Analysis Notes */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Analysis Notes</h5>
        <div className="text-sm text-gray-400 space-y-2">
          <p>• Elevation range of {elevationData.statistics.range} meters indicates terrain complexity</p>
          <p>• Standard deviation of {elevationData.statistics.stdDev.toFixed(2)} meters shows surface roughness</p>
          <p>• Mean elevation of {elevationData.statistics.mean.toFixed(2)} meters provides regional context</p>
          <p>• Risk assessment based on terrain variability and elevation differences</p>
          <p>• Negative elevations indicate areas below lunar reference level</p>
        </div>
      </div>

      {/* Lunar Context */}
      <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-xl p-4 border border-blue-500/20">
        <h5 className="text-md font-bold text-blue-400 mb-3 flex items-center">
          <span className="mr-2">🌙</span>
          Lunar Context
        </h5>
        <div className="text-sm text-gray-300 space-y-2">
          <p>• Lunar surface has significant elevation variations</p>
          <p>• Mare regions typically have lower elevations</p>
          <p>• Highland regions have higher elevations</p>
          <p>• Elevation affects landing site selection</p>
          <p>• Extreme elevation differences can indicate geological features</p>
        </div>
      </div>
    </div>
  );
};

export default ElevationAnalysis; 
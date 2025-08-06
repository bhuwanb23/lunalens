import React from 'react';

const ElevationAnalysis = ({ data }) => {
  // Default data based on lunar_elevation_analysis_report.txt
  const safeData = {
    riskLevel: data?.riskLevel ?? 'HIGH',
    riskFactors: data?.riskFactors ?? ['High terrain variability', 'Extreme elevation differences'],
    statistics: {
      min: data?.statistics?.min ?? -3641.00,
      max: data?.statistics?.max ?? 205.00,
      mean: data?.statistics?.mean ?? -1977.48,
      stdDev: data?.statistics?.stdDev ?? 625.98,
      range: data?.statistics?.range ?? 3846.00
    },
    thresholds: {
      lowElevation: data?.thresholds?.lowElevation ?? -2679.50,
      mediumElevation: data?.thresholds?.mediumElevation ?? -1718.00,
      highElevation: data?.thresholds?.highElevation ?? -756.50
    },
    elevationDistribution: {
      low: {
        pixels: data?.elevationDistribution?.low?.pixels ?? 1000000,
        percentage: data?.elevationDistribution?.low?.percentage ?? 20.0
      },
      medium: {
        pixels: data?.elevationDistribution?.medium?.pixels ?? 3000000,
        percentage: data?.elevationDistribution?.medium?.percentage ?? 60.0
      },
      high: {
        pixels: data?.elevationDistribution?.high?.pixels ?? 1000000,
        percentage: data?.elevationDistribution?.high?.percentage ?? 20.0
      }
    }
  };

  // Helper function to safely format numbers
  const safeFormat = (value, decimals = 2) => {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.00';
    }
    return Number(value).toFixed(decimals);
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
          <div className={`px-3 py-1 rounded-full ${getRiskBgColor(safeData.riskLevel)} text-white text-xs font-medium`}>
            {safeData.riskLevel} RISK
          </div>
        </div>
        <p className="text-gray-400 text-sm">
          Elevation analysis indicates terrain complexity and surface roughness
        </p>
      </div>

      {/* Statistics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-blue-400">{safeFormat(safeData.statistics.min)} m</div>
          <div className="text-sm text-gray-400">Minimum</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-orange-400">{safeFormat(safeData.statistics.max)} m</div>
          <div className="text-sm text-gray-400">Maximum</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-green-400">{safeFormat(safeData.statistics.mean)} m</div>
          <div className="text-sm text-gray-400">Mean</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-purple-400">{safeFormat(safeData.statistics.range)} m</div>
          <div className="text-sm text-gray-400">Range</div>
        </div>
      </div>

      {/* Elevation Distribution */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-4">Elevation Distribution</h5>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-lg font-bold text-blue-400">{safeFormat(safeData.thresholds.lowElevation)} m</div>
            <div className="text-sm text-gray-400">Low Elevation</div>
            <div className="text-xs text-blue-400 mt-1">Below Sea Level</div>
            <div className="text-xs text-gray-400 mt-1">{safeFormat(safeData.elevationDistribution.low.pixels, 0)} px ({safeFormat(safeData.elevationDistribution.low.percentage)}%)</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-yellow-400">{safeFormat(safeData.thresholds.mediumElevation)} m</div>
            <div className="text-sm text-gray-400">Medium Elevation</div>
            <div className="text-xs text-yellow-400 mt-1">Mid-Range</div>
            <div className="text-xs text-gray-400 mt-1">{safeFormat(safeData.elevationDistribution.medium.pixels, 0)} px ({safeFormat(safeData.elevationDistribution.medium.percentage)}%)</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-green-400">{safeFormat(safeData.thresholds.highElevation)} m</div>
            <div className="text-sm text-gray-400">High Elevation</div>
            <div className="text-xs text-green-400 mt-1">Above Sea Level</div>
            <div className="text-xs text-gray-400 mt-1">{safeFormat(safeData.elevationDistribution.high.pixels, 0)} px ({safeFormat(safeData.elevationDistribution.high.percentage)}%)</div>
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
            <span>{safeFormat(safeData.statistics.min)} m</span>
            <span>{safeFormat(safeData.statistics.mean)} m (mean)</span>
            <span>{safeFormat(safeData.statistics.max)} m</span>
          </div>
        </div>
        <div className="mt-3 text-sm text-gray-400">
          <p>• Total elevation range: {safeFormat(safeData.statistics.range)} meters</p>
          <p>• Standard deviation: {safeFormat(safeData.statistics.stdDev)} meters</p>
        </div>
      </div>

      {/* Risk Factors */}
      <div className="bg-gradient-to-r from-orange-500/10 to-red-500/10 rounded-xl p-4 border border-orange-500/20">
        <h5 className="text-md font-bold text-orange-400 mb-3 flex items-center">
          <span className="mr-2">⚠️</span>
          Risk Factors
        </h5>
        <ul className="text-gray-300 space-y-1">
          {(safeData.riskFactors || []).map((factor, index) => (
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
          <p>• Elevation range: {safeFormat(safeData.statistics.min)} m to {safeFormat(safeData.statistics.max)} m</p>
          <p>• Mean elevation: {safeFormat(safeData.statistics.mean)} m</p>
          <p>• Std deviation: {safeFormat(safeData.statistics.stdDev)} m</p>
          <p>• Range: {safeFormat(safeData.statistics.range)} m</p>
          <p>• Low: {safeFormat(safeData.elevationDistribution.low.pixels, 0)} px ({safeFormat(safeData.elevationDistribution.low.percentage)}%)</p>
          <p>• Medium: {safeFormat(safeData.elevationDistribution.medium.pixels, 0)} px ({safeFormat(safeData.elevationDistribution.medium.percentage)}%)</p>
          <p>• High: {safeFormat(safeData.elevationDistribution.high.pixels, 0)} px ({safeFormat(safeData.elevationDistribution.high.percentage)}%)</p>
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
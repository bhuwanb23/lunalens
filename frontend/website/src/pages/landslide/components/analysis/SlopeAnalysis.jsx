import React from 'react';

const SlopeAnalysis = ({ data }) => {
  // Default data based on lunar_slope_analysis_report.txt
  const safeData = {
    riskLevel: data?.riskLevel ?? 'LOW',
    riskFactors: data?.riskFactors ?? ['Gentle slopes', 'Low slope variability'],
    statistics: {
      min: data?.statistics?.min ?? 0.00,
      max: data?.statistics?.max ?? 11.54,
      mean: data?.statistics?.mean ?? 5.01,
      stdDev: data?.statistics?.stdDev ?? 2.00
    },
    thresholds: {
      gentleSlopes: data?.thresholds?.gentleSlopes ?? 3.01,
      moderateSlopes: data?.thresholds?.moderateSlopes ?? 5.01,
      steepSlopes: data?.thresholds?.steepSlopes ?? 7.01
    }
  };

  // Helper function to safely format numbers
  const safeFormat = (value, decimals = 2) => {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.00';
    }
    return Number(value).toFixed(decimals);
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
            <span className="mr-2">📈</span>
            Slope Analysis
          </h4>
          <div className={`px-3 py-1 rounded-full ${getRiskBgColor(safeData.riskLevel)} text-white text-xs font-medium`}>
            {safeData.riskLevel} RISK
          </div>
        </div>
        <p className="text-gray-400 text-sm">
          Slope analysis affects landing site suitability and landslide risk assessment
        </p>
      </div>

      {/* Statistics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-blue-400">{safeFormat(safeData.statistics.min)}°</div>
          <div className="text-sm text-gray-400">Minimum</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-orange-400">{safeFormat(safeData.statistics.max)}°</div>
          <div className="text-sm text-gray-400">Maximum</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-green-400">{safeFormat(safeData.statistics.mean)}°</div>
          <div className="text-sm text-gray-400">Mean</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-purple-400">{safeFormat(safeData.statistics.stdDev)}</div>
          <div className="text-sm text-gray-400">Std Dev</div>
        </div>
      </div>

      {/* Thresholds */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Slope Thresholds</h5>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-lg font-bold text-green-400">{safeFormat(safeData.thresholds.gentleSlopes)}°</div>
            <div className="text-sm text-gray-400">Gentle Slopes</div>
            <div className="text-xs text-green-400 mt-1">Low Risk</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-yellow-400">{safeFormat(safeData.thresholds.moderateSlopes)}°</div>
            <div className="text-sm text-gray-400">Moderate Slopes</div>
            <div className="text-xs text-yellow-400 mt-1">Moderate Risk</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-orange-400">{safeFormat(safeData.thresholds.steepSlopes)}°</div>
            <div className="text-sm text-gray-400">Steep Slopes</div>
            <div className="text-xs text-orange-400 mt-1">High Risk</div>
          </div>
        </div>
      </div>

      {/* Risk Factors */}
      <div className="bg-gradient-to-r from-green-500/10 to-blue-500/10 rounded-xl p-4 border border-green-500/20">
        <h5 className="text-md font-bold text-green-400 mb-3 flex items-center">
          <span className="mr-2">✅</span>
          Risk Factors
        </h5>
        <ul className="text-gray-300 space-y-1">
          {(safeData.riskFactors || []).map((factor, index) => (
            <li key={index} className="flex items-center">
              <span className="w-2 h-2 bg-green-400 rounded-full mr-3"></span>
              {factor}
            </li>
          ))}
        </ul>
      </div>

      {/* Analysis Notes */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Analysis Notes</h5>
        <div className="text-sm text-gray-400 space-y-2">
          <p>• Min: {safeFormat(safeData.statistics.min)}°, Max: {safeFormat(safeData.statistics.max)}°</p>
          <p>• Mean: {safeFormat(safeData.statistics.mean)}°, Std Dev: {safeFormat(safeData.statistics.stdDev)}°</p>
          <p>• Gentle: &lt; {safeFormat(safeData.thresholds.gentleSlopes)}°</p>
          <p>• Moderate: &lt; {safeFormat(safeData.thresholds.moderateSlopes)}°</p>
          <p>• Steep: &gt; {safeFormat(safeData.thresholds.steepSlopes)}°</p>
        </div>
      </div>
    </div>
  );
};

export default SlopeAnalysis; 
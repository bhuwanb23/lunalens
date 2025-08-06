import React from 'react';

const AspectAnalysis = ({ data }) => {
  // Default data based on lunar_aspect_analysis_report.txt
  const safeData = {
    statistics: {
      min: data?.statistics?.min ?? 0.00,
      max: data?.statistics?.max ?? 359.9999,
      mean: data?.statistics?.mean ?? 189.4721,
      stdDev: data?.statistics?.stdDev ?? 89.5053
    },
    analysis: {
      flatAreas: data?.analysis?.flatAreas ?? -1.0,
      southFacingAspects: data?.analysis?.southFacingAspects ?? 'Higher landslide risk',
      northFacingAspects: data?.analysis?.northFacingAspects ?? 'Lower landslide risk',
      gentleSlopes: data?.analysis?.gentleSlopes ?? 'Low landslide risk',
      moderateSlopes: data?.analysis?.moderateSlopes ?? 'Moderate risk',
      steepSlopes: data?.analysis?.steepSlopes ?? 'High landslide risk',
      verySteepSlopes: data?.analysis?.verySteepSlopes ?? 'Very high risk'
    }
  };

  // Helper function to safely format numbers
  const safeFormat = (value, decimals = 1) => {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.0';
    }
    return Number(value).toFixed(decimals);
  };

  const getAspectDirection = (degrees) => {
    if (degrees >= 315 || degrees < 45) return 'North';
    if (degrees >= 45 && degrees < 135) return 'East';
    if (degrees >= 135 && degrees < 225) return 'South';
    if (degrees >= 225 && degrees < 315) return 'West';
    return 'Unknown';
  };

  const getRiskLevel = (direction) => {
    const riskLevels = {
      'North': { level: 'LOW', color: 'text-green-400', bgColor: 'bg-green-500' },
      'East': { level: 'MODERATE', color: 'text-yellow-400', bgColor: 'bg-yellow-500' },
      'South': { level: 'HIGH', color: 'text-orange-400', bgColor: 'bg-orange-500' },
      'West': { level: 'MODERATE', color: 'text-yellow-400', bgColor: 'bg-yellow-500' }
    };
    return riskLevels[direction] || { level: 'UNKNOWN', color: 'text-gray-400', bgColor: 'bg-gray-500' };
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-lg font-bold text-gray-200 flex items-center">
            <span className="mr-2">🧭</span>
            Aspect Analysis
          </h4>
          <div className="px-3 py-1 rounded-full bg-blue-500 text-white text-xs font-medium">
            ORIENTATION
          </div>
        </div>
        <p className="text-gray-400 text-sm">
          Aspect analysis determines slope orientation and solar illumination patterns
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
          <div className="text-xs text-gray-500 mt-1">{getAspectDirection(safeData.statistics.mean)}</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-purple-400">{safeFormat(safeData.statistics.stdDev)}</div>
          <div className="text-sm text-gray-400">Std Dev</div>
        </div>
      </div>

      {/* Aspect Directions */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-4">Aspect Directions & Risk Levels</h5>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {['North', 'East', 'South', 'West'].map((direction) => {
            const risk = getRiskLevel(direction);
            const degrees = {
              'North': '315° - 45°',
              'East': '45° - 135°',
              'South': '135° - 225°',
              'West': '225° - 315°'
            };
            return (
              <div key={direction} className="bg-gray-600/50 rounded-lg p-3 border border-gray-500">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-200">{direction}</span>
                  <div className={`px-2 py-1 rounded text-xs font-medium ${risk.bgColor} text-white`}>
                    {risk.level}
                  </div>
                </div>
                <div className="flex items-center justify-between text-xs text-gray-400">
                  <span>{degrees[direction]}</span>
                  <span>{safeData.analysis[direction.toLowerCase() + 'FacingAspects'] || '-'}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Slope-Aspect Combinations */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Slope-Aspect Risk Combinations</h5>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-gray-600/30 rounded-lg">
            <span className="text-gray-300">Gentle Slopes (0-5°)</span>
            <span className="text-green-400 text-sm font-medium">Low Risk</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-600/30 rounded-lg">
            <span className="text-gray-300">Moderate Slopes (5-15°)</span>
            <span className="text-yellow-400 text-sm font-medium">Moderate Risk</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-600/30 rounded-lg">
            <span className="text-gray-300">Steep Slopes (&gt;15°)</span>
            <span className="text-orange-400 text-sm font-medium">High Risk</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-600/30 rounded-lg">
            <span className="text-gray-300">Very Steep Slopes (&gt;30°)</span>
            <span className="text-red-400 text-sm font-medium">Very High Risk</span>
          </div>
        </div>
      </div>

      {/* Lunar-Specific Considerations */}
      <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-xl p-4 border border-blue-500/20">
        <h5 className="text-md font-bold text-blue-400 mb-3 flex items-center">
          <span className="mr-2">🌙</span>
          Lunar-Specific Considerations
        </h5>
        <div className="text-sm text-gray-300 space-y-2">
          <p>• Moon's lower gravity (1.62 m/s²) affects slope stability</p>
          <p>• No atmosphere means direct solar radiation impact</p>
          <p>• Thermal cycling affects surface cohesion</p>
          <p>• Micro-meteorite impacts can trigger landslides</p>
          <p>• South-facing slopes receive more solar heating</p>
        </div>
      </div>

      {/* Analysis Notes */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Analysis Notes</h5>
        <div className="text-sm text-gray-400 space-y-2">
          <p>• Min: {safeFormat(safeData.statistics.min)}°, Max: {safeFormat(safeData.statistics.max)}°</p>
          <p>• Mean: {safeFormat(safeData.statistics.mean)}°, Std Dev: {safeFormat(safeData.statistics.stdDev)}°</p>
          <p>• South-facing: {safeData.analysis.southFacingAspects}</p>
          <p>• North-facing: {safeData.analysis.northFacingAspects}</p>
          <p>• Gentle slopes: {safeData.analysis.gentleSlopes}</p>
          <p>• Moderate slopes: {safeData.analysis.moderateSlopes}</p>
          <p>• Steep slopes: {safeData.analysis.steepSlopes}</p>
          <p>• Very steep slopes: {safeData.analysis.verySteepSlopes}</p>
        </div>
      </div>
    </div>
  );
};

export default AspectAnalysis; 
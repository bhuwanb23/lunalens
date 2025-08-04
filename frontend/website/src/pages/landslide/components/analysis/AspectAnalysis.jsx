import React from 'react';

const AspectAnalysis = ({ data }) => {
  // Default data based on lunar_aspect_analysis_report.txt
  const aspectData = data || {
    statistics: {
      min: 0.00,
      max: 359.9999,
      mean: 189.4721,
      stdDev: 89.5053
    },
    analysis: {
      flatAreas: -1.0,
      southFacingAspects: "Higher landslide risk",
      northFacingAspects: "Lower landslide risk",
      gentleSlopes: "Low landslide risk",
      moderateSlopes: "Moderate risk",
      steepSlopes: "High landslide risk",
      verySteepSlopes: "Very high risk"
    }
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
          <div className="text-2xl font-bold text-blue-400">{aspectData.statistics.min}°</div>
          <div className="text-sm text-gray-400">Minimum</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-orange-400">{aspectData.statistics.max}°</div>
          <div className="text-sm text-gray-400">Maximum</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-green-400">{aspectData.statistics.mean.toFixed(1)}°</div>
          <div className="text-sm text-gray-400">Mean</div>
          <div className="text-xs text-gray-500 mt-1">{getAspectDirection(aspectData.statistics.mean)}</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-purple-400">{aspectData.statistics.stdDev.toFixed(1)}</div>
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
                <div className="text-sm text-gray-400">{degrees[direction]}</div>
                <div className={`text-xs mt-1 ${risk.color}`}>
                  {direction === 'North' && 'Lower landslide risk'}
                  {direction === 'East' && 'Moderate landslide risk'}
                  {direction === 'South' && 'Higher landslide risk'}
                  {direction === 'West' && 'Moderate landslide risk'}
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
            <span className="text-gray-300">Steep Slopes (>15°)</span>
            <span className="text-orange-400 text-sm font-medium">High Risk</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-600/30 rounded-lg">
            <span className="text-gray-300">Very Steep Slopes (>30°)</span>
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
          <p>• Aspect values range from 0-360 degrees (0° = North, 90° = East, etc.)</p>
          <p>• Flat areas are assigned -1 (no aspect)</p>
          <p>• South-facing aspects (135-225°) have higher landslide risk</p>
          <p>• North-facing aspects (315-45°) have lower landslide risk</p>
          <p>• Mean aspect of {aspectData.statistics.mean.toFixed(1)}° indicates predominant orientation</p>
        </div>
      </div>
    </div>
  );
};

export default AspectAnalysis; 
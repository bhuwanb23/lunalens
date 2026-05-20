import React from 'react';

const ContourAnalysis = ({ data }) => {
  // Default data based on lunar_contour_analysis_report.txt
  const safeData = {
    terrainComplexity: data?.terrainComplexity ?? 'HIGH',
    statistics: {
      numberOfContours: data?.statistics?.numberOfContours ?? 12,
      numberOfLevels: data?.statistics?.numberOfLevels ?? 14,
      contourDensity: data?.statistics?.contourDensity ?? 0.1211,
      elevationRange: {
        min: data?.statistics?.elevationRange?.min ?? 0.0,
        max: data?.statistics?.elevationRange?.max ?? 650.0
      }
    },
    elevationDistribution: data?.elevationDistribution ?? {
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
  };

  // Helper function to safely format numbers
  const safeFormat = (value, decimals = 2) => {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.00';
    }
    return Number(value).toFixed(decimals);
  };


  const getComplexityBgColor = (complexity) => {
    const colors = {
      'LOW': 'bg-green-500',
      'MODERATE': 'bg-yellow-500',
      'HIGH': 'bg-orange-500',
      'VERY HIGH': 'bg-red-500'
    };
    return colors[complexity] || 'bg-gray-500';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-lg font-bold text-gray-200 flex items-center">
            <span className="mr-2">📐</span>
            Contour Analysis
          </h4>
          <div className={`px-3 py-1 rounded-full ${getComplexityBgColor(safeData.terrainComplexity)} text-white text-xs font-medium`}>
            {safeData.terrainComplexity} COMPLEXITY
          </div>
        </div>
        <p className="text-gray-400 text-sm">
          Contour analysis reveals terrain complexity and elevation distribution patterns
        </p>
      </div>

      {/* Statistics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-blue-400">{safeFormat(safeData.statistics.numberOfContours, 0)}</div>
          <div className="text-sm text-gray-400">Contours</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-orange-400">{safeFormat(safeData.statistics.numberOfLevels, 0)}</div>
          <div className="text-sm text-gray-400">Levels</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-green-400">{safeFormat(safeData.statistics.contourDensity)}</div>
          <div className="text-sm text-gray-400">Density</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-purple-400">{safeFormat(safeData.statistics.elevationRange.max - safeData.statistics.elevationRange.min)} m</div>
          <div className="text-sm text-gray-400">Range</div>
        </div>
      </div>

      {/* Elevation Range */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Elevation Range</h5>
        <div className="flex items-center justify-between p-3 bg-gray-600/30 rounded-lg">
          <div className="text-center">
            <div className="text-lg font-bold text-blue-400">{safeFormat(safeData.statistics.elevationRange.min)} m</div>
            <div className="text-sm text-gray-400">Minimum</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-green-400">{safeFormat(safeData.statistics.elevationRange.max)} m</div>
            <div className="text-sm text-gray-400">Maximum</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-orange-400">{safeFormat(safeData.statistics.elevationRange.max - safeData.statistics.elevationRange.min)} m</div>
            <div className="text-sm text-gray-400">Total Range</div>
          </div>
        </div>
      </div>

      {/* Elevation Distribution */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-4">Elevation Distribution</h5>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {Object.entries(safeData.elevationDistribution || {}).map(([range, count]) => (
            <div key={range} className="bg-gray-600/30 rounded-lg p-3 text-center">
              <div className="text-sm font-medium text-gray-200">{range}</div>
              <div className="text-lg font-bold text-blue-400">{safeFormat(count, 0)}</div>
              <div className="text-xs text-gray-400">contours</div>
            </div>
          ))}
        </div>
      </div>

      {/* Contour Density Analysis */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Contour Density Analysis</h5>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-gray-600/30 rounded-lg">
            <span className="text-gray-300">Density Value</span>
            <span className="text-blue-400 font-mono">{safeFormat(safeData.statistics.contourDensity)}</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-600/30 rounded-lg">
            <span className="text-gray-300">Contours per Level</span>
            <span className="text-green-400 font-mono">{safeFormat(safeData.statistics.numberOfContours / safeData.statistics.numberOfLevels)}</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-600/30 rounded-lg">
            <span className="text-gray-300">Average Elevation Interval</span>
            <span className="text-orange-400 font-mono">{safeFormat((safeData.statistics.elevationRange.max - safeData.statistics.elevationRange.min) / safeData.statistics.numberOfLevels, 1)} m</span>
          </div>
        </div>
      </div>

      {/* Terrain Complexity Assessment */}
      <div className="bg-gradient-to-r from-orange-500/10 to-red-500/10 rounded-xl p-4 border border-orange-500/20">
        <h5 className="text-md font-bold text-orange-400 mb-3 flex items-center">
          <span className="mr-2">🏔️</span>
          Terrain Complexity Assessment
        </h5>
        <div className="text-sm text-gray-300 space-y-2">
          <p>• <strong className="text-orange-400">{safeData.terrainComplexity}</strong> terrain complexity detected</p>
          <p>• {safeFormat(safeData.statistics.numberOfContours, 0)} contour lines indicate varied topography</p>
          <p>• {safeFormat(safeData.statistics.numberOfLevels, 0)} elevation levels show significant relief</p>
          <p>• Contour density of {safeFormat(safeData.statistics.contourDensity)} suggests complex terrain features</p>
          <p>• Elevation range of {safeFormat(safeData.statistics.elevationRange.max - safeData.statistics.elevationRange.min)} meters indicates substantial relief</p>
        </div>
      </div>

      {/* Analysis Notes */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Analysis Notes</h5>
        <div className="text-sm text-gray-400 space-y-2">
          <p>• Contour lines represent lines of equal elevation</p>
          <p>• Closer contour lines indicate steeper slopes</p>
          <p>• Widely spaced contours indicate gentle slopes</p>
          <p>• Contour density indicates terrain complexity</p>
          <p>• Elevation distribution shows relief patterns</p>
          <p>• High contour density suggests potential landslide-prone areas</p>
        </div>
      </div>

      {/* Lunar Context */}
      <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-xl p-4 border border-blue-500/20">
        <h5 className="text-md font-bold text-blue-400 mb-3 flex items-center">
          <span className="mr-2">🌙</span>
          Lunar Context
        </h5>
        <div className="text-sm text-gray-300 space-y-2">
          <p>• Lunar contours reveal ancient impact and volcanic features</p>
          <p>• Contour patterns indicate geological history</p>
          <p>• Steep contours may indicate crater rims or scarps</p>
          <p>• Gentle contours suggest mare plains or degraded features</p>
          <p>• Contour analysis helps identify stable landing sites</p>
        </div>
      </div>
    </div>
  );
};

export default ContourAnalysis; 
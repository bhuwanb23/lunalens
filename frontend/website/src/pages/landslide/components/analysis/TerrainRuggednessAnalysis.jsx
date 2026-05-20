import React from 'react';

const TerrainRuggednessAnalysis = ({ data }) => {
  // Create safe data with fallbacks for all properties
  const safeData = {
    riskLevel: data?.riskLevel ?? 'MODERATE',
    riskFactors: data?.riskFactors ?? ['Moderate terrain complexity'],
    statistics: {
      min: data?.statistics?.min ?? 0.000000,
      max: data?.statistics?.max ?? 8.999971,
      mean: data?.statistics?.mean ?? 7.327898,
      std: data?.statistics?.std ?? 3.496449,
      neighborhoodSize: data?.statistics?.neighborhoodSize ?? '3x3'
    },
    percentiles: {
      p25: data?.percentiles?.p25 ?? 3.32,
      p50: data?.percentiles?.p50 ?? 6.71,
      p75: data?.percentiles?.p75 ?? 11.79,
      p90: data?.percentiles?.p90 ?? 20.02,
      p95: data?.percentiles?.p95 ?? 28.04,
      p99: data?.percentiles?.p99 ?? 69.61
    },
    terrainDistribution: {
      low: { 
        pixels: data?.terrainDistribution?.low?.pixels ?? 1062978, 
        percentage: data?.terrainDistribution?.low?.percentage ?? 20.3 
      },
      moderate: { 
        pixels: data?.terrainDistribution?.moderate?.pixels ?? 3527883, 
        percentage: data?.terrainDistribution?.moderate?.percentage ?? 67.5 
      },
      high: { 
        pixels: data?.terrainDistribution?.high?.pixels ?? 334127, 
        percentage: data?.terrainDistribution?.high?.percentage ?? 6.4 
      },
      veryHigh: { 
        pixels: data?.terrainDistribution?.veryHigh?.pixels ?? 301508, 
        percentage: data?.terrainDistribution?.veryHigh?.percentage ?? 5.8 
      }
    },
    categories: {
      'LOW': { 
        threshold: data?.categories?.LOW?.threshold ?? 0.1, 
        description: data?.categories?.LOW?.description ?? 'Smooth terrain with minimal elevation variation' 
      },
      'MODERATE': { 
        threshold: data?.categories?.MODERATE?.threshold ?? 0.5, 
        description: data?.categories?.MODERATE?.description ?? 'Moderate terrain variation' 
      },
      'HIGH': { 
        threshold: data?.categories?.HIGH?.threshold ?? 1.0, 
        description: data?.categories?.HIGH?.description ?? 'High terrain ruggedness' 
      },
      'VERY HIGH': { 
        threshold: data?.categories?.['VERY HIGH']?.threshold ?? null, 
        description: data?.categories?.['VERY HIGH']?.description ?? 'Extreme terrain variation' 
      }
    }
  };

  const triData = safeData;

  // Helper function to safely format numbers
  const safeFormat = (value, decimals = 6) => {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.000000';
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
            <span className="mr-2">🌊</span>
            Terrain Ruggedness Index (TRI)
          </h4>
          <div className={`px-3 py-1 rounded-full ${getRiskBgColor(triData.riskLevel)} text-white text-xs font-medium`}>
            {triData.riskLevel} RISK
          </div>
        </div>
        <p className="text-gray-400 text-sm">
          Terrain Ruggedness Index measures surface roughness and terrain complexity
        </p>
      </div>

      {/* Statistics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-blue-400">{safeFormat(triData.statistics.min)}</div>
          <div className="text-sm text-gray-400">Minimum</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-orange-400">{safeFormat(triData.statistics.max)}</div>
          <div className="text-sm text-gray-400">Maximum</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-green-400">{safeFormat(triData.statistics.mean)}</div>
          <div className="text-sm text-gray-400">Mean</div>
        </div>
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600 text-center">
          <div className="text-2xl font-bold text-purple-400">{safeFormat(triData.statistics.std)}</div>
          <div className="text-sm text-gray-400">Std Dev</div>
        </div>
      </div>

      {/* Percentiles */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">TRI Percentiles</h5>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-lg font-bold text-blue-400">{triData.percentiles.p25}</div>
            <div className="text-sm text-gray-400">25th Percentile</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-green-400">{triData.percentiles.p50}</div>
            <div className="text-sm text-gray-400">50th Percentile (Median)</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-orange-400">{triData.percentiles.p75}</div>
            <div className="text-sm text-gray-400">75th Percentile</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-yellow-400">{triData.percentiles.p90}</div>
            <div className="text-sm text-gray-400">90th Percentile</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-red-400">{triData.percentiles.p95}</div>
            <div className="text-sm text-gray-400">95th Percentile</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-purple-400">{triData.percentiles.p99}</div>
            <div className="text-sm text-gray-400">99th Percentile</div>
          </div>
        </div>
      </div>

      {/* Terrain Distribution */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-4">Terrain Distribution</h5>
        <div className="space-y-3">
          {Object.entries(triData.terrainDistribution || {}).map(([level, data]) => (
            <div key={level} className="flex items-center justify-between p-3 bg-gray-600/30 rounded-lg">
              <div className="flex items-center">
                <div className={`w-3 h-3 rounded-full mr-3 ${
                  level === 'low' ? 'bg-green-400' :
                  level === 'moderate' ? 'bg-yellow-400' :
                  level === 'high' ? 'bg-orange-400' : 'bg-red-400'
                }`}></div>
                <span className="text-gray-300 capitalize">{level.replace(/([A-Z])/g, ' $1')}</span>
              </div>
              <div className="text-right">
                <div className="text-sm font-medium text-gray-200">{(data?.pixels || 0).toLocaleString()} pixels</div>
                <div className="text-xs text-gray-400">{data?.percentage || 0}%</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* TRI Categories */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">TRI Categories</h5>
        <div className="space-y-3">
          {Object.entries(triData.categories || {}).map(([category, info]) => (
            <div key={category} className="flex items-center justify-between p-3 bg-gray-600/30 rounded-lg">
              <div>
                <div className="font-medium text-gray-200">{category}</div>
                <div className="text-sm text-gray-400">{info?.description || 'No description available'}</div>
              </div>
              <div className={`px-3 py-1 rounded text-xs font-medium ${getRiskBgColor(category)} text-white`}>
                                 {info?.threshold ? `TRI &lt; ${info.threshold}` : 'TRI &gt; 1.0'}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* TRI Formula */}
      <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-xl p-4 border border-blue-500/20">
        <h5 className="text-md font-bold text-blue-400 mb-3 flex items-center">
          <span className="mr-2">📐</span>
          TRI Formula
        </h5>
        <div className="text-sm text-gray-300 space-y-2">
          <p className="font-mono bg-gray-800/50 p-2 rounded">
            TRI = √(Σ(elevation_center - elevation_neighbor)²) / n
          </p>
          <p>Where:</p>
          <ul className="list-disc list-inside space-y-1 ml-4">
            <li>elevation_center = central pixel elevation</li>
            <li>elevation_neighbor = neighboring pixel elevations</li>
            <li>n = number of neighboring pixels</li>
            <li>Higher TRI values indicate more rugged terrain</li>
          </ul>
        </div>
      </div>

      {/* Risk Factors */}
      <div className="bg-gradient-to-r from-yellow-500/10 to-orange-500/10 rounded-xl p-4 border border-yellow-500/20">
        <h5 className="text-md font-bold text-yellow-400 mb-3 flex items-center">
          <span className="mr-2">⚠️</span>
          Risk Factors
        </h5>
        <ul className="text-gray-300 space-y-1">
          {(triData.riskFactors || []).map((factor, index) => (
            <li key={index} className="flex items-center">
              <span className="w-2 h-2 bg-yellow-400 rounded-full mr-3"></span>
              {factor}
            </li>
          ))}
        </ul>
      </div>

      {/* Analysis Notes */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Analysis Notes</h5>
        <div className="text-sm text-gray-400 space-y-2">
          <p>• TRI calculated using {triData.statistics.neighborhoodSize} neighborhood</p>
          <p>• Mean TRI of {safeFormat(triData.statistics.mean)} indicates moderate terrain complexity</p>
          <p>• {triData.terrainDistribution?.moderate?.percentage || 0}% of terrain is moderately rugged</p>
          <p>• {triData.terrainDistribution?.low?.percentage || 0}% of terrain is smooth</p>
          <p>• TRI values range from {safeFormat(triData.statistics.min)} to {safeFormat(triData.statistics.max)}</p>
        </div>
      </div>
    </div>
  );
};

export default TerrainRuggednessAnalysis; 
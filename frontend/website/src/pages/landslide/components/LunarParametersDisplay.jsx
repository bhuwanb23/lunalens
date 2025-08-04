import React, { useState, useEffect } from 'react';

const riskIcons = {
  slope: (
    <svg className="w-5 h-5 text-orange-400 mr-1 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 17l6-6 4 4 8-8" /></svg>
  ),
  aspect: (
    <svg className="w-5 h-5 text-blue-400 mr-1 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth={2} /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6l4 2" /></svg>
  ),
  contour_density: (
    <svg className="w-5 h-5 text-purple-400 mr-1 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" strokeWidth={2} /></svg>
  ),
  elevation: (
    <svg className="w-5 h-5 text-green-400 mr-1 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 17l6-6 4 4 8-8" /></svg>
  ),
  roughness: (
    <svg className="w-5 h-5 text-pink-400 mr-1 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" /></svg>
  ),
  profile_gradient: (
    <svg className="w-5 h-5 text-yellow-400 mr-1 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
  ),
  hillshade: (
    <svg className="w-5 h-5 text-gray-400 mr-1 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth={2} /></svg>
  ),
  crater_ratio: (
    <svg className="w-5 h-5 text-red-400 mr-1 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth={2} /><circle cx="12" cy="12" r="4" stroke="currentColor" strokeWidth={2} /></svg>
  ),
};

const LunarParametersDisplay = ({ isVisible }) => {
  const [lunarData, setLunarData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  // Mock lunar data based on Parameters folder
  const mockLunarData = {
    composite_risk: {
      score: 10.13,
      level: "LOW",
      description: "Safe terrain for lunar operations",
      timestamp: "2025-08-03T18:20:43.908427"
    },
    individual_risks: {
      slope: { score: 19.23, level: "LOW", factors: ["Gentle slopes", "Low slope variability"] },
      aspect: { score: 0.0, level: "SAFE", factors: ["Favorable aspect distribution"] },
      contour_density: { score: 1.21, level: "SAFE", factors: ["Low contour complexity"] },
      elevation: { score: 0.0, level: "SAFE", factors: ["Minimal elevation changes"] },
      roughness: { score: 34.96, level: "MODERATE", factors: ["Moderate terrain complexity"] },
      profile_gradient: { score: 7.43, level: "SAFE", factors: ["Gentle profile gradients"] },
      hillshade: { score: 0.0, level: "SAFE", factors: ["Consistent illumination"] },
      crater_ratio: { score: 0.0, level: "SAFE", factors: ["Low crater density"] }
    },
    detailed_analyses: {
      slope: {
        min: 0.0,
        max: 11.54,
        mean: 5.01,
        std_dev: 2.0,
        risk_level: "LOW",
        risk_factors: ["Gentle slopes", "Low slope variability"],
        thresholds: {
          gentle_slopes: 3.01,
          moderate_slopes: 5.01,
          steep_slopes: 7.01
        }
      },
      aspect: {
        flat_areas: -1.0,
        south_facing_aspects: "Higher landslide risk",
        north_facing_aspects: "Lower landslide risk",
        gentle_slopes: "Low landslide risk",
        moderate_slopes: "Moderate risk",
        steep_slopes: "High landslide risk",
        very_steep_slopes: "Very high risk"
      },
      curvature: {
        profile_curvature_mean: -0.010725,
        plan_curvature_mean: 0.0,
        risk_level: "HIGH",
        risk_factors: ["High curvature variability", "Complex terrain features"]
      },
      elevation: {
        min: 0.0,
        max: 90.0,
        mean: 0.3,
        elevation_range: 90.0,
        standard_deviation: 5.23
      },
      terrain_ruggedness: {
        mean_ruggedness: 34.96,
        risk_level: "MODERATE",
        risk_factors: ["Moderate terrain complexity"]
      },
      scarps_headwalls: {
        detected_features: 12,
        risk_level: "LOW",
        risk_factors: ["Limited scarp features"]
      },
      debris_paths: {
        detected_paths: 8,
        risk_level: "LOW",
        risk_factors: ["Minimal debris flow potential"]
      }
    }
  };

  useEffect(() => {
    if (isVisible) {
      setLoading(true);
      // Simulate loading lunar parameters
      setTimeout(() => {
        setLunarData(mockLunarData);
        setLoading(false);
      }, 1000);
    }
  }, [isVisible]);

  const getRiskColor = (level) => {
    const colors = {
      'SAFE': 'text-green-400',
      'LOW': 'text-yellow-400',
      'MODERATE': 'text-orange-400',
      'HIGH': 'text-red-400'
    };
    return colors[level] || 'text-gray-400';
  };

  const getRiskBgColor = (level) => {
    const colors = {
      'SAFE': 'bg-green-500',
      'LOW': 'bg-yellow-500',
      'MODERATE': 'bg-orange-500',
      'HIGH': 'bg-red-500'
    };
    return colors[level] || 'bg-gray-500';
  };

  if (!isVisible) return null;

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700 shadow-lg">
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400"></div>
          <span className="ml-3 text-gray-300">Loading lunar parameters...</span>
        </div>
      </div>
    );
  }

  if (!lunarData) return null;

  return (
    <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700 shadow-lg">
      <div className="mb-6">
        <h3 className="text-xl font-bold text-gray-100 mb-3">
          Lunar Terrain Parameters
        </h3>
        <p className="text-gray-400 text-sm">
          Comprehensive lunar terrain analysis results from QGIS processing
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-6 bg-gray-700 rounded-lg p-1">
        {['overview', 'slope', 'aspect', 'curvature', 'elevation', 'roughness', 'features'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`flex-1 px-3 py-2 text-xs font-medium rounded-md transition-colors ${
              activeTab === tab
                ? 'bg-blue-600 text-white'
                : 'text-gray-300 hover:text-white hover:bg-gray-600'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="space-y-4">
        {activeTab === 'overview' && (
          <div className="space-y-4">
            {/* Composite Risk */}
            <div className="bg-gray-700 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <h4 className="text-sm font-medium text-gray-200">Composite Risk Assessment</h4>
                <div className={`px-3 py-1 rounded-full ${getRiskBgColor(lunarData.composite_risk.level)} text-white text-xs font-medium`}>
                  {lunarData.composite_risk.level}
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-xs text-gray-400">Risk Score</span>
                  <span className={`text-lg font-bold ${getRiskColor(lunarData.composite_risk.level)}`}>
                    {lunarData.composite_risk.score.toFixed(2)}/100
                  </span>
                </div>
                <div className="w-full bg-gray-600 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${getRiskBgColor(lunarData.composite_risk.level)}`}
                    style={{ width: `${lunarData.composite_risk.score}%` }}
                  ></div>
                </div>
                <p className="text-xs text-gray-400">{lunarData.composite_risk.description}</p>
              </div>
            </div>

            {/* Individual Risk Components */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {Object.entries(lunarData.individual_risks).map(([component, data]) => (
                <div key={component} className="bg-gray-700 rounded-lg p-3 text-center">
                  <div className="text-xs text-gray-400 mb-1 capitalize">{component.replace('_', ' ')}</div>
                  <div className={`text-lg font-bold ${getRiskColor(data.level)}`}>
                    {data.score.toFixed(1)}
                  </div>
                  <div className={`text-xs ${getRiskBgColor(data.level)} text-white px-2 py-1 rounded-full mt-1`}>
                    {data.level}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'slope' && (
          <div className="space-y-4">
            <div className="bg-gray-700 rounded-lg p-4">
              <h4 className="text-sm font-medium text-gray-200 mb-3">Slope Analysis</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3">
                <div className="text-center">
                  <div className="text-xs text-gray-400">Min</div>
                  <div className="text-sm font-medium text-gray-200">{lunarData.detailed_analyses.slope.min}°</div>
                </div>
                <div className="text-center">
                  <div className="text-xs text-gray-400">Max</div>
                  <div className="text-sm font-medium text-gray-200">{lunarData.detailed_analyses.slope.max}°</div>
                </div>
                <div className="text-center">
                  <div className="text-xs text-gray-400">Mean</div>
                  <div className="text-sm font-medium text-gray-200">{lunarData.detailed_analyses.slope.mean}°</div>
                </div>
                <div className="text-center">
                  <div className="text-xs text-gray-400">Std Dev</div>
                  <div className="text-sm font-medium text-gray-200">{lunarData.detailed_analyses.slope.std_dev}</div>
                </div>
              </div>
              <div className="text-xs text-gray-400">
                Risk Factors: {lunarData.detailed_analyses.slope.risk_factors.join(', ')}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'aspect' && (
          <div className="space-y-4">
            <div className="bg-gray-700 rounded-lg p-4">
              <h4 className="text-sm font-medium text-gray-200 mb-3">Aspect Analysis</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-gray-400">South-facing aspects:</span>
                  <span className="text-gray-200">{lunarData.detailed_analyses.aspect.south_facing_aspects}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">North-facing aspects:</span>
                  <span className="text-gray-200">{lunarData.detailed_analyses.aspect.north_facing_aspects}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Gentle slopes:</span>
                  <span className="text-gray-200">{lunarData.detailed_analyses.aspect.gentle_slopes}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Steep slopes:</span>
                  <span className="text-gray-200">{lunarData.detailed_analyses.aspect.steep_slopes}</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'curvature' && (
          <div className="space-y-4">
            <div className="bg-gray-700 rounded-lg p-4">
              <h4 className="text-sm font-medium text-gray-200 mb-3">Curvature Analysis</h4>
              <div className="grid grid-cols-2 gap-3 mb-3">
                <div className="text-center">
                  <div className="text-xs text-gray-400">Profile Curvature</div>
                  <div className="text-sm font-medium text-gray-200">{lunarData.detailed_analyses.curvature.profile_curvature_mean.toFixed(6)}</div>
                </div>
                <div className="text-center">
                  <div className="text-xs text-gray-400">Plan Curvature</div>
                  <div className="text-sm font-medium text-gray-200">{lunarData.detailed_analyses.curvature.plan_curvature_mean}</div>
                </div>
              </div>
              <div className="text-xs text-gray-400">
                Risk Factors: {lunarData.detailed_analyses.curvature.risk_factors.join(', ')}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'elevation' && (
          <div className="space-y-4">
            <div className="bg-gray-700 rounded-lg p-4">
              <h4 className="text-sm font-medium text-gray-200 mb-3">Elevation Analysis</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div className="text-center">
                  <div className="text-xs text-gray-400">Min</div>
                  <div className="text-sm font-medium text-gray-200">{lunarData.detailed_analyses.elevation.min} m</div>
                </div>
                <div className="text-center">
                  <div className="text-xs text-gray-400">Max</div>
                  <div className="text-sm font-medium text-gray-200">{lunarData.detailed_analyses.elevation.max} m</div>
                </div>
                <div className="text-center">
                  <div className="text-xs text-gray-400">Mean</div>
                  <div className="text-sm font-medium text-gray-200">{lunarData.detailed_analyses.elevation.mean} m</div>
                </div>
                <div className="text-center">
                  <div className="text-xs text-gray-400">Range</div>
                  <div className="text-sm font-medium text-gray-200">{lunarData.detailed_analyses.elevation.elevation_range} m</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'roughness' && (
          <div className="space-y-4">
            <div className="bg-gray-700 rounded-lg p-4">
              <h4 className="text-sm font-medium text-gray-200 mb-3">Terrain Ruggedness</h4>
              <div className="text-center mb-3">
                <div className="text-xs text-gray-400">Mean Ruggedness Index</div>
                <div className="text-lg font-bold text-gray-200">{lunarData.detailed_analyses.terrain_ruggedness.mean_ruggedness.toFixed(2)}</div>
              </div>
              <div className="text-xs text-gray-400">
                Risk Factors: {lunarData.detailed_analyses.terrain_ruggedness.risk_factors.join(', ')}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'features' && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gray-700 rounded-lg p-4">
                <h4 className="text-sm font-medium text-gray-200 mb-3">Scarps & Headwalls</h4>
                <div className="text-center mb-3">
                  <div className="text-xs text-gray-400">Detected Features</div>
                  <div className="text-lg font-bold text-gray-200">{lunarData.detailed_analyses.scarps_headwalls.detected_features}</div>
                </div>
                <div className="text-xs text-gray-400">
                  Risk Factors: {lunarData.detailed_analyses.scarps_headwalls.risk_factors.join(', ')}
                </div>
              </div>
              <div className="bg-gray-700 rounded-lg p-4">
                <h4 className="text-sm font-medium text-gray-200 mb-3">Debris Flow Paths</h4>
                <div className="text-center mb-3">
                  <div className="text-xs text-gray-400">Detected Paths</div>
                  <div className="text-lg font-bold text-gray-200">{lunarData.detailed_analyses.debris_paths.detected_paths}</div>
                </div>
                <div className="text-xs text-gray-400">
                  Risk Factors: {lunarData.detailed_analyses.debris_paths.risk_factors.join(', ')}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default LunarParametersDisplay; 
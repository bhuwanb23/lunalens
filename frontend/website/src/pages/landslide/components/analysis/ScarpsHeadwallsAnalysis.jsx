import React from 'react';

const ScarpsHeadwallsAnalysis = ({ data }) => {
  // Default data based on scarps_headwalls_analysis_report.txt
  const scarpsData = data || {
    riskLevel: 'LOW',
    riskFactors: ['Limited scarp features'],
    statistics: {
      scarpPixels: 195324.0000,
      densityPercent: 0.0504,
      slopeThreshold: 30.0,
      curvatureThreshold: 0.001,
      triThreshold: 0.5,
      featureCount: 1331731
    },
    parameters: {
      slope: {
        min: 0.0000,
        max: 89.9996,
        mean: 0.2286,
        std: 4.5305
      },
      aspect: {
        min: 0.0000,
        max: 359.9999,
        mean: 189.4721,
        std: 89.5053
      },
      curvature: {
        min: 0.0000,
        max: 89.9996,
        mean: 0.2286,
        std: 4.5305
      },
      tri: {
        min: 0.0000,
        max: 89.9996,
        mean: 0.2286,
        std: 4.5305
      }
    },
    detectionResults: {
      totalPixels: 5227296,
      scarpPixels: 195324,
      densityPercent: 0.0504,
      featureCount: 1331731
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
            Scarps & Headwalls Analysis
          </h4>
          <div className={`px-3 py-1 rounded-full ${getRiskBgColor(scarpsData.riskLevel)} text-white text-xs font-medium`}>
            {scarpsData.riskLevel} RISK
          </div>
        </div>
        <p className="text-gray-400 text-sm">
          Detection of lunar scarps and headwalls indicating potential landslide features
        </p>
      </div>

      {/* Detection Results */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
          <h5 className="text-md font-bold text-gray-200 mb-3">Detection Results</h5>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-400">Scarp Pixels:</span>
              <span className="text-blue-400 font-mono">{scarpsData.statistics.scarpPixels.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Density:</span>
              <span className="text-green-400 font-mono">{scarpsData.statistics.densityPercent}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Feature Count:</span>
              <span className="text-orange-400 font-mono">{scarpsData.statistics.featureCount.toLocaleString()}</span>
            </div>
          </div>
        </div>

        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
          <h5 className="text-md font-bold text-gray-200 mb-3">Detection Thresholds</h5>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-400">Slope Threshold:</span>
              <span className="text-blue-400 font-mono">{scarpsData.statistics.slopeThreshold}°</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Curvature Threshold:</span>
              <span className="text-green-400 font-mono">{scarpsData.statistics.curvatureThreshold}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">TRI Threshold:</span>
              <span className="text-orange-400 font-mono">{scarpsData.statistics.triThreshold}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Parameter Analysis */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-4">Parameter Analysis</h5>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h6 className="font-semibold text-blue-400 mb-2">Slope Analysis</h6>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Min:</span>
                <span className="text-gray-300">{scarpsData.parameters.slope.min}°</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Max:</span>
                <span className="text-gray-300">{scarpsData.parameters.slope.max}°</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Mean:</span>
                <span className="text-gray-300">{scarpsData.parameters.slope.mean}°</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Std Dev:</span>
                <span className="text-gray-300">{scarpsData.parameters.slope.std}</span>
              </div>
            </div>
          </div>

          <div>
            <h6 className="font-semibold text-green-400 mb-2">Aspect Analysis</h6>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Min:</span>
                <span className="text-gray-300">{scarpsData.parameters.aspect.min}°</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Max:</span>
                <span className="text-gray-300">{scarpsData.parameters.aspect.max}°</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Mean:</span>
                <span className="text-gray-300">{scarpsData.parameters.aspect.mean}°</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Std Dev:</span>
                <span className="text-gray-300">{scarpsData.parameters.aspect.std}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Detection Methodology */}
      <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-xl p-4 border border-blue-500/20">
        <h5 className="text-md font-bold text-blue-400 mb-3 flex items-center">
          <span className="mr-2">🔍</span>
          Detection Methodology
        </h5>
        <div className="text-sm text-gray-300 space-y-2">
          <p>1. <strong>DEM Loading:</strong> Digital Elevation Model loaded for terrain analysis</p>
                      <p>2. <strong>Slope Calculation:</strong> Identifies steep areas (&gt;30°) indicating cliffs/headwalls</p>
          <p>3. <strong>Hillshade Generation:</strong> Visual enhancement for manual verification</p>
          <p>4. <strong>Curvature Analysis:</strong> Detects concave/convex forms of scarps</p>
          <p>5. <strong>Aspect Mapping:</strong> Orientation analysis of scarp faces</p>
          <p>6. <strong>TRI Calculation:</strong> Terrain Ruggedness Index for rugged terrain</p>
          <p>7. <strong>Multi-Parameter Detection:</strong> Combined thresholding for scarp identification</p>
          <p>8. <strong>Vector Conversion:</strong> Raster features converted to editable polygons</p>
        </div>
      </div>

      {/* Risk Factors */}
      <div className="bg-gradient-to-r from-green-500/10 to-blue-500/10 rounded-xl p-4 border border-green-500/20">
        <h5 className="text-md font-bold text-green-400 mb-3 flex items-center">
          <span className="mr-2">✅</span>
          Risk Factors
        </h5>
        <ul className="text-gray-300 space-y-1">
          {scarpsData.riskFactors.map((factor, index) => (
            <li key={index} className="flex items-center">
              <span className="w-2 h-2 bg-green-400 rounded-full mr-3"></span>
              {factor}
            </li>
          ))}
        </ul>
      </div>

      {/* Recommendations */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Recommendations</h5>
        <div className="text-sm text-gray-400 space-y-2">
          <p>• Use hillshade layer for visual verification of detected scarps</p>
          <p>• Adjust slope, curvature, and TRI thresholds based on terrain characteristics</p>
          <p>• Manually edit the generated shapefile for precise scarp boundaries</p>
          <p>• Consider using additional filters for noise reduction</p>
          <p>• Validate results against optical imagery when available</p>
                      <p>• High slope areas (&gt;30°) often indicate scarps or headwalls</p>
          <p>• Dense contour lines often trace along scarp faces</p>
        </div>
      </div>

      {/* Analysis Notes */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Analysis Notes</h5>
        <div className="text-sm text-gray-400 space-y-2">
          <p>• {scarpsData.statistics.scarpPixels.toLocaleString()} scarp pixels detected</p>
          <p>• Scarp density of {scarpsData.statistics.densityPercent}% indicates limited features</p>
          <p>• {scarpsData.statistics.featureCount.toLocaleString()} vector features generated</p>
                      <p>• Detection based on slope &gt; {scarpsData.statistics.slopeThreshold}°</p>
          <p>• Curvature threshold of {scarpsData.statistics.curvatureThreshold} for feature detection</p>
          <p>• TRI threshold of {scarpsData.statistics.triThreshold} for ruggedness assessment</p>
        </div>
      </div>
    </div>
  );
};

export default ScarpsHeadwallsAnalysis; 
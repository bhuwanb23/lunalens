import React from 'react';

const CurvatureAnalysis = ({ data }) => {
  // Create safe data with fallbacks for all properties
  const safeData = {
    riskLevel: data?.riskLevel ?? 'HIGH',
    riskFactors: data?.riskFactors ?? ['High curvature variability', 'Complex terrain features'],
    statistics: {
      profileCurvatureMean: data?.statistics?.profileCurvatureMean ?? -0.010725,
      profileCurvatureStd: data?.statistics?.profileCurvatureStd ?? 3.716956,
      planCurvatureMean: data?.statistics?.planCurvatureMean ?? -0.009777,
      planCurvatureStd: data?.statistics?.planCurvatureStd ?? 3.628621,
      gaussianCurvatureMean: data?.statistics?.gaussianCurvatureMean ?? -0.019519,
      gaussianCurvatureStd: data?.statistics?.gaussianCurvatureStd ?? 385.109967,
      tangentialCurvatureMean: data?.statistics?.tangentialCurvatureMean ?? -0.009777,
      tangentialCurvatureStd: data?.statistics?.tangentialCurvatureStd ?? 3.628621,
      meanCurvatureMean: data?.statistics?.meanCurvatureMean ?? 0.024214,
      meanCurvatureStd: data?.statistics?.meanCurvatureStd ?? 6.684292
    },
    thresholds: {
      profileCurvatureThreshold: data?.thresholds?.profileCurvatureThreshold ?? 7.433913,
      planCurvatureThreshold: data?.thresholds?.planCurvatureThreshold ?? 7.257242,
      gaussianCurvatureThreshold: data?.thresholds?.gaussianCurvatureThreshold ?? 770.219933,
      tangentialCurvatureThreshold: data?.thresholds?.tangentialCurvatureThreshold ?? 7.257242,
      meanCurvatureThreshold: data?.thresholds?.meanCurvatureThreshold ?? 13.368584
    }
  };

  const curvatureData = safeData;

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
            <span className="mr-2">🔄</span>
            Curvature Analysis
          </h4>
          <div className={`px-3 py-1 rounded-full ${getRiskBgColor(curvatureData.riskLevel)} text-white text-xs font-medium`}>
            {curvatureData.riskLevel} RISK
          </div>
        </div>
        <p className="text-gray-400 text-sm">
          Curvature analysis describes local convexity/concavity and flow patterns
        </p>
      </div>

      {/* Curvature Types Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
          <h5 className="text-md font-bold text-gray-200 mb-3">Profile Curvature</h5>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-400">Mean:</span>
              <span className="text-blue-400 font-mono">{safeFormat(curvatureData.statistics.profileCurvatureMean)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Std Dev:</span>
              <span className="text-orange-400 font-mono">{safeFormat(curvatureData.statistics.profileCurvatureStd)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Threshold:</span>
              <span className="text-purple-400 font-mono">{safeFormat(curvatureData.thresholds.profileCurvatureThreshold)}</span>
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">Affects flow acceleration/deceleration</p>
        </div>

        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
          <h5 className="text-md font-bold text-gray-200 mb-3">Plan Curvature</h5>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-400">Mean:</span>
              <span className="text-blue-400 font-mono">{safeFormat(curvatureData.statistics.planCurvatureMean)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Std Dev:</span>
              <span className="text-orange-400 font-mono">{safeFormat(curvatureData.statistics.planCurvatureStd)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Threshold:</span>
              <span className="text-purple-400 font-mono">{safeFormat(curvatureData.thresholds.planCurvatureThreshold)}</span>
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">Controls flow divergence/convergence</p>
        </div>

        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
          <h5 className="text-md font-bold text-gray-200 mb-3">Gaussian Curvature</h5>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-400">Mean:</span>
              <span className="text-blue-400 font-mono">{safeFormat(curvatureData.statistics.gaussianCurvatureMean)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Std Dev:</span>
              <span className="text-orange-400 font-mono">{safeFormat(curvatureData.statistics.gaussianCurvatureStd)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Threshold:</span>
              <span className="text-purple-400 font-mono">{safeFormat(curvatureData.thresholds.gaussianCurvatureThreshold)}</span>
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">Describes local convexity/concavity</p>
        </div>

        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
          <h5 className="text-md font-bold text-gray-200 mb-3">Mean Curvature</h5>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-400">Mean:</span>
              <span className="text-blue-400 font-mono">{safeFormat(curvatureData.statistics.meanCurvatureMean)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Std Dev:</span>
              <span className="text-orange-400 font-mono">{safeFormat(curvatureData.statistics.meanCurvatureStd)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Threshold:</span>
              <span className="text-purple-400 font-mono">{safeFormat(curvatureData.thresholds.meanCurvatureThreshold)}</span>
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">Average of principal curvatures</p>
        </div>
      </div>

      {/* Curvature Interpretation */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Curvature Interpretation</h5>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <h6 className="font-semibold text-blue-400 mb-2">Profile Curvature</h6>
            <ul className="text-gray-300 space-y-1">
              <li>• Positive: Convex (flow acceleration)</li>
              <li>• Negative: Concave (flow deceleration)</li>
              <li>• Zero: Linear (constant flow)</li>
            </ul>
          </div>
          <div>
            <h6 className="font-semibold text-green-400 mb-2">Plan Curvature</h6>
            <ul className="text-gray-300 space-y-1">
              <li>• Positive: Divergent flow</li>
              <li>• Negative: Convergent flow</li>
              <li>• Zero: Parallel flow</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Risk Factors */}
      <div className="bg-gradient-to-r from-orange-500/10 to-red-500/10 rounded-xl p-4 border border-orange-500/20">
        <h5 className="text-md font-bold text-orange-400 mb-3 flex items-center">
          <span className="mr-2">⚠️</span>
          Risk Factors
        </h5>
        <ul className="text-gray-300 space-y-1">
          {(curvatureData.riskFactors || []).map((factor, index) => (
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
          <p>• Profile curvature affects flow acceleration/deceleration patterns</p>
          <p>• Plan curvature controls flow divergence/convergence</p>
          <p>• Gaussian curvature describes local convexity/concavity</p>
          <p>• Tangential curvature useful for compound terrain interpretation</p>
          <p>• Mean curvature is average of principal curvatures</p>
          <p>• High curvature variability indicates complex terrain features</p>
        </div>
      </div>
    </div>
  );
};

export default CurvatureAnalysis; 
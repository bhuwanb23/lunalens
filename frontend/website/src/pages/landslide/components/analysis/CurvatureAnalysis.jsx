import React from 'react';

const CurvatureAnalysis = ({ data }) => {
  // Default data based on lunar_curvature_analysis_report.txt
  const curvatureData = data || {
    riskLevel: 'HIGH',
    riskFactors: ['High curvature variability', 'Complex terrain features'],
    statistics: {
      profileCurvatureMean: -0.010725,
      profileCurvatureStd: 3.716956,
      planCurvatureMean: -0.009777,
      planCurvatureStd: 3.628621,
      gaussianCurvatureMean: -0.019519,
      gaussianCurvatureStd: 385.109967,
      tangentialCurvatureMean: -0.009777,
      tangentialCurvatureStd: 3.628621,
      meanCurvatureMean: 0.024214,
      meanCurvatureStd: 6.684292
    },
    thresholds: {
      profileCurvatureThreshold: 7.433913,
      planCurvatureThreshold: 7.257242,
      gaussianCurvatureThreshold: 770.219933,
      tangentialCurvatureThreshold: 7.257242,
      meanCurvatureThreshold: 13.368584
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
              <span className="text-blue-400 font-mono">{curvatureData.statistics.profileCurvatureMean.toFixed(6)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Std Dev:</span>
              <span className="text-orange-400 font-mono">{curvatureData.statistics.profileCurvatureStd.toFixed(6)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Threshold:</span>
              <span className="text-purple-400 font-mono">{curvatureData.thresholds.profileCurvatureThreshold.toFixed(6)}</span>
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">Affects flow acceleration/deceleration</p>
        </div>

        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
          <h5 className="text-md font-bold text-gray-200 mb-3">Plan Curvature</h5>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-400">Mean:</span>
              <span className="text-blue-400 font-mono">{curvatureData.statistics.planCurvatureMean.toFixed(6)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Std Dev:</span>
              <span className="text-orange-400 font-mono">{curvatureData.statistics.planCurvatureStd.toFixed(6)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Threshold:</span>
              <span className="text-purple-400 font-mono">{curvatureData.thresholds.planCurvatureThreshold.toFixed(6)}</span>
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">Controls flow divergence/convergence</p>
        </div>

        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
          <h5 className="text-md font-bold text-gray-200 mb-3">Gaussian Curvature</h5>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-400">Mean:</span>
              <span className="text-blue-400 font-mono">{curvatureData.statistics.gaussianCurvatureMean.toFixed(6)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Std Dev:</span>
              <span className="text-orange-400 font-mono">{curvatureData.statistics.gaussianCurvatureStd.toFixed(6)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Threshold:</span>
              <span className="text-purple-400 font-mono">{curvatureData.thresholds.gaussianCurvatureThreshold.toFixed(6)}</span>
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">Describes local convexity/concavity</p>
        </div>

        <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
          <h5 className="text-md font-bold text-gray-200 mb-3">Mean Curvature</h5>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-400">Mean:</span>
              <span className="text-blue-400 font-mono">{curvatureData.statistics.meanCurvatureMean.toFixed(6)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Std Dev:</span>
              <span className="text-orange-400 font-mono">{curvatureData.statistics.meanCurvatureStd.toFixed(6)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Threshold:</span>
              <span className="text-purple-400 font-mono">{curvatureData.thresholds.meanCurvatureThreshold.toFixed(6)}</span>
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
          {curvatureData.riskFactors.map((factor, index) => (
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
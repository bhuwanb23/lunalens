import React from 'react';

const CompositeRiskAssessment = ({ data }) => {
  // Default data based on lunar_risk_analysis_results.txt
  const riskData = data || {
    overallRisk: {
      score: 10.13,
      level: 'LOW',
      description: 'Safe terrain for lunar operations'
    },
    components: [
      {
        name: 'SLOPE',
        riskScore: 19.23,
        weight: 0.30,
        weightedContribution: 5.77
      },
      {
        name: 'ASPECT',
        riskScore: 0.00,
        weight: 0.15,
        weightedContribution: 0.00
      },
      {
        name: 'CONTOUR_DENSITY',
        riskScore: 1.21,
        weight: 0.10,
        weightedContribution: 0.12
      },
      {
        name: 'ELEVATION',
        riskScore: 0.00,
        weight: 0.05,
        weightedContribution: 0.00
      },
      {
        name: 'ROUGHNESS',
        riskScore: 34.96,
        weight: 0.10,
        weightedContribution: 3.50
      },
      {
        name: 'PROFILE_GRADIENT',
        riskScore: 7.43,
        weight: 0.10,
        weightedContribution: 0.74
      },
      {
        name: 'HILLSHADE',
        riskScore: 0.00,
        weight: 0.15,
        weightedContribution: 0.00
      },
      {
        name: 'CRATER_RATIO',
        riskScore: 0.00,
        weight: 0.05,
        weightedContribution: 0.00
      }
    ],
    analysis: {
      totalReportsProcessed: 8,
      availableComponents: ['slope', 'aspect', 'contour_density', 'elevation', 'roughness', 'profile_gradient', 'hillshade', 'crater_ratio'],
      missingComponents: ['hillshade', 'crater_ratio']
    },
    weights: {
      slope: 0.30,
      aspect: 0.15,
      hillshade: 0.15,
      contour_density: 0.10,
      profile_gradient: 0.10,
      crater_ratio: 0.05,
      roughness: 0.10,
      elevation: 0.05
    }
  };

  const getRiskColor = (level) => {
    const colors = {
      'LOW': 'text-green-400',
      'MODERATE': 'text-yellow-400',
      'HIGH': 'text-orange-400',
      'VERY HIGH': 'text-red-400',
      'EXTREME': 'text-red-600'
    };
    return colors[level] || 'text-gray-400';
  };

  const getRiskBgColor = (level) => {
    const colors = {
      'LOW': 'bg-green-500',
      'MODERATE': 'bg-yellow-500',
      'HIGH': 'bg-orange-500',
      'VERY HIGH': 'bg-red-500',
      'EXTREME': 'bg-red-600'
    };
    return colors[level] || 'bg-gray-500';
  };

  const getRiskLevelDescription = (level) => {
    const descriptions = {
      'LOW': 'Safe terrain for lunar operations',
      'MODERATE': 'Moderate terrain challenges',
      'HIGH': 'High risk terrain - caution required',
      'VERY HIGH': 'Very high risk - extreme caution',
      'EXTREME': 'Extreme risk - avoid if possible'
    };
    return descriptions[level] || 'Unknown risk level';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-lg font-bold text-gray-200 flex items-center">
            <span className="mr-2">⚠️</span>
            Composite Risk Assessment
          </h4>
          <div className={`px-3 py-1 rounded-full ${getRiskBgColor(riskData.overallRisk.level)} text-white text-xs font-medium`}>
            {riskData.overallRisk.level} RISK
          </div>
        </div>
        <p className="text-gray-400 text-sm">
          Weighted composite scoring of all terrain parameters for landslide risk assessment
        </p>
      </div>

      {/* Overall Risk Score */}
      <div className="bg-gradient-to-r from-green-500/10 to-blue-500/10 rounded-xl p-6 border border-green-500/20">
        <div className="text-center mb-4">
          <div className="text-4xl font-bold text-green-400 mb-2">{riskData.overallRisk.score}/100</div>
          <div className="text-lg text-gray-300 mb-1">Composite Risk Score</div>
          <div className={`text-sm font-medium ${getRiskColor(riskData.overallRisk.level)}`}>
            {riskData.overallRisk.level} RISK
          </div>
        </div>
        <p className="text-gray-300 text-center">
          {getRiskLevelDescription(riskData.overallRisk.level)}
        </p>
      </div>

      {/* Risk Components */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-4">Individual Risk Components</h5>
        <div className="space-y-3">
          {riskData.components.map((component, index) => (
            <div key={index} className="bg-gray-600/30 rounded-lg p-3">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-gray-200">{component.name.replace(/_/g, ' ')}</span>
                <div className="flex items-center space-x-3">
                  <span className="text-sm text-gray-400">Weight: {(component.weight * 100).toFixed(0)}%</span>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    component.riskScore < 20 ? 'bg-green-500' :
                    component.riskScore < 40 ? 'bg-yellow-500' :
                    component.riskScore < 60 ? 'bg-orange-500' : 'bg-red-500'
                  } text-white`}>
                    {component.riskScore.toFixed(2)}
                  </span>
                </div>
              </div>
              <div className="w-full bg-gray-600 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${
                    component.riskScore < 20 ? 'bg-green-500' :
                    component.riskScore < 40 ? 'bg-yellow-500' :
                    component.riskScore < 60 ? 'bg-orange-500' : 'bg-red-500'
                  }`}
                  style={{ width: `${component.riskScore}%` }}
                ></div>
              </div>
              <div className="flex justify-between text-xs text-gray-400 mt-1">
                <span>Contribution: {component.weightedContribution.toFixed(2)}</span>
                <span>Score: {component.riskScore.toFixed(2)}/100</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Risk Weights */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Risk Weights</h5>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {Object.entries(riskData.weights).map(([parameter, weight]) => (
            <div key={parameter} className="bg-gray-600/30 rounded-lg p-3 text-center">
              <div className="text-sm font-medium text-gray-200 mb-1">{parameter.replace(/_/g, ' ')}</div>
              <div className="text-lg font-bold text-blue-400">{(weight * 100).toFixed(0)}%</div>
            </div>
          ))}
        </div>
      </div>

      {/* Analysis Summary */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Analysis Summary</h5>
        <div className="space-y-3">
          <div className="flex justify-between">
            <span className="text-gray-400">Total Reports Processed:</span>
            <span className="text-blue-400">{riskData.analysis.totalReportsProcessed}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Available Components:</span>
            <span className="text-green-400">{riskData.analysis.availableComponents.length}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Missing Components:</span>
            <span className="text-orange-400">{riskData.analysis.missingComponents.length}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Maximum Individual Risk:</span>
            <span className="text-red-400">{Math.max(...riskData.components.map(c => c.riskScore)).toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Minimum Individual Risk:</span>
            <span className="text-green-400">{Math.min(...riskData.components.map(c => c.riskScore)).toFixed(2)}</span>
          </div>
        </div>
      </div>

      {/* Risk Levels */}
      <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-xl p-4 border border-blue-500/20">
        <h5 className="text-md font-bold text-blue-400 mb-3 flex items-center">
          <span className="mr-2">📊</span>
          Risk Level Classifications
        </h5>
        <div className="space-y-2 text-sm">
          <div className="flex items-center justify-between p-2 bg-gray-600/30 rounded">
            <span className="text-gray-300">LOW (0-20)</span>
            <span className="text-green-400">Safe terrain for lunar operations</span>
          </div>
          <div className="flex items-center justify-between p-2 bg-gray-600/30 rounded">
            <span className="text-gray-300">MODERATE (20-40)</span>
            <span className="text-yellow-400">Moderate terrain challenges</span>
          </div>
          <div className="flex items-center justify-between p-2 bg-gray-600/30 rounded">
            <span className="text-gray-300">HIGH (40-60)</span>
            <span className="text-orange-400">High risk terrain - caution required</span>
          </div>
          <div className="flex items-center justify-between p-2 bg-gray-600/30 rounded">
            <span className="text-gray-300">VERY HIGH (60-80)</span>
            <span className="text-red-400">Very high risk - extreme caution</span>
          </div>
          <div className="flex items-center justify-between p-2 bg-gray-600/30 rounded">
            <span className="text-gray-300">EXTREME (80-100)</span>
            <span className="text-red-600">Extreme risk - avoid if possible</span>
          </div>
        </div>
      </div>

      {/* Formula */}
      <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
        <h5 className="text-md font-bold text-gray-200 mb-3">Risk Calculation Formula</h5>
        <div className="text-sm text-gray-400 space-y-2">
          <p className="font-mono bg-gray-800/50 p-2 rounded">
            Composite Risk = Σ(Component_Risk × Component_Weight)
          </p>
          <p>Where weights sum to 1.0 and individual risks are normalized to 0-100 scale.</p>
          <p>• Higher scores indicate greater landslide risk</p>
          <p>• Weights reflect relative importance of each parameter</p>
          <p>• Composite score provides overall terrain safety assessment</p>
        </div>
      </div>

      {/* Recommendations */}
      <div className="bg-gradient-to-r from-green-500/10 to-blue-500/10 rounded-xl p-4 border border-green-500/20">
        <h5 className="text-md font-bold text-green-400 mb-3 flex items-center">
          <span className="mr-2">✅</span>
          Risk Mitigation Recommendations
        </h5>
        <div className="text-sm text-gray-300 space-y-2">
          <p>• Terrain is generally safe for lunar operations</p>
          <p>• Standard safety protocols sufficient</p>
          <p>• Monitor for micro-meteorite impacts</p>
          <p>• Consider thermal cycling effects</p>
          <p>• Regular terrain monitoring advised</p>
        </div>
      </div>
    </div>
  );
};

export default CompositeRiskAssessment; 
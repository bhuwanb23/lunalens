import React, { useState } from 'react';
import SlopeAnalysis from './analysis/SlopeAnalysis';
import AspectAnalysis from './analysis/AspectAnalysis';
import ElevationAnalysis from './analysis/ElevationAnalysis';
import CurvatureAnalysis from './analysis/CurvatureAnalysis';
import TerrainRuggednessAnalysis from './analysis/TerrainRuggednessAnalysis';
import ContourAnalysis from './analysis/ContourAnalysis';
import ScarpsHeadwallsAnalysis from './analysis/ScarpsHeadwallsAnalysis';
import CompositeRiskAssessment from './analysis/CompositeRiskAssessment';

const AnalysisResults = ({ isVisible, analysisData }) => {
  const [activeTab, setActiveTab] = useState('overview');

  if (!isVisible) return null;

  const tabs = [
    { id: 'overview', name: 'Overview', icon: '📊' },
    { id: 'slope', name: 'Slope', icon: '📈' },
    { id: 'aspect', name: 'Aspect', icon: '🧭' },
    { id: 'elevation', name: 'Elevation', icon: '🏔️' },
    { id: 'curvature', name: 'Curvature', icon: '🔄' },
    { id: 'roughness', name: 'Roughness', icon: '🌊' },
    { id: 'contours', name: 'Contours', icon: '📐' },
    { id: 'scarps', name: 'Scarps', icon: '🏔️' },
    { id: 'composite', name: 'Risk Assessment', icon: '⚠️' }
  ];

  return (
    <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl p-6 border-2 border-gray-700 shadow-2xl relative overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-purple-500/3 to-orange-500/5 animate-pulse"></div>
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(255,255,255,0.05)_0%,transparent_70%)]"></div>
      
      <div className="relative z-10">
        {/* Header */}
        <div className="mb-6">
          <h3 className="text-2xl font-bold text-gray-100 mb-2 flex items-center">
            <span className="mr-3">🌑</span>
            Lunar Terrain Analysis Results
          </h3>
          <p className="text-gray-400 text-sm">
            Comprehensive analysis of lunar terrain parameters and landslide risk assessment
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex flex-wrap gap-2 mb-6 bg-gray-700/50 rounded-xl p-2">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg'
                  : 'text-gray-300 hover:text-white hover:bg-gray-600'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.name}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Quick Stats */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
                  <div className="text-2xl font-bold text-blue-400">10.13</div>
                  <div className="text-sm text-gray-400">Composite Risk Score</div>
                  <div className="text-xs text-green-400 mt-1">LOW RISK</div>
                </div>
                <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
                  <div className="text-2xl font-bold text-orange-400">5.01°</div>
                  <div className="text-sm text-gray-400">Mean Slope</div>
                  <div className="text-xs text-green-400 mt-1">GENTLE</div>
                </div>
                <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
                  <div className="text-2xl font-bold text-purple-400">9.95</div>
                  <div className="text-sm text-gray-400">Mean TRI</div>
                  <div className="text-xs text-yellow-400 mt-1">MODERATE</div>
                </div>
                <div className="bg-gray-700/50 rounded-xl p-4 border border-gray-600">
                  <div className="text-2xl font-bold text-green-400">8</div>
                  <div className="text-sm text-gray-400">Parameters Analyzed</div>
                  <div className="text-xs text-blue-400 mt-1">COMPLETE</div>
                </div>
              </div>

              {/* Risk Summary */}
              <div className="bg-gradient-to-r from-green-500/10 to-blue-500/10 rounded-xl p-6 border border-green-500/20">
                <h4 className="text-lg font-bold text-green-400 mb-3 flex items-center">
                  <span className="mr-2">✅</span>
                  Analysis Summary
                </h4>
                <p className="text-gray-300 mb-4">
                  The lunar terrain analysis indicates <strong className="text-green-400">LOW RISK</strong> for landslide events. 
                  The composite risk score of 10.13/100 suggests safe terrain for lunar operations.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <div className="text-gray-400 mb-2">Key Findings:</div>
                    <ul className="text-gray-300 space-y-1">
                      <li>• Gentle slopes (mean: 5.01°)</li>
                      <li>• Low terrain ruggedness</li>
                      <li>• Minimal scarp features detected</li>
                      <li>• Favorable aspect distribution</li>
                    </ul>
                  </div>
                  <div>
                    <div className="text-gray-400 mb-2">Recommendations:</div>
                    <ul className="text-gray-300 space-y-1">
                      <li>• Standard safety protocols sufficient</li>
                      <li>• Monitor for micro-meteorite impacts</li>
                      <li>• Consider thermal cycling effects</li>
                      <li>• Regular terrain monitoring advised</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'slope' && <SlopeAnalysis data={analysisData?.slope} />}
          {activeTab === 'aspect' && <AspectAnalysis data={analysisData?.aspect} />}
          {activeTab === 'elevation' && <ElevationAnalysis data={analysisData?.elevation} />}
          {activeTab === 'curvature' && <CurvatureAnalysis data={analysisData?.curvature} />}
          {activeTab === 'roughness' && <TerrainRuggednessAnalysis data={analysisData?.roughness} />}
          {activeTab === 'contours' && <ContourAnalysis data={analysisData?.contours} />}
          {activeTab === 'scarps' && <ScarpsHeadwallsAnalysis data={analysisData?.scarps} />}
          {activeTab === 'composite' && <CompositeRiskAssessment data={analysisData?.composite} />}
        </div>
      </div>

      {/* Corner decorations */}
      <div className="absolute top-4 left-4 w-6 h-6 border-l-2 border-t-2 border-blue-500/30 rounded-tl-lg"></div>
      <div className="absolute top-4 right-4 w-6 h-6 border-r-2 border-t-2 border-purple-500/30 rounded-tr-lg"></div>
      <div className="absolute bottom-4 left-4 w-6 h-6 border-l-2 border-b-2 border-blue-500/30 rounded-bl-lg"></div>
      <div className="absolute bottom-4 right-4 w-6 h-6 border-r-2 border-b-2 border-purple-500/30 rounded-br-lg"></div>
    </div>
  );
};

export default AnalysisResults; 
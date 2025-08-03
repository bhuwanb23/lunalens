import React from 'react';

const AnalyticsHeader = ({ totalRecords, totalObjects, averageConfidence }) => {
  return (
    <section className="relative h-[200px] flex items-center justify-center overflow-hidden">
      <div className="absolute inset-0 moon-glow"></div>
      <div className="absolute top-10 right-20 w-32 h-32 rounded-full bg-gradient-to-br from-gray-200 to-gray-400 opacity-20"></div>
      <div className="absolute bottom-10 left-16 w-20 h-20 rounded-full bg-gradient-to-br from-blue-300 to-blue-500 opacity-10"></div>
      
      <div className="text-center z-10">
        <h2 className="text-4xl font-light mb-4 bg-gradient-to-r from-gray-200 to-blue-300 bg-clip-text text-transparent">
          Boulder Detection Analytics
        </h2>
        <p className="text-lg text-gray-400 max-w-2xl mx-auto mb-6">
          Comprehensive analysis records and performance metrics for lunar surface detection
        </p>
        
        {/* Quick Stats */}
        <div className="flex justify-center space-x-8">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-400">{totalRecords}</div>
            <div className="text-sm text-gray-400">Total Analyses</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-400">{totalObjects}</div>
            <div className="text-sm text-gray-400">Objects Detected</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-400">{(averageConfidence * 100).toFixed(1)}%</div>
            <div className="text-sm text-gray-400">Avg Confidence</div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AnalyticsHeader; 
import React from 'react';

const ResultsSection = ({ analysisResults, handleProceed }) => {
  if (!analysisResults) return null;

  return (
    <section className="py-6 sm:py-8 px-4 sm:px-6">
      <div className="max-w-4xl sm:max-w-5xl mx-auto">
        {/* Success Header */}
        <div className="text-center mb-6 sm:mb-8">
          <div className="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-green-400 via-emerald-500 to-green-600 rounded-lg sm:rounded-xl flex items-center justify-center mx-auto mb-3 sm:mb-4 shadow-lg animate-pulse">
            <i className="text-lg sm:text-xl text-white">
              <svg className="w-6 h-6 sm:w-7 sm:h-7" fill="currentColor" viewBox="0 0 448 512">
                <path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z" />
              </svg>
            </i>
          </div>
          <h3 className="text-xl sm:text-2xl font-bold mb-2 sm:mb-3 bg-gradient-to-r from-green-400 via-emerald-500 to-green-600 bg-clip-text text-transparent">
            Analysis Complete!
          </h3>
          <p className="text-gray-300 text-sm sm:text-base font-light">
            Successfully detected <span className="text-green-400 font-bold">{analysisResults.totalObjects}</span> objects in the lunar surface
          </p>
          <div className="mt-3 flex justify-center space-x-2">
            <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-green-400 rounded-full animate-bounce"></div>
            <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-emerald-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
            <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-green-600 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
          </div>
        </div>

        {/* Main Results Grid */}
        <div className="grid lg:grid-cols-3 gap-4 sm:gap-6 mb-8">
          {/* Detection Visualization */}
          <div className="lg:col-span-2">
            <div className="bg-gradient-to-br from-gray-800 via-gray-700 to-gray-800 border-2 border-gray-600 rounded-lg sm:rounded-xl p-4 sm:p-6 shadow-lg">
              <h4 className="text-base sm:text-lg font-bold mb-3 sm:mb-4 text-gray-200 flex items-center">
                <div className="w-5 h-5 sm:w-6 sm:h-6 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-lg flex items-center justify-center mr-2">
                  <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </div>
                Detection Visualization
              </h4>
              {analysisResults.visualizationImage ? (
                <div className="relative group">
                  <img 
                    src={`http://localhost:5000${analysisResults.visualizationImage}`}
                    alt="Detection Visualization"
                    className="w-full rounded-lg sm:rounded-xl border-2 border-gray-600 shadow-lg transition-all duration-300 transform group-hover:scale-[1.01]"
                  />
                  <div className="absolute top-2 right-2 bg-gradient-to-r from-blue-600 to-indigo-700 text-white px-2 py-1 rounded text-xs font-semibold shadow-md">
                    {analysisResults.totalObjects} Objects
                  </div>
                </div>
              ) : (
                <div className="bg-gradient-to-br from-gray-700 to-gray-800 rounded-lg sm:rounded-xl p-6 text-center border-2 border-dashed border-gray-600">
                  <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gray-600 rounded-lg flex items-center justify-center mx-auto mb-3">
                    <svg className="w-5 h-5 sm:w-6 sm:h-6 text-gray-500" fill="currentColor" viewBox="0 0 512 512">
                      <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                    </svg>
                  </div>
                  <p className="text-gray-400 text-sm font-medium">Visualization not available</p>
                </div>
              )}
            </div>
          </div>

          {/* Statistics Cards */}
          <div className="space-y-4 sm:space-y-5">
            {/* Detection Summary */}
            <div className="bg-gradient-to-br from-blue-600 via-indigo-700 to-blue-800 rounded-lg sm:rounded-xl p-4 sm:p-5 text-white shadow-lg transform hover:scale-105 transition-all duration-300">
              <h4 className="text-sm sm:text-base font-bold mb-3 sm:mb-4 flex items-center">
                <div className="w-5 h-5 sm:w-6 sm:h-6 bg-white/20 rounded-lg flex items-center justify-center mr-2">
                  <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </div>
                Detection Summary
              </h4>
              <div className="space-y-2 sm:space-y-3">
                <div className="flex justify-between items-center p-2 bg-white/10 rounded-lg">
                  <span className="text-blue-100 font-medium text-xs sm:text-sm">Total:</span>
                  <span className="text-lg sm:text-xl font-bold text-white">{analysisResults.totalObjects}</span>
                </div>
                <div className="flex justify-between items-center p-2 bg-white/10 rounded-lg">
                  <span className="text-orange-200 font-medium text-xs sm:text-sm">Boulders:</span>
                  <span className="text-base sm:text-lg font-bold text-orange-300">{analysisResults.boulders}</span>
                </div>
                <div className="flex justify-between items-center p-2 bg-white/10 rounded-lg">
                  <span className="text-yellow-200 font-medium text-xs sm:text-sm">Craters:</span>
                  <span className="text-base sm:text-lg font-bold text-yellow-300">{analysisResults.craters}</span>
                </div>
              </div>
            </div>

            {/* Analysis Metrics */}
            <div className="bg-gradient-to-br from-purple-600 via-pink-700 to-purple-800 rounded-lg sm:rounded-xl p-4 sm:p-5 text-white shadow-lg transform hover:scale-105 transition-all duration-300">
              <h4 className="text-sm sm:text-base font-bold mb-3 sm:mb-4 flex items-center">
                <div className="w-5 h-5 sm:w-6 sm:h-6 bg-white/20 rounded-lg flex items-center justify-center mr-2">
                  <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </div>
                Analysis Metrics
              </h4>
              <div className="space-y-2 sm:space-y-3">
                <div className="flex justify-between items-center p-2 bg-white/10 rounded-lg">
                  <span className="text-purple-100 font-medium text-xs sm:text-sm">Confidence:</span>
                  <span className="text-base sm:text-lg font-bold text-purple-300">{(analysisResults.confidence * 100).toFixed(1)}%</span>
                </div>
                <div className="flex justify-between items-center p-2 bg-white/10 rounded-lg">
                  <span className="text-pink-100 font-medium text-xs sm:text-sm">Avg Size:</span>
                  <span className="text-sm sm:text-base font-bold text-pink-300">{analysisResults.averageSize.toFixed(1)}m</span>
                </div>
                <div className="flex justify-between items-center p-2 bg-white/10 rounded-lg">
                  <span className="text-purple-100 font-medium text-xs sm:text-sm">Density:</span>
                  <span className="text-xs sm:text-sm font-bold text-purple-300">{analysisResults.density.toFixed(6)} obj/m²</span>
                </div>
              </div>
            </div>

            {/* Processing Info */}
            <div className="bg-gradient-to-br from-green-600 via-emerald-700 to-green-800 rounded-lg sm:rounded-xl p-4 sm:p-5 text-white shadow-lg transform hover:scale-105 transition-all duration-300">
              <h4 className="text-sm sm:text-base font-bold mb-3 sm:mb-4 flex items-center">
                <div className="w-5 h-5 sm:w-6 sm:h-6 bg-white/20 rounded-lg flex items-center justify-center mr-2">
                  <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </div>
                Processing Info
              </h4>
              <div className="space-y-2 sm:space-y-3">
                <div className="flex justify-between items-center p-2 bg-white/10 rounded-lg">
                  <span className="text-green-100 font-medium text-xs sm:text-sm">Status:</span>
                  <span className="text-base sm:text-lg font-bold text-green-300">Complete</span>
                </div>
                <div className="flex justify-between items-center p-2 bg-white/10 rounded-lg">
                  <span className="text-emerald-100 font-medium text-xs sm:text-sm">Time:</span>
                  <span className="text-sm sm:text-base font-bold text-emerald-300">{analysisResults.processingTime}s</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Grad-CAM Visualization */}
        {analysisResults.gradcamImage && (
          <div className="mb-6">
            <div className="bg-gray-800 border border-gray-700 rounded-lg sm:rounded-xl p-3 sm:p-4">
              <h4 className="text-sm sm:text-base font-semibold mb-2 sm:mb-3 text-gray-200 flex items-center">
                <i className="mr-2">
                  <svg className="w-3 h-3 sm:w-4 sm:h-4" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </i>
                Grad-CAM Visualization
              </h4>
              <img 
                src={`http://localhost:5000${analysisResults.gradcamImage}`}
                alt="Grad-CAM Visualization"
                className="w-full rounded-lg sm:rounded-xl border border-gray-600 shadow-lg"
              />
            </div>
          </div>
        )}

        {/* Detailed Object Analysis */}
        {analysisResults.detectedObjects && analysisResults.detectedObjects.length > 0 && (
          <div className="mb-6">
            <div className="bg-gray-800 border border-gray-700 rounded-lg sm:rounded-xl p-3 sm:p-4">
              <h4 className="text-sm sm:text-base font-semibold mb-3 sm:mb-4 text-gray-200 flex items-center">
                <i className="mr-2">
                  <svg className="w-3 h-3 sm:w-4 sm:h-4" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </i>
                Detailed Object Analysis
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 sm:gap-3">
                {analysisResults.detectedObjects.map((obj, index) => (
                  <div key={index} className="bg-gradient-to-br from-gray-700 to-gray-800 rounded-lg sm:rounded-xl p-2 sm:p-3 border border-gray-600 hover:border-gray-500 transition-all duration-300">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-xs font-semibold text-gray-300 bg-gray-600 px-2 py-1 rounded-full">
                        {obj.class_name.charAt(0).toUpperCase() + obj.class_name.slice(1)} #{index + 1}
                      </span>
                      <span className="text-xs text-gray-400 bg-gray-600 px-2 py-1 rounded">
                        {(obj.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="space-y-1 text-xs text-gray-300">
                      <div className="flex justify-between">
                        <span>Diameter:</span>
                        <span className="font-semibold text-orange-400">{obj.diameter_real.toFixed(2)}m</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Area:</span>
                        <span className="font-semibold text-blue-400">{obj.area_real.toFixed(2)}m²</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Volume:</span>
                        <span className="font-semibold text-green-400">{obj.volume_real.toFixed(2)}m³</span>
                      </div>
                      {obj.estimated_depth && (
                        <div className="flex justify-between">
                          <span>Depth:</span>
                          <span className="font-semibold text-purple-400">{obj.estimated_depth.toFixed(2)}m</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row justify-center space-y-3 sm:space-y-0 sm:space-x-4">
          <button 
            onClick={handleProceed}
            className="bg-gradient-to-r from-blue-500 via-indigo-600 to-blue-700 hover:from-blue-600 hover:via-indigo-700 hover:to-blue-800 px-6 sm:px-8 py-3 sm:py-4 rounded-lg sm:rounded-xl font-bold text-sm sm:text-base transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 shadow-lg hover:shadow-blue-500/50"
          >
            <span className="flex items-center space-x-2">
              <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 512 512">
                <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
              </svg>
              <span>Back to Dashboard</span>
            </span>
          </button>
          <button className="bg-gradient-to-r from-green-500 via-emerald-600 to-green-700 hover:from-green-600 hover:via-emerald-700 hover:to-green-800 px-6 sm:px-8 py-3 sm:py-4 rounded-lg sm:rounded-xl font-bold text-sm sm:text-base transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 shadow-lg hover:shadow-green-500/50">
            <span className="flex items-center space-x-2">
              <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 512 512">
                <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
              </svg>
              <span>Export Results</span>
            </span>
          </button>
        </div>
      </div>
    </section>
  );
};

export default ResultsSection; 
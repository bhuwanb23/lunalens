import React from 'react';
import PdfExportButton from './PdfExportButton';

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
        <div className="flex flex-col items-center mb-8">
          {/* Detection Visualization - Centered */}
          <div className="w-full max-w-4xl mb-6">
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
                  <div className="max-w-full overflow-hidden rounded-lg sm:rounded-xl border-2 border-gray-600 shadow-lg">
                  <img 
                    src={`http://localhost:5000${analysisResults.visualizationImage}`}
                    alt="Detection Visualization"
                      className="w-full h-auto max-h-96 object-contain transition-all duration-300 transform group-hover:scale-[1.02]"
                      onError={(e) => {
                        console.error('Detection image failed to load:', e.target.src);
                        console.error('Error details:', e);
                      }}
                      onLoad={() => console.log('Detection image loaded successfully')}
                  />
                  </div>
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

          {/* Statistics Cards - Flex Layout Below Image */}
          <div className="w-full max-w-4xl">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
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
                  <span className="text-purple-100 font-medium text-xs sm:text-sm">Avg Area:</span>
                  <span className="text-xs sm:text-sm font-bold text-purple-300">{(analysisResults.analysisSummary?.average_area || 0).toFixed(1)}m²</span>
                </div>
                <div className="flex justify-between items-center p-2 bg-white/10 rounded-lg">
                  <span className="text-pink-100 font-medium text-xs sm:text-sm">Total Volume:</span>
                  <span className="text-xs sm:text-sm font-bold text-pink-300">{(analysisResults.analysisSummary?.total_volume || 0).toFixed(0)}m³</span>
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
                <div className="flex justify-between items-center p-2 bg-white/10 rounded-lg">
                  <span className="text-green-100 font-medium text-xs sm:text-sm">Type:</span>
                  <span className="text-xs sm:text-sm font-bold text-green-300 capitalize">{analysisResults.analysisType}</span>
                </div>
                <div className="flex justify-between items-center p-2 bg-white/10 rounded-lg">
                  <span className="text-emerald-100 font-medium text-xs sm:text-sm">Density:</span>
                  <span className="text-xs sm:text-sm font-bold text-emerald-300">{analysisResults.density.toFixed(6)} obj/m²</span>
                </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Grad-CAM Visualization */}
        {analysisResults.gradcamImage && (
          <div className="mb-6">
            <div className="bg-gray-800 border border-gray-700 rounded-lg sm:rounded-xl p-3 sm:p-4">
              <h4 className="text-sm sm:text-base font-semibold mb-3 sm:mb-4 text-gray-200 flex items-center">
                <i className="mr-2">
                  <svg className="w-3 h-3 sm:w-4 sm:h-4" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </i>
                Grad-CAM Visualization
              </h4>
              {console.log('Grad-CAM image path:', analysisResults.gradcamImage)}
              <div className="max-w-full overflow-hidden rounded-lg sm:rounded-xl border border-gray-600 shadow-lg">
              <img 
                src={`http://localhost:5000${analysisResults.gradcamImage}`}
                alt="Grad-CAM Visualization"
                  className="w-full h-auto max-h-80 object-contain"
                  onError={(e) => {
                    console.error('Grad-CAM image failed to load:', e.target.src);
                    console.error('Error details:', e);
                  }}
                  onLoad={() => console.log('Grad-CAM image loaded successfully')}
              />
              </div>
            </div>
          </div>
        )}

        {/* Detailed Object Analysis */}
        {analysisResults.detectedObjects && analysisResults.detectedObjects.length > 0 ? (
          <div className="mb-6">
            <div className="bg-gradient-to-br from-gray-800 via-gray-700 to-gray-800 border-2 border-gray-600 rounded-lg sm:rounded-xl p-4 sm:p-6 shadow-lg">
              <h4 className="text-base sm:text-lg font-bold mb-4 sm:mb-6 text-gray-200 flex items-center">
                <div className="w-5 h-5 sm:w-6 sm:h-6 bg-gradient-to-br from-purple-400 to-pink-500 rounded-lg flex items-center justify-center mr-3">
                  <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </div>
                Detailed Object Analysis
              </h4>
              
              {/* Table Container */}
              <div className="overflow-x-auto">
                <table className="w-full text-sm sm:text-base">
                  {/* Table Header */}
                  <thead>
                    <tr className="bg-gradient-to-r from-gray-700 to-gray-600 text-gray-200">
                      <th className="px-3 py-3 text-left font-bold rounded-l-lg">
                        <div className="flex items-center space-x-2">
                          <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                          <span>Object</span>
                        </div>
                      </th>
                      <th className="px-3 py-3 text-center font-bold">
                        <div className="flex items-center justify-center space-x-2">
                          <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                          <span>Confidence</span>
                        </div>
                      </th>
                      <th className="px-3 py-3 text-center font-bold">
                        <div className="flex items-center justify-center space-x-2">
                          <div className="w-2 h-2 bg-orange-400 rounded-full"></div>
                          <span>Diameter (m)</span>
                        </div>
                      </th>
                      <th className="px-3 py-3 text-center font-bold">
                        <div className="flex items-center justify-center space-x-2">
                          <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                          <span>Area (m²)</span>
                        </div>
                      </th>
                      <th className="px-3 py-3 text-center font-bold">
                        <div className="flex items-center justify-center space-x-2">
                          <div className="w-2 h-2 bg-pink-400 rounded-full"></div>
                          <span>Volume (m³)</span>
                        </div>
                      </th>
                      <th className="px-3 py-3 text-center font-bold">
                        <div className="flex items-center justify-center space-x-2">
                          <div className="w-2 h-2 bg-yellow-400 rounded-full"></div>
                          <span>Circularity</span>
                        </div>
                      </th>
                      <th className="px-3 py-3 text-center font-bold rounded-r-lg">
                        <div className="flex items-center justify-center space-x-2">
                          <div className="w-2 h-2 bg-indigo-400 rounded-full"></div>
                          <span>Depth (m)</span>
                        </div>
                      </th>
                    </tr>
                  </thead>
                  
                  {/* Table Body */}
                  <tbody className="divide-y divide-gray-600">
                {analysisResults.detectedObjects.map((obj, index) => (
                      <tr 
                        key={index} 
                        className="bg-gradient-to-r from-gray-800 to-gray-700 hover:from-gray-700 hover:to-gray-600 transition-all duration-300 group"
                      >
                        {/* Object Name */}
                        <td className="px-3 py-4">
                          <div className="flex items-center space-x-3">
                            <div className={`w-3 h-3 rounded-full ${
                              obj.class_name === 'boulder' 
                                ? 'bg-orange-400 shadow-lg shadow-orange-400/50' 
                                : 'bg-yellow-400 shadow-lg shadow-yellow-400/50'
                            }`}></div>
                            <div>
                              <div className="font-semibold text-gray-200 capitalize">
                                {obj.class_name} #{index + 1}
                              </div>
                              <div className="text-xs text-gray-400">
                                {obj.degradation_state !== "N/A" ? obj.degradation_state : "Standard"}
                              </div>
                              {obj.bounding_box && (
                                <div className="text-xs text-gray-500 mt-1">
                                  BBox: ({obj.bounding_box.x1}, {obj.bounding_box.y1}) - ({obj.bounding_box.x2}, {obj.bounding_box.y2})
                                </div>
                              )}
                            </div>
                          </div>
                        </td>
                        
                        {/* Confidence */}
                        <td className="px-3 py-4 text-center">
                          <div className="flex items-center justify-center">
                            <div className="relative">
                              <div className="w-12 h-12 rounded-full border-2 border-gray-600 flex items-center justify-center bg-gray-700">
                                <span className="text-xs font-bold text-gray-200">
                                  {(obj.confidence * 100).toFixed(0)}%
                                </span>
                              </div>
                              <div 
                                className="absolute inset-0 rounded-full border-2 border-transparent"
                                style={{
                                  background: `conic-gradient(${obj.confidence > 0.8 ? '#10b981' : obj.confidence > 0.6 ? '#f59e0b' : '#ef4444'} ${obj.confidence * 360}deg, transparent 0deg)`
                                }}
                              ></div>
                            </div>
                          </div>
                        </td>
                        
                        {/* Diameter */}
                        <td className="px-3 py-4 text-center">
                          <div className="bg-gradient-to-r from-orange-500/20 to-orange-600/20 rounded-lg px-3 py-2 border border-orange-500/30">
                            <span className="font-bold text-orange-300">
                              {obj.diameter_real.toFixed(2)}
                            </span>
                            {obj.pixel_measurements && (
                              <div className="text-xs text-orange-400 mt-1">
                                {obj.pixel_measurements.width_px}×{obj.pixel_measurements.height_px}px
                              </div>
                            )}
                          </div>
                        </td>
                        
                        {/* Area */}
                        <td className="px-3 py-4 text-center">
                          <div className="bg-gradient-to-r from-purple-500/20 to-purple-600/20 rounded-lg px-3 py-2 border border-purple-500/30">
                            <span className="font-bold text-purple-300">
                              {obj.area_real.toFixed(2)}
                            </span>
                            {obj.pixel_measurements && (
                              <div className="text-xs text-purple-400 mt-1">
                                {obj.pixel_measurements.area_px}px²
                              </div>
                            )}
                          </div>
                        </td>
                        
                        {/* Volume */}
                        <td className="px-3 py-4 text-center">
                          <div className="bg-gradient-to-r from-pink-500/20 to-pink-600/20 rounded-lg px-3 py-2 border border-pink-500/30">
                            <span className="font-bold text-pink-300">
                              {obj.volume_real.toFixed(2)}
                            </span>
                          </div>
                        </td>
                        
                        {/* Circularity */}
                        <td className="px-3 py-4 text-center">
                          <div className="bg-gradient-to-r from-yellow-500/20 to-yellow-600/20 rounded-lg px-3 py-2 border border-yellow-500/30">
                            <span className="font-bold text-yellow-300">
                              {obj.circularity.toFixed(3)}
                            </span>
                            <div className="text-xs text-yellow-400 mt-1">
                              Elong: {obj.elongation.toFixed(3)}
                            </div>
                          </div>
                        </td>
                        
                        {/* Depth */}
                        <td className="px-3 py-4 text-center">
                          {obj.estimated_depth ? (
                            <div className="bg-gradient-to-r from-indigo-500/20 to-indigo-600/20 rounded-lg px-3 py-2 border border-indigo-500/30">
                              <span className="font-bold text-indigo-300">
                                {obj.estimated_depth.toFixed(2)}
                      </span>
                            </div>
                          ) : (
                            <div className="bg-gradient-to-r from-gray-500/20 to-gray-600/20 rounded-lg px-3 py-2 border border-gray-500/30">
                              <span className="font-bold text-gray-400">
                                N/A
                      </span>
                    </div>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              
              {/* Summary Stats */}
              <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
                <div className="bg-gradient-to-r from-blue-500/20 to-blue-600/20 rounded-lg p-3 border border-blue-500/30">
                  <div className="text-xs text-blue-300 font-medium">Total Objects</div>
                  <div className="text-lg font-bold text-blue-200">{analysisResults.detectedObjects.length}</div>
                </div>
                <div className="bg-gradient-to-r from-orange-500/20 to-orange-600/20 rounded-lg p-3 border border-orange-500/30">
                  <div className="text-xs text-orange-300 font-medium">Avg Diameter</div>
                  <div className="text-lg font-bold text-orange-200">
                    {(analysisResults.detectedObjects.reduce((sum, obj) => sum + obj.diameter_real, 0) / analysisResults.detectedObjects.length).toFixed(2)}m
                  </div>
                </div>
                <div className="bg-gradient-to-r from-green-500/20 to-green-600/20 rounded-lg p-3 border border-green-500/30">
                  <div className="text-xs text-green-300 font-medium">Avg Confidence</div>
                  <div className="text-lg font-bold text-green-200">
                    {(analysisResults.detectedObjects.reduce((sum, obj) => sum + obj.confidence, 0) / analysisResults.detectedObjects.length * 100).toFixed(1)}%
                  </div>
                </div>
                <div className="bg-gradient-to-r from-purple-500/20 to-purple-600/20 rounded-lg p-3 border border-purple-500/30">
                  <div className="text-xs text-purple-300 font-medium">Total Volume</div>
                  <div className="text-lg font-bold text-purple-200">
                    {analysisResults.detectedObjects.reduce((sum, obj) => sum + obj.volume_real, 0).toFixed(2)}m³
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="mb-6">
            <div className="bg-gradient-to-br from-gray-800 via-gray-700 to-gray-800 border-2 border-gray-600 rounded-lg sm:rounded-xl p-4 sm:p-6 shadow-lg">
              <h4 className="text-base sm:text-lg font-bold mb-4 sm:mb-6 text-gray-200 flex items-center">
                <div className="w-5 h-5 sm:w-6 sm:h-6 bg-gradient-to-br from-purple-400 to-pink-500 rounded-lg flex items-center justify-center mr-3">
                  <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </div>
                Detailed Object Analysis
              </h4>
              <div className="text-center py-8">
                <div className="w-16 h-16 bg-gray-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-gray-400" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </div>
                <p className="text-gray-400 text-lg font-medium">No Valid Objects Detected</p>
                <p className="text-gray-500 text-sm mt-2">The analysis completed but no objects with sufficient confidence were found.</p>
              </div>
            </div>
          </div>
        )}

        {/* Comprehensive Analysis Details */}
        {analysisResults.analysisSummary && (
          <div className="mb-8">
            <div className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 border-2 border-gray-600 rounded-2xl p-6 sm:p-8 shadow-2xl">
              <h4 className="text-lg sm:text-xl font-bold mb-6 sm:mb-8 text-gray-100 flex items-center">
                <div className="w-6 h-6 sm:w-8 sm:h-8 bg-gradient-to-br from-teal-400 via-cyan-500 to-blue-500 rounded-xl flex items-center justify-center mr-4 shadow-lg">
                  <svg className="w-4 h-4 sm:w-5 sm:h-5 text-white" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </div>
                Comprehensive Analysis Details
              </h4>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Analysis Summary */}
                <div className="space-y-6">
                  <div className="bg-gradient-to-br from-teal-900/30 via-cyan-900/30 to-blue-900/30 rounded-xl p-6 border border-teal-500/20 shadow-lg">
                    <h5 className="text-base font-bold text-teal-300 mb-4 flex items-center">
                      <div className="w-3 h-3 bg-teal-400 rounded-full mr-3 animate-pulse"></div>
                      Analysis Summary
                    </h5>
                    <div className="space-y-4">
                      <div className="flex justify-between items-center p-4 bg-gray-800/50 rounded-lg border border-gray-700/50 hover:border-teal-500/30 transition-all duration-300">
                        <span className="text-gray-300 text-sm font-medium">Analysis Type:</span>
                        <span className="text-teal-300 font-semibold capitalize px-3 py-1 bg-teal-900/30 rounded-lg border border-teal-500/30">{analysisResults.analysisType}</span>
                      </div>
                      <div className="flex justify-between items-center p-4 bg-gray-800/50 rounded-lg border border-gray-700/50 hover:border-teal-500/30 transition-all duration-300">
                        <span className="text-gray-300 text-sm font-medium">Image File:</span>
                        <span className="text-teal-300 font-semibold text-xs">{analysisResults.imageFilename}</span>
                      </div>
                      <div className="flex justify-between items-center p-4 bg-gray-800/50 rounded-lg border border-gray-700/50 hover:border-teal-500/30 transition-all duration-300">
                        <span className="text-gray-300 text-sm font-medium">Processing Time:</span>
                        <span className="text-teal-300 font-semibold">{analysisResults.processingTime}s</span>
                      </div>
                      <div className="flex justify-between items-center p-4 bg-gray-800/50 rounded-lg border border-gray-700/50 hover:border-teal-500/30 transition-all duration-300">
                        <span className="text-gray-300 text-sm font-medium">Average Circularity:</span>
                        <span className="text-teal-300 font-semibold">{(analysisResults.analysisSummary.average_circularity || 0).toFixed(3)}</span>
                      </div>
                      <div className="flex justify-between items-center p-4 bg-gray-800/50 rounded-lg border border-gray-700/50 hover:border-teal-500/30 transition-all duration-300">
                        <span className="text-gray-300 text-sm font-medium">Average Elongation:</span>
                        <span className="text-teal-300 font-semibold">{(analysisResults.analysisSummary.average_elongation || 0).toFixed(3)}</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Density Analysis */}
                <div className="space-y-6">
                  <div className="bg-gradient-to-br from-cyan-900/30 via-blue-900/30 to-indigo-900/30 rounded-xl p-6 border border-cyan-500/20 shadow-lg">
                    <h5 className="text-base font-bold text-cyan-300 mb-4 flex items-center">
                      <div className="w-3 h-3 bg-cyan-400 rounded-full mr-3 animate-pulse"></div>
                      Density Analysis
                    </h5>
                    <div className="space-y-4">
                      {analysisResults.densityAnalysis && (
                        <>
                          <div className="flex justify-between items-center p-4 bg-gray-800/50 rounded-lg border border-gray-700/50 hover:border-cyan-500/30 transition-all duration-300">
                            <span className="text-gray-300 text-sm font-medium">Total Image Area:</span>
                            <span className="text-cyan-300 font-semibold">{(analysisResults.densityAnalysis.total_area || 0).toFixed(2)} m²</span>
                          </div>
                          <div className="flex justify-between items-center p-4 bg-gray-800/50 rounded-lg border border-gray-700/50 hover:border-cyan-500/30 transition-all duration-300">
                            <span className="text-gray-300 text-sm font-medium">Crater Density:</span>
                            <span className="text-cyan-300 font-semibold">{(analysisResults.densityAnalysis.crater_density || 0).toFixed(6)} craters/m²</span>
                          </div>
                          <div className="flex justify-between items-center p-4 bg-gray-800/50 rounded-lg border border-gray-700/50 hover:border-cyan-500/30 transition-all duration-300">
                            <span className="text-gray-300 text-sm font-medium">Boulder Density:</span>
                            <span className="text-cyan-300 font-semibold">{(analysisResults.densityAnalysis.boulder_density || 0).toFixed(6)} boulders/m²</span>
                          </div>
                          <div className="flex justify-between items-center p-4 bg-gray-800/50 rounded-lg border border-gray-700/50 hover:border-cyan-500/30 transition-all duration-300">
                            <span className="text-gray-300 text-sm font-medium">Overall Density:</span>
                            <span className="text-cyan-300 font-semibold">{(analysisResults.densityAnalysis.density || 0).toFixed(6)} objects/m²</span>
                          </div>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Detailed Measurements Section */}
        {analysisResults.detectedObjects && analysisResults.detectedObjects.length > 0 && (
          <div className="mb-8">
            <div className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 border-2 border-gray-600 rounded-2xl p-6 sm:p-8 shadow-2xl">
              <h4 className="text-lg sm:text-xl font-bold mb-6 sm:mb-8 text-gray-100 flex items-center">
                <div className="w-6 h-6 sm:w-8 sm:h-8 bg-gradient-to-br from-indigo-400 via-purple-500 to-pink-500 rounded-xl flex items-center justify-center mr-4 shadow-lg">
                  <svg className="w-4 h-4 sm:w-5 sm:h-5 text-white" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </div>
                Detailed Measurements & Technical Data
              </h4>
              
              <div className="space-y-6">
                {analysisResults.detectedObjects.map((obj, index) => (
                  <div key={index} className="bg-gradient-to-br from-gray-800/50 via-gray-700/50 to-gray-800/50 rounded-xl p-6 border border-gray-600/50 hover:border-purple-500/30 transition-all duration-300 shadow-lg">
                    <div className="flex items-center justify-between mb-6">
                      <div className="flex items-center space-x-4">
                        <div className={`w-4 h-4 rounded-full ${
                          obj.class_name === 'boulder' 
                            ? 'bg-orange-400 shadow-lg shadow-orange-400/50 animate-pulse' 
                            : 'bg-yellow-400 shadow-lg shadow-yellow-400/50 animate-pulse'
                        }`}></div>
                        <h5 className="text-base font-bold text-indigo-300 capitalize">
                          {obj.class_name} #{index + 1} - {obj.degradation_state !== "N/A" ? obj.degradation_state : "Standard"}
                        </h5>
                      </div>
                      <div className="flex items-center space-x-3">
                        <div className="bg-gradient-to-r from-green-500/20 to-emerald-500/20 rounded-lg px-4 py-2 border border-green-500/30">
                          <span className="text-xs text-green-300 font-medium">Confidence</span>
                          <div className="text-sm font-bold text-green-200">{(obj.confidence * 100).toFixed(1)}%</div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                      {/* Bounding Box */}
                      {obj.bounding_box && (
                        <div className="space-y-3">
                          <h6 className="text-sm font-bold text-purple-300 flex items-center">
                            <div className="w-2 h-2 bg-purple-400 rounded-full mr-2"></div>
                            Bounding Box (Pixels)
                          </h6>
                          <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700/50">
                            <div className="grid grid-cols-2 gap-3 text-xs">
                              <div className="flex justify-between items-center p-2 bg-gray-800/30 rounded border border-gray-600/30">
                                <span className="text-gray-400">X1:</span>
                                <span className="text-purple-300 font-semibold">{obj.bounding_box.x1}</span>
                              </div>
                              <div className="flex justify-between items-center p-2 bg-gray-800/30 rounded border border-gray-600/30">
                                <span className="text-gray-400">Y1:</span>
                                <span className="text-purple-300 font-semibold">{obj.bounding_box.y1}</span>
                              </div>
                              <div className="flex justify-between items-center p-2 bg-gray-800/30 rounded border border-gray-600/30">
                                <span className="text-gray-400">X2:</span>
                                <span className="text-purple-300 font-semibold">{obj.bounding_box.x2}</span>
                              </div>
                              <div className="flex justify-between items-center p-2 bg-gray-800/30 rounded border border-gray-600/30">
                                <span className="text-gray-400">Y2:</span>
                                <span className="text-purple-300 font-semibold">{obj.bounding_box.y2}</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Pixel Measurements */}
                      {obj.pixel_measurements && (
                        <div className="space-y-3">
                          <h6 className="text-sm font-bold text-blue-300 flex items-center">
                            <div className="w-2 h-2 bg-blue-400 rounded-full mr-2"></div>
                            Pixel Measurements
                          </h6>
                          <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700/50">
                            <div className="space-y-3 text-xs">
                              <div className="flex justify-between items-center p-2 bg-gray-800/30 rounded border border-gray-600/30">
                                <span className="text-gray-400">Width:</span>
                                <span className="text-blue-300 font-semibold">{obj.pixel_measurements.width_px}px</span>
                              </div>
                              <div className="flex justify-between items-center p-2 bg-gray-800/30 rounded border border-gray-600/30">
                                <span className="text-gray-400">Height:</span>
                                <span className="text-blue-300 font-semibold">{obj.pixel_measurements.height_px}px</span>
                              </div>
                              <div className="flex justify-between items-center p-2 bg-gray-800/30 rounded border border-gray-600/30">
                                <span className="text-gray-400">Area:</span>
                                <span className="text-blue-300 font-semibold">{obj.pixel_measurements.area_px}px²</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Real Measurements */}
                      <div className="space-y-3">
                        <h6 className="text-sm font-bold text-green-300 flex items-center">
                          <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
                          Real Measurements
                        </h6>
                        <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700/50">
                          <div className="space-y-3 text-xs">
                            <div className="flex justify-between items-center p-2 bg-gray-800/30 rounded border border-gray-600/30">
                              <span className="text-gray-400">Width:</span>
                              <span className="text-green-300 font-semibold">{obj.width_real.toFixed(2)}m</span>
                            </div>
                            <div className="flex justify-between items-center p-2 bg-gray-800/30 rounded border border-gray-600/30">
                              <span className="text-gray-400">Height:</span>
                              <span className="text-green-300 font-semibold">{obj.height_real.toFixed(2)}m</span>
                            </div>
                            <div className="flex justify-between items-center p-2 bg-gray-800/30 rounded border border-gray-600/30">
                              <span className="text-gray-400">Diameter:</span>
                              <span className="text-green-300 font-semibold">{obj.diameter_real.toFixed(2)}m</span>
                            </div>
                            <div className="flex justify-between items-center p-2 bg-gray-800/30 rounded border border-gray-600/30">
                              <span className="text-gray-400">Area:</span>
                              <span className="text-green-300 font-semibold">{obj.area_real.toFixed(2)}m²</span>
                            </div>
                            <div className="flex justify-between items-center p-2 bg-gray-800/30 rounded border border-gray-600/30">
                              <span className="text-gray-400">Volume:</span>
                              <span className="text-green-300 font-semibold">{obj.volume_real.toFixed(2)}m³</span>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Shape Properties */}
                      <div className="space-y-3">
                        <h6 className="text-sm font-bold text-yellow-300 flex items-center">
                          <div className="w-2 h-2 bg-yellow-400 rounded-full mr-2"></div>
                          Shape Properties
                        </h6>
                        <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700/50">
                          <div className="space-y-3 text-xs">
                            <div className="flex justify-between items-center p-2 bg-gray-800/30 rounded border border-gray-600/30">
                              <span className="text-gray-400">Circularity:</span>
                              <span className="text-yellow-300 font-semibold">{obj.circularity.toFixed(3)}</span>
                            </div>
                            <div className="flex justify-between items-center p-2 bg-gray-800/30 rounded border border-gray-600/30">
                              <span className="text-gray-400">Elongation:</span>
                              <span className="text-yellow-300 font-semibold">{obj.elongation.toFixed(3)}</span>
                            </div>
                            {obj.estimated_depth && (
                              <div className="flex justify-between items-center p-2 bg-gray-800/30 rounded border border-gray-600/30">
                                <span className="text-gray-400">Depth:</span>
                                <span className="text-yellow-300 font-semibold">{obj.estimated_depth.toFixed(2)}m</span>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
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
          <PdfExportButton analysisResults={analysisResults} />
        </div>
      </div>
    </section>
  );
};

export default ResultsSection; 
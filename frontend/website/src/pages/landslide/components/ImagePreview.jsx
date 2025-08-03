import React, { useState } from 'react';

const ImagePreview = ({ image, results, isAnalyzing }) => {
  const [showOverlay, setShowOverlay] = useState(true);
  const [zoom, setZoom] = useState(1);

  if (!image) return null;

  const handleZoomIn = () => {
    setZoom(Math.min(zoom + 0.2, 3));
  };

  const handleZoomOut = () => {
    setZoom(Math.max(zoom - 0.2, 0.5));
  };

  const handleResetZoom = () => {
    setZoom(1);
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-semibold text-gray-100">
          Image Preview
        </h3>
        <div className="flex items-center space-x-2">
          {/* Zoom Controls */}
          <div className="flex items-center space-x-1">
            <button
              onClick={handleZoomOut}
              className="p-1 bg-gray-700 hover:bg-gray-600 rounded text-gray-300 transition-colors"
              title="Zoom Out"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM13 10H7" />
              </svg>
            </button>
            <span className="text-xs text-gray-400 min-w-[3rem] text-center">
              {Math.round(zoom * 100)}%
            </span>
            <button
              onClick={handleZoomIn}
              className="p-1 bg-gray-700 hover:bg-gray-600 rounded text-gray-300 transition-colors"
              title="Zoom In"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v6m3-3H7" />
              </svg>
            </button>
            <button
              onClick={handleResetZoom}
              className="px-2 py-1 text-xs bg-gray-700 hover:bg-gray-600 rounded text-gray-300 transition-colors"
            >
              Reset
            </button>
          </div>

          {/* Overlay Toggle */}
          {results && (
            <button
              onClick={() => setShowOverlay(!showOverlay)}
              className={`px-3 py-1 text-xs rounded transition-colors ${
                showOverlay
                  ? 'bg-orange-500 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {showOverlay ? 'Hide' : 'Show'} Overlay
            </button>
          )}
        </div>
      </div>

      {/* Image Container */}
      <div className="relative bg-gray-900 rounded-lg overflow-hidden">
        <div className="relative overflow-auto max-h-96">
          <div
            className="relative"
            style={{
              transform: `scale(${zoom})`,
              transformOrigin: 'top left',
              minHeight: '300px'
            }}
          >
            <img
              src={URL.createObjectURL(image)}
              alt="Lunar surface for landslide analysis"
              className="w-full h-auto"
            />

            {/* Analysis Overlay */}
            {results && showOverlay && (
              <div className="absolute inset-0 pointer-events-none">
                {/* Risk Zones Overlay */}
                {results.riskZones && results.riskZones.map((zone, index) => (
                  <div
                    key={index}
                    className="absolute border-2 border-dashed"
                    style={{
                      left: `${zone.x}%`,
                      top: `${zone.y}%`,
                      width: `${zone.width}%`,
                      height: `${zone.height}%`,
                      borderColor: zone.risk === 'high' ? '#ef4444' : 
                                  zone.risk === 'medium' ? '#f97316' : 
                                  zone.risk === 'low' ? '#eab308' : '#22c55e',
                      backgroundColor: zone.risk === 'high' ? '#ef4444' : 
                                    zone.risk === 'medium' ? '#f97316' : 
                                    zone.risk === 'low' ? '#eab308' : '#22c55e',
                      opacity: 0.3
                    }}
                  >
                    <div className="absolute -top-6 left-0 bg-gray-800 text-white text-xs px-2 py-1 rounded">
                      {zone.risk.toUpperCase()} RISK
                    </div>
                  </div>
                ))}

                {/* Detected Features Overlay */}
                {results.detectedFeatures && results.detectedFeatures.map((feature, index) => (
                  <div
                    key={index}
                    className="absolute w-4 h-4 bg-red-500 rounded-full border-2 border-white shadow-lg"
                    style={{
                      left: `${feature.x}%`,
                      top: `${feature.y}%`,
                      transform: 'translate(-50%, -50%)'
                    }}
                    title={`${feature.name} detected`}
                  >
                    <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded whitespace-nowrap">
                      {feature.name}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Analysis Progress Overlay */}
            {isAnalyzing && (
              <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                <div className="text-center">
                  <div className="w-12 h-12 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                  <p className="text-white font-medium">Analyzing image...</p>
                  <p className="text-gray-300 text-sm">Detecting landslide indicators</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Image Info */}
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-4">
          <div className="text-white text-sm">
            <div className="flex justify-between items-center">
              <span>Image Size: {image.size > 1024 * 1024 ? `${(image.size / (1024 * 1024)).toFixed(1)} MB` : `${(image.size / 1024).toFixed(1)} KB`}</span>
              <span>Type: {image.type.split('/')[1].toUpperCase()}</span>
            </div>
            {results && (
              <div className="mt-2 text-xs text-gray-300">
                Analysis completed at {new Date().toLocaleTimeString()}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Legend */}
      {results && showOverlay && (
        <div className="mt-4 p-3 bg-gray-700 rounded-lg">
          <h5 className="text-sm font-medium text-gray-200 mb-2">Legend</h5>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-red-500 rounded"></div>
              <span className="text-gray-300">High Risk</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-orange-500 rounded"></div>
              <span className="text-gray-300">Medium Risk</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-yellow-500 rounded"></div>
              <span className="text-gray-300">Low Risk</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded"></div>
              <span className="text-gray-300">Safe</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImagePreview; 
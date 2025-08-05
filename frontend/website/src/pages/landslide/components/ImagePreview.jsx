import React, { useState } from 'react';

const riskColors = {
    high: 'bg-red-500',
    medium: 'bg-orange-500',
    low: 'bg-yellow-400',
    safe: 'bg-green-500',
};

const riskIcons = {
    high: <svg className="w-3 h-3 text-red-500 mr-1 inline-block" fill="currentColor" viewBox="0 0 20 20"><circle cx="10" cy="10" r="10" /></svg>,
    medium: <svg className="w-3 h-3 text-orange-500 mr-1 inline-block" fill="currentColor" viewBox="0 0 20 20"><circle cx="10" cy="10" r="10" /></svg>,
    low: <svg className="w-3 h-3 text-yellow-400 mr-1 inline-block" fill="currentColor" viewBox="0 0 20 20"><circle cx="10" cy="10" r="10" /></svg>,
    safe: <svg className="w-3 h-3 text-green-500 mr-1 inline-block" fill="currentColor" viewBox="0 0 20 20"><circle cx="10" cy="10" r="10" /></svg>,
};

const ImagePreview = ({ image, results, isAnalyzing }) => {
    const [showOverlay, setShowOverlay] = useState(true);
    const [zoom, setZoom] = useState(1);
    const [objectUrl, setObjectUrl] = useState(null);

    if (!image) return null;

    // Helper function to get image source
    const getImageSrc = () => {
        if (image instanceof File) {
            // Create object URL and store it for cleanup
            const url = URL.createObjectURL(image);
            setObjectUrl(url);
            return url;
        } else if (image.path) {
            // For file path objects
            return image.path;
        } else if (typeof image === 'string') {
            // For direct file paths or URLs
            return image;
        } else {
            // Fallback - create a placeholder or default image
            return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDQwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI0MDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjMzc0MTUxIi8+Cjx0ZXh0IHg9IjIwMCIgeT0iMTUwIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTYiIGZpbGw9IiM5Q0EzQUYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5ERV0gSW1hZ2UgUHJldmlldzwvdGV4dD4KPC9zdmc+';
        }
    };

    // Check if the image is a TIF/TIFF file
    const isTiffFile = () => {
        const fileName = image?.name || image?.path || '';
        return fileName.toLowerCase().includes('.tif') || fileName.toLowerCase().includes('.tiff');
    };

    // Cleanup object URL on unmount
    React.useEffect(() => {
        return () => {
            if (objectUrl) {
                URL.revokeObjectURL(objectUrl);
            }
        };
    }, [objectUrl]);

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
        <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl p-6 border-2 border-gray-700 shadow-2xl relative overflow-visible">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-100">
                    DEM Preview
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
                            className={`px-3 py-1 text-xs rounded transition-colors shadow ${showOverlay
                                ? 'bg-orange-500 text-white shadow-orange-500/30'
                                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                                }`}
                        >
                            {showOverlay ? 'Hide' : 'Show'} Overlay
                        </button>
                    )}
                </div>
            </div>
            {/* Image Container */}
            <div className="relative bg-gray-900 rounded-xl overflow-hidden border-2 border-gray-700 shadow-lg">
                <div className="relative overflow-auto max-h-96">
                    <div
                        className="relative transition-all duration-500"
                        style={{
                            transform: `scale(${zoom})`,
                            transformOrigin: 'top left',
                            minHeight: '300px',
                        }}
                    >
                        {isTiffFile() ? (
                            // TIF/TIFF file preview - show file info instead of image
                            <div className="w-full h-64 bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl border-4 border-gray-800 flex items-center justify-center relative overflow-hidden">
                                {/* Background pattern */}
                                <div className="absolute inset-0 bg-[linear-gradient(45deg,transparent_25%,rgba(255,255,255,0.02)_25%,rgba(255,255,255,0.02)_50%,transparent_50%,transparent_75%,rgba(255,255,255,0.02)_75%)] bg-[length:20px_20px]"></div>
                                
                                <div className="relative z-10 text-center p-6">
                                    <div className="w-16 h-16 mx-auto bg-gradient-to-br from-orange-500 to-red-500 rounded-full flex items-center justify-center mb-4 shadow-lg">
                                        <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                        </svg>
                                    </div>
                                    <h4 className="text-lg font-bold text-gray-100 mb-2">DEM File Preview</h4>
                                    <p className="text-sm text-gray-300 mb-4">TIF/TIFF files cannot be previewed in browser</p>
                                    
                                    {/* File Information */}
                                    <div className="bg-gray-700/50 rounded-lg p-4 backdrop-blur-sm">
                                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                                            <div>
                                                <span className="text-gray-400">File:</span>
                                                <p className="text-gray-200 font-mono truncate">{image?.name || 'lunar_dem.tif'}</p>
                                            </div>
                                            <div>
                                                <span className="text-gray-400">Size:</span>
                                                <p className="text-gray-200">{image?.size ? `${(image.size / (1024 * 1024)).toFixed(1)} MB` : 'Unknown'}</p>
                                            </div>
                                            <div>
                                                <span className="text-gray-400">Type:</span>
                                                <p className="text-gray-200">GeoTIFF / DEM</p>
                                            </div>
                                            <div>
                                                <span className="text-gray-400">Format:</span>
                                                <p className="text-gray-200">Digital Elevation Model</p>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div className="mt-4 p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                                        <p className="text-xs text-blue-300">
                                            <svg className="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M12 20a8 8 0 100-16 8 8 0 000 16z" />
                                            </svg>
                                            This file will be processed for terrain analysis
                                        </p>
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <img
                                src={getImageSrc()}
                                alt="Lunar surface for landslide analysis"
                                className="w-full h-auto drop-shadow-2xl border-4 border-gray-800 rounded-xl transition-all duration-500"
                            />
                        )}
                        {/* Analysis Overlay */}
                        {results && showOverlay && (
                            <div className="absolute inset-0 pointer-events-none transition-all duration-500">
                                {/* Risk Zones Overlay */}
                                {results.riskZones && results.riskZones.map((zone, index) => (
                                    <div
                                        key={index}
                                        className={`absolute border-2 border-dashed rounded-lg transition-all duration-500 ${riskColors[zone.risk]}`}
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
                                            opacity: 0.22
                                        }}
                                    >
                                        <div className="absolute -top-6 left-0 bg-gray-800/80 text-white text-xs px-2 py-1 rounded shadow-lg backdrop-blur-md">
                                            {riskIcons[zone.risk]}{zone.risk.toUpperCase()} RISK
                                        </div>
                                    </div>
                                ))}
                                {/* Detected Features Overlay */}
                                {results.detectedFeatures && results.detectedFeatures.map((feature, index) => (
                                    <div
                                        key={index}
                                        className="absolute w-4 h-4 bg-red-500 rounded-full border-2 border-white shadow-lg transition-all duration-500"
                                        style={{
                                            left: `${feature.x}%`,
                                            top: `${feature.y}%`,
                                            transform: 'translate(-50%, -50%)',
                                        }}
                                        title={`${feature.name} detected`}
                                    >
                                        <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-800/90 text-white text-xs px-2 py-1 rounded shadow-lg backdrop-blur-md whitespace-nowrap">
                                            {feature.name}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                        {/* Analysis Progress Overlay */}
                        {isAnalyzing && (
                            <div className="absolute inset-0 bg-black bg-opacity-60 flex items-center justify-center transition-all duration-500">
                                <div className="text-center">
                                    <div className="w-12 h-12 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                                    <p className="text-white font-medium">Analyzing image...</p>
                                    <p className="text-gray-300 text-sm">Detecting landslide indicators</p>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
                {/* Image Info (glassmorphism) */}
                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4 backdrop-blur-md rounded-b-xl">
                    <div className="text-white text-sm">
                        <div className="flex justify-between items-center">
                            <span>File Size: {image.size > 1024 * 1024 ? `${(image.size / (1024 * 1024)).toFixed(1)} MB` : `${(image.size / 1024).toFixed(1)} KB`}</span>
                            <span>Type: {isTiffFile() ? 'GeoTIFF/DEM' : (image.type ? image.type.split('/')[1].toUpperCase() : 'Unknown')}</span>
                        </div>
                        {results && (
                            <div className="mt-2 text-xs text-gray-300">
                                Analysis completed at {new Date().toLocaleTimeString()}
                            </div>
                        )}
                    </div>
                </div>
            </div>
            {/* Floating Legend */}
            {results && showOverlay && (
                <div className="fixed bottom-8 right-8 z-50 p-4 bg-gray-800/80 rounded-xl shadow-lg border border-gray-700 backdrop-blur-md animate-fade-in">
                    <h5 className="text-sm font-bold text-gray-200 mb-2 flex items-center">
                        <svg className="w-4 h-4 mr-2 text-orange-400 animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M12 20a8 8 0 100-16 8 8 0 000 16z" /></svg>
                        Legend
                    </h5>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                        <div className="flex items-center space-x-2">
                            {riskIcons.high}<span className="text-gray-300">High Risk</span>
                        </div>
                        <div className="flex items-center space-x-2">
                            {riskIcons.medium}<span className="text-gray-300">Medium Risk</span>
                        </div>
                        <div className="flex items-center space-x-2">
                            {riskIcons.low}<span className="text-gray-300">Low Risk</span>
                        </div>
                        <div className="flex items-center space-x-2">
                            {riskIcons.safe}<span className="text-gray-300">Safe</span>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ImagePreview; 
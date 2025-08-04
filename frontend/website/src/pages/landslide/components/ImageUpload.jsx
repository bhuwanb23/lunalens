import React, { useState } from 'react';
import { LANDSLIDE_CONSTANTS } from '../constants/constants';

const ImageUpload = ({ onImageUpload, isUploading }) => {
  const [filePath, setFilePath] = useState('');
  const [pathError, setPathError] = useState('');
  const [isValidating, setIsValidating] = useState(false);

  const handlePathChange = (e) => {
    const path = e.target.value;
    setFilePath(path);
    setPathError('');
  };

  const validateFilePath = (path) => {
    if (!path.trim()) {
      return 'Please enter a file path';
    }
    const validExtensions = ['.tif', '.tiff', '.asc', '.geotiff', '.dem'];
    const hasValidExtension = validExtensions.some(ext => path.toLowerCase().endsWith(ext));
    if (!hasValidExtension) {
      return 'Please enter a valid DEM file path (.tif, .tiff, .asc, .geotiff, .dem)';
    }
    if (!path.includes('/') && !path.includes('\\')) {
      return 'Please enter a valid file path';
    }
    return null;
  };

  const handlePathSubmit = () => {
    const error = validateFilePath(filePath);
    if (error) {
      setPathError(error);
      return;
    }
    setIsValidating(true);
    setTimeout(() => {
      setIsValidating(false);
      onImageUpload({ type: 'path', path: filePath });
    }, 1000);
  };

  const handleBrowseClick = () => {
    document.getElementById('file-path-input')?.focus();
  };

  return (
    <div className="relative rounded-2xl p-6 border-2 border-transparent bg-gradient-to-br from-gray-800/90 to-gray-900/90 shadow-2xl overflow-hidden group">
      {/* Subtle animated background pattern */}
      <div className="absolute inset-0 pointer-events-none z-0 bg-[radial-gradient(circle_at_60%_40%,rgba(255,255,255,0.04)_0%,transparent_70%)] animate-pulse" />
      <div className="absolute inset-0 pointer-events-none z-0 bg-[linear-gradient(135deg,rgba(255,255,255,0.02)_25%,transparent_100%)]" />
      {/* Glowing border on hover */}
      <div className="absolute inset-0 rounded-2xl border-2 border-gradient-to-br from-red-500/40 to-orange-400/30 opacity-0 group-hover:opacity-100 transition-all duration-500 pointer-events-none" />

      <div className="relative z-10">
        <div className="text-center mb-6">
          <h3 className="text-2xl font-extrabold text-gray-100 mb-2 tracking-tight drop-shadow-lg">
            <span className="inline-block align-middle mr-2">
              <svg className="w-7 h-7 text-orange-400 inline-block align-middle animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v4a1 1 0 001 1h3m10 0h3a1 1 0 001-1V7a2 2 0 00-2-2H5a2 2 0 00-2 2zm0 0V5a2 2 0 00-2-2H7a2 2 0 00-2 2v2" />
              </svg>
            </span>
            Add Lunar DEM Path
          </h3>
          <p className="text-gray-400 text-base max-w-xl mx-auto">
            Enter the file path to your Digital Elevation Model (DEM) for terrain analysis
          </p>
        </div>

        <div className="space-y-5">
          {/* File Path Input */}
          <div className="space-y-2">
            <label htmlFor="file-path-input" className="block text-sm font-semibold text-gray-200 mb-1">
              DEM File Path
            </label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-orange-400">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v4a1 1 0 001 1h3m10 0h3a1 1 0 001-1V7a2 2 0 00-2-2H5a2 2 0 00-2 2zm0 0V5a2 2 0 00-2-2H7a2 2 0 00-2 2v2" />
                </svg>
              </span>
              <input
                id="file-path-input"
                type="text"
                value={filePath}
                onChange={handlePathChange}
                placeholder="C:\\path\\to\\your\\lunar_dem.tif or /path/to/your/lunar_dem.tif"
                className={`w-full pl-10 pr-4 py-3 bg-gray-700 border-2 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-300 ${
                  pathError ? 'border-red-500' : 'border-gray-600'
                } shadow-inner`}
                disabled={isUploading || isValidating}
                autoComplete="off"
              />
              {isValidating && (
                <div className="absolute right-3 top-1/2 -translate-y-1/2">
                  <div className="w-5 h-5 border-2 border-orange-500 border-t-transparent rounded-full animate-spin"></div>
                </div>
              )}
            </div>
          </div>

          {/* Supported Formats */}
          <div className="bg-gray-700/60 rounded-lg p-4 flex flex-wrap items-center gap-2 shadow">
            <span className="text-sm font-semibold text-gray-200 mr-2">Supported formats:</span>
            {['GeoTIFF (.tif, .tiff)', 'ASC (.asc)', 'DEM (.dem)'].map((format) => (
              <span key={format} className="px-3 py-1 bg-gradient-to-r from-orange-500/60 to-red-500/60 rounded text-xs text-white font-semibold shadow">
                {format}
              </span>
            ))}
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3">
            <button
              onClick={handlePathSubmit}
              disabled={isUploading || isValidating || !filePath.trim()}
              className={`flex-1 px-6 py-3 rounded-lg font-bold transition-all duration-300 shadow-lg shadow-orange-500/10 border-2 border-transparent ${
                isUploading || isValidating || !filePath.trim()
                  ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-orange-500 via-red-500 to-yellow-400 hover:from-orange-600 hover:to-yellow-500 text-white hover:shadow-xl hover:scale-105 border-orange-400/40'
              }`}
            >
              {isValidating ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Validating...</span>
                </div>
              ) : isUploading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Processing...</span>
                </div>
              ) : (
                <span className="tracking-wide">Process DEM</span>
              )}
            </button>

            <button
              onClick={handleBrowseClick}
              disabled={isUploading || isValidating}
              className={`px-4 py-3 rounded-lg font-semibold transition-all duration-300 border-2 border-gray-600 shadow hover:shadow-lg ${
                isUploading || isValidating
                  ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                  : 'bg-gray-700 hover:bg-gray-600 text-gray-200 hover:text-white border-orange-400/40'
              }`}
            >
              <span className="inline-flex items-center">
                <svg className="w-4 h-4 mr-1 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v4a1 1 0 001 1h3m10 0h3a1 1 0 001-1V7a2 2 0 00-2-2H5a2 2 0 00-2 2zm0 0V5a2 2 0 00-2-2H7a2 2 0 00-2 2v2" />
                </svg>
                Browse
              </span>
            </button>
          </div>

          {/* Error Message */}
          {pathError && (
            <div className="p-3 bg-gradient-to-r from-red-500/20 to-orange-500/10 border border-red-500/30 rounded-lg shadow animate-pulse mt-2">
              <p className="text-red-400 text-sm font-semibold text-center flex items-center justify-center">
                <svg className="w-4 h-4 mr-2 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636l-1.414-1.414A9 9 0 105.636 18.364l1.414 1.414A9 9 0 1018.364 5.636z" />
                </svg>
                {pathError}
              </p>
            </div>
          )}

          {/* Processing Progress */}
          {isUploading && (
            <div className="space-y-2 mt-2">
              <div className="w-full bg-gray-600 rounded-full h-2 overflow-hidden">
                <div className="bg-gradient-to-r from-orange-500 via-red-500 to-yellow-400 h-2 rounded-full animate-pulse" style={{ width: '60%' }}></div>
              </div>
              <p className="text-xs text-orange-300 text-center font-semibold animate-pulse">Processing DEM file...</p>
            </div>
          )}
        </div>

        {/* Tips */}
        <div className="mt-7 p-5 bg-gradient-to-br from-gray-700/80 to-gray-800/80 rounded-xl shadow flex flex-col gap-2 border-l-4 border-orange-400/40">
          <h4 className="text-sm font-bold text-orange-200 mb-1 flex items-center">
            <svg className="w-4 h-4 mr-2 text-orange-300 animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M12 20a8 8 0 100-16 8 8 0 000 16z" />
            </svg>
            Tips for better analysis:
          </h4>
          <ul className="text-xs text-orange-100 space-y-1 pl-2">
            <li>• Use high-resolution DEM files (GeoTIFF, TIF, or ASC format)</li>
            <li>• Ensure proper coordinate system (Lunar coordinate system)</li>
            <li>• Include complete terrain coverage for accurate analysis</li>
            <li>• Minimum resolution: 30m/pixel for detailed analysis</li>
            <li>• Large files (GB+) are supported - processing may take time</li>
          </ul>
        </div>

        {/* Example Paths */}
        <div className="mt-5 p-4 bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-lg shadow">
          <h4 className="text-sm font-bold text-blue-200 mb-2 flex items-center">
            <svg className="w-4 h-4 mr-2 text-blue-300 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2a4 4 0 014-4h4m0 0V7a4 4 0 00-4-4H7a4 4 0 00-4 4v10a4 4 0 004 4h4" />
            </svg>
            Example file paths:
          </h4>
          <div className="text-xs text-blue-100 space-y-1 pl-2">
            <p>Windows: <code className="bg-gray-800 px-1 rounded">C:\Users\YourName\Documents\lunar_dem.tif</code></p>
            <p>Mac/Linux: <code className="bg-gray-800 px-1 rounded">/home/username/documents/lunar_dem.tif</code></p>
            <p>Network: <code className="bg-gray-800 px-1 rounded">\\server\share\lunar_data\dem.tif</code></p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageUpload; 
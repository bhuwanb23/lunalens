import React, { useState, useRef } from 'react';
import { LANDSLIDE_CONSTANTS } from '../constants/constants';

const ImageUpload = ({ onImageUpload, isUploading }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [uploadError, setUploadError] = useState('');
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    setUploadError('');

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  };

  const handleFileUpload = (file) => {
    // Validate file type
    if (!LANDSLIDE_CONSTANTS.SUPPORTED_FORMATS.includes(file.type)) {
      setUploadError('Please upload a valid image file (JPEG, PNG, TIFF)');
      return;
    }

    // Validate file size (max 50MB)
    if (file.size > 50 * 1024 * 1024) {
      setUploadError('File size must be less than 50MB');
      return;
    }

    onImageUpload(file);
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <div className="text-center mb-6">
        <h3 className="text-xl font-semibold text-gray-100 mb-2">
          Upload Lunar Surface Image
        </h3>
        <p className="text-gray-400 text-sm">
          Upload a high-resolution image of the lunar surface for landslide analysis
        </p>
      </div>

      <div
        className={`relative border-2 border-dashed rounded-lg p-8 transition-all duration-300 ${
          isDragOver
            ? 'border-red-400 bg-red-500/10'
            : 'border-gray-600 hover:border-red-500/50 bg-gray-700/50'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          className="hidden"
        />

        <div className="text-center">
          {/* Upload Icon */}
          <div className="mb-4">
            <div className="w-16 h-16 mx-auto bg-gradient-to-br from-red-500 to-orange-500 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
          </div>

          {/* Upload Text */}
          <div className="mb-4">
            <p className="text-lg font-medium text-gray-200 mb-2">
              {isUploading ? 'Uploading...' : 'Drag & Drop your image here'}
            </p>
            <p className="text-sm text-gray-400">
              or click to browse files
            </p>
          </div>

          {/* Supported Formats */}
          <div className="mb-4">
            <p className="text-xs text-gray-500 mb-2">Supported formats:</p>
            <div className="flex justify-center space-x-2">
              {['JPEG', 'PNG', 'TIFF'].map((format) => (
                <span key={format} className="px-2 py-1 bg-gray-600 rounded text-xs text-gray-300">
                  {format}
                </span>
              ))}
            </div>
          </div>

          {/* Browse Button */}
          <button
            onClick={handleBrowseClick}
            disabled={isUploading}
            className={`px-6 py-3 rounded-lg font-medium transition-all duration-300 ${
              isUploading
                ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-red-500 to-orange-500 hover:from-red-600 hover:to-orange-600 text-white hover:shadow-lg hover:shadow-red-500/25'
            }`}
          >
            {isUploading ? (
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Uploading...</span>
              </div>
            ) : (
              'Browse Files'
            )}
          </button>
        </div>

        {/* Error Message */}
        {uploadError && (
          <div className="mt-4 p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
            <p className="text-red-400 text-sm text-center">{uploadError}</p>
          </div>
        )}

        {/* Upload Progress */}
        {isUploading && (
          <div className="mt-4">
            <div className="w-full bg-gray-600 rounded-full h-2">
              <div className="bg-gradient-to-r from-red-500 to-orange-500 h-2 rounded-full animate-pulse" style={{ width: '60%' }}></div>
            </div>
            <p className="text-xs text-gray-400 text-center mt-2">Processing image...</p>
          </div>
        )}
      </div>

      {/* Tips */}
      <div className="mt-6 p-4 bg-gray-700/50 rounded-lg">
        <h4 className="text-sm font-medium text-gray-200 mb-2">💡 Tips for better analysis:</h4>
        <ul className="text-xs text-gray-400 space-y-1">
          <li>• Use high-resolution images (minimum 1024x1024 pixels)</li>
          <li>• Ensure good lighting and contrast in the image</li>
          <li>• Include clear surface features and terrain variations</li>
          <li>• Avoid heavily shadowed or overexposed areas</li>
        </ul>
      </div>
    </div>
  );
};

export default ImageUpload; 
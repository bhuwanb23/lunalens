import React from 'react';
import { ANALYSIS_TYPES } from '../constants';
import { apiUrl } from '../../../config/api';

const DetailModal = ({ record, isOpen, onClose }) => {
  if (!isOpen || !record) return null;

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const getAnalysisTypeInfo = (type) => {
    return ANALYSIS_TYPES[type] || { name: 'Unknown', icon: '❓' };
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 border border-gray-700 rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-700">
          <h3 className="text-xl font-semibold text-gray-200">Analysis Details</h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors duration-200"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Basic Information */}
            <div className="space-y-4">
              <div className="bg-gray-750 border border-gray-600 rounded-lg p-4">
                <h4 className="text-lg font-semibold text-gray-200 mb-3">Basic Information</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Analysis ID:</span>
                    <span className="text-gray-200 font-medium">#{record.id}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Type:</span>
                    <span className="text-gray-200 font-medium">
                      {getAnalysisTypeInfo(record.analysisType).icon} {getAnalysisTypeInfo(record.analysisType).name}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Image:</span>
                    <span className="text-gray-200 font-medium">{record.imageName}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">User:</span>
                    <span className="text-gray-200 font-medium">{record.user}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Date:</span>
                    <span className="text-gray-200 font-medium">{formatDate(record.timestamp)}</span>
                  </div>
                </div>
              </div>

              {/* Detection Results */}
              <div className="bg-gray-750 border border-gray-600 rounded-lg p-4">
                <h4 className="text-lg font-semibold text-gray-200 mb-3">Detection Results</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Total Objects:</span>
                    <span className="text-blue-400 font-bold">{record.totalObjects}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Boulders:</span>
                    <span className="text-orange-400 font-bold">{record.boulders}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Craters:</span>
                    <span className="text-yellow-400 font-bold">{record.craters}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Average Size:</span>
                    <span className="text-gray-200 font-bold">{record.averageSize.toFixed(2)}m</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Density:</span>
                    <span className="text-gray-200 font-bold">{record.density.toFixed(6)} obj/m²</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Performance Metrics */}
            <div className="space-y-4">
              <div className="bg-gray-750 border border-gray-600 rounded-lg p-4">
                <h4 className="text-lg font-semibold text-gray-200 mb-3">Performance Metrics</h4>
                <div className="space-y-4">
                  {/* Confidence */}
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-gray-400">Confidence</span>
                      <span className="text-green-400 font-bold">{(record.confidence * 100).toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-gray-600 rounded-full h-2">
                      <div 
                        className="bg-green-500 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${record.confidence * 100}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Processing Time */}
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-gray-400">Processing Time</span>
                      <span className="text-blue-400 font-bold">{record.processingTime}s</span>
                    </div>
                    <div className="w-full bg-gray-600 rounded-full h-2">
                      <div 
                        className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${Math.min((record.processingTime / 5) * 100, 100)}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Images */}
              <div className="bg-gray-750 border border-gray-600 rounded-lg p-4">
                <h4 className="text-lg font-semibold text-gray-200 mb-3">Generated Images</h4>
                <div className="space-y-3">
                  {record.visualizationImage && (
                    <div>
                      <div className="text-sm text-gray-400 mb-2">Detection Visualization</div>
                      <img 
                        src={apiUrl(record.visualizationImage)}
                        alt="Detection Visualization"
                        className="w-full h-32 object-cover rounded-lg border border-gray-600"
                      />
                    </div>
                  )}
                  {record.gradcamImage && (
                    <div>
                      <div className="text-sm text-gray-400 mb-2">Grad-CAM Visualization</div>
                      <img 
                        src={apiUrl(record.gradcamImage)}
                        alt="Grad-CAM Visualization"
                        className="w-full h-32 object-cover rounded-lg border border-gray-600"
                      />
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end p-6 border-t border-gray-700">
          <button
            onClick={onClose}
            className="bg-gray-600 hover:bg-gray-500 text-gray-200 px-4 py-2 rounded-lg transition-colors duration-200"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default DetailModal; 
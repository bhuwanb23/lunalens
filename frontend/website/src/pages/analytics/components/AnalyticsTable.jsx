import React from 'react';
import { ANALYSIS_TYPES } from '../constants';

const AnalyticsTable = ({ records, onViewDetails }) => {
  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusBadge = (status) => {
    const statusColors = {
      completed: 'bg-green-500',
      processing: 'bg-yellow-500',
      failed: 'bg-red-500',
      pending: 'bg-gray-500'
    };

    return (
      <span className={`${statusColors[status]} text-white px-2 py-1 rounded-full text-xs font-medium`}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  const getAnalysisTypeBadge = (type) => {
    const analysisType = ANALYSIS_TYPES[type];
    if (!analysisType) return null;

    const colorClasses = {
      orange: 'bg-orange-500',
      blue: 'bg-blue-500',
      green: 'bg-green-500',
      purple: 'bg-purple-500'
    };

    return (
      <div className="flex items-center space-x-2">
        <span className={`${colorClasses[analysisType.color]} text-white px-2 py-1 rounded text-xs font-medium`}>
          {analysisType.icon} {analysisType.name}
        </span>
      </div>
    );
  };

  return (
    <section className="py-6 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-700">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Analysis
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Image
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Results
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Performance
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    User
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {records.map((record) => (
                  <tr key={record.id} className="hover:bg-gray-750 transition-colors duration-200">
                    <td className="px-6 py-4">
                      {getAnalysisTypeBadge(record.analysisType)}
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-200 font-medium">
                        {record.imageName}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="space-y-1">
                        <div className="text-sm text-gray-300">
                          <span className="text-blue-400 font-medium">{record.totalObjects}</span> objects
                        </div>
                        <div className="text-xs text-gray-400">
                          {record.boulders} boulders, {record.craters} craters
                        </div>
                        <div className="text-xs text-gray-400">
                          Avg size: {record.averageSize.toFixed(1)}m
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="space-y-1">
                        <div className="text-sm text-gray-300">
                          Confidence: <span className="text-green-400 font-medium">{(record.confidence * 100).toFixed(1)}%</span>
                        </div>
                        <div className="text-xs text-gray-400">
                          Time: {record.processingTime}s
                        </div>
                        <div className="text-xs text-gray-400">
                          Density: {record.density.toFixed(6)} obj/m²
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-300">{record.user}</div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-300">{formatDate(record.timestamp)}</div>
                    </td>
                    <td className="px-6 py-4">
                      {getStatusBadge(record.status)}
                    </td>
                    <td className="px-6 py-4">
                      <button
                        onClick={() => onViewDetails(record)}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm transition-colors duration-200"
                      >
                        View Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AnalyticsTable; 
import React from 'react';

const RecentScans = ({ scans }) => {
  const getStatusColor = (color) => {
    const colors = {
      green: 'text-green-400',
      yellow: 'text-yellow-400',
      blue: 'text-blue-400'
    };
    return colors[color] || 'text-green-400';
  };

  return (
    <div className="bg-gray-800/60 backdrop-blur-lg rounded-2xl p-6 border border-gray-700/50 glow">
      <h2 className="text-xl font-bold text-blue-300 mb-6">Recent Lunar Scans</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {scans.map((scan) => (
          <div key={scan.id} className="bg-gray-900/50 rounded-xl p-4 border border-gray-700/30">
            <img 
              className="w-full h-32 object-cover rounded-lg mb-3"
              src={scan.image}
              alt={scan.title}
            />
            <h4 className="font-semibold text-blue-300 mb-1">{scan.title}</h4>
            <p className="text-sm text-gray-400 mb-2">{scan.description}</p>
            <div className="flex items-center justify-between">
              <span className={`text-xs ${getStatusColor(scan.statusColor)}`}>
                {scan.status}
              </span>
              <span className="text-xs text-gray-500">{scan.timeAgo}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecentScans; 
import React from 'react';

const AnalyticsStats = ({ stats }) => {
  const statCards = [
    {
      title: 'Total Analyses',
      value: stats.totalAnalyses,
      icon: '📊',
      color: 'blue',
      change: '+12%',
      changeType: 'positive'
    },
    {
      title: 'Objects Detected',
      value: stats.totalObjects,
      icon: '🔍',
      color: 'green',
      change: '+8%',
      changeType: 'positive'
    },
    {
      title: 'Avg Confidence',
      value: `${(stats.averageConfidence * 100).toFixed(1)}%`,
      icon: '🎯',
      color: 'purple',
      change: '+2.3%',
      changeType: 'positive'
    },
    {
      title: 'Success Rate',
      value: `${stats.successRate}%`,
      icon: '✅',
      color: 'green',
      change: '+1.5%',
      changeType: 'positive'
    }
  ];

  const getColorClasses = (color) => {
    const colors = {
      blue: 'from-blue-500 to-blue-600',
      green: 'from-green-500 to-green-600',
      purple: 'from-purple-500 to-purple-600',
      orange: 'from-orange-500 to-orange-600'
    };
    return colors[color] || colors.blue;
  };

  return (
    <section className="py-6 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {statCards.map((stat, index) => (
            <div key={index} className="bg-gray-800 border border-gray-700 rounded-xl p-6 hover:border-gray-600 transition-colors duration-200">
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 bg-gradient-to-br ${getColorClasses(stat.color)} rounded-lg flex items-center justify-center text-white text-xl`}>
                  {stat.icon}
                </div>
                <div className={`text-sm font-medium ${
                  stat.changeType === 'positive' ? 'text-green-400' : 'text-red-400'
                }`}>
                  {stat.change}
                </div>
              </div>
              
              <div className="mb-2">
                <div className="text-2xl font-bold text-gray-200">{stat.value}</div>
                <div className="text-sm text-gray-400">{stat.title}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default AnalyticsStats; 
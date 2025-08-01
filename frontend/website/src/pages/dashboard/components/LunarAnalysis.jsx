import React from 'react';

const LunarAnalysis = ({ data }) => {
  const getColorClasses = (color) => {
    const colors = {
      blue: 'text-blue-400',
      purple: 'text-purple-400',
      orange: 'text-orange-400'
    };
    return colors[color] || 'text-blue-400';
  };

  return (
    <div className="bg-gray-800/60 backdrop-blur-lg rounded-2xl p-6 border border-gray-700/50 glow">
      <h2 className="text-xl font-bold orbitron text-blue-300 mb-6">Lunar Surface Analysis</h2>
      
      <div className="relative h-80 bg-gray-900 rounded-xl overflow-hidden mb-4">
        <img 
          className="w-full h-full object-cover"
          src={data.image}
          alt="lunar surface with craters and boulders, dark space background, high contrast"
        />
        
        <div className="absolute top-4 left-4 bg-blue-500/80 backdrop-blur-sm rounded-lg px-3 py-2">
          <span className="text-sm font-semibold">Region: {data.region}</span>
        </div>
        
        <div className="absolute bottom-4 right-4 flex space-x-2">
          <div className="bg-purple-500/80 backdrop-blur-sm rounded-lg px-3 py-2">
            <span className="text-sm">{data.overlay.craters} Craters</span>
          </div>
          <div className="bg-orange-500/80 backdrop-blur-sm rounded-lg px-3 py-2">
            <span className="text-sm">{data.overlay.boulders} Boulders</span>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-3 gap-4">
        {data.stats.map((stat, index) => (
          <div key={index} className="text-center">
            <div className={`text-2xl font-bold ${getColorClasses(stat.color)}`}>
              {stat.value}
            </div>
            <div className="text-sm text-gray-400">{stat.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LunarAnalysis; 
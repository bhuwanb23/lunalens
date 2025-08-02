import React from 'react';

const StatsCard = ({ stat, animationClass = 'floating' }) => {
  const getIcon = (iconName) => {
    const icons = {
      robot: (
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 640 512">
          <path d="M320 0c17.7 0 32 14.3 32 32V96H472c39.8 0 72 32.2 72 72V440c0 39.8-32.2 72-72 72H168c-39.8 0-72-32.2-72-72V168c0-39.8 32.2-72 72-72H288V32c0-17.7 14.3-32 32-32zM208 384c-8.8 0-16 7.2-16 16s7.2 16 16 16h32c8.8 0 16-7.2 16-16s-7.2-16-16-16H208zm96 0c-8.8 0-16 7.2-16 16s7.2 16 16 16h32c8.8 0 16-7.2 16-16s-7.2-16-16-16H304zm96 0c-8.8 0-16 7.2-16 16s7.2 16 16 16h32c8.8 0 16-7.2 16-16s-7.2-16-16-16H400zM264 256a40 40 0 1 0 -80 0 40 40 0 1 0 80 0zm152 40a40 40 0 1 0 0-80 40 40 0 1 0 0 80zM48 224H64V416H48c-26.5 0-48-21.5-48-48V272c0-26.5 21.5-48 48-48zm544 0c26.5 0 48 21.5 48 48v96c0 26.5-21.5 48-48 48H576V224h16z" />
        </svg>
      ),
      circle: (
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 512 512">
          <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512z" />
        </svg>
      ),
      mountain: (
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 512 512">
          <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
        </svg>
      ),
      'gauge-high': (
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 512 512">
          <path d="M0 256a256 256 0 1 1 512 0A256 256 0 1 1 0 256zM288 96a32 32 0 1 0 -64 0 32 32 0 1 0 64 0zM256 416c35.3 0 64-28.7 64-64c0-17.4-6.9-33.1-18.1-44.6L366 161.7c5.3-12.1-.2-26.3-12.3-31.6s-26.3 .2-31.6 12.3L257.9 288c-.6 0-1.3 0-1.9 0c-35.3 0-64 28.7-64 64s28.7 64 64 64zM176 144a32 32 0 1 0 -64 0 32 32 0 1 0 64 0zM96 288a32 32 0 1 0 0-64 32 32 0 1 0 0 64zm352-32a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
        </svg>
      )
    };
    return icons[iconName] || null;
  };

  const getColorClasses = (color) => {
    const colors = {
      green: 'text-green-400',
      purple: 'text-purple-400',
      orange: 'text-orange-400',
      yellow: 'text-yellow-400',
      blue: 'text-blue-400'
    };
    return colors[color] || 'text-blue-400';
  };

  return (
    <div className={`${animationClass} bg-gray-800/60 backdrop-blur-lg rounded-2xl p-6 border border-gray-700/50 ${stat.glow}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-blue-300">{stat.title}</h3>
        <i className={`${getColorClasses(stat.color)} text-xl`}>
          {getIcon(stat.icon)}
        </i>
      </div>
      <div className={`text-3xl font-bold ${getColorClasses(stat.color)} mb-2`}>
        {stat.value}
      </div>
      <div className="text-sm text-gray-400">{stat.subtitle}</div>
    </div>
  );
};

export default StatsCard; 
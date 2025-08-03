import React from 'react';

const AlertsPanel = ({ alerts }) => {
  const getIcon = (iconName) => {
    const icons = {
      'triangle-exclamation': (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 512 512">
          <path d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
        </svg>
      ),
      'circle-info': (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 512 512">
          <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM216 336h24V272H216c-13.3 0-24-10.7-24-24s10.7-24 24-24h48c13.3 0 24 10.7 24 24v88h8c13.3 0 24 10.7 24 24s-10.7 24-24 24H216c-13.3 0-24-10.7-24-24s10.7-24 24-24zm40-208a32 32 0 1 1 0 64 32 32 0 1 1 0-64z" />
        </svg>
      ),
      'circle-check': (
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 512 512">
          <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209L241 337c-9.4 9.4-24.6 9.4-33.9 0l-64-64c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l47 47L335 175c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9z" />
        </svg>
      )
    };
    return icons[iconName] || null;
  };

  const getColorClasses = (color) => {
    const colors = {
      red: {
        bg: 'bg-red-500/10',
        border: 'border-red-500/30',
        text: 'text-red-300',
        icon: 'text-red-400'
      },
      yellow: {
        bg: 'bg-yellow-500/10',
        border: 'border-yellow-500/30',
        text: 'text-yellow-300',
        icon: 'text-yellow-400'
      },
      green: {
        bg: 'bg-green-500/10',
        border: 'border-green-500/30',
        text: 'text-green-300',
        icon: 'text-green-400'
      }
    };
    return colors[color] || colors.red;
  };

  return (
    <div className="bg-gray-800/60 backdrop-blur-lg rounded-2xl p-6 border border-gray-700/50 glow-purple">
      <h3 className="text-lg font-bold text-purple-300 mb-4">System Alerts</h3>
      <div className="space-y-3">
        {alerts.map((alert) => {
          const colors = getColorClasses(alert.color);
          return (
            <div
              key={alert.id}
              className={`flex items-center space-x-3 p-3 ${colors.bg} border ${colors.border} rounded-lg`}
            >
              <i className={colors.icon}>
                {getIcon(alert.icon)}
              </i>
              <div>
                <div className={`text-sm font-semibold ${colors.text}`}>
                  {alert.title}
                </div>
                <div className="text-xs text-gray-400">{alert.subtitle}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default AlertsPanel; 
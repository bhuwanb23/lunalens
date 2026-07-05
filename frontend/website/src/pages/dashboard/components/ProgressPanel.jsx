import { useState, useEffect } from 'react';

const ProgressPanel = ({ progress }) => {
  const [animatedValues, setAnimatedValues] = useState(progress.map(() => 0));
  const [hoveredIndex, setHoveredIndex] = useState(null);

  // Animate progress bars on mount
  useEffect(() => {
    const timers = progress.map((item, index) => {
      return setTimeout(() => {
        setAnimatedValues(prev => {
          const newValues = [...prev];
          newValues[index] = item.value;
          return newValues;
        });
      }, 400 + index * 150);
    });

    return () => timers.forEach(clearTimeout);
  }, [progress]);

  const getArrowIcon = (value) => {
    if (value >= 80) {
      return (
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="transition-transform duration-200" style={{ color: '#10B981' }}>
          <polyline points="18 15 12 9 6 15" />
        </svg>
      );
    }
    return (
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="transition-transform duration-200" style={{ color: '#F59E0B' }}>
        <polyline points="6 9 12 15 18 9" />
      </svg>
    );
  };

  return (
    <div className="dashboard-card p-6 animate-fade-in-up delay-6">
      {/* Header */}
      <h3 className="text-[17px] font-bold mb-2" style={{ color: 'var(--text-primary)' }}>
        Analysis Progress
      </h3>
      <p className="text-[13px] mb-5" style={{ color: 'var(--text-secondary)' }}>
        Most common areas of interests
      </p>

      {/* Progress Items */}
      <div className="space-y-4">
        {progress.map((item, index) => (
          <div
            key={index}
            className="p-2 -mx-2 rounded-lg transition-all duration-300 cursor-default"
            style={{
              backgroundColor: hoveredIndex === index ? 'var(--bg-primary)' : 'transparent',
              transform: hoveredIndex === index ? 'translateX(4px)' : 'translateX(0)',
            }}
            onMouseEnter={() => setHoveredIndex(index)}
            onMouseLeave={() => setHoveredIndex(null)}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-[13px] font-medium" style={{ color: 'var(--text-primary)' }}>
                {item.label}
              </span>
              <div className="flex items-center gap-2">
                <span className="text-[13px] font-semibold tabular-nums" style={{ color: 'var(--text-primary)' }}>
                  {animatedValues[index]}%
                </span>
                <div className="transition-transform duration-200" style={{ transform: hoveredIndex === index ? 'scale(1.2)' : 'scale(1)' }}>
                  {getArrowIcon(item.value)}
                </div>
              </div>
            </div>
            <div className="progress-bar-container">
              <div
                className={`progress-bar-fill ${item.color}`}
                style={{
                  width: `${animatedValues[index]}%`,
                  transition: 'width 0.8s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease',
                  boxShadow: hoveredIndex === index ? `0 0 12px var(--accent-${item.color})` : 'none',
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProgressPanel;

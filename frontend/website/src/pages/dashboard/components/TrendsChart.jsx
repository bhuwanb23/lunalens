import { useState, useEffect, useRef } from 'react';

const TrendsChart = ({ trends }) => {
  const [hoveredIndex, setHoveredIndex] = useState(null);
  const [isVisible, setIsVisible] = useState(false);
  const svgRef = useRef(null);
  const containerRef = useRef(null);

  const data = trends.data;
  const maxValue = 100;
  const chartWidth = 600;
  const chartHeight = 180;
  const padding = { top: 20, right: 20, bottom: 30, left: 40 };

  const innerWidth = chartWidth - padding.left - padding.right;
  const innerHeight = chartHeight - padding.top - padding.bottom;

  // Generate smooth curve path using cubic bezier
  const generateSmoothPath = (values) => {
    const points = values.map((val, i) => ({
      x: padding.left + (i / (values.length - 1)) * innerWidth,
      y: padding.top + innerHeight - (val / maxValue) * innerHeight,
    }));

    if (points.length < 2) return '';

    let path = `M ${points[0].x} ${points[0].y}`;

    for (let i = 0; i < points.length - 1; i++) {
      const current = points[i];
      const next = points[i + 1];
      const cpx = (current.x + next.x) / 2;
      path += ` C ${cpx} ${current.y}, ${cpx} ${next.y}, ${next.x} ${next.y}`;
    }

    return path;
  };

  // Generate area fill path (closed path for gradient)
  const generateAreaPath = (values) => {
    const linePath = generateSmoothPath(values);
    const lastX = padding.left + innerWidth;
    const firstX = padding.left;
    const bottomY = padding.top + innerHeight;
    return `${linePath} L ${lastX} ${bottomY} L ${firstX} ${bottomY} Z`;
  };

  const craterValues = data.map(d => d.craters);
  const boulderValues = data.map(d => d.boulders || d.boulder || 0);

  const craterPath = generateSmoothPath(craterValues);
  const boulderPath = generateSmoothPath(boulderValues);
  const craterAreaPath = generateAreaPath(craterValues);
  const boulderAreaPath = generateAreaPath(boulderValues);

  // Get point coordinates for hover
  const getPointCoords = (values, index) => ({
    x: padding.left + (index / (values.length - 1)) * innerWidth,
    y: padding.top + innerHeight - (values[index] / maxValue) * innerHeight,
  });

  // Animate on mount
  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), 100);
    return () => clearTimeout(timer);
  }, []);

  // Handle mouse move for tooltip
  const handleMouseMove = (e) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;

    // Calculate which data point is closest
    const chartX = x - padding.left;
    const segmentWidth = innerWidth / (data.length - 1);
    const index = Math.round(chartX / segmentWidth);
    const clampedIndex = Math.max(0, Math.min(data.length - 1, index));
    setHoveredIndex(clampedIndex);
  };

  const handleMouseLeave = () => {
    setHoveredIndex(null);
  };

  // Y-axis labels
  const yLabels = [0, 25, 50, 75, 100];

  return (
    <div className="dashboard-card p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-[17px] font-bold" style={{ color: 'var(--text-primary)' }}>
            {trends.title}
          </h3>
          <p className="text-[13px]" style={{ color: 'var(--text-secondary)' }}>
            {trends.subtitle}
          </p>
        </div>
        <button className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-[13px] font-medium" style={{ backgroundColor: 'var(--bg-primary)', color: 'var(--text-secondary)', border: '1px solid var(--border)' }}>
          Range: {trends.range}
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="6 9 12 15 18 9" />
          </svg>
        </button>
      </div>

      {/* Chart Container */}
      <div
        ref={containerRef}
        className="relative"
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
      >
        {/* SVG Chart */}
        <svg
          ref={svgRef}
          viewBox={`0 0 ${chartWidth} ${chartHeight}`}
          className="w-full h-auto"
          style={{ overflow: 'visible' }}
        >
          <defs>
            {/* Gradient for crater area */}
            <linearGradient id="craterGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#EC4899" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#EC4899" stopOpacity="0.02" />
            </linearGradient>
            {/* Gradient for boulder area */}
            <linearGradient id="boulderGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#8B5CF6" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#8B5CF6" stopOpacity="0.02" />
            </linearGradient>
          </defs>

          {/* Grid lines */}
          {yLabels.map((val) => {
            const y = padding.top + innerHeight - (val / maxValue) * innerHeight;
            return (
              <line
                key={val}
                x1={padding.left}
                y1={y}
                x2={padding.left + innerWidth}
                y2={y}
                stroke="#E5E7EB"
                strokeWidth="1"
                strokeDasharray="4 4"
              />
            );
          })}

          {/* Y-axis labels */}
          {yLabels.map((val) => {
            const y = padding.top + innerHeight - (val / maxValue) * innerHeight;
            return (
              <text
                key={val}
                x={padding.left - 8}
                y={y + 4}
                textAnchor="end"
                fontSize="11"
                fill="#9CA3AF"
              >
                {val}
              </text>
            );
          })}

          {/* X-axis labels */}
          {data.map((d, i) => {
            const x = padding.left + (i / (data.length - 1)) * innerWidth;
            return (
              <text
                key={i}
                x={x}
                y={chartHeight - 5}
                textAnchor="middle"
                fontSize="10"
                fill="#9CA3AF"
              >
                {d.week.replace('Week ', 'W')}
              </text>
            );
          })}

          {/* Area fills */}
          <path
            d={craterAreaPath}
            fill="url(#craterGradient)"
            style={{
              opacity: isVisible ? 1 : 0,
              transition: 'opacity 0.6s ease',
            }}
          />
          <path
            d={boulderAreaPath}
            fill="url(#boulderGradient)"
            style={{
              opacity: isVisible ? 1 : 0,
              transition: 'opacity 0.6s ease 0.2s',
            }}
          />

          {/* Lines */}
          <path
            d={craterPath}
            fill="none"
            stroke="#EC4899"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{
              strokeDasharray: isVisible ? 'none' : '1000',
              strokeDashoffset: isVisible ? '0' : '1000',
              transition: 'stroke-dashoffset 1.2s ease',
            }}
          />
          <path
            d={boulderPath}
            fill="none"
            stroke="#8B5CF6"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{
              strokeDasharray: isVisible ? 'none' : '1000',
              strokeDashoffset: isVisible ? '0' : '1000',
              transition: 'stroke-dashoffset 1.2s ease 0.3s',
            }}
          />

          {/* Hover elements */}
          {hoveredIndex !== null && (
            <>
              {/* Vertical guide line */}
              <line
                x1={getPointCoords(craterValues, hoveredIndex).x}
                y1={padding.top}
                x2={getPointCoords(craterValues, hoveredIndex).x}
                y2={padding.top + innerHeight}
                stroke="#D1D5DB"
                strokeWidth="1"
                strokeDasharray="4 4"
              />

              {/* Crater dot */}
              <circle
                cx={getPointCoords(craterValues, hoveredIndex).x}
                cy={getPointCoords(craterValues, hoveredIndex).y}
                r="5"
                fill="white"
                stroke="#EC4899"
                strokeWidth="2.5"
              />

              {/* Boulder dot */}
              <circle
                cx={getPointCoords(boulderValues, hoveredIndex).x}
                cy={getPointCoords(boulderValues, hoveredIndex).y}
                r="5"
                fill="white"
                stroke="#8B5CF6"
                strokeWidth="2.5"
              />
            </>
          )}
        </svg>

        {/* Tooltip */}
        {hoveredIndex !== null && (
          <div
            className="absolute z-10 pointer-events-none"
            style={{
              left: `${getPointCoords(craterValues, hoveredIndex).x / chartWidth * 100}%`,
              top: `${Math.min(getPointCoords(craterValues, hoveredIndex).y, getPointCoords(boulderValues, hoveredIndex).y) / chartHeight * 100 - 15}%`,
              transform: 'translate(-50%, -100%)',
            }}
          >
            <div
              className="px-3 py-2 rounded-lg shadow-lg text-[12px]"
              style={{ backgroundColor: '#1A1D26', color: 'white' }}
            >
              <div className="font-semibold mb-1">{data[hoveredIndex].week}</div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#EC4899' }} />
                <span>Craters: {craterValues[hoveredIndex]}</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#8B5CF6' }} />
                <span>Boulders: {boulderValues[hoveredIndex]}</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Legend */}
      <div className="flex items-center justify-between mt-4">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#EC4899' }} />
            <span className="text-[12px]" style={{ color: 'var(--text-secondary)' }}>Craters Detected</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#8B5CF6' }} />
            <span className="text-[12px]" style={{ color: 'var(--text-secondary)' }}>Boulders Found</span>
          </div>
        </div>
        <div className="text-right">
          <div className="text-[28px] font-bold" style={{ color: 'var(--text-primary)' }}>
            {trends.average}
          </div>
          <div className="text-[11px]" style={{ color: 'var(--text-secondary)' }}>
            {trends.averageLabel}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrendsChart;

const TrendsChart = ({ trends }) => {
  const maxValue = Math.max(...trends.data.map(d => d.craters));

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

      {/* Chart */}
      <div className="relative">
        {/* Y-axis labels */}
        <div className="absolute left-0 top-0 bottom-8 w-8 flex flex-col justify-between text-[11px]" style={{ color: 'var(--text-muted)' }}>
          <span>Aug</span>
          <span className="px-2 py-0.5 rounded-full text-white text-[11px] font-medium" style={{ backgroundColor: 'var(--accent-blue)' }}>Sep</span>
          <span>Oct</span>
          <span>Nov</span>
        </div>

        {/* Chart area */}
        <div className="ml-10">
          <div className="chart-container">
            {trends.data.map((d, i) => (
              <div key={i} className="flex-1 flex flex-col gap-1">
                <div
                  className="chart-bar blue"
                  style={{ height: `${(d.craters / maxValue) * 140}px` }}
                />
                <div
                  className="chart-bar purple"
                  style={{ height: `${((d.boulders || d.boulder || 0) / maxValue) * 140}px` }}
                />
              </div>
            ))}
          </div>

          {/* Legend */}
          <div className="flex items-center gap-6 mt-4">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: 'var(--accent-pink)' }} />
              <span className="text-[12px]" style={{ color: 'var(--text-secondary)' }}>Maximum of focus</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: 'var(--accent-purple)' }} />
              <span className="text-[12px]" style={{ color: 'var(--text-secondary)' }}>Min or lack of focus</span>
            </div>
          </div>
        </div>

        {/* Average display */}
        <div className="absolute right-0 bottom-8 text-right">
          <div className="text-[36px] font-bold" style={{ color: 'var(--text-primary)' }}>
            {trends.average}
          </div>
          <div className="text-[12px]" style={{ color: 'var(--text-secondary)' }}>
            {trends.averageLabel}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrendsChart;

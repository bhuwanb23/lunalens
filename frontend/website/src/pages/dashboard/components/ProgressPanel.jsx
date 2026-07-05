const ProgressPanel = ({ progress }) => {
  return (
    <div className="dashboard-card p-6">
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
          <div key={index}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-[13px] font-medium" style={{ color: 'var(--text-primary)' }}>
                {item.label}
              </span>
              <div className="flex items-center gap-2">
                <span className="text-[13px] font-medium" style={{ color: 'var(--text-secondary)' }}>
                  {item.value}%
                </span>
                <div className="w-5 h-5 rounded-full flex items-center justify-center" style={{ backgroundColor: `var(--accent-${item.color})`, opacity: 0.15 }}>
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" style={{ color: `var(--accent-${item.color})` }}>
                    <polyline points="18 15 12 9 6 15" />
                  </svg>
                </div>
              </div>
            </div>
            <div className="progress-bar-container">
              <div
                className={`progress-bar-fill ${item.color}`}
                style={{ width: `${item.value}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProgressPanel;

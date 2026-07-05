const TrackersCard = ({ trackers }) => {
  return (
    <div className="dashboard-card p-5">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-[15px] font-semibold mb-1" style={{ color: 'var(--text-primary)' }}>
            {trackers.title}
          </h3>
          <p className="text-[13px]" style={{ color: 'var(--text-secondary)' }}>
            {trackers.subtitle}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {trackers.sources.map((source, index) => (
            <div
              key={source.id}
              className="tracker-icon"
              style={{
                backgroundColor: source.color,
                animationDelay: `${index * 0.1}s`,
              }}
              title={source.name}
            >
              {source.name.charAt(0)}
            </div>
          ))}
          <button className="w-9 h-9 rounded-full flex items-center justify-center transition-all duration-200 hover:bg-gray-100" style={{ backgroundColor: 'var(--bg-primary)' }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ color: 'var(--text-muted)' }}>
              <circle cx="12" cy="12" r="1" />
              <circle cx="19" cy="12" r="1" />
              <circle cx="5" cy="12" r="1" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default TrackersCard;

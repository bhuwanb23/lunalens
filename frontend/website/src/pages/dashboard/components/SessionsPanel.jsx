const SessionsPanel = ({ sessions }) => {
  return (
    <div className="dashboard-card p-6 animate-fade-in-up delay-5">
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <h3 className="text-[17px] font-bold" style={{ color: 'var(--text-primary)' }}>
          My Sessions
        </h3>
        <button className="p-2 rounded-lg transition-all duration-200 hover:bg-gray-100" style={{ backgroundColor: 'var(--bg-primary)' }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ color: 'var(--text-secondary)' }}>
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
            <line x1="16" y1="2" x2="16" y2="6" />
            <line x1="8" y1="2" x2="8" y2="6" />
            <line x1="3" y1="10" x2="21" y2="10" />
          </svg>
        </button>
      </div>

      {/* Sessions List */}
      <div>
        {sessions.map((session, index) => (
          <div
            key={session.id}
            className="session-item"
            style={{ animationDelay: `${0.5 + index * 0.1}s` }}
          >
            <div className="session-date">
              <div>{session.date}</div>
              <div className="font-medium" style={{ color: 'var(--text-primary)' }}>{session.time}</div>
            </div>
            <div className="session-info">
              <div className="session-name">{session.name}</div>
              <div className="session-platform">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: session.platformColor }} />
                {session.platform}
              </div>
            </div>
            <button className="p-1.5 rounded-lg transition-all duration-200 hover:bg-gray-100 hover:translate-x-1" style={{ color: 'var(--text-muted)' }}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="7" y1="17" x2="17" y2="7" />
                <polyline points="7 7 17 7 17 17" />
              </svg>
            </button>
          </div>
        ))}
      </div>

      {/* See all link */}
      <div className="mt-4 text-center">
        <a href="#" className="dashboard-link transition-all duration-200 hover:gap-2" style={{ color: 'var(--text-secondary)' }}>
          See all sessions
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="transition-transform duration-200 group-hover:translate-x-1">
            <polyline points="9 18 15 12 9 6" />
          </svg>
        </a>
      </div>
    </div>
  );
};

export default SessionsPanel;

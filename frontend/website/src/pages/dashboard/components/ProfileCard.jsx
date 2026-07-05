const ProfileCard = ({ user }) => {
  return (
    <div className="dashboard-card p-6 flex flex-col items-center text-center animate-fade-in-up delay-1">
      {/* Header */}
      <div className="w-full flex items-center justify-between mb-6">
        <h3 className="text-[15px] font-semibold" style={{ color: 'var(--text-primary)' }}>
          Profile
        </h3>
        <button className="p-1.5 rounded-lg transition-all duration-200 hover:bg-gray-100" style={{ color: 'var(--text-muted)' }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8" />
            <path d="M21 3v5h-5" />
          </svg>
        </button>
      </div>

      {/* Avatar */}
      <div className="profile-avatar mb-4">
        <div className="w-[72px] h-[72px] rounded-full bg-gradient-to-br from-pink-400 to-purple-500 flex items-center justify-center text-white text-[24px] font-bold shadow-lg">
          {user.name.charAt(0)}
        </div>
      </div>

      {/* Name & Role */}
      <h2 className="text-[17px] font-bold mb-1" style={{ color: 'var(--text-primary)' }}>
        {user.name}
      </h2>
      <p className="text-[13px] mb-5" style={{ color: 'var(--text-secondary)' }}>
        {user.role}
      </p>

      {/* Stats Row */}
      <div className="flex items-center gap-2 w-full">
        {user.stats.map((stat, index) => (
          <div
            key={index}
            className="profile-stat flex-1 justify-center cursor-default transition-all duration-200 hover:scale-105 hover:shadow-sm"
          >
            {stat.icon === 'users' && (
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ color: '#EF4444' }}>
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
              </svg>
            )}
            {stat.icon === 'check' && (
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ color: '#EF4444' }}>
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                <polyline points="22 4 12 14.01 9 11.01" />
              </svg>
            )}
            {stat.icon === 'star' && (
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ color: '#EF4444' }}>
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
              </svg>
            )}
            <span>{stat.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProfileCard;

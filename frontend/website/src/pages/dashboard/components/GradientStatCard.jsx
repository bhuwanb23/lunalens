const GradientStatCard = ({ stat, index = 0 }) => {
  const gradientClass = `stat-card-${stat.gradient}`;
  const delayClass = `delay-${index + 2}`;

  return (
    <div className={`${gradientClass} rounded-[20px] p-6 flex flex-col justify-between min-h-[180px] relative overflow-hidden animate-fade-in-up ${delayClass} cursor-default`}>
      {/* Shimmer overlay (added via CSS ::after) */}

      {/* Header */}
      <div className="flex items-start justify-between relative z-10">
        <h3 className="text-[14px] font-semibold text-gray-700 max-w-[120px] leading-tight">
          {stat.title}
        </h3>
        <div className="w-9 h-9 rounded-full bg-white/60 flex items-center justify-center transition-transform duration-300 hover:rotate-12">
          {stat.id === 'craters' ? (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gray-600">
              <circle cx="12" cy="12" r="10" />
              <path d="M12 6v6l4 2" />
            </svg>
          ) : (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gray-600">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
          )}
        </div>
      </div>

      {/* Value */}
      <div className="relative z-10">
        <div className="text-[42px] font-bold text-gray-800 leading-none mb-1">
          {stat.value}
        </div>
        <div className="text-[13px] text-gray-500">
          {stat.subtitle}
        </div>
      </div>
    </div>
  );
};

export default GradientStatCard;

const RightPanel = () => {
  const cards = [
    {
      title: 'Total Revenue',
      value: '$48,395',
      change: '+14.6%',
      positive: true,
      color: 'from-green-400 to-emerald-500',
      bars: [80, 60, 90, 70, 85, 75, 95],
    },
    {
      title: 'Active Users',
      value: '2,847',
      change: '+8.2%',
      positive: true,
      color: 'from-blue-400 to-indigo-500',
      dots: [1, 0, 1, 1, 0, 1, 1],
    },
    {
      title: 'Capital Allocations',
      value: '$12.8M',
      change: '+23.5%',
      positive: true,
      color: 'from-purple-400 to-pink-500',
      progress: 72,
    },
  ];

  return (
    <div className="relative hidden lg:flex w-1/2 h-screen bg-gradient-to-br from-[#0D3B35] via-[#0F4A42] to-[#1A7A6D] items-center justify-center overflow-hidden">
      <div className="absolute inset-0 opacity-5">
        <div className="absolute top-10 left-10 w-72 h-72 bg-white rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-teal-300 rounded-full blur-3xl"></div>
      </div>

      <div className="relative z-10 w-full max-w-md px-8">
        <div className="mb-10 text-center">
          <div className="w-16 h-16 bg-white/15 backdrop-blur-sm rounded-2xl flex items-center justify-center mx-auto mb-5 border border-white/10">
            <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">LunaLens</h2>
          <p className="text-teal-100/80 text-sm leading-relaxed">
            A Unified Hub for Satellite Data, Analytics & Monitoring
          </p>
        </div>

        <div className="space-y-5">
          {cards.map((card, index) => (
            <div
              key={index}
              className="bg-white/10 backdrop-blur-md rounded-xl p-5 border border-white/10 hover:bg-white/15 transition-all duration-300"
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-white/60 text-xs font-medium uppercase tracking-wider">{card.title}</span>
                <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${card.positive ? 'bg-green-400/20 text-green-300' : 'bg-red-400/20 text-red-300'}`}>
                  {card.change}
                </span>
              </div>

              <p className="text-2xl font-bold text-white mb-3">{card.value}</p>

              {card.bars && (
                <div className="flex items-end gap-1.5 h-12">
                  {card.bars.map((h, i) => (
                    <div key={i} className={`flex-1 rounded-t-sm bg-gradient-to-t ${card.color} transition-all duration-500`} style={{ height: `${h}%` }}></div>
                  ))}
                </div>
              )}

              {card.dots && (
                <div className="flex items-center gap-2 h-6">
                  {card.dots.map((d, i) => (
                    <div key={i} className={`w-2 h-2 rounded-full ${d ? 'bg-blue-400' : 'bg-white/20'}`}></div>
                  ))}
                </div>
              )}

              {card.progress != null && (
                <div className="w-full bg-white/10 rounded-full h-2">
                  <div className={`h-2 rounded-full bg-gradient-to-r ${card.color}`} style={{ width: `${card.progress}%` }}></div>
                </div>
              )}
            </div>
          ))}
        </div>

        <p className="text-teal-100/60 text-xs text-center mt-8 leading-relaxed">
          Access real-time satellite imagery, perform advanced analytics, and monitor geographic changes through an integrated mission control platform.
        </p>
      </div>
    </div>
  );
};

export default RightPanel;

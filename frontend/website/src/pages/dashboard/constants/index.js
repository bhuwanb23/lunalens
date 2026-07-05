export const DASHBOARD_DATA = {
  user: {
    name: 'Kristin Watson',
    role: 'Design Manager',
    avatar: null,
    stats: [
      { label: 'Scans', value: 11, icon: 'users' },
      { label: 'Craters', value: 56, icon: 'check' },
      { label: 'Boulders', value: 12, icon: 'star' },
    ],
  },

  statCards: [
    {
      id: 'craters',
      title: 'Craters Detected',
      value: '1,247',
      subtitle: 'Avg. Completed',
      change: '+12%',
      positive: true,
      gradient: 'pink',
    },
    {
      id: 'boulders',
      title: 'Boulders Found',
      value: '892',
      subtitle: 'Avg. Completed',
      change: '+8.2%',
      positive: true,
      gradient: 'blue',
    },
  ],

  trackers: {
    title: 'Trackers connected',
    subtitle: '3 active connections',
    sources: [
      { id: 1, name: 'ISRO', color: '#3B82F6' },
      { id: 2, name: 'NASA', color: '#8B5CF6' },
      { id: 3, name: 'ESA', color: '#10B981' },
    ],
  },

  trends: {
    title: 'Analysis Trends',
    subtitle: 'Productivity analytics',
    range: 'Last 30 days',
    data: [
      { week: 'Week 1', craters: 45, boulders: 30 },
      { week: 'Week 2', craters: 62, boulder: 42 },
      { week: 'Week 3', craters: 58, boulders: 55 },
      { week: 'Week 4', craters: 75, boulders: 48 },
      { week: 'Week 5', craters: 68, boulders: 62 },
      { week: 'Week 6', craters: 82, boulders: 58 },
      { week: 'Week 7', craters: 71, boulders: 70 },
      { week: 'Week 8', craters: 88, boulders: 65 },
    ],
    average: '41%',
    averageLabel: 'Avg. Conc-ion',
  },

  sessions: [
    {
      id: 1,
      date: 'Tue, 11 Jul',
      time: '08:15 am',
      name: 'Mare Tranquillitatis Scan',
      platform: 'Automated',
      platformColor: '#3B82F6',
    },
    {
      id: 2,
      date: 'Tue, 11 Jul',
      time: '09:30 pm',
      name: 'Crater Alpha-7 Analysis',
      platform: 'Manual Review',
      platformColor: '#8B5CF6',
    },
    {
      id: 3,
      date: 'Tue, 12 Jul',
      time: '02:30 pm',
      name: 'Boulder Field Beta-12',
      platform: 'Automated',
      platformColor: '#3B82F6',
    },
    {
      id: 4,
      date: 'Tue, 15 Jul',
      time: '04:00 pm',
      name: 'Highland Region Gamma-5',
      platform: 'Queued',
      platformColor: '#F59E0B',
    },
  ],

  progress: [
    { label: 'Crater Detection', value: 85, color: 'blue' },
    { label: 'Boulder Analysis', value: 67, color: 'purple' },
    { label: 'Region Mapping', value: 92, color: 'green' },
    { label: 'Model Accuracy', value: 88, color: 'orange' },
  ],
};

export const FOOTER_DATA = {
  status: 'Operational',
  uptime: '99.7%',
  lastUpdate: '2 min ago',
};

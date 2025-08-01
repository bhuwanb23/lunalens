export const DASHBOARD_DATA = {
  stats: [
    {
      id: 'model-status',
      title: 'Model Status',
      value: 'Online',
      subtitle: 'Last updated: 2m ago',
      icon: 'robot',
      color: 'green',
      glow: 'glow'
    },
    {
      id: 'crater-detection',
      title: 'Craters Detected',
      value: '1,247',
      subtitle: '↑ 12% from last scan',
      icon: 'circle',
      color: 'purple',
      glow: 'glow-purple'
    },
    {
      id: 'boulder-analysis',
      title: 'Boulder Analysis',
      value: '892',
      subtitle: 'Objects classified',
      icon: 'mountain',
      color: 'orange',
      glow: 'glow'
    },
    {
      id: 'processing-speed',
      title: 'Processing Speed',
      value: '2.4s',
      subtitle: 'Per image analysis',
      icon: 'gauge-high',
      color: 'yellow',
      glow: 'glow-purple'
    }
  ],
  alerts: [
    {
      id: 1,
      type: 'error',
      title: 'High Crater Density',
      subtitle: 'Sector 7-Alpha',
      icon: 'triangle-exclamation',
      color: 'red'
    },
    {
      id: 2,
      type: 'warning',
      title: 'Model Update Available',
      subtitle: 'Version 2.4.1',
      icon: 'circle-info',
      color: 'yellow'
    },
    {
      id: 3,
      type: 'success',
      title: 'Scan Complete',
      subtitle: 'Mare Serenitatis',
      icon: 'circle-check',
      color: 'green'
    }
  ],
  quickActions: [
    {
      id: 1,
      title: 'Start New Scan',
      icon: 'play',
      color: 'blue',
      action: 'scan'
    },
    {
      id: 2,
      title: 'Export Results',
      icon: 'download',
      color: 'purple',
      action: 'export'
    },
    {
      id: 3,
      title: 'Model Settings',
      icon: 'gear',
      color: 'gray',
      action: 'settings'
    }
  ],
  recentScans: [
    {
      id: 1,
      title: 'Crater Formation Alpha-7',
      description: 'Diameter: 2.3km • Depth: 450m',
      status: 'Analyzed',
      statusColor: 'green',
      timeAgo: '2 hours ago',
      image: 'https://storage.googleapis.com/uxpilot-auth.appspot.com/01c61ad778-03f4674ad7dbba969208.png'
    },
    {
      id: 2,
      title: 'Boulder Field Beta-12',
      description: 'Objects: 34 • Size: 0.5-3.2m',
      status: 'Processing',
      statusColor: 'yellow',
      timeAgo: '5 minutes ago',
      image: 'https://storage.googleapis.com/uxpilot-auth.appspot.com/93694a70eb-7e0b0cb34153c342e219.png'
    },
    {
      id: 3,
      title: 'Highland Region Gamma-5',
      description: 'Elevation: 4.2km • Features: 67',
      status: 'Queued',
      statusColor: 'blue',
      timeAgo: 'Pending',
      image: 'https://storage.googleapis.com/uxpilot-auth.appspot.com/6dbfa107d8-e81582e5d655cc891411.png'
    }
  ],
  lunarAnalysis: {
    region: 'Mare Tranquillitatis',
    image: 'https://storage.googleapis.com/uxpilot-auth.appspot.com/f66f4d46a4-ff60f6803bae54706d23.png',
    stats: [
      { label: 'Accuracy', value: '94.2%', color: 'blue' },
      { label: 'Features', value: '156', color: 'purple' },
      { label: 'Area Scanned', value: '8.7km²', color: 'orange' }
    ],
    overlay: {
      craters: 47,
      boulders: 23
    }
  }
};

export const NAVIGATION_ITEMS = [
  { label: 'Dashboard', active: true },
  { label: 'Analytics', active: false },
  { label: 'Boulder Detection', active: false },
];

export const FOOTER_DATA = {
  status: 'Operational',
  uptime: '99.7%',
  lastUpdate: '2 min ago'
}; 
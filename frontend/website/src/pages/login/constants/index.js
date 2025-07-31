export const LOGIN_CONSTANTS = {
  // Theme colors
  colors: {
    primary: {
      blue: '#60a5fa',
      purple: '#9333ea',
      orange: '#fb923c',
      red: '#ef4444',
      green: '#4ade80',
      gray: {
        300: '#d1d5db',
        400: '#9ca3af',
        500: '#6b7280',
        600: '#4b5563',
        700: '#374151',
        800: '#1f2937',
        900: '#111827'
      }
    }
  },

  // Text content
  content: {
    header: {
      title: 'ISRO',
      subtitle: 'Indian Space Research Organisation',
      missionControl: 'Mission Control'
    },
    login: {
      title: 'Lunar Access',
      subtitle: 'Enter your mission credentials',
      missionId: 'Mission ID',
      accessCode: 'Access Code',
      rememberMission: 'Remember mission',
      forgotCode: 'Forgot code?',
      launchMission: 'Launch Mission'
    },
    status: {
      systemsOnline: 'Systems Online',
      chandrayaan3: 'Chandrayaan-3',
      secureConnection: 'Secure connection to Lunar Mission Control',
      encrypted: 'Encrypted',
      monitoring: '24/7 Monitoring',
      connectedToDeepSpace: 'Connected to Deep Space Network'
    },
    footer: {
      copyright: '© 2024 ISRO',
      lunarExploration: 'Lunar Exploration Program'
    }
  },

  // Animation configurations
  animations: {
    float: {
      duration: '6s',
      timing: 'ease-in-out',
      iteration: 'infinite'
    },
    sparkle: {
      duration: '8s',
      timing: 'linear',
      iteration: 'infinite'
    },
    pulse: {
      duration: '2s',
      timing: 'cubic-bezier(0.4, 0, 0.6, 1)',
      iteration: 'infinite'
    }
  },

  // Form validation
  validation: {
    missionId: {
      required: 'Mission ID is required',
      minLength: 3,
      maxLength: 50
    },
    accessCode: {
      required: 'Access code is required',
      minLength: 6,
      maxLength: 100
    }
  }
};

export const ICONS = {
  rocket: 'fas fa-rocket',
  moon: 'fas fa-moon',
  user: 'fas fa-user',
  lock: 'fas fa-lock',
  globe: 'fas fa-globe',
  satellite: 'fas fa-satellite',
  shield: 'fas fa-shield-halved',
  clock: 'fas fa-clock',
  wifi: 'fas fa-wifi',
  spinner: 'fas fa-spinner',
  check: 'fas fa-check'
}; 
# LunaLens Dashboard

This is the React + Tailwind CSS implementation of the LunaLens dashboard, converted from the original HTML version.

## Structure

```
dashboard/
├── components/
│   ├── Header.jsx          # Navigation header with logo and menu
│   ├── StatsCard.jsx       # Individual stat cards with animations
│   ├── LunarAnalysis.jsx   # Main lunar surface analysis panel
│   ├── AlertsPanel.jsx     # System alerts and notifications
│   ├── QuickActions.jsx    # Action buttons (scan, export, settings)
│   ├── RecentScans.jsx     # Recent lunar scan results
│   ├── Footer.jsx          # Footer with status information
│   └── index.js            # Component exports
├── constants/
│   └── index.js            # Dashboard data and configuration
├── dashboard.jsx           # Main dashboard component
├── dashboard.css           # Custom styles and animations
└── README.md              # This file
```

## Components

### Header
- Navigation bar with LunaLens logo
- Menu items (Dashboard, Models, Analytics, Settings)
- User avatar and status indicator

### StatsCard
- Displays individual statistics (Model Status, Craters Detected, etc.)
- Supports different colors and icons
- Floating animations with staggered timing

### LunarAnalysis
- Main content area with lunar surface image
- Overlay information (region, crater count, boulder count)
- Statistics grid (accuracy, features, area scanned)

### AlertsPanel
- System alerts with different severity levels
- Color-coded alerts (red for errors, yellow for warnings, green for success)
- Icons for each alert type

### QuickActions
- Action buttons for common tasks
- Start New Scan, Export Results, Model Settings
- Hover effects and click handlers

### RecentScans
- Grid of recent lunar scan results
- Images with status indicators
- Time stamps and descriptions

### Footer
- System status information
- Uptime and last update time
- LunaLens branding

## Features

- **Responsive Design**: Works on desktop and mobile devices
- **Animations**: Floating cards, pulse effects, and smooth transitions
- **Dark Theme**: Space-themed dark interface
- **Real-time Data**: Structured for real-time updates
- **Modular Components**: Easy to maintain and extend

## Custom CSS Classes

- `.orbitron`: Orbitron font family for headings
- `.glow`: Blue glow effect for cards
- `.glow-purple`: Purple glow effect for cards
- `.floating`: Floating animation for cards
- `.floating-delayed`: Delayed floating animation
- `.pulse-glow`: Pulsing glow animation
- `.lunar-surface`: Background gradient for lunar surface effect

## Usage

The dashboard is currently set as the main component in `App.jsx`. To integrate with routing:

1. Install React Router: `npm install react-router-dom`
2. Set up routes in `App.jsx`
3. Navigate between Login and Dashboard components

## Data Structure

All dashboard data is centralized in `constants/index.js`:

- `DASHBOARD_DATA.stats`: Statistics cards data
- `DASHBOARD_DATA.alerts`: System alerts
- `DASHBOARD_DATA.quickActions`: Action buttons
- `DASHBOARD_DATA.recentScans`: Recent scan results
- `DASHBOARD_DATA.lunarAnalysis`: Main analysis panel data

## Customization

To customize the dashboard:

1. Update data in `constants/index.js`
2. Modify component styles in individual component files
3. Add new components to the `components/` directory
4. Import and use new components in `dashboard.jsx` 
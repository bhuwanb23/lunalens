# Analytics Page

## Overview
The Analytics page provides a comprehensive lunar surface analysis interface with three main detection types:

1. **Boulder Detection** - Identifies and analyzes large rock formations
2. **Landslide Detection** - Monitors slope stability and potential landslide areas
3. **Combined Analysis** - Comprehensive geological assessment

## Features

### Interactive Selection Cards
- Three analysis type cards with hover effects
- Visual feedback on selection
- Smooth animations and transitions
- Color-coded by analysis type (Orange, Green, Blue)

### Confirmation System
- Shows confirmation after selection
- Displays selected analysis type
- "Proceed to Dashboard" button for navigation

### Responsive Design
- Mobile-friendly layout
- Adaptive grid system
- Touch-friendly interactions

## Components

### Main Analytics Component (`analytics.jsx`)
- Handles state management for card selection
- Manages confirmation display
- Provides navigation functionality

### Styling (`analytics.css`)
- Custom animations and effects
- Glow effects and hover states
- Responsive design rules
- Accessibility features

## Usage

1. **Select Analysis Type**: Click on any of the three analysis cards
2. **View Confirmation**: See the selected analysis being initiated
3. **Navigate**: Use "Proceed to Dashboard" to return to main dashboard

## Navigation

- **Dashboard**: Returns to main dashboard
- **Analytics**: Current page (active)
- **Reports**: Future feature
- **User Menu**: Profile and logout options

## Technical Details

### State Management
- `selectedCard`: Tracks which analysis type is selected
- `showConfirmation`: Controls confirmation section visibility

### Routing
- Protected route requiring authentication
- Redirects to login if not authenticated
- Integrates with main app routing

### Styling
- Tailwind CSS for layout and basic styling
- Custom CSS for animations and effects
- Responsive design with mobile breakpoints

## Future Enhancements

- Real-time analysis progress
- Detailed analysis results view
- Export functionality
- Historical analysis data
- Advanced filtering options 
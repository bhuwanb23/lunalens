export const LANDSLIDE_CONSTANTS = {
  // Analysis Parameters
  ANALYSIS_PARAMETERS: {
    SLOPE_THRESHOLD: {
      name: 'Slope Threshold',
      unit: 'degrees',
      min: 0,
      max: 90,
      default: 30,
      description: 'Minimum slope angle for landslide detection'
    },
    ELEVATION_CHANGE: {
      name: 'Elevation Change',
      unit: 'meters',
      min: 0,
      max: 1000,
      default: 50,
      description: 'Minimum elevation change for landslide identification'
    },
    SURFACE_ROUGHNESS: {
      name: 'Surface Roughness',
      unit: 'index',
      min: 0,
      max: 1,
      default: 0.3,
      description: 'Surface roughness threshold for detection'
    },
    COHERENCE_THRESHOLD: {
      name: 'Coherence Threshold',
      unit: 'index',
      min: 0,
      max: 1,
      default: 0.7,
      description: 'Minimum coherence for reliable detection'
    }
  },

  // Status Messages
  STATUS_MESSAGES: {
    IDLE: 'Ready for analysis',
    UPLOADING: 'Uploading image...',
    PROCESSING: 'Analyzing landslide data...',
    ANALYZING: 'Detecting landslide features...',
    COMPLETED: 'Analysis completed successfully',
    ERROR: 'Analysis failed. Please try again.',
    EXPORTING: 'Exporting results...',
    EXPORTED: 'Results exported successfully'
  },

  // File Types
  SUPPORTED_FORMATS: [
    'image/jpeg',
    'image/jpg',
    'image/png',
    'image/tiff',
    'image/tif'
  ],

  // Export Formats
  EXPORT_FORMATS: [
    { value: 'json', label: 'JSON Report', icon: '📄' },
    { value: 'csv', label: 'CSV Data', icon: '📊' },
    { value: 'pdf', label: 'PDF Report', icon: '📋' },
    { value: 'geojson', label: 'GeoJSON', icon: '🗺️' }
  ],

  // Detection Results Categories
  DETECTION_CATEGORIES: {
    HIGH_RISK: {
      label: 'High Risk',
      color: 'red',
      description: 'Significant landslide indicators detected',
      threshold: 0.8
    },
    MEDIUM_RISK: {
      label: 'Medium Risk',
      color: 'orange',
      description: 'Moderate landslide indicators present',
      threshold: 0.5
    },
    LOW_RISK: {
      label: 'Low Risk',
      color: 'yellow',
      description: 'Minor landslide indicators detected',
      threshold: 0.2
    },
    SAFE: {
      label: 'Safe',
      color: 'green',
      description: 'No significant landslide indicators',
      threshold: 0.0
    }
  },

  // Analysis Features
  ANALYSIS_FEATURES: [
    'Slope Analysis',
    'Elevation Mapping',
    'Surface Deformation',
    'Coherence Analysis',
    'Temporal Change Detection',
    'Risk Assessment'
  ],

  // Moon Regions
  MOON_REGIONS: [
    'Mare Tranquillitatis',
    'Mare Serenitatis',
    'Mare Imbrium',
    'Mare Nubium',
    'Mare Cognitum',
    'Mare Humorum',
    'Mare Vaporum',
    'Mare Frigoris',
    'Lunar Highlands',
    'Lunar Craters',
    'Lunar Rilles',
    'Lunar Mountains'
  ]
};

export const ANALYSIS_STEPS = [
  {
    id: 1,
    name: 'Image Upload',
    description: 'Upload lunar surface image for analysis',
    icon: '📤'
  },
  {
    id: 2,
    name: 'Preprocessing',
    description: 'Enhance and prepare image for analysis',
    icon: '🔧'
  },
  {
    id: 3,
    name: 'Feature Detection',
    description: 'Detect landslide indicators and features',
    icon: '🔍'
  },
  {
    id: 4,
    name: 'Risk Assessment',
    description: 'Calculate landslide risk probability',
    icon: '⚠️'
  },
  {
    id: 5,
    name: 'Report Generation',
    description: 'Generate comprehensive analysis report',
    icon: '📊'
  }
]; 
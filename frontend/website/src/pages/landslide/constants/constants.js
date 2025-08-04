export const LANDSLIDE_CONSTANTS = {
  // Analysis Parameters
  ANALYSIS_PARAMETERS: {
    SLOPE_THRESHOLD: {
      name: 'Slope Threshold',
      unit: 'degrees',
      min: 0,
      max: 90,
      default: 15,
      description: 'Slope angle threshold for landslide risk assessment'
    },
    ASPECT_THRESHOLD: {
      name: 'Aspect Threshold',
      unit: 'degrees',
      min: 0,
      max: 360,
      default: 315,
      description: 'Optimal aspect angle (315° = North-facing, lower risk)'
    },
    ELEVATION_RANGE: {
      name: 'Elevation Range',
      unit: 'meters',
      min: 0,
      max: 2000,
      default: 1000,
      description: 'Elevation range for risk assessment (1000-2000m optimal)'
    },
    TERRAIN_RUGGEDNESS: {
      name: 'Terrain Ruggedness Index',
      unit: 'TRI',
      min: 0,
      max: 10,
      default: 1.0,
      description: 'Terrain Ruggedness Index threshold (TRI > 1.0 = high risk)'
    },
    CONTOUR_DENSITY: {
      name: 'Contour Density',
      unit: 'contours/km²',
      min: 0,
      max: 20,
      default: 10,
      description: 'Contour density threshold for terrain complexity'
    },
    PROFILE_GRADIENT: {
      name: 'Profile Gradient',
      unit: 'm/km',
      min: 0,
      max: 100,
      default: 50,
      description: 'Profile gradient threshold for slope steepness'
    },
    CRATER_RATIO: {
      name: 'Crater Depth Ratio',
      unit: 'ratio',
      min: 0,
      max: 50,
      default: 30,
      description: 'Crater depth to diameter ratio for impact assessment'
    },
    HILLSHADE_THRESHOLD: {
      name: 'Hillshade Threshold',
      unit: 'index',
      min: 0,
      max: 255,
      default: 128,
      description: 'Hillshade threshold for solar illumination analysis'
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
    'image/tiff',
    'image/tif',
    'application/octet-stream', // For .asc files
    'text/plain' // For .txt files
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

  // Risk Weights (based on lunar_risk_analysis.py)
  RISK_WEIGHTS: {
    slope: 0.30,
    aspect: 0.15,
    hillshade: 0.15,
    contour_density: 0.10,
    profile_gradient: 0.10,
    crater_ratio: 0.05,
    roughness: 0.10,
    elevation: 0.05
  },

  // Analysis Features
  ANALYSIS_FEATURES: [
    'Slope Analysis',
    'Aspect Analysis',
    'Terrain Ruggedness Index',
    'Contour Density Analysis',
    'Profile Gradient Analysis',
    'Crater Impact Assessment',
    'Hillshade Analysis',
    'Elevation Analysis',
    'Composite Risk Assessment'
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
    name: 'DEM Upload',
    description: 'Upload Digital Elevation Model (DEM) for lunar terrain',
    icon: '📤'
  },
  {
    id: 2,
    name: 'Terrain Analysis',
    description: 'Calculate slope, aspect, and terrain ruggedness',
    icon: '🗺️'
  },
  {
    id: 3,
    name: 'Feature Extraction',
    description: 'Extract contours, gradients, and crater features',
    icon: '🔍'
  },
  {
    id: 4,
    name: 'Risk Calculation',
    description: 'Calculate composite risk scores using weighted parameters',
    icon: '⚠️'
  },
  {
    id: 5,
    name: 'Report Generation',
    description: 'Generate comprehensive lunar landslide risk report',
    icon: '📊'
  }
]; 
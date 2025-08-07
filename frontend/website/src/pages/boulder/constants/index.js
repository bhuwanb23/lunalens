export const BOULDER_ANALYSIS_TYPES = [
  {
    id: 'basic',
    title: 'Basic Detection',
    description: 'Standard YOLO-based boulder detection with physical measurements.',
    icon: 'mountain',
    color: 'orange',
    features: ['Object Detection', 'Size Measurement', 'Density Analysis'],
    processingTime: '1-2 seconds',
    accuracy: '85-90%',
    requirements: ['YOLO Model', 'Image Input']
  },
  {
    id: 'advanced',
    title: 'Advanced Analysis',
    description: 'Dual-model detection using YOLO and Vision Transformer for enhanced accuracy.',
    icon: 'brain',
    color: 'blue',
    features: ['ViT Fallback', 'High Accuracy', 'Confidence Validation'],
    processingTime: '2-3 seconds',
    accuracy: '92-95%',
    requirements: ['YOLO Model', 'ViT Model', 'Image Input']
  },
  {
    id: 'depth',
    title: 'Depth Estimation',
    description: 'Boulder depth estimation using shadow analysis and solar incidence angle.',
    icon: 'layer-group',
    color: 'green',
    features: ['Shadow Analysis', 'Depth Calculation', 'Solar Angle'],
    processingTime: '3-4 seconds',
    accuracy: '88-92%',
    requirements: ['YOLO Model', 'Solar Angle', 'Image Input']
  },
  {
    id: 'gradcam',
    title: 'Grad-CAM Visualization',
    description: 'Model interpretability with attention maps and visualization.',
    icon: 'eye',
    color: 'purple',
    features: ['Attention Maps', 'Model Interpretability', 'Visualization'],
    processingTime: '4-5 seconds',
    accuracy: '90-94%',
    requirements: ['YOLO Model', 'ViT Model', 'Grad-CAM']
  }
];

export const BOULDER_DETECTION_FEATURES = [
  {
    id: 'physical-measurements',
    title: 'Physical Measurements',
    description: 'Calculate size, diameter, area, volume, circularity, and elongation of detected objects.',
    icon: 'ruler',
    color: 'blue'
  },
  {
    id: 'density-analysis',
    title: 'Density Analysis',
    description: 'Calculate object density per unit area for comprehensive surface analysis.',
    icon: 'chart-bar',
    color: 'green'
  },
  {
    id: 'depth-estimation',
    title: 'Depth Estimation',
    description: 'Estimate boulder depth using shadow analysis and solar incidence angle.',
    icon: 'layer-group',
    color: 'purple'
  },
  {
    id: 'gradcam-visualization',
    title: 'Grad-CAM Visualization',
    description: 'Model interpretability with attention maps for better understanding.',
    icon: 'eye',
    color: 'orange'
  },
  {
    id: 'degradation-assessment',
    title: 'Degradation Assessment',
    description: 'Qualitative assessment of boulder freshness based on confidence levels.',
    icon: 'star',
    color: 'yellow'
  },
  {
    id: 'dual-model-detection',
    title: 'Dual Model Detection',
    description: 'Use YOLO for initial detection and ViT for validation of low-confidence detections.',
    icon: 'brain',
    color: 'indigo'
  }
];

export const BOULDER_DETECTION_STATS = {
  modelAccuracy: '94.2%',
  processingSpeed: '2.4s',
  objectsDetected: '1,247',
  averageConfidence: '0.87',
  totalScans: '892',
  uptime: '99.7%'
};

export const BOULDER_NAVIGATION_ITEMS = [
  { label: 'Dashboard', path: '/dashboard', active: false },
  { label: 'Analytics', path: '/analytics', active: false },
  { label: 'Boulder Detection', path: '/boulder', active: true },
  { label: 'Settings', path: '/settings', active: false }
];

export const BOULDER_FOOTER_DATA = {
  status: 'Operational',
  uptime: '99.7%',
  lastUpdate: '2 min ago',
  version: 'v2.4.1'
};

export const BOULDER_DETECTION_MODELS = {
  yolo: {
    name: 'YOLO Model',
    file: 'best.pt',
    size: '6.0MB',
    accuracy: '85-90%',
    classes: ['boulder'],
    inputSize: '640x640'
  },
  vit: {
    name: 'Vision Transformer',
    file: 'vit_model.pth',
    size: '327MB',
    accuracy: '92-95%',
    classes: ['boulder'],
    inputSize: '224x224'
  }
};

export const BOULDER_DETECTION_PARAMETERS = {
  scale: {
    description: 'Scale factor (meters per pixel)',
    default: 1.0,
    range: [0.1, 10.0],
    unit: 'm/pixel'
  },
  confidenceThreshold: {
    description: 'Confidence threshold for ViT fallback',
    default: 0.6,
    range: [0.1, 1.0],
    unit: 'probability'
  },
  solarIncidenceAngle: {
    description: 'Solar incidence angle for depth estimation',
    default: 45.0,
    range: [0, 90],
    unit: 'degrees'
  }
};

export const BOULDER_DETECTION_OUTPUTS = {
  physicalMeasurements: [
    'Size/Diameter',
    'Area',
    'Volume',
    'Circularity',
    'Elongation',
    'Depth (boulders only)'
  ],
  degradationState: [
    'Fresh (confidence ≥ 0.8)',
    'Moderately degraded (0.6 ≤ confidence < 0.8)',
    'Highly degraded (confidence < 0.6)'
  ],
  densityAnalysis: [
    'Boulder density (boulders per square meter)'
  ]
}; 
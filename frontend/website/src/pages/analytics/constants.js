// Mock data for analytics records
export const MOCK_ANALYSIS_RECORDS = [
  {
    id: 1,
    timestamp: '2024-01-15T10:30:00Z',
    analysisType: 'basic',
    imageName: 'lunar_surface_001.jpg',
    totalObjects: 12,
    boulders: 8,
    craters: 4,
    averageSize: 2.4,
    confidence: 0.87,
    processingTime: 2.3,
    status: 'completed',
    user: 'ISRO Mission Control',
    density: 0.000156,
    visualizationImage: '/uploads/lunar_surface_001_detected.png',
    gradcamImage: '/uploads/lunar_surface_001_gradcam.png'
  },
  {
    id: 2,
    timestamp: '2024-01-14T15:45:00Z',
    analysisType: 'advanced',
    imageName: 'crater_analysis_002.jpg',
    totalObjects: 18,
    boulders: 12,
    craters: 6,
    averageSize: 3.1,
    confidence: 0.92,
    processingTime: 3.1,
    status: 'completed',
    user: 'Lunar Mission Team',
    density: 0.000234,
    visualizationImage: '/uploads/crater_analysis_002_detected.png',
    gradcamImage: '/uploads/crater_analysis_002_gradcam.png'
  }
];

export const ANALYSIS_TYPES = {
  basic: { name: 'Basic Detection', color: 'orange', icon: '🔍' },
  advanced: { name: 'Advanced Analysis', color: 'blue', icon: '🧠' },
  depth: { name: 'Depth Estimation', color: 'green', icon: '📏' },
  gradcam: { name: 'Grad-CAM Visualization', color: 'purple', icon: '👁️' }
};

export const STATUS_COLORS = {
  completed: 'green',
  processing: 'yellow',
  failed: 'red',
  pending: 'gray'
};

export const FILTER_OPTIONS = {
  analysisType: ['all', 'basic', 'advanced', 'depth', 'gradcam'],
  status: ['all', 'completed', 'processing', 'failed', 'pending'],
  dateRange: ['all', 'today', 'week', 'month', 'year']
}; 
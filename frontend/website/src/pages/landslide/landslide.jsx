import React, { useState, useEffect } from 'react';
import HeroSection from './components/HeroSection';
import ImageUpload from './components/ImageUpload';
import AnalysisParameters from './components/AnalysisParameters';
import AnalysisResults from './components/AnalysisResults';
import ImagePreview from './components/ImagePreview';
import ProgressSteps from './components/ProgressSteps';
import { LANDSLIDE_CONSTANTS } from './constants/constants';

const LandslideDetection = () => {
  const [image, setImage] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [results, setResults] = useState(null);
  const [parameters, setParameters] = useState({
    SLOPE_THRESHOLD: LANDSLIDE_CONSTANTS.ANALYSIS_PARAMETERS.SLOPE_THRESHOLD.default,
    ELEVATION_CHANGE: LANDSLIDE_CONSTANTS.ANALYSIS_PARAMETERS.ELEVATION_CHANGE.default,
    SURFACE_ROUGHNESS: LANDSLIDE_CONSTANTS.ANALYSIS_PARAMETERS.SURFACE_ROUGHNESS.default,
    COHERENCE_THRESHOLD: LANDSLIDE_CONSTANTS.ANALYSIS_PARAMETERS.COHERENCE_THRESHOLD.default,
  });

  const handleImageUpload = async (file) => {
    setIsUploading(true);
    setCurrentStep(0);
    setResults(null);

    // Simulate upload delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    setImage(file);
    setIsUploading(false);
    setCurrentStep(1);
  };

  const handleParameterChange = (paramKey, value) => {
    setParameters(prev => ({
      ...prev,
      [paramKey]: value
    }));
  };

  const startAnalysis = async () => {
    if (!image) return;

    setIsAnalyzing(true);
    setCurrentStep(2);

    // Simulate analysis steps
    const analysisSteps = [
      { step: 2, duration: 3000, message: 'Preprocessing image...' },
      { step: 3, duration: 4000, message: 'Detecting landslide features...' },
      { step: 4, duration: 3000, message: 'Calculating risk assessment...' },
      { step: 5, duration: 2000, message: 'Generating report...' }
    ];

    for (const analysisStep of analysisSteps) {
      await new Promise(resolve => setTimeout(resolve, analysisStep.duration));
      setCurrentStep(analysisStep.step);
    }

    // Generate mock results
    const mockResults = generateMockResults();
    setResults(mockResults);
    setIsAnalyzing(false);
  };

  const generateMockResults = () => {
    const riskScore = Math.random() * 0.9 + 0.1; // 0.1 to 1.0
    const confidence = Math.random() * 0.3 + 0.7; // 0.7 to 1.0
    const precision = Math.random() * 0.2 + 0.8; // 0.8 to 1.0
    const recall = Math.random() * 0.2 + 0.8; // 0.8 to 1.0

    return {
      riskScore,
      confidence,
      precision,
      recall,
      affectedArea: (Math.random() * 50 + 10).toFixed(1),
      slopeRange: {
        min: Math.floor(Math.random() * 20 + 10),
        max: Math.floor(Math.random() * 30 + 40)
      },
      elevationChange: Math.floor(Math.random() * 100 + 20),
      detectedFeatures: [
        { name: 'Slope Instability', count: Math.floor(Math.random() * 10 + 5), icon: '⛰️', x: 20, y: 30 },
        { name: 'Surface Cracks', count: Math.floor(Math.random() * 15 + 8), icon: '🔍', x: 60, y: 45 },
        { name: 'Debris Flow', count: Math.floor(Math.random() * 8 + 3), icon: '🌊', x: 80, y: 70 },
        { name: 'Rock Falls', count: Math.floor(Math.random() * 12 + 6), icon: '🪨', x: 40, y: 80 }
      ],
      riskZones: [
        { x: 15, y: 25, width: 20, height: 15, risk: 'high' },
        { x: 60, y: 40, width: 25, height: 20, risk: 'medium' },
        { x: 80, y: 65, width: 15, height: 10, risk: 'low' }
      ],
      summary: `Analysis of the lunar surface image reveals ${riskScore > 0.7 ? 'significant' : riskScore > 0.4 ? 'moderate' : 'minimal'} landslide risk indicators. The detected features suggest ${riskScore > 0.7 ? 'high' : riskScore > 0.4 ? 'moderate' : 'low'} probability of surface instability in the analyzed region.`,
      recommendations: [
        'Conduct detailed ground truth verification of detected features',
        'Monitor the identified high-risk zones for temporal changes',
        'Consider additional imaging at different wavelengths for validation',
        'Implement early warning systems for the affected areas'
      ]
    };
  };

  const handleExport = (format) => {
    if (!results) return;

    const exportData = {
      timestamp: new Date().toISOString(),
      parameters,
      results,
      imageInfo: {
        name: image?.name,
        size: image?.size,
        type: image?.type
      }
    };

    let content, filename, mimeType;

    switch (format) {
      case 'json':
        content = JSON.stringify(exportData, null, 2);
        filename = 'landslide-analysis.json';
        mimeType = 'application/json';
        break;
      case 'csv':
        content = generateCSV(exportData);
        filename = 'landslide-analysis.csv';
        mimeType = 'text/csv';
        break;
      case 'pdf':
        // For PDF, we'd typically use a library like jsPDF
        alert('PDF export would be implemented with jsPDF library');
        return;
      case 'geojson':
        content = generateGeoJSON(exportData);
        filename = 'landslide-analysis.geojson';
        mimeType = 'application/geo+json';
        break;
      default:
        return;
    }

    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const generateCSV = (data) => {
    const headers = ['Parameter', 'Value', 'Unit'];
    const rows = [
      ['Risk Score', (data.results.riskScore * 100).toFixed(1), '%'],
      ['Confidence', (data.results.confidence * 100).toFixed(1), '%'],
      ['Precision', (data.results.precision * 100).toFixed(1), '%'],
      ['Recall', (data.results.recall * 100).toFixed(1), '%'],
      ['Affected Area', data.results.affectedArea, 'km²'],
      ['Elevation Change', data.results.elevationChange, 'm'],
      ['Slope Range Min', data.results.slopeRange.min, '°'],
      ['Slope Range Max', data.results.slopeRange.max, '°']
    ];

    return [headers, ...rows].map(row => row.join(',')).join('\n');
  };

  const generateGeoJSON = (data) => {
    return JSON.stringify({
      type: 'FeatureCollection',
      features: data.results.riskZones.map((zone, index) => ({
        type: 'Feature',
        properties: {
          id: index,
          risk: zone.risk,
          area: zone.width * zone.height / 100
        },
        geometry: {
          type: 'Polygon',
          coordinates: [[
            [zone.x, zone.y],
            [zone.x + zone.width, zone.y],
            [zone.x + zone.width, zone.y + zone.height],
            [zone.x, zone.y + zone.height],
            [zone.x, zone.y]
          ]]
        }
      }))
    }, null, 2);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Hero Section */}
        <HeroSection />

        <div className="block gap-6 mt-8" style={{ width: '-webkit-fill-available' }}>
          {/* Left Column - Upload and Parameters */}
          <div className="w-full lg:w-1/3 space-y-6" style={{ width: '-webkit-fill-available' }}>
            {/* Image Upload */}
            <ImageUpload 
              onImageUpload={handleImageUpload}
              isUploading={isUploading}
            />

            {/* Analysis Parameters */}
            <AnalysisParameters
              parameters={parameters}
              onParameterChange={handleParameterChange}
              isAnalyzing={isAnalyzing}
            />

            {/* Progress Steps */}
            <ProgressSteps
              currentStep={currentStep}
              isAnalyzing={isAnalyzing}
            />
          </div>

          {/* Right Column - Preview and Results */}
          <div className="w-full lg:w-2/3 space-y-6" style={{ width: '-webkit-fill-available' }}>
            {/* Image Preview */}
            {image && (
              <ImagePreview
                image={image}
                results={results}
                isAnalyzing={isAnalyzing}
              />
            )}

            {/* Analysis Results */}
            {results && (
              <AnalysisResults
                results={results}
                onExport={handleExport}
              />
            )}

            {/* Start Analysis Button */}
            {image && !isAnalyzing && !results && (
              <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                <div className="text-center">
                  <h3 className="text-xl font-semibold text-gray-100 mb-4">
                    Ready to Analyze
                  </h3>
                  <p className="text-gray-400 mb-6">
                    Click the button below to start the landslide detection analysis
                  </p>
                  <button
                    onClick={startAnalysis}
                    className="px-8 py-4 bg-gradient-to-r from-red-500 to-orange-500 hover:from-red-600 hover:to-orange-600 text-white font-semibold rounded-lg transition-all duration-300 hover:shadow-lg hover:shadow-red-500/25 transform hover:scale-105"
                  >
                    Start Analysis
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandslideDetection;

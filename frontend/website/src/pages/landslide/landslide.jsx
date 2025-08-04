import React, { useState, useEffect } from 'react';
import HeroSection from './components/HeroSection';
import ImageUpload from './components/ImageUpload';
import ImagePreview from './components/ImagePreview';
import AnalysisConfig from './components/AnalysisConfig';
import LunarParametersDisplay from './components/LunarParametersDisplay';

const LandslideDetection = () => {
  const [image, setImage] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showParameters, setShowParameters] = useState(false);

  const handleImageUpload = async (file) => {
    setIsUploading(true);
    setShowParameters(false);

    // Simulate upload delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    setImage(file);
    setIsUploading(false);
  };

  const startAnalysis = async () => {
    if (!image) return;

    setIsAnalyzing(true);

    // Simulate analysis processing
    await new Promise(resolve => setTimeout(resolve, 3000));

    setShowParameters(true);
    setIsAnalyzing(false);
  };

  const handleExport = (format) => {
    if (!image) return;

    const exportData = {
      timestamp: new Date().toISOString(),
      imageInfo: {
        name: image?.name,
        size: image?.size,
        type: image?.type
      },
      lunarParameters: {
        composite_risk_score: 10.13,
        risk_level: "LOW",
        description: "Safe terrain for lunar operations"
      }
    };

    let content, filename, mimeType;

    switch (format) {
      case 'json':
        content = JSON.stringify(exportData, null, 2);
        filename = 'lunar-analysis.json';
        mimeType = 'application/json';
        break;
      case 'csv':
        content = generateCSV(exportData);
        filename = 'lunar-analysis.csv';
        mimeType = 'text/csv';
        break;
      case 'pdf':
        alert('PDF export would be implemented with jsPDF library');
        return;
      case 'geojson':
        content = generateGeoJSON(exportData);
        filename = 'lunar-analysis.geojson';
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
      ['Composite Risk Score', data.lunarParameters.composite_risk_score, 'score'],
      ['Risk Level', data.lunarParameters.risk_level, 'level'],
      ['Description', data.lunarParameters.description, 'text']
    ];

    return [headers, ...rows].map(row => row.join(',')).join('\n');
  };

  const generateGeoJSON = (data) => {
    return JSON.stringify({
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: {
          risk_score: data.lunarParameters.composite_risk_score,
          risk_level: data.lunarParameters.risk_level,
          description: data.lunarParameters.description
        },
        geometry: {
          type: 'Point',
          coordinates: [0, 0]
        }
      }]
    }, null, 2);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Hero Section */}
        <HeroSection />

        {/* Main Content Layout */}
        <div className="flex flex-col xl:flex-row gap-8 mt-8">
          {/* Left Column - Controls and Configuration */}
          <div className="xl:w-[420px] flex-shrink-0">
            <div className="space-y-6">
              {/* Image Upload */}
              <ImageUpload 
                onImageUpload={handleImageUpload}
                isUploading={isUploading}
              />

              {/* Analysis Configuration */}
              <AnalysisConfig
                onStartAnalysis={startAnalysis}
                isAnalyzing={isAnalyzing}
              />
            </div>
          </div>

          {/* Right Column - Preview and Parameters */}
          <div className="flex-1 min-w-0">
            <div className="space-y-6">
              {/* Image Preview */}
              {image && (
                <ImagePreview
                  image={image}
                  isAnalyzing={isAnalyzing}
                />
              )}

              {/* Lunar Parameters Display */}
              <LunarParametersDisplay
                isVisible={showParameters}
              />

              {/* Placeholder for right column when no content */}
              {!image && (
                <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-8 border border-gray-700 shadow-lg">
                  <div className="text-center">
                    <div className="w-24 h-24 mx-auto bg-gradient-to-br from-gray-700 to-gray-600 rounded-full flex items-center justify-center mb-6">
                      <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                    </div>
                    <h3 className="text-2xl font-bold text-gray-100 mb-4">
                      Upload a Lunar DEM
                    </h3>
                    <p className="text-gray-400 text-lg">
                      Upload a Digital Elevation Model to begin lunar terrain analysis
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandslideDetection;

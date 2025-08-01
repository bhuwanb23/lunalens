import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './boulder.css';

const Boulder = () => {
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleAnalysisSelect = (analysisType) => {
    setSelectedAnalysis(analysisType);
    
    setTimeout(() => {
      setShowConfirmation(true);
    }, 800);
  };

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setUploadedFile(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setUploadedImage(e.target.result);
      };
      reader.readAsDataURL(file);
      setError(null);
    }
  };

  const uploadImage = async (file) => {
    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetch('http://localhost:5000/api/boulder/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload image');
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Upload error:', error);
      throw error;
    }
  };

  const analyzeImage = async (filepath, analysisType) => {
    try {
      const response = await fetch('http://localhost:5000/api/boulder/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          filepath: filepath,
          analysisType: analysisType
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze image');
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Analysis error:', error);
      throw error;
    }
  };

  const handleStartAnalysis = async () => {
    if (!uploadedFile || !selectedAnalysis) {
      setError('Please upload an image and select an analysis type');
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      // Upload image
      const uploadResult = await uploadImage(uploadedFile);
      
      // Analyze image
      const analysisResult = await analyzeImage(uploadResult.filepath, selectedAnalysis);
      
      if (analysisResult.success) {
        // Process results
        const results = {
          totalObjects: analysisResult.detected_objects.length,
          boulders: analysisResult.detected_objects.filter(obj => obj.class_name === 'boulder').length,
          craters: analysisResult.detected_objects.filter(obj => obj.class_name === 'crater').length,
          density: analysisResult.density_analysis?.density || 0,
          averageSize: analysisResult.detected_objects.reduce((sum, obj) => sum + obj.diameter_real, 0) / analysisResult.detected_objects.length || 0,
          confidence: analysisResult.detected_objects.reduce((sum, obj) => sum + obj.confidence, 0) / analysisResult.detected_objects.length || 0,
          processingTime: 2.4, // This would come from backend
          detectedObjects: analysisResult.detected_objects,
          additionalFiles: analysisResult.additional_files || []
        };
        
        setAnalysisResults(results);
      } else {
        setError(analysisResult.message || 'Analysis failed');
      }
    } catch (error) {
      setError(error.message || 'An error occurred during analysis');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleProceed = () => {
    navigate('/dashboard');
  };

  const getAnalysisName = (analysisType) => {
    switch (analysisType) {
      case 'basic':
        return 'Basic Boulder Detection';
      case 'advanced':
        return 'Advanced Analysis with ViT Fallback';
      case 'depth':
        return 'Depth Estimation Analysis';
      case 'gradcam':
        return 'Grad-CAM Visualization Analysis';
      default:
        return 'Analysis';
    }
  };

  const analysisTypes = [
    {
      id: 'basic',
      title: 'Basic Detection',
      description: 'Standard YOLO-based boulder and crater detection with physical measurements.',
      icon: 'mountain',
      color: 'orange',
      features: ['Object Detection', 'Size Measurement', 'Density Analysis']
    },
    {
      id: 'advanced',
      title: 'Advanced Analysis',
      description: 'Dual-model detection using YOLO and Vision Transformer for enhanced accuracy.',
      icon: 'brain',
      color: 'blue',
      features: ['ViT Fallback', 'High Accuracy', 'Confidence Validation']
    },
    {
      id: 'depth',
      title: 'Depth Estimation',
      description: 'Crater depth estimation using shadow analysis and solar incidence angle.',
      icon: 'layer-group',
      color: 'green',
      features: ['Shadow Analysis', 'Depth Calculation', 'Solar Angle']
    },
    {
      id: 'gradcam',
      title: 'Grad-CAM Visualization',
      description: 'Model interpretability with attention maps and visualization.',
      icon: 'eye',
      color: 'purple',
      features: ['Attention Maps', 'Model Interpretability', 'Visualization']
    }
  ];

  return (
    <div className="bg-gray-900 text-white overflow-x-hidden">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center">
                <i className="text-white text-lg">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </i>
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-orange-400 to-red-500 bg-clip-text text-transparent">
                Boulder Detection
              </h1>
            </div>
            <nav className="flex items-center space-x-6">
              <span 
                className="text-gray-300 hover:text-blue-400 transition-colors cursor-pointer"
                onClick={() => navigate('/dashboard')}
              >
                Dashboard
              </span>
              <span 
                className="text-gray-300 hover:text-blue-400 transition-colors cursor-pointer"
                onClick={() => navigate('/analytics')}
              >
                Analytics
              </span>
              <span className="text-orange-400 font-medium cursor-pointer">Boulder Detection</span>
              <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center">
                <i className="text-sm">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 448 512">
                    <path d="M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H418.3c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304H178.3z" />
                  </svg>
                </i>
              </div>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="min-h-screen bg-gray-900">
        {/* Hero Section */}
        <section className="relative h-[300px] flex items-center justify-center overflow-hidden">
          <div className="absolute inset-0 moon-glow"></div>
          <div className="absolute top-10 right-20 w-32 h-32 rounded-full bg-gradient-to-br from-orange-200 to-red-400 opacity-20"></div>
          <div className="absolute bottom-10 left-16 w-20 h-20 rounded-full bg-gradient-to-br from-orange-300 to-red-500 opacity-10"></div>
          <div className="text-center z-10">
            <h2 className="text-5xl font-light mb-4 bg-gradient-to-r from-gray-200 to-orange-300 bg-clip-text text-transparent">
              Boulder & Crater Detection
            </h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Advanced AI-powered detection system for lunar boulders and craters with physical measurements and analysis
            </p>
          </div>
        </section>

        {/* Image Upload Section */}
        <section className="py-8 px-6">
          <div className="max-w-4xl mx-auto">
            <div className="bg-gray-800 border-2 border-dashed border-gray-600 rounded-2xl p-8 text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <i className="text-2xl text-white">
                  <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </i>
              </div>
              <h3 className="text-2xl font-semibold mb-4 text-gray-200">Upload Lunar Image</h3>
              <p className="text-gray-400 mb-6">Upload a lunar surface image for boulder and crater detection analysis</p>
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="hidden"
                id="image-upload"
              />
              <label
                htmlFor="image-upload"
                className="bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 px-8 py-3 rounded-xl font-medium transition-all duration-300 glow-effect cursor-pointer inline-block"
              >
                Choose Image
              </label>
              {uploadedImage && (
                <div className="mt-4">
                  <img src={uploadedImage} alt="Uploaded" className="max-w-xs mx-auto rounded-lg" />
                  <p className="text-green-400 mt-2">✓ Image uploaded successfully</p>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Analysis Selection Section */}
        <section className="py-16 px-6">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <h3 className="text-3xl font-semibold mb-4 text-gray-200">Choose Analysis Type</h3>
              <p className="text-gray-400">Select your preferred detection method for lunar surface analysis</p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {analysisTypes.map((analysis) => (
                <div 
                  key={analysis.id}
                  className={`selection-card bg-gray-800 border-2 border-gray-700 rounded-2xl p-6 cursor-pointer transition-all duration-300 card-hover relative overflow-hidden ${
                    selectedAnalysis === analysis.id ? 'selected-card' : ''
                  }`}
                  onClick={() => handleAnalysisSelect(analysis.id)}
                >
                  <div className={`absolute top-0 right-0 w-20 h-20 rounded-full bg-gradient-to-br from-${analysis.color}-400 to-${analysis.color === 'orange' ? 'red' : analysis.color === 'blue' ? 'indigo' : analysis.color === 'green' ? 'emerald' : 'purple'}-500 opacity-10 -mr-10 -mt-10`}></div>
                  <div className="relative z-10">
                    <div className={`w-12 h-12 bg-gradient-to-br from-${analysis.color}-400 to-${analysis.color === 'orange' ? 'red' : analysis.color === 'blue' ? 'indigo' : analysis.color === 'green' ? 'emerald' : 'purple'}-500 rounded-xl flex items-center justify-center mb-4 glow-effect`}>
                      <i className="text-xl text-white">
                        <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 512 512">
                          {analysis.icon === 'mountain' && (
                            <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                          )}
                          {analysis.icon === 'brain' && (
                            <path d="M184 0c30.9 0 56 25.1 56 56V456c0 30.9-25.1 56-56 56c-28.9 0-52.7-21.9-55.7-50.1c-5.2 1.4-10.7 2.1-16.3 2.1c-35.3 0-64-28.7-64-64c0-7.4 1.3-14.6 3.6-21.2C21.4 367.4 0 338.2 0 304c0-31.9 18.7-59.5 45.8-72.3C37.1 220.8 32 207 32 192c0-30.7 21.6-56.3 50.4-62.6C80.8 123.9 80 118 80 112c0-29.9 20.6-55.1 48.3-62.1C131.3 21.9 155.1 0 184 0zM328 0c28.9 0 52.6 21.9 55.7 49.9c27.8 7 48.3 32.1 48.3 62.1c0 6-.8 11.9-2.4 17.4c28.8 6.2 50.4 31.9 50.4 62.6c0 15-5.1 28.8-13.8 39.7C493.3 244.5 512 272.1 512 304c0 34.2-21.4 63.4-51.6 74.8c2.3 6.6 3.6 13.8 3.6 21.2c0 35.3-28.7 64-64 64c-5.6 0-11.1-.7-16.3-2.1c-3 28.2-26.8 50.1-55.7 50.1c-30.9 0-56-25.1-56-56V56c0-30.9 25.1-56 56-56z" />
                          )}
                          {analysis.icon === 'layer-group' && (
                            <path d="M264.5 5.2c14.9-6.9 32.1-6.9 47 0l218.6 101c8.5 3.9 13.9 12.4 13.9 21.8s-5.4 17.9-13.9 21.8l-218.6 101c-14.9 6.9-32.1 6.9-47 0L45.9 149.8C37.4 145.8 32 137.3 32 128s5.4-17.9 13.9-21.8L264.5 5.2zM476.9 209.6l53.2 24.6c8.5 3.9 13.9 12.4 13.9 21.8s-5.4 17.9-13.9 21.8l-218.6 101c-14.9 6.9-32.1 6.9-47 0L45.9 277.8C37.4 273.8 32 265.3 32 256s5.4-17.9 13.9-21.8l53.2-24.6 152 70.2c23.4 10.8 50.4 10.8 73.8 0l152-70.2zm-152 198.2l152-70.2 53.2 24.6c8.5 3.9 13.9 12.4 13.9 21.8s-5.4 17.9-13.9 21.8l-218.6 101c-14.9 6.9-32.1 6.9-47 0L45.9 405.8C37.4 401.8 32 393.3 32 384s5.4-17.9 13.9-21.8l53.2-24.6 152 70.2c23.4 10.8 50.4 10.8 73.8 0z" />
                          )}
                          {analysis.icon === 'eye' && (
                            <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                          )}
                        </svg>
                      </i>
                    </div>
                    <h4 className="text-lg font-semibold mb-2 text-gray-200">{analysis.title}</h4>
                    <p className="text-gray-400 text-sm mb-4 leading-relaxed">{analysis.description}</p>
                    <div className="space-y-1">
                      {analysis.features.map((feature, index) => (
                        <div key={index} className="flex items-center text-xs text-gray-300">
                          <span className="w-1 h-1 bg-gray-400 rounded-full mr-2"></span>
                          {feature}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Confirmation Section */}
        {showConfirmation && (
          <section className="py-12 px-6">
            <div className="max-w-2xl mx-auto text-center">
              <div className="bg-gray-800 border border-gray-700 rounded-2xl p-8">
                <div className="w-20 h-20 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center mx-auto mb-6 pulse-animation">
                  <i className="text-3xl text-white">
                    <svg className="w-10 h-10" fill="currentColor" viewBox="0 0 448 512">
                      <path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z" />
                    </svg>
                  </i>
                </div>
                <h3 className="text-2xl font-semibold mb-4 text-gray-200">Analysis Initiated</h3>
                <p className="text-gray-400 mb-8">
                  {getAnalysisName(selectedAnalysis)} has been initiated and is now processing lunar surface data...
                </p>
                {error && (
                  <div className="mb-4 p-4 bg-red-900 border border-red-700 rounded-lg">
                    <p className="text-red-300">{error}</p>
                  </div>
                )}
                <button 
                  onClick={handleStartAnalysis}
                  disabled={isAnalyzing}
                  className={`px-8 py-3 rounded-xl font-medium transition-all duration-300 glow-effect ${
                    isAnalyzing 
                      ? 'bg-gray-600 cursor-not-allowed' 
                      : 'bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700'
                  }`}
                >
                  {isAnalyzing ? (
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Analyzing...</span>
                    </div>
                  ) : (
                    'Start Analysis'
                  )}
                </button>
              </div>
            </div>
          </section>
        )}

        {/* Results Section */}
        {analysisResults && (
          <section className="py-12 px-6">
            <div className="max-w-6xl mx-auto">
              <div className="bg-gray-800 border border-gray-700 rounded-2xl p-8">
                <h3 className="text-2xl font-semibold mb-6 text-gray-200">Analysis Results</h3>
                <div className="grid md:grid-cols-3 gap-6">
                  <div className="bg-gray-700 rounded-xl p-6">
                    <h4 className="text-lg font-semibold mb-2 text-gray-200">Objects Detected</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Boulders:</span>
                        <span className="text-orange-400 font-semibold">{analysisResults.boulders}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Craters:</span>
                        <span className="text-blue-400 font-semibold">{analysisResults.craters}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Total:</span>
                        <span className="text-green-400 font-semibold">{analysisResults.totalObjects}</span>
                      </div>
                    </div>
                  </div>
                  <div className="bg-gray-700 rounded-xl p-6">
                    <h4 className="text-lg font-semibold mb-2 text-gray-200">Analysis Metrics</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Density:</span>
                        <span className="text-purple-400 font-semibold">{analysisResults.density} obj/m²</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Avg Size:</span>
                        <span className="text-yellow-400 font-semibold">{analysisResults.averageSize}m</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Confidence:</span>
                        <span className="text-green-400 font-semibold">{(analysisResults.confidence * 100).toFixed(1)}%</span>
                      </div>
                    </div>
                  </div>
                  <div className="bg-gray-700 rounded-xl p-6">
                    <h4 className="text-lg font-semibold mb-2 text-gray-200">Processing Info</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Time:</span>
                        <span className="text-blue-400 font-semibold">{analysisResults.processingTime}s</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Status:</span>
                        <span className="text-green-400 font-semibold">Complete</span>
                      </div>
                    </div>
                  </div>
                </div>
                {analysisResults.detectedObjects && analysisResults.detectedObjects.length > 0 && (
                  <div className="mt-8">
                    <h4 className="text-lg font-semibold mb-4 text-gray-200">Detected Objects Details</h4>
                    <div className="bg-gray-700 rounded-xl p-4 max-h-64 overflow-y-auto">
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {analysisResults.detectedObjects.map((obj, index) => (
                          <div key={index} className="bg-gray-600 rounded-lg p-3">
                            <div className="flex justify-between items-center mb-2">
                              <span className="text-sm font-medium text-gray-300">
                                {obj.class_name.charAt(0).toUpperCase() + obj.class_name.slice(1)} {index + 1}
                              </span>
                              <span className="text-xs text-gray-400">
                                {(obj.confidence * 100).toFixed(1)}%
                              </span>
                            </div>
                            <div className="space-y-1 text-xs text-gray-400">
                              <div>Size: {obj.diameter_real.toFixed(2)}m</div>
                              <div>Area: {obj.area_real.toFixed(2)}m²</div>
                              <div>Volume: {obj.volume_real.toFixed(2)}m³</div>
                              {obj.estimated_depth && (
                                <div>Depth: {obj.estimated_depth.toFixed(2)}m</div>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
                <div className="mt-8 flex justify-center space-x-4">
                  <button 
                    onClick={handleProceed}
                    className="bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 px-6 py-3 rounded-xl font-medium transition-all duration-300"
                  >
                    Back to Dashboard
                  </button>
                  <button className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 px-6 py-3 rounded-xl font-medium transition-all duration-300">
                    Export Results
                  </button>
                </div>
              </div>
            </div>
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 border-t border-gray-700 py-8">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-gray-400">© 2024 LunaLens Boulder Detection. Advanced AI-powered lunar analysis.</p>
        </div>
      </footer>
    </div>
  );
};

export default Boulder; 
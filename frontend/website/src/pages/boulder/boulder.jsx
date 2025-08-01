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
          additionalFiles: analysisResult.additional_files || [],
          visualizationImage: analysisResult.additional_files?.find(file => file.type === 'visualization')?.path,
          gradcamImage: analysisResult.additional_files?.find(file => file.type === 'gradcam')?.path
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
      {/* Enhanced Header */}
      <header className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 border-b border-gray-700 shadow-2xl backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-6">
              <div className="w-12 h-12 bg-gradient-to-br from-orange-400 via-red-500 to-orange-600 rounded-2xl flex items-center justify-center shadow-lg hover:shadow-orange-500/25 transition-all duration-300 transform hover:scale-110">
                <i className="text-white text-xl">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </i>
              </div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-orange-400 via-red-500 to-orange-600 bg-clip-text text-transparent animate-pulse">
                Boulder Detection
              </h1>
            </div>
            <nav className="flex items-center space-x-8">
              <span 
                className="text-gray-300 hover:text-blue-400 transition-all duration-300 cursor-pointer font-medium hover:scale-105 transform"
                onClick={() => navigate('/dashboard')}
              >
                Dashboard
              </span>
              <span 
                className="text-gray-300 hover:text-blue-400 transition-all duration-300 cursor-pointer font-medium hover:scale-105 transform"
                onClick={() => navigate('/analytics')}
              >
                Analytics
              </span>
              <span className="text-orange-400 font-semibold cursor-pointer bg-gradient-to-r from-orange-500/20 to-red-500/20 px-4 py-2 rounded-xl border border-orange-500/30">Boulder Detection</span>
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-gray-600 to-gray-700 flex items-center justify-center shadow-lg hover:shadow-gray-500/25 transition-all duration-300 transform hover:scale-110">
                <i className="text-sm">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 448 512">
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
        {/* Enhanced Hero Section */}
        <section className="relative h-[400px] flex items-center justify-center overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
          {/* Animated background elements */}
          <div className="absolute inset-0 bg-gradient-to-br from-orange-500/5 via-red-500/3 to-orange-600/5 animate-pulse"></div>
          <div className="absolute top-10 right-20 w-40 h-40 rounded-full bg-gradient-to-br from-orange-200 to-red-400 opacity-20 animate-bounce"></div>
          <div className="absolute bottom-10 left-16 w-24 h-24 rounded-full bg-gradient-to-br from-orange-300 to-red-500 opacity-15 animate-pulse"></div>
          <div className="absolute top-1/4 left-1/4 w-16 h-16 rounded-full bg-gradient-to-br from-red-300 to-orange-400 opacity-10 animate-spin"></div>
          
          <div className="text-center z-10 relative">
            <div className="mb-8">
              <div className="w-20 h-20 bg-gradient-to-br from-orange-400 via-red-500 to-orange-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-2xl hover:shadow-orange-500/50 transition-all duration-500 transform hover:scale-110">
                <i className="text-white text-3xl">
                  <svg className="w-10 h-10" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </i>
              </div>
            </div>
            <h2 className="text-6xl font-bold mb-6 bg-gradient-to-r from-gray-100 via-orange-200 to-red-300 bg-clip-text text-transparent animate-pulse">
              Boulder & Crater Detection
            </h2>
            <p className="text-2xl text-gray-300 max-w-3xl mx-auto leading-relaxed font-light">
              Advanced AI-powered detection system for lunar boulders and craters with physical measurements and analysis
            </p>
            <div className="mt-8 flex justify-center space-x-4">
              <div className="w-3 h-3 bg-orange-400 rounded-full animate-bounce"></div>
              <div className="w-3 h-3 bg-red-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
              <div className="w-3 h-3 bg-orange-600 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
            </div>
          </div>
        </section>

        {/* Enhanced Image Upload Section */}
        <section className="py-12 px-6">
          <div className="max-w-5xl mx-auto">
            <div className="bg-gradient-to-br from-gray-800 via-gray-700 to-gray-800 border-2 border-dashed border-orange-500/30 rounded-3xl p-12 text-center shadow-2xl hover:shadow-orange-500/20 transition-all duration-500 transform hover:scale-[1.02]">
              <div className="w-20 h-20 bg-gradient-to-br from-orange-400 via-red-500 to-orange-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl hover:shadow-orange-500/50 transition-all duration-300 transform hover:scale-110">
                <i className="text-3xl text-white">
                  <svg className="w-10 h-10" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                </i>
              </div>
              <h3 className="text-3xl font-bold mb-4 bg-gradient-to-r from-gray-200 to-orange-300 bg-clip-text text-transparent">Upload Lunar Image</h3>
              <p className="text-gray-300 mb-8 text-lg leading-relaxed">Upload a lunar surface image for boulder and crater detection analysis</p>
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="hidden"
                id="image-upload"
              />
              <label
                htmlFor="image-upload"
                className="bg-gradient-to-r from-orange-500 via-red-600 to-orange-700 hover:from-orange-600 hover:via-red-700 hover:to-orange-800 px-10 py-4 rounded-2xl font-semibold transition-all duration-300 shadow-lg hover:shadow-orange-500/50 cursor-pointer inline-block transform hover:scale-105 hover:-translate-y-1"
              >
                <span className="flex items-center space-x-2">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 512 512">
                    <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                  </svg>
                  <span>Choose Image</span>
                </span>
              </label>
              {uploadedImage && (
                <div className="mt-8 animate-fade-in">
                  <div className="relative inline-block">
                    <img src={uploadedImage} alt="Uploaded" className="max-w-sm mx-auto rounded-2xl shadow-2xl border-4 border-green-500/30" />
                    <div className="absolute -top-2 -right-2 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center shadow-lg">
                      <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 448 512">
                        <path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z" />
                      </svg>
                    </div>
                  </div>
                  <p className="text-green-400 mt-4 text-lg font-semibold flex items-center justify-center">
                    <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 448 512">
                      <path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z" />
                    </svg>
                    Image uploaded successfully
                  </p>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Enhanced Analysis Selection Section */}
        <section className="py-20 px-6">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h3 className="text-4xl font-bold mb-6 bg-gradient-to-r from-gray-200 to-orange-300 bg-clip-text text-transparent">Choose Analysis Type</h3>
              <p className="text-gray-300 text-xl leading-relaxed max-w-3xl mx-auto">Select your preferred detection method for lunar surface analysis</p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {analysisTypes.map((analysis) => (
                <div 
                  key={analysis.id}
                  className={`bg-gradient-to-br from-gray-800 via-gray-700 to-gray-800 border-2 border-gray-600 rounded-3xl p-8 cursor-pointer transition-all duration-500 transform hover:scale-105 hover:-translate-y-2 relative overflow-hidden shadow-xl hover:shadow-2xl ${
                    selectedAnalysis === analysis.id 
                      ? 'border-orange-500 shadow-orange-500/50 bg-gradient-to-br from-orange-900/20 via-red-900/20 to-orange-900/20' 
                      : 'hover:border-gray-500'
                  }`}
                  onClick={() => handleAnalysisSelect(analysis.id)}
                >
                  {/* Background glow effect */}
                  <div className={`absolute top-0 right-0 w-24 h-24 rounded-full bg-gradient-to-br from-${analysis.color}-400 to-${analysis.color === 'orange' ? 'red' : analysis.color === 'blue' ? 'indigo' : analysis.color === 'green' ? 'emerald' : 'purple'}-500 opacity-10 -mr-12 -mt-12 animate-pulse`}></div>
                  
                  <div className="relative z-10">
                    <div className={`w-16 h-16 bg-gradient-to-br from-${analysis.color}-400 via-${analysis.color === 'orange' ? 'red' : analysis.color === 'blue' ? 'indigo' : analysis.color === 'green' ? 'emerald' : 'purple'}-500 to-${analysis.color === 'orange' ? 'red' : analysis.color === 'blue' ? 'indigo' : analysis.color === 'green' ? 'emerald' : 'purple'}-600 rounded-2xl flex items-center justify-center mb-6 shadow-lg hover:shadow-${analysis.color}-500/50 transition-all duration-300 transform hover:scale-110`}>
                      <i className="text-2xl text-white">
                        <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 512 512">
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
                    <h4 className="text-xl font-bold mb-3 text-gray-200">{analysis.title}</h4>
                    <p className="text-gray-300 text-sm mb-6 leading-relaxed">{analysis.description}</p>
                    <div className="space-y-2">
                      {analysis.features.map((feature, index) => (
                        <div key={index} className="flex items-center text-sm text-gray-300">
                          <span className="w-2 h-2 bg-gray-400 rounded-full mr-3"></span>
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

        {/* Enhanced Confirmation Section */}
        {showConfirmation && (
          <section className="py-16 px-6">
            <div className="max-w-3xl mx-auto text-center">
              <div className="bg-gradient-to-br from-gray-800 via-gray-700 to-gray-800 border-2 border-orange-500/30 rounded-3xl p-12 shadow-2xl">
                <div className="w-24 h-24 bg-gradient-to-br from-orange-400 via-red-500 to-orange-600 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-xl animate-pulse">
                  <i className="text-4xl text-white">
                    <svg className="w-12 h-12" fill="currentColor" viewBox="0 0 448 512">
                      <path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z" />
                    </svg>
                  </i>
                </div>
                <h3 className="text-3xl font-bold mb-6 bg-gradient-to-r from-gray-200 to-orange-300 bg-clip-text text-transparent">Analysis Initiated</h3>
                <p className="text-gray-300 text-lg mb-10 leading-relaxed">
                  {getAnalysisName(selectedAnalysis)} has been initiated and is now processing lunar surface data...
                </p>
                {error && (
                  <div className="mb-6 p-6 bg-gradient-to-r from-red-900 to-red-800 border-2 border-red-600 rounded-2xl">
                    <p className="text-red-200 font-semibold">{error}</p>
                  </div>
                )}
                <button 
                  onClick={handleStartAnalysis}
                  disabled={isAnalyzing}
                  className={`px-12 py-5 rounded-2xl font-bold text-lg transition-all duration-500 shadow-xl transform hover:scale-105 ${
                    isAnalyzing 
                      ? 'bg-gray-600 cursor-not-allowed shadow-gray-600/50' 
                      : 'bg-gradient-to-r from-orange-500 via-red-600 to-orange-700 hover:from-orange-600 hover:via-red-700 hover:to-orange-800 shadow-orange-500/50 hover:shadow-orange-500/75'
                  }`}
                >
                  {isAnalyzing ? (
                    <div className="flex items-center space-x-3">
                      <div className="w-6 h-6 border-3 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Analyzing...</span>
                    </div>
                  ) : (
                    <span className="flex items-center space-x-2">
                      <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 512 512">
                        <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                      </svg>
                      <span>Start Analysis</span>
                    </span>
                  )}
                </button>
              </div>
            </div>
          </section>
        )}

        {/* Enhanced Results Section */}
        {analysisResults && (
          <section className="py-20 px-6">
            <div className="max-w-7xl mx-auto">
              {/* Enhanced Success Header */}
              <div className="text-center mb-16">
                <div className="w-24 h-24 bg-gradient-to-br from-green-400 via-emerald-500 to-green-600 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-2xl animate-pulse">
                  <i className="text-4xl text-white">
                    <svg className="w-12 h-12" fill="currentColor" viewBox="0 0 448 512">
                      <path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z" />
                    </svg>
                  </i>
                </div>
                <h3 className="text-5xl font-bold mb-4 bg-gradient-to-r from-green-400 via-emerald-500 to-green-600 bg-clip-text text-transparent animate-pulse">
                  Analysis Complete!
                </h3>
                <p className="text-gray-300 text-2xl font-light">
                  Successfully detected <span className="text-green-400 font-bold">{analysisResults.totalObjects}</span> objects in the lunar surface
                </p>
                <div className="mt-8 flex justify-center space-x-4">
                  <div className="w-3 h-3 bg-green-400 rounded-full animate-bounce"></div>
                  <div className="w-3 h-3 bg-emerald-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-3 h-3 bg-green-600 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
              </div>

              {/* Enhanced Main Results Grid */}
              <div className="grid lg:grid-cols-3 gap-10 mb-12">
                {/* Enhanced Detection Visualization */}
                <div className="lg:col-span-2">
                  <div className="bg-gradient-to-br from-gray-800 via-gray-700 to-gray-800 border-2 border-gray-600 rounded-3xl p-8 shadow-2xl">
                    <h4 className="text-2xl font-bold mb-6 text-gray-200 flex items-center">
                      <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-xl flex items-center justify-center mr-3">
                        <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 512 512">
                          <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                        </svg>
                      </div>
                      Detection Visualization
                    </h4>
                    {analysisResults.visualizationImage ? (
                      <div className="relative group">
                        <img 
                          src={`http://localhost:5000${analysisResults.visualizationImage}`}
                          alt="Detection Visualization"
                          className="w-full rounded-2xl border-2 border-gray-600 shadow-2xl transition-all duration-500 transform group-hover:scale-[1.02] group-hover:shadow-3xl"
                        />
                        <div className="absolute top-6 right-6 bg-gradient-to-r from-blue-600 to-indigo-700 text-white px-4 py-2 rounded-xl text-sm font-semibold shadow-lg">
                          {analysisResults.totalObjects} Objects Detected
                        </div>
                        <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                      </div>
                    ) : (
                      <div className="bg-gradient-to-br from-gray-700 to-gray-800 rounded-2xl p-12 text-center border-2 border-dashed border-gray-600">
                        <div className="w-20 h-20 bg-gray-600 rounded-3xl flex items-center justify-center mx-auto mb-6">
                          <svg className="w-12 h-12 text-gray-500" fill="currentColor" viewBox="0 0 512 512">
                            <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                          </svg>
                        </div>
                        <p className="text-gray-400 text-lg font-medium">Visualization not available</p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Enhanced Statistics Cards */}
                <div className="space-y-8">
                  {/* Enhanced Detection Summary */}
                  <div className="bg-gradient-to-br from-blue-600 via-indigo-700 to-blue-800 rounded-3xl p-8 text-white shadow-2xl transform hover:scale-105 transition-all duration-300">
                    <h4 className="text-xl font-bold mb-6 flex items-center">
                      <div className="w-8 h-8 bg-white/20 rounded-xl flex items-center justify-center mr-3">
                        <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 512 512">
                          <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                        </svg>
                      </div>
                      Detection Summary
                    </h4>
                    <div className="space-y-4">
                      <div className="flex justify-between items-center p-3 bg-white/10 rounded-xl">
                        <span className="text-blue-100 font-medium">Total Objects:</span>
                        <span className="text-3xl font-bold text-white">{analysisResults.totalObjects}</span>
                      </div>
                      <div className="flex justify-between items-center p-3 bg-white/10 rounded-xl">
                        <span className="text-orange-200 font-medium">Boulders:</span>
                        <span className="text-2xl font-bold text-orange-300">{analysisResults.boulders}</span>
                      </div>
                      <div className="flex justify-between items-center p-3 bg-white/10 rounded-xl">
                        <span className="text-yellow-200 font-medium">Craters:</span>
                        <span className="text-2xl font-bold text-yellow-300">{analysisResults.craters}</span>
                      </div>
                    </div>
                  </div>

                  {/* Enhanced Analysis Metrics */}
                  <div className="bg-gradient-to-br from-purple-600 via-pink-700 to-purple-800 rounded-3xl p-8 text-white shadow-2xl transform hover:scale-105 transition-all duration-300">
                    <h4 className="text-xl font-bold mb-6 flex items-center">
                      <div className="w-8 h-8 bg-white/20 rounded-xl flex items-center justify-center mr-3">
                        <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 512 512">
                          <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                        </svg>
                      </div>
                      Analysis Metrics
                    </h4>
                    <div className="space-y-4">
                      <div className="flex justify-between items-center p-3 bg-white/10 rounded-xl">
                        <span className="text-purple-100 font-medium">Confidence:</span>
                        <span className="text-2xl font-bold text-purple-300">{(analysisResults.confidence * 100).toFixed(1)}%</span>
                      </div>
                      <div className="flex justify-between items-center p-3 bg-white/10 rounded-xl">
                        <span className="text-pink-100 font-medium">Avg Size:</span>
                        <span className="text-xl font-bold text-pink-300">{analysisResults.averageSize.toFixed(1)}m</span>
                      </div>
                      <div className="flex justify-between items-center p-3 bg-white/10 rounded-xl">
                        <span className="text-purple-100 font-medium">Density:</span>
                        <span className="text-lg font-bold text-purple-300">{analysisResults.density.toFixed(6)} obj/m²</span>
                      </div>
                    </div>
                  </div>

                  {/* Enhanced Processing Info */}
                  <div className="bg-gradient-to-br from-green-600 via-emerald-700 to-green-800 rounded-3xl p-8 text-white shadow-2xl transform hover:scale-105 transition-all duration-300">
                    <h4 className="text-xl font-bold mb-6 flex items-center">
                      <div className="w-8 h-8 bg-white/20 rounded-xl flex items-center justify-center mr-3">
                        <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 512 512">
                          <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                        </svg>
                      </div>
                      Processing Info
                    </h4>
                    <div className="space-y-4">
                      <div className="flex justify-between items-center p-3 bg-white/10 rounded-xl">
                        <span className="text-green-100 font-medium">Status:</span>
                        <span className="text-2xl font-bold text-green-300">Complete</span>
                      </div>
                      <div className="flex justify-between items-center p-3 bg-white/10 rounded-xl">
                        <span className="text-emerald-100 font-medium">Time:</span>
                        <span className="text-xl font-bold text-emerald-300">{analysisResults.processingTime}s</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Grad-CAM Visualization */}
              {analysisResults.gradcamImage && (
                <div className="mb-8">
                  <div className="bg-gray-800 border border-gray-700 rounded-2xl p-6">
                    <h4 className="text-xl font-semibold mb-4 text-gray-200 flex items-center">
                      <i className="mr-2">
                        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 512 512">
                          <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                        </svg>
                      </i>
                      Grad-CAM Visualization
                    </h4>
                    <img 
                      src={`http://localhost:5000${analysisResults.gradcamImage}`}
                      alt="Grad-CAM Visualization"
                      className="w-full rounded-xl border border-gray-600 shadow-2xl"
                    />
                  </div>
                </div>
              )}

              {/* Detailed Object Analysis */}
              {analysisResults.detectedObjects && analysisResults.detectedObjects.length > 0 && (
                <div className="mb-8">
                  <div className="bg-gray-800 border border-gray-700 rounded-2xl p-6">
                    <h4 className="text-xl font-semibold mb-6 text-gray-200 flex items-center">
                      <i className="mr-2">
                        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 512 512">
                          <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                        </svg>
                      </i>
                      Detailed Object Analysis
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {analysisResults.detectedObjects.map((obj, index) => (
                        <div key={index} className="bg-gradient-to-br from-gray-700 to-gray-800 rounded-xl p-4 border border-gray-600 hover:border-gray-500 transition-all duration-300">
                          <div className="flex justify-between items-center mb-3">
                            <span className="text-sm font-semibold text-gray-300 bg-gray-600 px-3 py-1 rounded-full">
                              {obj.class_name.charAt(0).toUpperCase() + obj.class_name.slice(1)} #{index + 1}
                            </span>
                            <span className="text-xs text-gray-400 bg-gray-600 px-2 py-1 rounded">
                              {(obj.confidence * 100).toFixed(1)}%
                            </span>
                          </div>
                          <div className="space-y-2 text-sm text-gray-300">
                            <div className="flex justify-between">
                              <span>Diameter:</span>
                              <span className="font-semibold text-orange-400">{obj.diameter_real.toFixed(2)}m</span>
                            </div>
                            <div className="flex justify-between">
                              <span>Area:</span>
                              <span className="font-semibold text-blue-400">{obj.area_real.toFixed(2)}m²</span>
                            </div>
                            <div className="flex justify-between">
                              <span>Volume:</span>
                              <span className="font-semibold text-green-400">{obj.volume_real.toFixed(2)}m³</span>
                            </div>
                            {obj.estimated_depth && (
                              <div className="flex justify-between">
                                <span>Depth:</span>
                                <span className="font-semibold text-purple-400">{obj.estimated_depth.toFixed(2)}m</span>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Enhanced Action Buttons */}
              <div className="flex justify-center space-x-8">
                <button 
                  onClick={handleProceed}
                  className="bg-gradient-to-r from-blue-500 via-indigo-600 to-blue-700 hover:from-blue-600 hover:via-indigo-700 hover:to-blue-800 px-12 py-5 rounded-2xl font-bold text-lg transition-all duration-500 transform hover:scale-110 hover:-translate-y-1 shadow-2xl hover:shadow-blue-500/50"
                >
                  <span className="flex items-center space-x-3">
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 512 512">
                      <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                    </svg>
                    <span>Back to Dashboard</span>
                  </span>
                </button>
                <button className="bg-gradient-to-r from-green-500 via-emerald-600 to-green-700 hover:from-green-600 hover:via-emerald-700 hover:to-green-800 px-12 py-5 rounded-2xl font-bold text-lg transition-all duration-500 transform hover:scale-110 hover:-translate-y-1 shadow-2xl hover:shadow-green-500/50">
                  <span className="flex items-center space-x-3">
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 512 512">
                      <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                    </svg>
                    <span>Export Results</span>
                  </span>
                </button>
              </div>
            </div>
          </section>
        )}
      </main>

      {/* Enhanced Footer */}
      <footer className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 border-t border-gray-700 py-12">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <div className="flex items-center justify-center space-x-4 mb-4">
            <div className="w-8 h-8 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 512 512">
                <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold bg-gradient-to-r from-orange-400 to-red-500 bg-clip-text text-transparent">
              LunaLens Boulder Detection
            </h3>
          </div>
          <p className="text-gray-300 text-lg font-light">© 2024 Advanced AI-powered lunar analysis</p>
        </div>
      </footer>
    </div>
  );
};

export default Boulder; 
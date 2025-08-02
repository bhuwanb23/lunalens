import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Header,
  HeroSection,
  ImageUpload,
  AnalysisSelection,
  ConfirmationSection,
  ResultsSection,
  Footer
} from './components';
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
      <Header />

      <main className="min-h-screen bg-gray-900">
        <HeroSection />

        <ImageUpload 
          uploadedImage={uploadedImage}
          handleImageUpload={handleImageUpload}
        />

        <AnalysisSelection 
          analysisTypes={analysisTypes}
          selectedAnalysis={selectedAnalysis}
          handleAnalysisSelect={handleAnalysisSelect}
        />

        <ConfirmationSection 
          showConfirmation={showConfirmation}
          selectedAnalysis={selectedAnalysis}
          getAnalysisName={getAnalysisName}
          error={error}
          isAnalyzing={isAnalyzing}
          handleStartAnalysis={handleStartAnalysis}
        />

        <ResultsSection 
          analysisResults={analysisResults}
          handleProceed={handleProceed}
        />
      </main>

      <Footer />
    </div>
  );
};

export default Boulder; 
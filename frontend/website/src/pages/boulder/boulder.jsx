import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  HeroSection,
  ImageUpload,
  AnalysisSelection,
  ConfirmationSection,
  ResultsSection,
  Footer
} from './components';
import { BOULDER_ANALYSIS_TYPES } from './constants';
import { apiUrl } from '../../config/api';
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
      const response = await fetch(apiUrl('/api/boulder/upload'), {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('lunalens_token')}`
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
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
      const response = await fetch(apiUrl('/api/boulder/analyze'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('lunalens_token')}`
        },
        body: JSON.stringify({
          filepath: filepath,
          analysisType: analysisType
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
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
        // Process results with comprehensive data
        const results = {
          // Basic counts
          totalObjects: analysisResult.analysis_summary?.total_objects || analysisResult.detected_objects.length,
          boulders: analysisResult.analysis_summary?.boulder_count || analysisResult.detected_objects.filter(obj => obj.class_name === 'boulder').length,
          
          // Analysis metrics
          density: analysisResult.density_analysis?.density || 0,
          averageSize: analysisResult.analysis_summary?.average_diameter || analysisResult.detected_objects.reduce((sum, obj) => sum + obj.diameter_real, 0) / analysisResult.detected_objects.length || 0,
          confidence: analysisResult.analysis_summary?.average_confidence || analysisResult.detected_objects.reduce((sum, obj) => sum + obj.confidence, 0) / analysisResult.detected_objects.length || 0,
          processingTime: analysisResult.analysis_summary?.processing_time || 2.4,
          
          // Comprehensive data
          detectedObjects: analysisResult.detected_objects,
          additionalFiles: analysisResult.additional_files || [],
          visualizationImage: analysisResult.additional_files?.find(file => file.type === 'visualization')?.path,
          gradcamImage: analysisResult.additional_files?.find(file => file.type === 'gradcam')?.path,
          
          // Analysis summary
          analysisSummary: analysisResult.analysis_summary || {},
          densityAnalysis: analysisResult.density_analysis || {},
          analysisType: analysisResult.analysis_type || selectedAnalysis,
          imageFilename: analysisResult.analysis_summary?.image_filename || 'Unknown'
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



  return (
    <div className="bg-gray-900 text-white overflow-x-hidden">
      <main className="min-h-screen bg-gray-900">
        <HeroSection />

        <ImageUpload 
          uploadedImage={uploadedImage}
          handleImageUpload={handleImageUpload}
        />

        <AnalysisSelection 
          analysisTypes={BOULDER_ANALYSIS_TYPES}
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
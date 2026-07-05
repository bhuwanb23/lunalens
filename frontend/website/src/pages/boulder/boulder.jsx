import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { BOULDER_ANALYSIS_TYPES } from './constants';
import { apiUrl } from '../../config/api';
import './boulder.css';

// Mock data for preview
const MOCK_RESULTS = {
  totalObjects: 12,
  boulders: 8,
  confidence: 0.87,
  processingTime: 2.4,
  imageFilename: 'lunar_surface_001.jpg',
  detectedObjects: [
    { confidence: 0.95, diameter_real: 2.4, area_real: 4.52, volume_real: 0.0032 },
    { confidence: 0.92, diameter_real: 1.8, area_real: 2.54, volume_real: 0.0018 },
    { confidence: 0.89, diameter_real: 3.1, area_real: 7.55, volume_real: 0.0054 },
    { confidence: 0.87, diameter_real: 1.2, area_real: 1.13, volume_real: 0.0008 },
    { confidence: 0.85, diameter_real: 2.8, area_real: 6.16, volume_real: 0.0044 },
    { confidence: 0.82, diameter_real: 1.5, area_real: 1.77, volume_real: 0.0013 },
    { confidence: 0.78, diameter_real: 2.1, area_real: 3.46, volume_real: 0.0025 },
    { confidence: 0.75, diameter_real: 1.9, area_real: 2.84, volume_real: 0.0020 },
  ],
};

const Boulder = () => {
  const [selectedAnalysis, setSelectedAnalysis] = useState('advanced');
  const [uploadedImage, setUploadedImage] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(MOCK_RESULTS);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const navigate = useNavigate();

  const handleImageUpload = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedFile(file);
      const reader = new FileReader();
      reader.onload = (e) => setUploadedImage(e.target.result);
      reader.readAsDataURL(file);
      setError(null);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith('image/')) {
      setUploadedFile(file);
      const reader = new FileReader();
      reader.onload = (ev) => setUploadedImage(ev.target.result);
      reader.readAsDataURL(file);
      setError(null);
    }
  };

  const uploadImage = async (file) => {
    const formData = new FormData();
    formData.append('image', file);
    const response = await fetch(apiUrl('/api/boulder/upload'), {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${localStorage.getItem('lunalens_token')}` },
      body: formData,
    });
    if (!response.ok) throw new Error('Upload failed');
    return response.json();
  };

  const analyzeImage = async (filepath, analysisType) => {
    const response = await fetch(apiUrl('/api/boulder/analyze'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('lunalens_token')}`,
      },
      body: JSON.stringify({ filepath, analysisType }),
    });
    if (!response.ok) throw new Error('Analysis failed');
    return response.json();
  };

  const handleStartAnalysis = async () => {
    if (!uploadedFile || !selectedAnalysis) {
      setError('Please upload an image and select an analysis type');
      return;
    }
    setIsAnalyzing(true);
    setError(null);
    try {
      const uploadResult = await uploadImage(uploadedFile);
      const analysisResult = await analyzeImage(uploadResult.filepath, selectedAnalysis);
      if (analysisResult.success) {
        setAnalysisResults({
          totalObjects: analysisResult.analysis_summary?.total_objects || analysisResult.detected_objects.length,
          boulders: analysisResult.analysis_summary?.boulder_count || analysisResult.detected_objects.filter(o => o.class_name === 'boulder').length,
          confidence: analysisResult.analysis_summary?.average_confidence || analysisResult.detected_objects.reduce((s, o) => s + o.confidence, 0) / analysisResult.detected_objects.length,
          processingTime: analysisResult.analysis_summary?.processing_time || 2.4,
          detectedObjects: analysisResult.detected_objects,
          visualizationImage: analysisResult.additional_files?.find(f => f.type === 'visualization')?.path,
          gradcamImage: analysisResult.additional_files?.find(f => f.type === 'gradcam')?.path,
          analysisType: selectedAnalysis,
          imageFilename: analysisResult.analysis_summary?.image_filename || 'Unknown',
        });
      } else {
        setError(analysisResult.message || 'Analysis failed');
      }
    } catch (err) {
      setError(err.message || 'An error occurred');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getAnalysisName = (type) => {
    const names = { basic: 'Basic Detection', advanced: 'Advanced Analysis', depth: 'Depth Estimation', gradcam: 'Grad-CAM Visualization' };
    return names[type] || 'Analysis';
  };

  return (
    <div style={{ backgroundColor: 'var(--bg-primary)', minHeight: '100vh' }}>
      <main className="pt-10 pb-12 px-4 sm:px-6 lg:px-8 max-w-[1400px] mx-auto">
        <div className="boulder-layout">

          {/* Sidebar */}
          <div className="boulder-sidebar space-y-6">
            {/* Upload Card */}
            <div className="boulder-card">
              <h3 className="text-[15px] font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
                Upload Image
              </h3>
              <div
                className={`upload-area ${dragOver ? 'dragover' : ''} ${uploadedImage ? 'has-image' : ''}`}
                onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                onDragLeave={() => setDragOver(false)}
                onDrop={handleDrop}
                onClick={() => document.getElementById('boulder-upload').click()}
              >
                {uploadedImage ? (
                  <img src={uploadedImage} alt="Uploaded" className="max-h-40 mx-auto rounded-lg" />
                ) : (
                  <>
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="mx-auto mb-3" style={{ color: 'var(--text-muted)' }}>
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                      <polyline points="17 8 12 3 7 8" />
                      <line x1="12" y1="3" x2="12" y2="15" />
                    </svg>
                    <p className="text-[13px] font-medium" style={{ color: 'var(--text-primary)' }}>Drop image here</p>
                    <p className="text-[12px] mt-1" style={{ color: 'var(--text-muted)' }}>or click to browse</p>
                  </>
                )}
              </div>
              <input id="boulder-upload" type="file" accept="image/*" className="hidden" onChange={handleImageUpload} />
            </div>

            {/* Analysis Type Card */}
            <div className="boulder-card">
              <h3 className="text-[15px] font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
                Analysis Type
              </h3>
              <div className="space-y-3">
                {Object.entries(BOULDER_ANALYSIS_TYPES).map(([key, type]) => (
                  <div
                    key={key}
                    className={`analysis-card ${selectedAnalysis === key ? 'selected' : ''}`}
                    onClick={() => setSelectedAnalysis(key)}
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ backgroundColor: type.color === 'blue' ? '#DBEAFE' : '#EDE9FE' }}>
                        <span className="text-[18px]">{type.icon}</span>
                      </div>
                      <div>
                        <div className="text-[13px] font-semibold" style={{ color: 'var(--text-primary)' }}>{type.name}</div>
                        <div className="text-[11px]" style={{ color: 'var(--text-muted)' }}>{type.accuracy}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Start Button */}
            <button
              className="btn-primary"
              onClick={handleStartAnalysis}
              disabled={!uploadedFile || !selectedAnalysis || isAnalyzing}
            >
              {isAnalyzing ? (
                <>
                  <svg className="animate-spin" width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Analyzing...
                </>
              ) : (
                <>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polygon points="5 3 19 12 5 21 5 3" />
                  </svg>
                  Start Analysis
                </>
              )}
            </button>

            {error && (
              <div className="p-3 rounded-lg text-[13px]" style={{ backgroundColor: '#FEF2F2', color: 'var(--accent-red)' }}>
                {error}
              </div>
            )}
          </div>

          {/* Main Content */}
          <div className="boulder-main">
            {analysisResults ? (
              <ResultsView results={analysisResults} onBack={() => setAnalysisResults(null)} />
            ) : (
              <EmptyState />
            )}
          </div>

        </div>
      </main>
    </div>
  );
};

/* Empty State */
const EmptyState = () => (
  <div className="boulder-card flex flex-col items-center justify-center py-24">
    <div className="w-16 h-16 rounded-full flex items-center justify-center mb-4" style={{ backgroundColor: '#FFF7ED' }}>
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" style={{ color: 'var(--accent-orange)' }}>
        <circle cx="12" cy="12" r="10" />
        <path d="M12 6v6l4 2" />
      </svg>
    </div>
    <h3 className="text-[17px] font-bold mb-2" style={{ color: 'var(--text-primary)' }}>No Analysis Results</h3>
    <p className="text-[13px] text-center max-w-sm" style={{ color: 'var(--text-secondary)' }}>
      Upload a lunar surface image and select an analysis type to begin boulder detection.
    </p>
  </div>
);

/* Results View */
const ResultsView = ({ results, onBack }) => (
  <div className="space-y-6">
    {/* Header */}
    <div className="boulder-card">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-[18px] font-bold" style={{ color: 'var(--text-primary)' }}>Analysis Complete</h2>
          <p className="text-[13px]" style={{ color: 'var(--text-secondary)' }}>{results.imageFilename}</p>
        </div>
        <button className="btn-secondary" onClick={onBack}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="19" y1="12" x2="5" y2="12" />
            <polyline points="12 19 5 12 12 5" />
          </svg>
          New Analysis
        </button>
      </div>
    </div>

    {/* Stats Grid */}
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div className="stat-card">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-2 h-2 rounded-full" style={{ backgroundColor: 'var(--accent-blue)' }} />
          <span className="text-[12px] font-medium" style={{ color: 'var(--text-secondary)' }}>Total Objects</span>
        </div>
        <div className="text-[24px] font-bold" style={{ color: 'var(--text-primary)' }}>{results.totalObjects}</div>
      </div>
      <div className="stat-card">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-2 h-2 rounded-full" style={{ backgroundColor: 'var(--accent-orange)' }} />
          <span className="text-[12px] font-medium" style={{ color: 'var(--text-secondary)' }}>Boulders</span>
        </div>
        <div className="text-[24px] font-bold" style={{ color: 'var(--text-primary)' }}>{results.boulders}</div>
      </div>
      <div className="stat-card">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-2 h-2 rounded-full" style={{ backgroundColor: 'var(--accent-green)' }} />
          <span className="text-[12px] font-medium" style={{ color: 'var(--text-secondary)' }}>Confidence</span>
        </div>
        <div className="text-[24px] font-bold" style={{ color: 'var(--text-primary)' }}>{(results.confidence * 100).toFixed(0)}%</div>
      </div>
      <div className="stat-card">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-2 h-2 rounded-full" style={{ backgroundColor: 'var(--accent-purple)' }} />
          <span className="text-[12px] font-medium" style={{ color: 'var(--text-secondary)' }}>Time</span>
        </div>
        <div className="text-[24px] font-bold" style={{ color: 'var(--text-primary)' }}>{results.processingTime}s</div>
      </div>
    </div>

    {/* Detection Image */}
    {results.visualizationImage && (
      <div className="boulder-card">
        <h3 className="text-[15px] font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>Detection Visualization</h3>
        <img
          src={apiUrl(results.visualizationImage)}
          alt="Detection"
          className="w-full rounded-lg"
          style={{ border: '1px solid var(--border)' }}
        />
      </div>
    )}

    {/* Objects Table */}
    {results.detectedObjects?.length > 0 && (
      <div className="boulder-card">
        <h3 className="text-[15px] font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
          Detected Objects ({results.detectedObjects.length})
        </h3>
        <div className="overflow-x-auto">
          <table className="boulder-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Confidence</th>
                <th>Diameter (m)</th>
                <th>Area (m²)</th>
                <th>Volume (m³)</th>
              </tr>
            </thead>
            <tbody>
              {results.detectedObjects.map((obj, i) => (
                <tr key={i}>
                  <td className="font-medium">Object {i + 1}</td>
                  <td>{(obj.confidence * 100).toFixed(1)}%</td>
                  <td>{obj.diameter_real?.toFixed(2) || 'N/A'}</td>
                  <td>{obj.area_real?.toFixed(2) || 'N/A'}</td>
                  <td>{obj.volume_real?.toFixed(4) || 'N/A'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    )}
  </div>
);

export default Boulder;

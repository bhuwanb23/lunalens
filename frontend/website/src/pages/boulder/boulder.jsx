import { useState, useEffect } from 'react';
import { BOULDER_ANALYSIS_TYPES } from './constants';
import { apiUrl } from '../../config/api';
import './boulder.css';

const Boulder = () => {
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [animated, setAnimated] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setAnimated(true), 100);
    return () => clearTimeout(timer);
  }, []);

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
              <ResultsView results={analysisResults} onBack={() => setAnalysisResults(null)} animated={animated} />
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

/* Donut Chart Component */
const DonutChart = ({ value, max, color, size = 120, label, animated }) => {
  const radius = (size - 16) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = animated ? (value / max) * circumference : 0;

  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle cx={size/2} cy={size/2} r={radius} fill="none" stroke="#E5E7EB" strokeWidth="8" />
        <circle
          cx={size/2} cy={size/2} r={radius} fill="none"
          stroke={color} strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={circumference - progress}
          strokeLinecap="round"
          transform={`rotate(-90 ${size/2} ${size/2})`}
          style={{ transition: 'stroke-dashoffset 1s cubic-bezier(0.4, 0, 0.2, 1)' }}
        />
        <text x={size/2} y={size/2 - 8} textAnchor="middle" fontSize="24" fontWeight="700" fill="#1A1D26">{animated ? value : 0}</text>
        <text x={size/2} y={size/2 + 12} textAnchor="middle" fontSize="11" fill="#6B7280">{label}</text>
      </svg>
    </div>
  );
};

/* Bar Chart Component */
const BarChart = ({ data, maxValue, animated }) => (
  <div className="space-y-3">
    {data.map((item, i) => (
      <div key={i} className="group">
        <div className="flex items-center justify-between mb-1">
          <span className="text-[11px] font-medium" style={{ color: 'var(--text-secondary)' }}>{item.label}</span>
          <span className="text-[12px] font-semibold" style={{ color: 'var(--text-primary)' }}>{item.value}</span>
        </div>
        <div className="h-3 rounded-full overflow-hidden" style={{ backgroundColor: 'var(--bg-primary)' }}>
          <div
            className="h-full rounded-full transition-all duration-1000 ease-out group-hover:brightness-110"
            style={{
              width: animated ? `${(item.value / maxValue) * 100}%` : '0%',
              backgroundColor: item.color,
              transitionDelay: `${i * 150}ms`,
            }}
          />
        </div>
      </div>
    ))}
  </div>
);

/* Confidence Ring */
const ConfidenceRing = ({ confidence, size = 48, animated }) => {
  const radius = (size - 8) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = animated ? circumference - (confidence * circumference) : circumference;
  const color = confidence >= 0.9 ? '#10B981' : confidence >= 0.8 ? '#F59E0B' : '#EF4444';

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="transition-transform duration-200 hover:scale-110">
      <circle cx={size/2} cy={size/2} r={radius} fill="none" stroke="#E5E7EB" strokeWidth="4" />
      <circle cx={size/2} cy={size/2} r={radius} fill="none" stroke={color} strokeWidth="4"
        strokeDasharray={circumference} strokeDashoffset={offset} strokeLinecap="round"
        transform={`rotate(-90 ${size/2} ${size/2})`}
        style={{ transition: 'stroke-dashoffset 1s cubic-bezier(0.4, 0, 0.2, 1)' }} />
      <text x={size/2} y={size/2 + 4} textAnchor="middle" fontSize="10" fontWeight="600" fill="#1A1D26">
        {animated ? (confidence * 100).toFixed(0) : 0}
      </text>
    </svg>
  );
};

/* Results View */
const ResultsView = ({ results, onBack, animated }) => {
  const boulderPct = ((results.boulders / results.totalObjects) * 100).toFixed(0);
  const otherPct = (100 - boulderPct).toFixed(0);
  const avgDiameter = (results.detectedObjects.reduce((s, o) => s + (o.diameter_real || 0), 0) / results.detectedObjects.length).toFixed(2);
  const totalArea = results.detectedObjects.reduce((s, o) => s + (o.area_real || 0), 0).toFixed(2);

  const sizeDistribution = [
    { label: 'Small', value: results.detectedObjects.filter(o => o.diameter_real < 2).length, color: '#3B82F6' },
    { label: 'Medium', value: results.detectedObjects.filter(o => o.diameter_real >= 2 && o.diameter_real < 3).length, color: '#F59E0B' },
    { label: 'Large', value: results.detectedObjects.filter(o => o.diameter_real >= 3).length, color: '#EF4444' },
  ];

  return (
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
            <span className="text-[12px] font-medium" style={{ color: 'var(--text-secondary)' }}>Avg Confidence</span>
          </div>
          <div className="text-[24px] font-bold" style={{ color: 'var(--text-primary)' }}>{(results.confidence * 100).toFixed(0)}%</div>
        </div>
        <div className="stat-card">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: 'var(--accent-purple)' }} />
            <span className="text-[12px] font-medium" style={{ color: 'var(--text-secondary)' }}>Total Area</span>
          </div>
          <div className="text-[24px] font-bold" style={{ color: 'var(--text-primary)' }}>{totalArea}m²</div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Donut Chart - Distribution */}
        <div className="boulder-card">
          <h3 className="text-[14px] font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>Object Distribution</h3>
          <div className="flex items-center justify-center gap-6">
            <DonutChart value={results.boulders} max={results.totalObjects} color="#F97316" label="Boulders" animated={animated} />
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#F97316' }} />
                <span className="text-[12px]" style={{ color: 'var(--text-secondary)' }}>Boulders: {boulderPct}%</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#3B82F6' }} />
                <span className="text-[12px]" style={{ color: 'var(--text-secondary)' }}>Other: {otherPct}%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Bar Chart - Size Distribution */}
        <div className="boulder-card">
          <h3 className="text-[14px] font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>Size Distribution</h3>
          <BarChart data={sizeDistribution} maxValue={Math.max(...sizeDistribution.map(d => d.value))} animated={animated} />
        </div>

        {/* Confidence Overview */}
        <div className="boulder-card">
          <h3 className="text-[14px] font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>Confidence Overview</h3>
          <div className="flex items-center justify-center">
            <DonutChart value={Math.round(results.confidence * 100)} max={100} color="#10B981" size={100} label="Avg %" animated={animated} />
          </div>
          <div className="text-center mt-3">
            <span className="text-[12px]" style={{ color: 'var(--text-secondary)' }}>
              Avg Diameter: {avgDiameter}m
            </span>
          </div>
        </div>
      </div>

      {/* Objects Table with Confidence Rings */}
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
                    <td>
                      <div className="flex items-center gap-2">
                        <ConfidenceRing confidence={obj.confidence} animated={animated} />
                        <span className="text-[12px]" style={{ color: 'var(--text-secondary)' }}>
                          {(obj.confidence * 100).toFixed(1)}%
                        </span>
                      </div>
                    </td>
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
};

export default Boulder;

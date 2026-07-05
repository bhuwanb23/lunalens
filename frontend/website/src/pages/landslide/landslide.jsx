import { useState, useEffect } from 'react';
import { apiUrl } from '../../config/api';

function mapBackendResultsToAnalysisData(results) {
  const slopeJson = results['slope_analysis_results.json'];
  const slopeStats = slopeJson?.statistics || {};
  const slope = slopeJson ? {
    riskLevel: slopeJson.analysis_results?.risk_level || 'N/A',
    riskFactors: slopeJson.analysis_results?.risk_factors || [],
    statistics: {
      min: slopeStats.min_value ?? slopeStats.min ?? 0,
      max: slopeStats.max_value ?? slopeStats.max ?? 0,
      mean: slopeStats.mean_value ?? slopeStats.mean ?? 0,
      stdDev: slopeStats.std_dev ?? slopeStats.std ?? 0,
    },
  } : undefined;

  const elevJson = results['elevation_statistics_results.json'];
  const elevation = elevJson ? {
    statistics: {
      min: elevJson.min_elevation,
      max: elevJson.max_elevation,
      mean: elevJson.mean_elevation,
      stdDev: elevJson.std_elevation,
    },
  } : undefined;

  const curvJson = results['curvature_statistics_results.json'];
  const curvature = curvJson ? {
    statistics: {
      profileMean: curvJson.profile_mean,
      planMean: curvJson.plan_mean,
      gaussianMean: curvJson.gaussian_mean,
    },
  } : undefined;

  const triJson = results['terrain_ruggedness_pipeline_summary.json'];
  let triStats = triJson?.results?.ruggedness_analysis || triJson?.calculation_results?.ruggedness_analysis;
  const roughness = triStats ? {
    riskLevel: triStats.category || 'N/A',
    statistics: { min: triStats.min_tri, max: triStats.max_tri, mean: triStats.mean_tri },
  } : undefined;

  const riskJson = results['lunar_risk_analysis_results.json'];
  const composite = riskJson ? {
    overallRisk: { score: riskJson.composite_risk_score, level: riskJson.risk_level },
    components: Object.entries(riskJson.individual_risk_scores || {}).map(([name, score]) => ({
      name: name.toUpperCase(), riskScore: score,
    })),
  } : undefined;

  return { slope, elevation, curvature, roughness, composite };
}

const LandslideDetection = () => {
  const [image, setImage] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [animated, setAnimated] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setAnimated(true), 100);
    return () => clearTimeout(timer);
  }, []);

  const handleFile = (file) => {
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setImage({ name: file.name, path: e.target.result, size: file.size });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleImageUpload = (e) => handleFile(e.target.files?.[0]);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleFile(e.dataTransfer.files?.[0]);
  };

  const startAnalysis = async () => {
    if (!image) return;
    setIsAnalyzing(true);
    setError(null);
    setShowResults(false);
    try {
      const response = await fetch(apiUrl('/api/lunar-analysis'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('lunalens_token')}`,
        },
        body: JSON.stringify({ dem_path: image.path }),
      });
      if (!response.ok) throw new Error('Analysis failed');
      const data = await response.json();
      if (data.success) {
        setAnalysisData(mapBackendResultsToAnalysisData(data.results));
        setShowResults(true);
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch {
      setError('Error connecting to backend');
    }
    setIsAnalyzing(false);
  };

  return (
    <div style={{ backgroundColor: '#F5F7FA', minHeight: '100vh' }}>
      <style>{`
        .ll-card { background: #FFF; border: 1px solid #E5E7EB; border-radius: 16px; padding: 20px; }
        .ll-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
        .ll-upload { border: 2px dashed #E5E7EB; border-radius: 16px; padding: 32px; text-align: center; cursor: pointer; transition: all 0.2s; background: #F5F7FA; }
        .ll-upload:hover { border-color: #3B82F6; background: #EFF6FF; }
        .ll-upload.has-file { border-style: solid; border-color: #10B981; background: #ECFDF5; padding: 16px; }
        .ll-btn { display: flex; align-items: center; justify-content: center; gap: 8px; width: 100%; padding: 12px; background: #3B82F6; color: #FFF; border: none; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
        .ll-btn:hover { background: #2563EB; transform: translateY(-1px); }
        .ll-btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        .ll-stat { background: #FFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 16px; }
        .ll-table { width: 100%; border-collapse: separate; border-spacing: 0; }
        .ll-table th { padding: 10px 14px; text-align: left; font-size: 11px; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #E5E7EB; background: #F5F7FA; }
        .ll-table td { padding: 10px 14px; font-size: 13px; color: #1A1D26; border-bottom: 1px solid #E5E7EB; }
        .ll-table tr:hover td { background: #F5F7FA; }
        .ll-badge { display: inline-flex; align-items: center; gap: 4px; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; }
        .ll-badge.high { background: #FEF2F2; color: #DC2626; }
        .ll-badge.medium { background: #FFFBEB; color: #D97706; }
        .ll-badge.low { background: #ECFDF5; color: #059669; }
      `}</style>

      <main className="pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-[1400px] mx-auto">
        <div className="flex flex-col lg:flex-row gap-6">

          {/* Sidebar */}
          <div className="w-full lg:w-[320px] flex-shrink-0 space-y-6">
            {/* Upload Card */}
            <div className="ll-card">
              <h3 style={{ fontSize: 15, fontWeight: 600, color: '#1A1D26', marginBottom: 16 }}>Upload DEM</h3>
              <div
                className={`ll-upload ${dragOver ? 'dragover' : ''} ${image ? 'has-file' : ''}`}
                onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                onDragLeave={() => setDragOver(false)}
                onDrop={handleDrop}
                onClick={() => document.getElementById('landslide-upload').click()}
              >
                {image ? (
                  <div style={{ fontSize: 13, fontWeight: 500, color: '#059669' }}>{image.name}</div>
                ) : (
                  <>
                    <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" strokeWidth="1.5" style={{ margin: '0 auto 12px' }}>
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                      <polyline points="17 8 12 3 7 8" />
                      <line x1="12" y1="3" x2="12" y2="15" />
                    </svg>
                    <div style={{ fontSize: 13, fontWeight: 500, color: '#1A1D26' }}>Drop DEM file here</div>
                    <div style={{ fontSize: 12, color: '#9CA3AF', marginTop: 4 }}>or click to browse</div>
                  </>
                )}
              </div>
              <input id="landslide-upload" type="file" accept=".tif,.tiff,.dem,.img" className="hidden" onChange={handleImageUpload} />
            </div>

            {/* Start Button */}
            <button className="ll-btn" onClick={startAnalysis} disabled={!image || isAnalyzing}>
              {isAnalyzing ? (
                <>
                  <svg className="animate-spin" width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Analyzing...
                </>
              ) : 'Start Analysis'}
            </button>

            {error && (
              <div style={{ padding: 12, borderRadius: 10, fontSize: 13, background: '#FEF2F2', color: '#DC2626' }}>{error}</div>
            )}

            {/* Risk Breakdown */}
            {showResults && analysisData?.composite && (
              <div className="ll-card">
                <h3 style={{ fontSize: 15, fontWeight: 600, color: '#1A1D26', marginBottom: 12 }}>Risk Breakdown</h3>
                <div style={{ fontSize: 28, fontWeight: 700, color: '#1A1D26', marginBottom: 4 }}>
                  {analysisData.composite.overallRisk.score || 'N/A'}
                </div>
                <span className={`ll-badge ${(analysisData.composite.overallRisk.level || '').toLowerCase()}`}>
                  {analysisData.composite.overallRisk.level || 'N/A'} Risk
                </span>
                <div style={{ marginTop: 16 }}>
                  {analysisData.composite.components.map((c, i) => (
                    <div key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #E5E7EB', fontSize: 13 }}>
                      <span style={{ color: '#6B7280' }}>{c.name}</span>
                      <span style={{ fontWeight: 600, color: '#1A1D26' }}>{c.riskScore?.toFixed(1)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Main Content */}
          <div className="flex-1 min-w-0">
            {showResults && analysisData ? (
              <div className="space-y-6">
                {/* Header */}
                <div className="ll-card">
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <div>
                      <h2 style={{ fontSize: 18, fontWeight: 700, color: '#1A1D26' }}>Analysis Complete</h2>
                      <p style={{ fontSize: 13, color: '#6B7280' }}>Lunar terrain risk assessment</p>
                    </div>
                    <button onClick={() => { setShowResults(false); setAnalysisData(null); setImage(null); }}
                      style={{ padding: '8px 14px', background: '#FFF', border: '1px solid #E5E7EB', borderRadius: 8, fontSize: 13, fontWeight: 500, cursor: 'pointer', color: '#1A1D26' }}>
                      New Analysis
                    </button>
                  </div>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                  {[
                    { label: 'Risk Level', value: analysisData.composite?.overallRisk?.level || 'N/A', color: '#EF4444' },
                    { label: 'Risk Score', value: analysisData.composite?.overallRisk?.score || 'N/A', color: '#F59E0B' },
                    { label: 'Slope Mean', value: `${analysisData.slope?.statistics?.mean?.toFixed(1) || 'N/A'}°`, color: '#3B82F6' },
                    { label: 'Elevation Range', value: `${analysisData.elevation?.statistics?.min?.toFixed(0) || 0}-${analysisData.elevation?.statistics?.max?.toFixed(0) || 0}m`, color: '#10B981' },
                  ].map((s, i) => (
                    <div key={i} className="ll-stat">
                      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 8 }}>
                        <div style={{ width: 8, height: 8, borderRadius: '50%', background: s.color }} />
                        <span style={{ fontSize: 12, fontWeight: 500, color: '#6B7280' }}>{s.label}</span>
                      </div>
                      <div style={{ fontSize: 24, fontWeight: 700, color: '#1A1D26' }}>{s.value}</div>
                    </div>
                  ))}
                </div>

                {/* Risk Gauge + Charts Row */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Risk Gauge */}
                  <div className="ll-card">
                    <h3 style={{ fontSize: 14, fontWeight: 600, color: '#1A1D26', marginBottom: 16 }}>Risk Score</h3>
                    <div style={{ display: 'flex', justifyContent: 'center' }}>
                      <svg width="140" height="100" viewBox="0 0 140 100">
                        <path d="M 10 90 A 60 60 0 0 1 130 90" fill="none" stroke="#E5E7EB" strokeWidth="12" strokeLinecap="round" />
                        <path d="M 10 90 A 60 60 0 0 1 130 90" fill="none" stroke={analysisData.composite?.overallRisk?.score > 70 ? '#EF4444' : analysisData.composite?.overallRisk?.score > 40 ? '#F59E0B' : '#10B981'} strokeWidth="12" strokeLinecap="round"
                          strokeDasharray="188" strokeDashoffset={animated ? 188 - (analysisData.composite?.overallRisk?.score / 100) * 188 : 188}
                          style={{ transition: 'stroke-dashoffset 1.2s cubic-bezier(0.4, 0, 0.2, 1)' }} />
                        <text x="70" y="75" textAnchor="middle" fontSize="28" fontWeight="700" fill="#1A1D26">{animated ? analysisData.composite?.overallRisk?.score : 0}</text>
                        <text x="70" y="92" textAnchor="middle" fontSize="10" fill="#6B7280">out of 100</text>
                      </svg>
                    </div>
                    <div style={{ textAlign: 'center', marginTop: 8 }}>
                      <span className={`ll-badge ${(analysisData.composite?.overallRisk?.level || '').toLowerCase()}`}>
                        {analysisData.composite?.overallRisk?.level || 'N/A'} Risk
                      </span>
                    </div>
                  </div>

                  {/* Risk Components Bar Chart */}
                  <div className="ll-card lg:col-span-2">
                    <h3 style={{ fontSize: 14, fontWeight: 600, color: '#1A1D26', marginBottom: 16 }}>Risk Components</h3>
                    <div className="space-y-4">
                      {analysisData.composite?.components?.map((c, i) => {
                        const colors = ['#EF4444', '#F59E0B', '#3B82F6', '#8B5CF6'];
                        return (
                          <div key={i} className="group" style={{ cursor: 'default' }}>
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6 }}>
                              <span style={{ fontSize: 12, fontWeight: 500, color: '#6B7280' }}>{c.name}</span>
                              <span style={{ fontSize: 13, fontWeight: 600, color: '#1A1D26' }}>{c.riskScore?.toFixed(1)}</span>
                            </div>
                            <div style={{ height: 10, background: '#F5F7FA', borderRadius: 5, overflow: 'hidden' }}>
                              <div style={{
                                width: animated ? `${c.riskScore}%` : '0%',
                                height: '100%',
                                background: colors[i % colors.length],
                                borderRadius: 5,
                                transition: 'width 1s cubic-bezier(0.4, 0, 0.2, 1)',
                                transitionDelay: `${i * 150}ms`,
                              }} />
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>

                {/* Terrain Profile Chart */}
                <div className="ll-card">
                  <h3 style={{ fontSize: 14, fontWeight: 600, color: '#1A1D26', marginBottom: 16 }}>Terrain Profile</h3>
                  <svg width="100%" height="120" viewBox="0 0 500 120" preserveAspectRatio="none">
                    <defs>
                      <linearGradient id="terrainGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stopColor="#3B82F6" stopOpacity="0.3" />
                        <stop offset="100%" stopColor="#3B82F6" stopOpacity="0.05" />
                      </linearGradient>
                    </defs>
                    <path d="M0,100 Q50,80 100,85 T200,60 T300,75 T400,40 T500,50 V120 H0 Z" fill="url(#terrainGrad)"
                      style={{ opacity: animated ? 1 : 0, transition: 'opacity 0.8s ease 0.5s' }} />
                    <path d="M0,100 Q50,80 100,85 T200,60 T300,75 T400,40 T500,50" fill="none" stroke="#3B82F6" strokeWidth="2.5"
                      strokeDasharray="700" strokeDashoffset={animated ? 0 : 700}
                      style={{ transition: 'stroke-dashoffset 1.5s cubic-bezier(0.4, 0, 0.2, 1)' }} />
                    {[0, 100, 200, 300, 400, 500].map((x, i) => (
                      <g key={i} style={{ opacity: animated ? 1 : 0, transition: `opacity 0.5s ease ${0.3 + i * 0.1}s` }}>
                        <line x1={x} y1="0" x2={x} y2="120" stroke="#E5E7EB" strokeWidth="1" strokeDasharray="4" />
                        <text x={x} y="115" textAnchor="middle" fontSize="9" fill="#9CA3AF">{['0m', '200m', '400m', '600m', '800m', '1000m'][i]}</text>
                      </g>
                    ))}
                  </svg>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8, fontSize: 11, color: '#6B7280' }}>
                    <span>Elevation Range: {analysisData.elevation?.statistics?.min?.toFixed(0)}m - {analysisData.elevation?.statistics?.max?.toFixed(0)}m</span>
                    <span>Mean: {analysisData.elevation?.statistics?.mean?.toFixed(0)}m</span>
                  </div>
                </div>

                {/* Analysis Tables */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Slope Analysis */}
                  {analysisData.slope && (
                    <div className="ll-card">
                      <h3 style={{ fontSize: 15, fontWeight: 600, color: '#1A1D26', marginBottom: 12 }}>Slope Analysis</h3>
                      <table className="ll-table">
                        <thead><tr><th>Parameter</th><th>Value</th></tr></thead>
                        <tbody>
                          <tr><td>Min</td><td>{analysisData.slope.statistics.min?.toFixed(2)}°</td></tr>
                          <tr><td>Max</td><td>{analysisData.slope.statistics.max?.toFixed(2)}°</td></tr>
                          <tr><td>Mean</td><td>{analysisData.slope.statistics.mean?.toFixed(2)}°</td></tr>
                          <tr><td>Std Dev</td><td>{analysisData.slope.statistics.stdDev?.toFixed(2)}</td></tr>
                        </tbody>
                      </table>
                    </div>
                  )}

                  {/* Elevation Analysis */}
                  {analysisData.elevation && (
                    <div className="ll-card">
                      <h3 style={{ fontSize: 15, fontWeight: 600, color: '#1A1D26', marginBottom: 12 }}>Elevation Analysis</h3>
                      <table className="ll-table">
                        <thead><tr><th>Parameter</th><th>Value</th></tr></thead>
                        <tbody>
                          <tr><td>Min</td><td>{analysisData.elevation.statistics.min?.toFixed(2)}m</td></tr>
                          <tr><td>Max</td><td>{analysisData.elevation.statistics.max?.toFixed(2)}m</td></tr>
                          <tr><td>Mean</td><td>{analysisData.elevation.statistics.mean?.toFixed(2)}m</td></tr>
                          <tr><td>Std Dev</td><td>{analysisData.elevation.statistics.stdDev?.toFixed(2)}</td></tr>
                        </tbody>
                      </table>
                    </div>
                  )}

                  {/* Curvature Analysis */}
                  {analysisData.curvature && (
                    <div className="ll-card">
                      <h3 style={{ fontSize: 15, fontWeight: 600, color: '#1A1D26', marginBottom: 12 }}>Curvature Analysis</h3>
                      <table className="ll-table">
                        <thead><tr><th>Parameter</th><th>Value</th></tr></thead>
                        <tbody>
                          <tr><td>Profile Mean</td><td>{analysisData.curvature.statistics.profileMean?.toFixed(4)}</td></tr>
                          <tr><td>Plan Mean</td><td>{analysisData.curvature.statistics.planMean?.toFixed(4)}</td></tr>
                          <tr><td>Gaussian Mean</td><td>{analysisData.curvature.statistics.gaussianMean?.toFixed(4)}</td></tr>
                        </tbody>
                      </table>
                    </div>
                  )}

                  {/* Roughness Analysis */}
                  {analysisData.roughness && (
                    <div className="ll-card">
                      <h3 style={{ fontSize: 15, fontWeight: 600, color: '#1A1D26', marginBottom: 12 }}>Terrain Roughness</h3>
                      <table className="ll-table">
                        <thead><tr><th>Parameter</th><th>Value</th></tr></thead>
                        <tbody>
                          <tr><td>Min TRI</td><td>{analysisData.roughness.statistics.min?.toFixed(4)}</td></tr>
                          <tr><td>Max TRI</td><td>{analysisData.roughness.statistics.max?.toFixed(4)}</td></tr>
                          <tr><td>Mean TRI</td><td>{analysisData.roughness.statistics.mean?.toFixed(4)}</td></tr>
                          <tr><td>Category</td><td><span className={`ll-badge ${(analysisData.roughness.riskLevel || '').toLowerCase()}`}>{analysisData.roughness.riskLevel}</span></td></tr>
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              /* Empty State */
              <div className="ll-card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '80px 20px' }}>
                <div style={{ width: 64, height: 64, borderRadius: '50%', background: '#EFF6FF', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: 16 }}>
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" strokeWidth="1.5">
                    <path d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                <h3 style={{ fontSize: 17, fontWeight: 700, color: '#1A1D26', marginBottom: 8 }}>No Analysis Results</h3>
                <p style={{ fontSize: 13, color: '#6B7280', textAlign: 'center', maxWidth: 320 }}>
                  Upload a Digital Elevation Model to begin lunar terrain analysis and risk assessment.
                </p>
              </div>
            )}
          </div>

        </div>
      </main>
    </div>
  );
};

export default LandslideDetection;

import { useState, useMemo } from 'react';
import { MOCK_ANALYSIS_RECORDS, ANALYSIS_TYPES } from './constants';
import './analytics.css';

const Analytics = () => {
  const [records] = useState(MOCK_ANALYSIS_RECORDS);
  const [activeTab, setActiveTab] = useState('all');
  const [search, setSearch] = useState('');
  const [selectedIds, setSelectedIds] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 6;

  // Filter records
  const filteredRecords = useMemo(() => {
    let filtered = [...records];

    if (activeTab !== 'all') {
      filtered = filtered.filter(r => r.analysisType === activeTab);
    }

    if (search) {
      const term = search.toLowerCase();
      filtered = filtered.filter(r =>
        r.imageName.toLowerCase().includes(term) ||
        r.user.toLowerCase().includes(term)
      );
    }

    return filtered;
  }, [records, activeTab, search]);

  // Pagination
  const totalPages = Math.ceil(filteredRecords.length / itemsPerPage);
  const paginatedRecords = filteredRecords.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  // Stats
  const stats = {
    total: records.length,
    pending: records.filter(r => r.status === 'pending' || r.status === 'processing').length,
    completed: records.filter(r => r.status === 'completed').length,
    failed: records.filter(r => r.status === 'failed').length,
  };

  // Tab counts
  const tabCounts = {
    all: records.length,
    basic: records.filter(r => r.analysisType === 'basic').length,
    advanced: records.filter(r => r.analysisType === 'advanced').length,
    depth: records.filter(r => r.analysisType === 'depth').length,
    gradcam: records.filter(r => r.analysisType === 'gradcam').length,
  };

  const toggleSelectAll = () => {
    if (selectedIds.length === paginatedRecords.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(paginatedRecords.map(r => r.id));
    }
  };

  const toggleSelect = (id) => {
    setSelectedIds(prev =>
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    );
  };

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' });
  };

  const tabs = ['all', 'basic', 'advanced', 'depth', 'gradcam'];

  return (
    <div style={{ backgroundColor: 'var(--bg-primary)', minHeight: '100vh' }}>
      <main className="pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-[1400px] mx-auto">

        {/* Page Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
          <div>
            <h1 className="text-[22px] font-bold" style={{ color: 'var(--text-primary)' }}>
              Analytics
            </h1>
            <p className="text-[14px]" style={{ color: 'var(--text-secondary)' }}>
              Boulder detection analysis records and performance metrics
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="search-input">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ color: 'var(--text-muted)' }}>
                <circle cx="11" cy="11" r="8" />
                <path d="m21 21-4.35-4.35" />
              </svg>
              <input
                type="text"
                placeholder="Search anything..."
                value={search}
                onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }}
              />
            </div>
            <button className="btn-secondary">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="7 10 12 15 17 10" />
                <line x1="12" y1="15" x2="12" y2="3" />
              </svg>
              Export
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="stat-card">
            <div className="flex items-center gap-2 mb-2">
              <div className="stat-dot" style={{ backgroundColor: 'var(--accent-blue)' }} />
              <span className="text-[13px] font-medium" style={{ color: 'var(--text-secondary)' }}>Total Analyses</span>
            </div>
            <div className="text-[28px] font-bold" style={{ color: 'var(--text-primary)' }}>{stats.total}</div>
          </div>
          <div className="stat-card">
            <div className="flex items-center gap-2 mb-2">
              <div className="stat-dot" style={{ backgroundColor: 'var(--accent-orange)' }} />
              <span className="text-[13px] font-medium" style={{ color: 'var(--text-secondary)' }}>Pending</span>
            </div>
            <div className="text-[28px] font-bold" style={{ color: 'var(--text-primary)' }}>{stats.pending}</div>
          </div>
          <div className="stat-card">
            <div className="flex items-center gap-2 mb-2">
              <div className="stat-dot" style={{ backgroundColor: 'var(--accent-green)' }} />
              <span className="text-[13px] font-medium" style={{ color: 'var(--text-secondary)' }}>Completed</span>
            </div>
            <div className="text-[28px] font-bold" style={{ color: 'var(--text-primary)' }}>{stats.completed}</div>
          </div>
          <div className="stat-card">
            <div className="flex items-center gap-2 mb-2">
              <div className="stat-dot" style={{ backgroundColor: 'var(--accent-red)' }} />
              <span className="text-[13px] font-medium" style={{ color: 'var(--text-secondary)' }}>Failed</span>
            </div>
            <div className="text-[28px] font-bold" style={{ color: 'var(--text-primary)' }}>{stats.failed}</div>
          </div>
        </div>

        {/* Tab Filters */}
        <div className="flex items-center justify-between mb-6">
          <div className="tab-filters">
            {tabs.map((tab) => (
              <button
                key={tab}
                className={`tab-button ${activeTab === tab ? 'active' : ''}`}
                onClick={() => { setActiveTab(tab); setCurrentPage(1); }}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
                <span className="ml-1.5 text-[11px] opacity-60">({tabCounts[tab]})</span>
              </button>
            ))}
          </div>
        </div>

        {/* Data Table */}
        <div className="bg-white rounded-2xl border overflow-hidden" style={{ borderColor: 'var(--border)' }}>
          <table className="analytics-table">
            <thead>
              <tr>
                <th style={{ width: '40px' }}>
                  <div
                    className={`custom-checkbox ${selectedIds.length === paginatedRecords.length && paginatedRecords.length > 0 ? 'checked' : ''}`}
                    onClick={toggleSelectAll}
                  />
                </th>
                <th>Type</th>
                <th>Image Name</th>
                <th>Objects</th>
                <th>Confidence</th>
                <th>Status</th>
                <th>Date</th>
                <th>User</th>
              </tr>
            </thead>
            <tbody>
              {paginatedRecords.map((record) => (
                <tr key={record.id}>
                  <td>
                    <div
                      className={`custom-checkbox ${selectedIds.includes(record.id) ? 'checked' : ''}`}
                      onClick={() => toggleSelect(record.id)}
                    />
                  </td>
                  <td>
                    <span className={`type-badge ${record.analysisType}`}>
                      {ANALYSIS_TYPES[record.analysisType]?.name || record.analysisType}
                    </span>
                  </td>
                  <td className="font-medium">{record.imageName}</td>
                  <td>{record.totalObjects}</td>
                  <td>{(record.confidence * 100).toFixed(0)}%</td>
                  <td>
                    <span className={`status-badge status-${record.status}`}>
                      {record.status.charAt(0).toUpperCase() + record.status.slice(1)}
                    </span>
                  </td>
                  <td style={{ color: 'var(--text-secondary)' }}>{formatDate(record.timestamp)}</td>
                  <td style={{ color: 'var(--text-secondary)' }}>{record.user}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Pagination */}
          <div className="flex items-center justify-between px-6 py-4 border-t" style={{ borderColor: 'var(--border)' }}>
            <span className="text-[13px]" style={{ color: 'var(--text-secondary)' }}>
              Showing {((currentPage - 1) * itemsPerPage) + 1}-{Math.min(currentPage * itemsPerPage, filteredRecords.length)} of {filteredRecords.length} entries
            </span>
            <div className="pagination">
              <button
                className="page-button"
                disabled={currentPage === 1}
                onClick={() => setCurrentPage(p => p - 1)}
              >
                &lt; Previous
              </button>
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <button
                  key={page}
                  className={`page-button ${currentPage === page ? 'active' : ''}`}
                  onClick={() => setCurrentPage(page)}
                >
                  {page}
                </button>
              ))}
              <button
                className="page-button"
                disabled={currentPage === totalPages}
                onClick={() => setCurrentPage(p => p + 1)}
              >
                Next &gt;
              </button>
            </div>
          </div>
        </div>

      </main>
    </div>
  );
};

export default Analytics;

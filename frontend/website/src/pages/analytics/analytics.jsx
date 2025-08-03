import React, { useState, useEffect } from 'react';
import {
  AnalyticsHeader,
  AnalyticsStats,
  AnalyticsTable,
  DetailModal,
  FiltersSection
} from './components';
import { MOCK_ANALYSIS_RECORDS } from './constants';
import './analytics.css';

const Analytics = () => {
  const [records, setRecords] = useState(MOCK_ANALYSIS_RECORDS);
  const [filteredRecords, setFilteredRecords] = useState(MOCK_ANALYSIS_RECORDS);
  const [filters, setFilters] = useState({
    analysisType: 'all',
    search: '',
    dateRange: 'all'
  });
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Calculate stats
  const stats = {
    totalAnalyses: records.length,
    totalObjects: records.reduce((sum, record) => sum + record.totalObjects, 0),
    averageConfidence: records.reduce((sum, record) => sum + record.confidence, 0) / records.length,
    successRate: 100 // All records are completed for now
  };

  // Filter records based on current filters
  useEffect(() => {
    let filtered = [...records];

    // Filter by analysis type
    if (filters.analysisType !== 'all') {
      filtered = filtered.filter(record => record.analysisType === filters.analysisType);
    }

    // Filter by search
    if (filters.search) {
      const searchTerm = filters.search.toLowerCase();
      filtered = filtered.filter(record => 
        record.imageName.toLowerCase().includes(searchTerm) ||
        record.user.toLowerCase().includes(searchTerm)
      );
    }

    // Filter by date range
    if (filters.dateRange !== 'all') {
      const now = new Date();
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
      const monthAgo = new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000);

      filtered = filtered.filter(record => {
        const recordDate = new Date(record.timestamp);
        switch (filters.dateRange) {
          case 'today':
            return recordDate >= today;
          case 'week':
            return recordDate >= weekAgo;
          case 'month':
            return recordDate >= monthAgo;
      default:
            return true;
        }
      });
    }

    setFilteredRecords(filtered);
  }, [records, filters]);

  const handleViewDetails = (record) => {
    setSelectedRecord(record);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedRecord(null);
  };

  return (
    <div className="bg-gray-900 text-white overflow-x-hidden">
      <main className="min-h-screen bg-gray-900">
        <AnalyticsHeader 
          totalRecords={stats.totalAnalyses}
          totalObjects={stats.totalObjects}
          averageConfidence={stats.averageConfidence}
        />

        <AnalyticsStats stats={stats} />

        <FiltersSection 
          filters={filters}
          setFilters={setFilters}
        />

        <AnalyticsTable 
          records={filteredRecords}
          onViewDetails={handleViewDetails}
        />

        <DetailModal 
          record={selectedRecord}
          isOpen={isModalOpen}
          onClose={handleCloseModal}
        />
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 border-t border-gray-700 py-8">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-gray-400">© 2024 Lunar Analytics. Advanced surface detection technology.</p>
        </div>
      </footer>
    </div>
  );
};

export default Analytics; 
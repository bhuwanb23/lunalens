import React from 'react';
import { usePdfExport } from '../hooks/usePdfExport';

const PdfExportButton = ({ analysisResults, disabled = false }) => {
  const { generatePdfReport, isExporting, exportProgress } = usePdfExport();

  const handleExport = async () => {
    if (!analysisResults || disabled) return;

    try {
      const result = await generatePdfReport(analysisResults);
      
      if (result.success) {
        console.log(`PDF exported successfully: ${result.filename}`);
        // Show success message to user
        alert(`PDF report generated successfully!\n\nTo save as PDF:\n1. In the print dialog, select "Save as PDF"\n2. Choose your download location\n3. Click Save\n\nFilename: ${result.filename}`);
      } else {
        console.error('PDF export failed:', result.error);
        alert('PDF generation failed. Please try again.');
      }
    } catch (error) {
      console.error('PDF export error:', error);
      alert('An error occurred while generating the PDF. Please try again.');
    }
  };

  return (
    <button
      onClick={handleExport}
      disabled={disabled || isExporting || !analysisResults}
      className={`
        relative overflow-hidden bg-gradient-to-r from-green-500 via-emerald-600 to-green-700 
        hover:from-green-600 hover:via-emerald-700 hover:to-green-800 
        px-6 sm:px-8 py-3 sm:py-4 rounded-lg sm:rounded-xl font-bold text-sm sm:text-base 
        transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 
        shadow-lg hover:shadow-green-500/50 disabled:opacity-50 disabled:cursor-not-allowed
        ${isExporting ? 'animate-pulse' : ''}
      `}
    >
      {/* Progress bar overlay */}
      {isExporting && (
        <div 
          className="absolute inset-0 bg-green-600/20 transition-all duration-300"
          style={{ width: `${exportProgress}%` }}
        />
      )}
      
      <span className="flex items-center space-x-2 relative z-10">
        {isExporting ? (
          <>
            <div className="w-4 h-4 sm:w-5 sm:h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <span>Generating PDF... {exportProgress}%</span>
          </>
        ) : (
          <>
            <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 512 512">
              <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
            </svg>
            <span>Export Results</span>
          </>
        )}
      </span>
    </button>
  );
};

export default PdfExportButton; 
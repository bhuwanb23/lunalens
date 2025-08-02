import React from 'react';

const ConfirmationSection = ({ showConfirmation, selectedAnalysis, getAnalysisName, error, isAnalyzing, handleStartAnalysis }) => {
  if (!showConfirmation) return null;

  return (
    <section className="py-6 sm:py-8 px-4 sm:px-6">
      <div className="max-w-lg sm:max-w-xl mx-auto text-center">
        <div className="bg-gradient-to-br from-gray-800 via-gray-700 to-gray-800 border-2 border-orange-500/30 rounded-lg sm:rounded-xl p-4 sm:p-6 shadow-lg">
          <div className="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-orange-400 via-red-500 to-orange-600 rounded-lg sm:rounded-xl flex items-center justify-center mx-auto mb-4 sm:mb-5 shadow-md animate-pulse">
            <i className="text-xl sm:text-2xl text-white">
              <svg className="w-6 h-6 sm:w-7 sm:h-7" fill="currentColor" viewBox="0 0 448 512">
                <path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z" />
              </svg>
            </i>
          </div>
          <h3 className="text-lg sm:text-xl font-bold mb-3 sm:mb-4 bg-gradient-to-r from-gray-200 to-orange-300 bg-clip-text text-transparent">Analysis Initiated</h3>
          <p className="text-gray-300 text-sm sm:text-base mb-6 sm:mb-7 leading-relaxed">
            {getAnalysisName(selectedAnalysis)} has been initiated and is now processing lunar surface data...
          </p>
          {error && (
            <div className="mb-4 p-3 sm:p-4 bg-gradient-to-r from-red-900 to-red-800 border-2 border-red-600 rounded-lg sm:rounded-xl">
              <p className="text-red-200 font-semibold text-xs sm:text-sm">{error}</p>
            </div>
          )}
          <button 
            onClick={handleStartAnalysis}
            disabled={isAnalyzing}
            className={`px-6 sm:px-8 py-3 sm:py-4 rounded-lg sm:rounded-xl font-bold text-sm sm:text-base transition-all duration-300 shadow-md transform hover:scale-105 ${
              isAnalyzing 
                ? 'bg-gray-600 cursor-not-allowed shadow-gray-600/50' 
                : 'bg-gradient-to-r from-orange-500 via-red-600 to-orange-700 hover:from-orange-600 hover:via-red-700 hover:to-orange-800 shadow-orange-500/50 hover:shadow-orange-500/75'
            }`}
          >
            {isAnalyzing ? (
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 sm:w-5 sm:h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Analyzing...</span>
              </div>
            ) : (
              <span className="flex items-center space-x-2">
                <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 512 512">
                  <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                </svg>
                <span>Start Analysis</span>
              </span>
            )}
          </button>
        </div>
      </div>
    </section>
  );
};

export default ConfirmationSection; 
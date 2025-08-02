import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 border-t border-gray-700 py-4 sm:py-6">
      <div className="max-w-4xl sm:max-w-5xl mx-auto px-4 sm:px-6 text-center">
        <div className="flex items-center justify-center space-x-2 sm:space-x-3 mb-2 sm:mb-3">
          <div className="w-5 h-5 sm:w-6 sm:h-6 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center">
            <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="currentColor" viewBox="0 0 512 512">
              <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
            </svg>
          </div>
          <h3 className="text-sm sm:text-base font-bold bg-gradient-to-r from-orange-400 to-red-500 bg-clip-text text-transparent">
            LunaLens Boulder Detection
          </h3>
        </div>
        <p className="text-gray-300 text-xs sm:text-sm font-light">© 2024 Advanced AI-powered lunar analysis</p>
      </div>
    </footer>
  );
};

export default Footer; 
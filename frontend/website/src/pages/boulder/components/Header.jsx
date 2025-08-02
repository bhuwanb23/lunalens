import React from 'react';
import { useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();

  return (
    <header className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 border-b border-gray-700 shadow-lg backdrop-blur-sm">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-3 sm:py-4">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-3 sm:space-y-0">
          <div className="flex items-center space-x-2 sm:space-x-4">
            <div className="w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-br from-orange-400 via-red-500 to-orange-600 rounded-lg sm:rounded-xl flex items-center justify-center shadow-md hover:shadow-orange-500/25 transition-all duration-300 transform hover:scale-110">
              <i className="text-white text-sm sm:text-lg">
                <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 512 512">
                  <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                </svg>
              </i>
            </div>
            <h1 className="text-lg sm:text-xl font-bold bg-gradient-to-r from-orange-400 via-red-500 to-orange-600 bg-clip-text text-transparent">
              Boulder Detection
            </h1>
          </div>
          <nav className="flex items-center justify-center sm:justify-end space-x-3 sm:space-x-6 text-xs sm:text-sm">
            <span 
              className="text-gray-300 hover:text-blue-400 transition-all duration-300 cursor-pointer font-medium hover:scale-105 transform"
              onClick={() => navigate('/dashboard')}
            >
              Dashboard
            </span>
            <span 
              className="text-gray-300 hover:text-blue-400 transition-all duration-300 cursor-pointer font-medium hover:scale-105 transform"
              onClick={() => navigate('/analytics')}
            >
              Analytics
            </span>
            <span className="text-orange-400 font-semibold cursor-pointer bg-gradient-to-r from-orange-500/20 to-red-500/20 px-2 sm:px-3 py-1 sm:py-2 rounded-lg border border-orange-500/30 text-xs">
              Boulder Detection
            </span>
            <div className="w-6 h-6 sm:w-8 sm:h-8 rounded-full bg-gradient-to-br from-gray-600 to-gray-700 flex items-center justify-center shadow-md hover:shadow-gray-500/25 transition-all duration-300 transform hover:scale-110">
              <i className="text-xs">
                <svg className="w-3 h-3 sm:w-4 sm:h-4" fill="currentColor" viewBox="0 0 448 512">
                  <path d="M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H418.3c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304H178.3z" />
                </svg>
              </i>
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header; 
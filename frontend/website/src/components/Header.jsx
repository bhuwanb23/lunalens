import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const Header = ({ onLogout }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-gray-900/90 backdrop-blur-lg border-b border-gray-700/50 shadow-xl">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo and Brand */}
          <div className="flex items-center space-x-4">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-purple-500 rounded-xl flex items-center justify-center shadow-lg hover:shadow-blue-500/25 transition-all duration-300 transform hover:scale-110">
              <i className="text-white text-lg">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 384 512">
                  <path d="M223.5 32C100 32 0 132.3 0 256S100 480 223.5 480c60.6 0 115.5-24.2 155.8-63.4c5-4.9 6.3-12.5 3.1-18.7s-10.1-9.7-17-8.5c-9.8 1.7-19.8 2.6-30.1 2.6c-96.9 0-175.5-78.8-175.5-176c0-65.8 36-123.1 89.3-153.3c6.1-3.5 9.2-10.5 7.7-17.3s-7.3-11.9-14.3-12.5c-6.3-.5-12.6-.8-19-.8z" />
                </svg>
              </i>
            </div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
              LunaLens
            </h1>
          </div>
          
          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <span
              className={`transition-all duration-300 cursor-pointer font-medium ${
                isActive('/dashboard') 
                  ? 'text-blue-300 border-b-2 border-blue-300' 
                  : 'text-gray-400 hover:text-blue-300 hover:scale-105'
              }`}
              onClick={() => navigate('/dashboard')}
            >
              Dashboard
            </span>
            <span
              className={`transition-all duration-300 cursor-pointer font-medium ${
                isActive('/analytics') 
                  ? 'text-blue-300 border-b-2 border-blue-300' 
                  : 'text-gray-400 hover:text-blue-300 hover:scale-105'
              }`}
              onClick={() => navigate('/analytics')}
            >
              Analytics
            </span>
            <span
              className={`transition-all duration-300 cursor-pointer font-medium ${
                isActive('/boulder') 
                  ? 'text-orange-300 border-b-2 border-orange-300' 
                  : 'text-gray-400 hover:text-orange-300 hover:scale-105'
              }`}
              onClick={() => navigate('/boulder')}
            >
              Boulder Detection
            </span>
            <span
              className={`transition-all duration-300 cursor-pointer font-medium ${
                isActive('/landslide') 
                  ? 'text-red-300 border-b-2 border-red-300' 
                  : 'text-gray-400 hover:text-red-300 hover:scale-105'
              }`}
              onClick={() => navigate('/landslide')}
            >
              Landslide Detection
            </span>
          </nav>
          
          {/* User Section */}
          <div className="flex items-center space-x-4">
            {/* Status Indicator */}
            <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse shadow-lg shadow-green-400/50"></div>
            
            {/* User Avatar */}
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-gray-600 to-gray-700 flex items-center justify-center shadow-lg hover:shadow-gray-500/25 transition-all duration-300 transform hover:scale-110">
              <i className="text-white text-sm">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 448 512">
                  <path d="M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H418.3c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304H178.3z" />
                </svg>
              </i>
            </div>
            
            {/* Logout Button */}
            {onLogout && (
              <button
                onClick={onLogout}
                className="text-gray-400 hover:text-red-400 transition-all duration-300 text-sm font-medium hover:scale-105"
              >
                Logout
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

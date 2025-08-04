import React from 'react';

const HeroSection = () => {
  return (
    <section className="relative h-[200px] sm:h-[240px] lg:h-[280px] flex items-center justify-center overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 mt-6 mb-8 rounded-2xl border border-gray-700/50">
      {/* Animated starfield background */}
      <div className="absolute inset-0 z-0 pointer-events-none">
        <svg className="w-full h-full" viewBox="0 0 400 120" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="30" cy="30" r="1.5" fill="#fff" opacity="0.15">
            <animate attributeName="cy" values="30;110;30" dur="8s" repeatCount="indefinite" />
          </circle>
          <circle cx="120" cy="80" r="1.2" fill="#fff" opacity="0.12">
            <animate attributeName="cy" values="80;10;80" dur="10s" repeatCount="indefinite" />
          </circle>
          <circle cx="200" cy="50" r="1.8" fill="#fff" opacity="0.18">
            <animate attributeName="cy" values="50;100;50" dur="12s" repeatCount="indefinite" />
          </circle>
          <circle cx="320" cy="100" r="1.1" fill="#fff" opacity="0.10">
            <animate attributeName="cy" values="100;20;100" dur="9s" repeatCount="indefinite" />
          </circle>
          <circle cx="370" cy="40" r="1.4" fill="#fff" opacity="0.13">
            <animate attributeName="cy" values="40;110;40" dur="11s" repeatCount="indefinite" />
          </circle>
        </svg>
      </div>
      
      {/* Enhanced animated background elements */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/8 via-purple-500/5 to-blue-600/8 animate-pulse"></div>
      
      {/* Floating particles - moved away from edges */}
      <div className="absolute top-12 right-12 sm:right-16 w-10 h-10 sm:w-14 sm:h-14 rounded-full bg-gradient-to-br from-blue-200 to-purple-400 opacity-30 animate-bounce shadow-lg shadow-blue-400/30"></div>
      <div className="absolute bottom-12 left-12 sm:left-16 w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-gradient-to-br from-purple-300 to-blue-500 opacity-25 animate-pulse shadow-lg shadow-purple-500/30"></div>
      <div className="absolute top-1/2 left-1/3 w-6 h-6 sm:w-8 sm:h-8 rounded-full bg-gradient-to-br from-indigo-300 to-blue-400 opacity-20 animate-bounce" style={{animationDelay: '0.5s'}}></div>
      <div className="absolute top-1/3 right-1/3 w-4 h-4 sm:w-6 sm:h-6 rounded-full bg-gradient-to-br from-purple-300 to-blue-400 opacity-30 animate-pulse" style={{animationDelay: '1s'}}></div>
      
      {/* Glowing orbs - moved away from edges */}
      <div className="absolute top-1/3 left-1/4 w-2 h-2 sm:w-3 sm:h-3 bg-blue-400 rounded-full animate-ping opacity-60"></div>
      <div className="absolute bottom-1/3 right-1/4 w-2 h-2 sm:w-3 sm:h-3 bg-purple-400 rounded-full animate-ping opacity-60" style={{animationDelay: '0.3s'}}></div>
      
      {/* Grid pattern overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:20px_20px] opacity-30"></div>
      
      <div className="text-center z-10 relative px-8 py-6 max-w-4xl mx-auto">
        <div className="mb-4 sm:mb-6">
          <div className="w-12 h-12 sm:w-14 sm:h-14 lg:w-16 lg:h-16 bg-gradient-to-br from-blue-400 via-purple-500 to-blue-600 rounded-xl sm:rounded-2xl flex items-center justify-center mx-auto mb-4 sm:mb-5 shadow-2xl hover:shadow-blue-500/50 transition-all duration-500 transform hover:scale-110 hover:rotate-3">
            <i className="text-white text-lg sm:text-xl lg:text-2xl">
              <svg className="w-6 h-6 sm:w-7 sm:h-7 lg:w-8 lg:h-8" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </i>
          </div>
        </div>
        
        {/* Enhanced title with glow effect */}
        <h2 className="text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold mb-4 sm:mb-5 bg-gradient-to-r from-gray-100 via-blue-200 to-purple-300 bg-clip-text text-transparent drop-shadow-lg animate-pulse leading-tight">
          Lunar Terrain Analysis
        </h2>
        
        {/* Enhanced subtitle */}
        <p className="text-sm sm:text-base lg:text-lg xl:text-xl text-gray-300 max-w-2xl sm:max-w-3xl lg:max-w-4xl mx-auto leading-relaxed font-light mb-4 sm:mb-5 px-4">
          Advanced lunar landslide risk assessment using terrain parameters and geomorphological analysis
        </p>
        
        {/* Enhanced animated dots */}
        <div className="flex justify-center space-x-3 sm:space-x-4 mb-4 sm:mb-5">
          <div className="w-2 h-2 sm:w-2.5 sm:h-2.5 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full animate-bounce shadow-lg shadow-blue-400/50"></div>
          <div className="w-2 h-2 sm:w-2.5 sm:h-2.5 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-full animate-bounce shadow-lg shadow-purple-500/50" style={{animationDelay: '0.1s'}}></div>
          <div className="w-2 h-2 sm:w-2.5 sm:h-2.5 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full animate-bounce shadow-lg shadow-blue-600/50" style={{animationDelay: '0.2s'}}></div>
        </div>
        
        {/* Status indicator */}
        <div className="flex items-center justify-center space-x-2 mb-4 sm:mb-5">
          <div className="w-2 h-2 sm:w-2.5 sm:h-2.5 bg-green-400 rounded-full animate-pulse"></div>
          <span className="text-sm sm:text-base text-green-400 font-medium">Lunar Analysis Ready</span>
        </div>
        
        {/* Glowing CTA button */}
        <button className="px-8 py-3 sm:px-10 sm:py-4 rounded-xl font-bold text-base sm:text-lg bg-gradient-to-r from-blue-500 via-purple-500 to-orange-400 text-white shadow-lg shadow-blue-500/30 hover:shadow-2xl hover:scale-105 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-400 animate-pulse">
          Start New Analysis
        </button>
      </div>
      
      {/* Corner decorations - moved away from edges */}
      <div className="absolute top-4 left-4 w-12 h-12 sm:w-16 sm:h-16 border-l-2 border-t-2 border-blue-500/30 rounded-tl-lg"></div>
      <div className="absolute top-4 right-4 w-12 h-12 sm:w-16 sm:h-16 border-r-2 border-t-2 border-purple-500/30 rounded-tr-lg"></div>
      <div className="absolute bottom-4 left-4 w-12 h-12 sm:w-16 sm:h-16 border-l-2 border-b-2 border-blue-500/30 rounded-bl-lg"></div>
      <div className="absolute bottom-4 right-4 w-12 h-12 sm:w-16 sm:h-16 border-r-2 border-b-2 border-purple-500/30 rounded-br-lg"></div>
    </section>
  );
};

export default HeroSection; 
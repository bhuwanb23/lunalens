import React from 'react';

const HeroSection = () => {
  return (
    <section className="relative h-[180px] sm:h-[220px] lg:h-[240px] flex items-center justify-center overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 mt-6 mb-8">
      {/* Enhanced animated background elements */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/8 via-purple-500/5 to-blue-600/8 animate-pulse"></div>
      
      {/* Floating particles */}
      <div className="absolute top-8 right-8 sm:right-12 w-10 h-10 sm:w-14 sm:h-14 rounded-full bg-gradient-to-br from-blue-200 to-purple-400 opacity-30 animate-bounce shadow-lg shadow-blue-400/30"></div>
      <div className="absolute bottom-8 left-8 sm:left-12 w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-gradient-to-br from-purple-300 to-blue-500 opacity-25 animate-pulse shadow-lg shadow-purple-500/30"></div>
      <div className="absolute top-1/2 left-1/4 w-6 h-6 sm:w-8 sm:h-8 rounded-full bg-gradient-to-br from-indigo-300 to-blue-400 opacity-20 animate-bounce" style={{animationDelay: '0.5s'}}></div>
      <div className="absolute top-1/3 right-1/4 w-4 h-4 sm:w-6 sm:h-6 rounded-full bg-gradient-to-br from-purple-300 to-blue-400 opacity-30 animate-pulse" style={{animationDelay: '1s'}}></div>
      
      {/* Glowing orbs */}
      <div className="absolute top-1/4 left-1/3 w-2 h-2 sm:w-3 sm:h-3 bg-blue-400 rounded-full animate-ping opacity-60"></div>
      <div className="absolute bottom-1/4 right-1/3 w-2 h-2 sm:w-3 sm:h-3 bg-purple-400 rounded-full animate-ping opacity-60" style={{animationDelay: '0.3s'}}></div>
      
      {/* Grid pattern overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:20px_20px] opacity-30"></div>
      
      <div className="text-center z-10 relative px-6 py-4">
        <div className="mb-4 sm:mb-5">
          <div className="w-10 h-10 sm:w-12 sm:h-12 lg:w-14 lg:h-14 bg-gradient-to-br from-blue-400 via-purple-500 to-blue-600 rounded-xl sm:rounded-2xl flex items-center justify-center mx-auto mb-3 sm:mb-4 shadow-2xl hover:shadow-blue-500/50 transition-all duration-500 transform hover:scale-110 hover:rotate-3">
            <i className="text-white text-sm sm:text-lg lg:text-xl">
              <svg className="w-5 h-5 sm:w-6 sm:h-6 lg:w-7 lg:h-7" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </i>
          </div>
        </div>
        
        {/* Enhanced title with glow effect */}
        <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold mb-3 sm:mb-4 bg-gradient-to-r from-gray-100 via-blue-200 to-purple-300 bg-clip-text text-transparent drop-shadow-lg animate-pulse">
          Lunar Terrain Analysis
        </h2>
        
        {/* Enhanced subtitle */}
        <p className="text-sm sm:text-base lg:text-lg text-gray-300 max-w-lg sm:max-w-xl lg:max-w-2xl mx-auto leading-relaxed font-light mb-3 sm:mb-4">
          Advanced lunar landslide risk assessment using terrain parameters and geomorphological analysis
        </p>
        
        {/* Enhanced animated dots */}
        <div className="flex justify-center space-x-3 sm:space-x-4 mb-3">
          <div className="w-2 h-2 sm:w-2.5 sm:h-2.5 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full animate-bounce shadow-lg shadow-blue-400/50"></div>
          <div className="w-2 h-2 sm:w-2.5 sm:h-2.5 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-full animate-bounce shadow-lg shadow-purple-500/50" style={{animationDelay: '0.1s'}}></div>
          <div className="w-2 h-2 sm:w-2.5 sm:h-2.5 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full animate-bounce shadow-lg shadow-blue-600/50" style={{animationDelay: '0.2s'}}></div>
        </div>
        
        {/* Status indicator */}
        <div className="flex items-center justify-center space-x-2">
          <div className="w-2 h-2 sm:w-2.5 sm:h-2.5 bg-green-400 rounded-full animate-pulse"></div>
          <span className="text-sm text-green-400 font-medium">Lunar Analysis Ready</span>
        </div>
      </div>
      
      {/* Corner decorations */}
      <div className="absolute top-0 left-0 w-12 h-12 sm:w-16 sm:h-16 border-l-2 border-t-2 border-blue-500/30 rounded-tl-lg"></div>
      <div className="absolute top-0 right-0 w-12 h-12 sm:w-16 sm:h-16 border-r-2 border-t-2 border-purple-500/30 rounded-tr-lg"></div>
      <div className="absolute bottom-0 left-0 w-12 h-12 sm:w-16 sm:h-16 border-l-2 border-b-2 border-blue-500/30 rounded-bl-lg"></div>
      <div className="absolute bottom-0 right-0 w-12 h-12 sm:w-16 sm:h-16 border-r-2 border-b-2 border-purple-500/30 rounded-br-lg"></div>
    </section>
  );
};

export default HeroSection; 
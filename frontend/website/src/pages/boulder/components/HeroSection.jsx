import React from 'react';

const HeroSection = () => {
  return (
    <section className="relative h-[160px] sm:h-[200px] flex items-center justify-center overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 mt-4">
      {/* Enhanced animated background elements */}
      <div className="absolute inset-0 bg-gradient-to-br from-orange-500/8 via-red-500/5 to-orange-600/8 animate-pulse"></div>
      
      {/* Floating particles */}
      <div className="absolute top-6 right-6 sm:right-10 w-10 h-10 sm:w-14 sm:h-14 rounded-full bg-gradient-to-br from-orange-200 to-red-400 opacity-30 animate-bounce shadow-lg shadow-orange-400/30"></div>
      <div className="absolute bottom-6 left-6 sm:left-10 w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-gradient-to-br from-orange-300 to-red-500 opacity-25 animate-pulse shadow-lg shadow-red-500/30"></div>
      <div className="absolute top-1/2 left-1/4 w-6 h-6 sm:w-8 sm:h-8 rounded-full bg-gradient-to-br from-yellow-300 to-orange-400 opacity-20 animate-bounce" style={{animationDelay: '0.5s'}}></div>
      <div className="absolute top-1/3 right-1/4 w-4 h-4 sm:w-6 sm:h-6 rounded-full bg-gradient-to-br from-red-300 to-pink-400 opacity-30 animate-pulse" style={{animationDelay: '1s'}}></div>
      
      {/* Glowing orbs */}
      <div className="absolute top-1/4 left-1/3 w-2 h-2 sm:w-3 sm:h-3 bg-orange-400 rounded-full animate-ping opacity-60"></div>
      <div className="absolute bottom-1/4 right-1/3 w-2 h-2 sm:w-3 sm:h-3 bg-red-400 rounded-full animate-ping opacity-60" style={{animationDelay: '0.3s'}}></div>
      
      {/* Grid pattern overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:20px_20px] opacity-30"></div>
      
      <div className="text-center z-10 relative px-4">
        <div className="mb-2 sm:mb-3">
          <div className="w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-br from-orange-400 via-red-500 to-orange-600 rounded-xl sm:rounded-2xl flex items-center justify-center mx-auto mb-2 sm:mb-3 shadow-2xl hover:shadow-orange-500/50 transition-all duration-500 transform hover:scale-110 hover:rotate-3">
            <i className="text-white text-sm sm:text-lg">
              <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 512 512">
                <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
              </svg>
            </i>
          </div>
        </div>
        
        {/* Enhanced title with glow effect */}
        <h2 className="text-xl sm:text-2xl lg:text-3xl font-bold mb-2 sm:mb-3 bg-gradient-to-r from-gray-100 via-orange-200 to-red-300 bg-clip-text text-transparent drop-shadow-lg animate-pulse">
        Chandrayaan 2 OHRC Image based Boulder Detection
        </h2>
        
        {/* Enhanced subtitle */}
        <p className="text-xs sm:text-sm lg:text-base text-gray-300 max-w-lg sm:max-w-xl mx-auto leading-relaxed font-light mb-2 sm:mb-3">
          Advanced AI-powered detection system for lunar boulders
        </p>
        {/* Enhanced animated dots */}
        <div className="flex justify-center space-x-2 sm:space-x-3">
          <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-gradient-to-r from-orange-400 to-red-500 rounded-full animate-bounce shadow-lg shadow-orange-400/50"></div>
          <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-gradient-to-r from-red-500 to-pink-500 rounded-full animate-bounce shadow-lg shadow-red-500/50" style={{animationDelay: '0.1s'}}></div>
          <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-gradient-to-r from-orange-600 to-red-600 rounded-full animate-bounce shadow-lg shadow-orange-600/50" style={{animationDelay: '0.2s'}}></div>
        </div>
        
        {/* Status indicator */}
        <div className="mt-2 sm:mt-3 flex items-center justify-center space-x-2">
          <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span className="text-xs text-green-400 font-medium">System Ready</span>
        </div>
      </div>
      
      {/* Corner decorations */}
      <div className="absolute top-0 left-0 w-12 h-12 sm:w-16 sm:h-16 border-l-2 border-t-2 border-orange-500/30 rounded-tl-lg"></div>
      <div className="absolute top-0 right-0 w-12 h-12 sm:w-16 sm:h-16 border-r-2 border-t-2 border-red-500/30 rounded-tr-lg"></div>
      <div className="absolute bottom-0 left-0 w-12 h-12 sm:w-16 sm:h-16 border-l-2 border-b-2 border-orange-500/30 rounded-bl-lg"></div>
      <div className="absolute bottom-0 right-0 w-12 h-12 sm:w-16 sm:h-16 border-r-2 border-b-2 border-red-500/30 rounded-br-lg"></div>
    </section>
  );
};

export default HeroSection; 
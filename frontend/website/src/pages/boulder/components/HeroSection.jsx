import React from 'react';

const HeroSection = () => {
  return (
    <section className="relative h-[120px] sm:h-[150px] flex items-center justify-center overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Animated background elements */}
      <div className="absolute inset-0 bg-gradient-to-br from-orange-500/5 via-red-500/3 to-orange-600/5 animate-pulse"></div>
      <div className="absolute top-4 right-4 sm:right-8 w-8 h-8 sm:w-12 sm:h-12 rounded-full bg-gradient-to-br from-orange-200 to-red-400 opacity-20 animate-bounce"></div>
      <div className="absolute bottom-4 left-4 sm:left-8 w-6 h-6 sm:w-8 sm:h-8 rounded-full bg-gradient-to-br from-orange-300 to-red-500 opacity-15 animate-pulse"></div>
      
      <div className="text-center z-10 relative px-4">
        <div className="mb-2 sm:mb-3">
          <div className="w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-br from-orange-400 via-red-500 to-orange-600 rounded-lg sm:rounded-xl flex items-center justify-center mx-auto mb-2 sm:mb-3 shadow-lg hover:shadow-orange-500/50 transition-all duration-300 transform hover:scale-110">
            <i className="text-white text-sm sm:text-lg">
              <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 512 512">
                <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
              </svg>
            </i>
          </div>
        </div>
        <h2 className="text-xl sm:text-2xl lg:text-3xl font-bold mb-2 sm:mb-3 bg-gradient-to-r from-gray-100 via-orange-200 to-red-300 bg-clip-text text-transparent">
          Boulder & Crater Detection
        </h2>
        <p className="text-sm sm:text-base text-gray-300 max-w-lg sm:max-w-xl mx-auto leading-relaxed font-light">
          Advanced AI-powered detection system for lunar boulders and craters
        </p>
        <div className="mt-2 sm:mt-3 flex justify-center space-x-2">
          <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-orange-400 rounded-full animate-bounce"></div>
          <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-red-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
          <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-orange-600 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection; 
import React from 'react';

const HeroSection = () => {
    return (
        <section className="relative min-h-[200px] sm:min-h-[240px] md:min-h-[280px] lg:min-h-[320px] xl:min-h-[360px] flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 mt-4 sm:mt-6 lg:mt-8 mb-6 sm:mb-8 lg:mb-12 rounded-2xl sm:rounded-3xl border border-gray-700/30 shadow-2xl py-4 sm:py-6 lg:py-8 xl:py-12">
            {/* Subtle animated background */}
            <div className="absolute inset-0 z-0 pointer-events-none">
                {/* Radial gradients for depth */}
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_30%,rgba(59,130,246,0.08)_0%,transparent_50%)]"></div>
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_70%,rgba(147,51,234,0.06)_0%,transparent_50%)]"></div>
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(16,185,129,0.04)_0%,transparent_50%)]"></div>

                {/* Subtle grid pattern */}
                <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.015)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.015)_1px,transparent_1px)] bg-[size:40px_40px] opacity-40"></div>

                {/* Floating elements - positioned away from content */}
                <div className="absolute top-6 right-6 w-12 h-12 rounded-full bg-gradient-to-br from-blue-400/20 to-purple-500/20 animate-pulse"></div>
                <div className="absolute bottom-6 left-6 w-10 h-10 rounded-full bg-gradient-to-br from-purple-400/15 to-blue-500/15 animate-pulse" style={{ animationDelay: '1s' }}></div>
                <div className="absolute top-1/4 left-1/4 w-6 h-6 rounded-full bg-gradient-to-br from-indigo-400/10 to-blue-500/10 animate-bounce" style={{ animationDelay: '0.5s' }}></div>
                <div className="absolute bottom-1/4 right-1/4 w-8 h-8 rounded-full bg-gradient-to-br from-green-400/10 to-blue-500/10 animate-pulse" style={{ animationDelay: '1.5s' }}></div>
            </div>

            {/* Main content container with proper spacing */}
            <div className="relative z-10 text-center px-4 sm:px-6 lg:px-8 xl:px-12 max-w-3xl sm:max-w-4xl mx-auto">
                {/* Icon section with better spacing */}
                <div className="mb-3 sm:mb-4 lg:mb-6 xl:mb-8">
                    <div className="relative mx-auto w-10 h-10 sm:w-12 sm:h-12 md:w-16 md:h-16 lg:w-18 lg:h-18 xl:w-20 xl:h-20 bg-gradient-to-br from-blue-500 via-purple-600 to-blue-700 rounded-xl sm:rounded-2xl flex items-center justify-center shadow-2xl hover:shadow-blue-500/40 transition-all duration-500 transform hover:scale-105">
                        {/* Inner glow */}
                        <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent rounded-2xl"></div>

                        {/* Icon */}
                        <svg className="w-5 h-5 sm:w-6 sm:h-6 md:w-8 md:h-8 lg:w-9 lg:h-9 xl:w-10 xl:h-10 text-white" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                        </svg>

                        {/* Floating accent */}
                        <div className="absolute -top-1 -right-1 w-2 h-2 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full animate-bounce opacity-70"></div>
                    </div>
                </div>

                {/* Title with improved typography and spacing */}
                <h1 className="text-lg sm:text-xl md:text-2xl lg:text-3xl xl:text-4xl font-extrabold mb-2 sm:mb-3 lg:mb-4 xl:mb-6 bg-gradient-to-r from-gray-100 via-blue-200 to-purple-300 bg-clip-text text-transparent leading-tight tracking-tight">
                    Lunar Terrain Analysis
                </h1>

                {/* Subtitle with better readability */}
                <p className="text-xs sm:text-sm md:text-base lg:text-lg xl:text-lg text-gray-300 max-w-xl sm:max-w-2xl lg:max-w-3xl xl:max-w-4xl mx-auto leading-relaxed font-light mb-3 sm:mb-4 lg:mb-6 xl:mb-8 px-2 sm:px-4">
                    Advanced lunar landslide risk assessment using terrain parameters and geomorphological analysis
                </p>

                {/* Status indicator with better positioning */}
                <div className="flex items-center justify-center space-x-2 mb-3 sm:mb-4 lg:mb-6 xl:mb-8">
                    <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full animate-pulse shadow-lg shadow-green-400/50"></div>
                    <span className="text-xs sm:text-sm text-green-400 font-medium">Lunar Analysis Ready</span>
                </div>

                {/* CTA Button with enhanced styling */}
                <button className="px-4 sm:px-6 py-1.5 sm:py-2 lg:px-8 lg:py-3 xl:px-10 xl:py-4 rounded-lg sm:rounded-xl font-bold text-xs sm:text-sm md:text-base lg:text-lg bg-gradient-to-r from-blue-500 via-purple-600 to-orange-500 text-white shadow-xl hover:shadow-2xl hover:shadow-blue-500/40 hover:scale-105 transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-blue-400/50 transform hover:-translate-y-1">
                    Start New Analysis
                </button>
            </div>

            {/* Subtle corner decorations - positioned away from content */}
            <div className="absolute top-3 left-3 w-8 h-8 border-l-2 border-t-2 border-blue-500/20 rounded-tl-lg"></div>
            <div className="absolute top-3 right-3 w-8 h-8 border-r-2 border-t-2 border-purple-500/20 rounded-tr-lg"></div>
            <div className="absolute bottom-3 left-3 w-8 h-8 border-l-2 border-b-2 border-blue-500/20 rounded-bl-lg"></div>
            <div className="absolute bottom-3 right-3 w-8 h-8 border-r-2 border-b-2 border-purple-500/20 rounded-br-lg"></div>

            {/* Bottom accent line */}
            <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-blue-500/30 to-transparent"></div>
        </section>
    );
};

export default HeroSection; 
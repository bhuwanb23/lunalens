import React from 'react';

const AnalysisSelection = ({ analysisTypes, selectedAnalysis, handleAnalysisSelect }) => {
  return (
    <section className="py-6 sm:py-8 px-4 sm:px-6">
      <div className="max-w-4xl sm:max-w-5xl mx-auto">
        <div className="text-center mb-6 sm:mb-8">
          <h3 className="text-xl sm:text-2xl font-bold mb-2 sm:mb-3 bg-gradient-to-r from-gray-200 to-orange-300 bg-clip-text text-transparent">Choose Analysis Type</h3>
          <p className="text-gray-300 text-sm sm:text-base leading-relaxed max-w-lg sm:max-w-xl mx-auto">Select your preferred detection method for lunar surface analysis</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
          {analysisTypes.map((analysis) => (
            <div 
              key={analysis.id}
              className={`bg-gradient-to-br from-gray-800 via-gray-700 to-gray-800 border-2 border-gray-600 rounded-lg sm:rounded-xl p-4 sm:p-5 cursor-pointer transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 relative overflow-hidden shadow-lg hover:shadow-xl ${
                selectedAnalysis === analysis.id 
                  ? 'border-orange-500 shadow-orange-500/50 bg-gradient-to-br from-orange-900/20 via-red-900/20 to-orange-900/20' 
                  : 'hover:border-gray-500'
              }`}
              onClick={() => handleAnalysisSelect(analysis.id)}
            >
              {/* Background glow effect */}
              <div className={`absolute top-0 right-0 w-8 h-8 sm:w-12 sm:h-12 rounded-full bg-gradient-to-br from-${analysis.color}-400 to-${analysis.color === 'orange' ? 'red' : analysis.color === 'blue' ? 'indigo' : analysis.color === 'green' ? 'emerald' : 'purple'}-500 opacity-10 -mr-4 sm:-mr-6 -mt-4 sm:-mt-6 animate-pulse`}></div>
              
              <div className="relative z-10">
                <div className={`w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-br from-${analysis.color}-400 via-${analysis.color === 'orange' ? 'red' : analysis.color === 'blue' ? 'indigo' : analysis.color === 'green' ? 'emerald' : 'purple'}-500 to-${analysis.color === 'orange' ? 'red' : analysis.color === 'blue' ? 'indigo' : analysis.color === 'green' ? 'emerald' : 'purple'}-600 rounded-lg sm:rounded-xl flex items-center justify-center mb-3 sm:mb-4 shadow-md hover:shadow-${analysis.color}-500/50 transition-all duration-300 transform hover:scale-110`}>
                  <i className="text-sm sm:text-lg text-white">
                    <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 512 512">
                      {analysis.icon === 'mountain' && (
                        <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                      )}
                      {analysis.icon === 'brain' && (
                        <path d="M184 0c30.9 0 56 25.1 56 56V456c0 30.9-25.1 56-56 56c-28.9 0-52.7-21.9-55.7-50.1c-5.2 1.4-10.7 2.1-16.3 2.1c-35.3 0-64-28.7-64-64c0-7.4 1.3-14.6 3.6-21.2C21.4 367.4 0 338.2 0 304c0-31.9 18.7-59.5 45.8-72.3C37.1 220.8 32 207 32 192c0-30.7 21.6-56.3 50.4-62.6C80.8 123.9 80 118 80 112c0-29.9 20.6-55.1 48.3-62.1C131.3 21.9 155.1 0 184 0zM328 0c28.9 0 52.6 21.9 55.7 49.9c27.8 7 48.3 32.1 48.3 62.1c0 6-.8 11.9-2.4 17.4c28.8 6.2 50.4 31.9 50.4 62.6c0 15-5.1 28.8-13.8 39.7C493.3 244.5 512 272.1 512 304c0 34.2-21.4 63.4-51.6 74.8c2.3 6.6 3.6 13.8 3.6 21.2c0 35.3-28.7 64-64 64c-5.6 0-11.1-.7-16.3-2.1c-3 28.2-26.8 50.1-55.7 50.1c-30.9 0-56-25.1-56-56V56c0-30.9 25.1-56 56-56z" />
                      )}
                      {analysis.icon === 'layer-group' && (
                        <path d="M264.5 5.2c14.9-6.9 32.1-6.9 47 0l218.6 101c8.5 3.9 13.9 12.4 13.9 21.8s-5.4 17.9-13.9 21.8l-218.6 101c-14.9 6.9-32.1 6.9-47 0L45.9 149.8C37.4 145.8 32 137.3 32 128s5.4-17.9 13.9-21.8L264.5 5.2zM476.9 209.6l53.2 24.6c8.5 3.9 13.9 12.4 13.9 21.8s-5.4 17.9-13.9 21.8l-218.6 101c-14.9 6.9-32.1 6.9-47 0L45.9 277.8C37.4 273.8 32 265.3 32 256s5.4-17.9 13.9-21.8l53.2-24.6 152 70.2c23.4 10.8 50.4 10.8 73.8 0l152-70.2zm-152 198.2l152-70.2 53.2 24.6c8.5 3.9 13.9 12.4 13.9 21.8s-5.4 17.9-13.9 21.8l-218.6 101c-14.9 6.9-32.1 6.9-47 0L45.9 405.8C37.4 401.8 32 393.3 32 384s5.4-17.9 13.9-21.8l53.2-24.6 152 70.2c23.4 10.8 50.4 10.8 73.8 0z" />
                      )}
                      {analysis.icon === 'eye' && (
                        <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                      )}
                    </svg>
                  </i>
                </div>
                <h4 className="text-sm sm:text-base font-bold mb-1 sm:mb-2 text-gray-200">{analysis.title}</h4>
                <p className="text-gray-300 text-xs sm:text-sm mb-3 sm:mb-4 leading-relaxed">{analysis.description}</p>
                <div className="space-y-1">
                  {analysis.features.map((feature, index) => (
                    <div key={index} className="flex items-center text-xs text-gray-300">
                      <span className="w-1 h-1 sm:w-1.5 sm:h-1.5 bg-gray-400 rounded-full mr-2"></span>
                      {feature}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default AnalysisSelection; 
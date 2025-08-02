import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './analytics.css';

const Analytics = () => {
  const [selectedCard, setSelectedCard] = useState(null);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const navigate = useNavigate();

  const handleCardClick = (cardType) => {
    setSelectedCard(cardType);
    
    setTimeout(() => {
      setShowConfirmation(true);
    }, 800);
  };

  const handleProceed = () => {
    navigate('/dashboard');
  };

  const getAnalysisName = (cardType) => {
    switch (cardType) {
      case 'boulder':
        return 'Boulder Detection Analysis';
      case 'landslide':
        return 'Landslide Detection Analysis';
      case 'combined':
        return 'Combined Surface Analysis';
      default:
        return 'Analysis';
    }
  };

  return (
    <div className="bg-gray-900 text-white overflow-x-hidden">
      {/* Main Content */}
      <main className="min-h-screen bg-gray-900">
        {/* Hero Section */}
        <section className="relative h-[300px] flex items-center justify-center overflow-hidden">
          <div className="absolute inset-0 moon-glow"></div>
          <div className="absolute top-10 right-20 w-32 h-32 rounded-full bg-gradient-to-br from-gray-200 to-gray-400 opacity-20"></div>
          <div className="absolute bottom-10 left-16 w-20 h-20 rounded-full bg-gradient-to-br from-blue-300 to-blue-500 opacity-10"></div>
          <div className="text-center z-10">
            <h2 className="text-5xl font-light mb-4 bg-gradient-to-r from-gray-200 to-blue-300 bg-clip-text text-transparent">
              Lunar Surface Analysis
            </h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Advanced detection systems for comprehensive lunar terrain monitoring and geological assessment
            </p>
          </div>
        </section>

        {/* Selection Section */}
        <section className="py-16 px-6">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <h3 className="text-3xl font-semibold mb-4 text-gray-200">Choose Analysis Type</h3>
              <p className="text-gray-400">Select your preferred detection method for lunar surface analysis</p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {/* Boulder Detection Card */}
              <div 
                className={`selection-card bg-gray-800 border-2 border-gray-700 rounded-2xl p-8 cursor-pointer transition-all duration-300 card-hover relative overflow-hidden ${
                  selectedCard === 'boulder' ? 'selected-card' : ''
                }`}
                onClick={() => handleCardClick('boulder')}
              >
                <div className="absolute top-0 right-0 w-24 h-24 rounded-full bg-gradient-to-br from-orange-400 to-red-500 opacity-10 -mr-12 -mt-12"></div>
                <div className="relative z-10">
                  <div className="w-16 h-16 bg-gradient-to-br from-orange-400 to-red-500 rounded-2xl flex items-center justify-center mb-6 glow-effect">
                    <i className="text-2xl text-white">
                      <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 512 512">
                        <path d="M256 32c12.5 0 24.1 6.4 30.8 17L503.4 394.4c5.6 8.9 8.6 19.2 8.6 29.7c0 30.9-25 55.9-55.9 55.9H55.9C25 480 0 455 0 424.1c0-10.5 3-20.8 8.6-29.7L225.2 49c6.6-10.6 18.3-17 30.8-17zm65 192L256 120.4 176.9 246.5l18.3 24.4c6.4 8.5 19.2 8.5 25.6 0l25.6-34.1c6-8.1 15.5-12.8 25.6-12.8h49z" />
                      </svg>
                    </i>
                  </div>
                  <h4 className="text-2xl font-semibold mb-4 text-gray-200">Boulder Detection</h4>
                  <p className="text-gray-400 mb-6 leading-relaxed">
                    Identify and analyze large rock formations and boulder fields across lunar terrain using advanced computer vision algorithms.
                  </p>
                  <div className="flex items-center text-orange-400 font-medium">
                    <span>Select Analysis</span>
                    <i className="ml-2">
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 448 512">
                        <path d="M438.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L338.8 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l306.7 0L233.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160z" />
                      </svg>
                    </i>
                  </div>
                </div>
              </div>

              {/* Landslide Detection Card */}
              <div 
                className={`selection-card bg-gray-800 border-2 border-gray-700 rounded-2xl p-8 cursor-pointer transition-all duration-300 card-hover relative overflow-hidden ${
                  selectedCard === 'landslide' ? 'selected-card' : ''
                }`}
                onClick={() => handleCardClick('landslide')}
              >
                <div className="absolute top-0 right-0 w-24 h-24 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 opacity-10 -mr-12 -mt-12"></div>
                <div className="relative z-10">
                  <div className="w-16 h-16 bg-gradient-to-br from-green-400 to-emerald-500 rounded-2xl flex items-center justify-center mb-6 glow-effect">
                    <i className="text-2xl text-white">
                      <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 576 512">
                        <path d="M264.5 5.2c14.9-6.9 32.1-6.9 47 0l218.6 101c8.5 3.9 13.9 12.4 13.9 21.8s-5.4 17.9-13.9 21.8l-218.6 101c-14.9 6.9-32.1 6.9-47 0L45.9 149.8C37.4 145.8 32 137.3 32 128s5.4-17.9 13.9-21.8L264.5 5.2zM476.9 209.6l53.2 24.6c8.5 3.9 13.9 12.4 13.9 21.8s-5.4 17.9-13.9 21.8l-218.6 101c-14.9 6.9-32.1 6.9-47 0L45.9 277.8C37.4 273.8 32 265.3 32 256s5.4-17.9 13.9-21.8l53.2-24.6 152 70.2c23.4 10.8 50.4 10.8 73.8 0l152-70.2zm-152 198.2l152-70.2 53.2 24.6c8.5 3.9 13.9 12.4 13.9 21.8s-5.4 17.9-13.9 21.8l-218.6 101c-14.9 6.9-32.1 6.9-47 0L45.9 405.8C37.4 401.8 32 393.3 32 384s5.4-17.9 13.9-21.8l53.2-24.6 152 70.2c23.4 10.8 50.4 10.8 73.8 0z" />
                      </svg>
                    </i>
                  </div>
                  <h4 className="text-2xl font-semibold mb-4 text-gray-200">Landslide Detection</h4>
                  <p className="text-gray-400 mb-6 leading-relaxed">
                    Monitor slope stability and detect potential landslide areas through geological pattern recognition and terrain analysis.
                  </p>
                  <div className="flex items-center text-green-400 font-medium">
                    <span>Select Analysis</span>
                    <i className="ml-2">
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 448 512">
                        <path d="M438.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L338.8 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l306.7 0L233.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160z" />
                      </svg>
                    </i>
                  </div>
                </div>
              </div>

              {/* Combined Analysis Card */}
              <div 
                className={`selection-card bg-gray-800 border-2 border-gray-700 rounded-2xl p-8 cursor-pointer transition-all duration-300 card-hover relative overflow-hidden ${
                  selectedCard === 'combined' ? 'selected-card' : ''
                }`}
                onClick={() => handleCardClick('combined')}
              >
                <div className="absolute top-0 right-0 w-24 h-24 rounded-full bg-gradient-to-br from-blue-400 to-indigo-500 opacity-10 -mr-12 -mt-12"></div>
                <div className="relative z-10">
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-2xl flex items-center justify-center mb-6 glow-effect">
                    <i className="text-2xl text-white">
                      <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 512 512">
                        <path d="M184 0c30.9 0 56 25.1 56 56V456c0 30.9-25.1 56-56 56c-28.9 0-52.7-21.9-55.7-50.1c-5.2 1.4-10.7 2.1-16.3 2.1c-35.3 0-64-28.7-64-64c0-7.4 1.3-14.6 3.6-21.2C21.4 367.4 0 338.2 0 304c0-31.9 18.7-59.5 45.8-72.3C37.1 220.8 32 207 32 192c0-30.7 21.6-56.3 50.4-62.6C80.8 123.9 80 118 80 112c0-29.9 20.6-55.1 48.3-62.1C131.3 21.9 155.1 0 184 0zM328 0c28.9 0 52.6 21.9 55.7 49.9c27.8 7 48.3 32.1 48.3 62.1c0 6-.8 11.9-2.4 17.4c28.8 6.2 50.4 31.9 50.4 62.6c0 15-5.1 28.8-13.8 39.7C493.3 244.5 512 272.1 512 304c0 34.2-21.4 63.4-51.6 74.8c2.3 6.6 3.6 13.8 3.6 21.2c0 35.3-28.7 64-64 64c-5.6 0-11.1-.7-16.3-2.1c-3 28.2-26.8 50.1-55.7 50.1c-30.9 0-56-25.1-56-56V56c0-30.9 25.1-56 56-56z" />
                      </svg>
                    </i>
                  </div>
                  <h4 className="text-2xl font-semibold mb-4 text-gray-200">Combined Analysis</h4>
                  <p className="text-gray-400 mb-6 leading-relaxed">
                    Comprehensive surface analysis combining both boulder and landslide detection for complete geological assessment.
                  </p>
                  <div className="flex items-center text-blue-400 font-medium">
                    <span>Select Analysis</span>
                    <i className="ml-2">
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 448 512">
                        <path d="M438.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L338.8 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l306.7 0L233.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160z" />
                      </svg>
                    </i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Confirmation Section */}
        {showConfirmation && (
          <section className="py-12 px-6">
            <div className="max-w-2xl mx-auto text-center">
              <div className="bg-gray-800 border border-gray-700 rounded-2xl p-8">
                <div className="w-20 h-20 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-full flex items-center justify-center mx-auto mb-6 pulse-animation">
                  <i className="text-3xl text-white">
                    <svg className="w-10 h-10" fill="currentColor" viewBox="0 0 448 512">
                      <path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z" />
                    </svg>
                  </i>
                </div>
                <h3 className="text-2xl font-semibold mb-4 text-gray-200">Analysis Initiated</h3>
                <p className="text-gray-400 mb-8">
                  {getAnalysisName(selectedCard)} has been initiated and is now processing lunar surface data...
                </p>
                <button 
                  onClick={handleProceed}
                  className="bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 px-8 py-3 rounded-xl font-medium transition-all duration-300 glow-effect"
                >
                  Proceed to Dashboard
                </button>
              </div>
            </div>
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 border-t border-gray-700 py-8">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-gray-400">© 2024 Lunar Analytics. Advanced surface detection technology.</p>
        </div>
      </footer>
    </div>
  );
};

export default Analytics; 
import React from 'react';
import { ANALYSIS_STEPS } from '../constants/constants';

const ProgressSteps = ({ currentStep, isAnalyzing }) => {
  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <div className="mb-6">
        <h3 className="text-xl font-semibold text-gray-100 mb-2">
          Analysis Progress
        </h3>
        <p className="text-gray-400 text-sm">
          Current step in the landslide detection workflow
        </p>
      </div>

      <div className="space-y-4">
        {ANALYSIS_STEPS.map((step, index) => {
          const isCompleted = index < currentStep;
          const isCurrent = index === currentStep;
          const isPending = index > currentStep;

          return (
            <div key={step.id} className="flex items-center space-x-4">
              {/* Step Icon */}
              <div className={`w-10 h-10 rounded-full flex items-center justify-center text-lg ${
                isCompleted
                  ? 'bg-green-500 text-white'
                  : isCurrent
                  ? 'bg-orange-500 text-white animate-pulse'
                  : 'bg-gray-600 text-gray-400'
              }`}>
                {isCompleted ? (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                ) : (
                  <span>{step.icon}</span>
                )}
              </div>

              {/* Step Content */}
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className={`text-sm font-medium ${
                      isCompleted
                        ? 'text-green-400'
                        : isCurrent
                        ? 'text-orange-400'
                        : 'text-gray-400'
                    }`}>
                      {step.name}
                    </h4>
                    <p className="text-xs text-gray-500 mt-1">
                      {step.description}
                    </p>
                  </div>
                  
                  {/* Status Indicator */}
                  {isCurrent && isAnalyzing && (
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-orange-500 rounded-full animate-ping"></div>
                      <span className="text-xs text-orange-400">Processing...</span>
                    </div>
                  )}
                </div>

                {/* Progress Bar */}
                {isCurrent && (
                  <div className="mt-2 w-full bg-gray-600 rounded-full h-1">
                    <div className="bg-orange-500 h-1 rounded-full animate-pulse" style={{ width: '60%' }}></div>
                  </div>
                )}
              </div>

              {/* Step Number */}
              <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium ${
                isCompleted
                  ? 'bg-green-500 text-white'
                  : isCurrent
                  ? 'bg-orange-500 text-white'
                  : 'bg-gray-600 text-gray-400'
              }`}>
                {step.id}
              </div>
            </div>
          );
        })}
      </div>

      {/* Overall Progress */}
      <div className="mt-6 pt-6 border-t border-gray-700">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-300">Overall Progress</span>
          <span className="text-sm font-medium text-gray-200">
            {Math.round((currentStep / ANALYSIS_STEPS.length) * 100)}%
          </span>
        </div>
        <div className="w-full bg-gray-600 rounded-full h-2">
          <div 
            className="bg-gradient-to-r from-orange-500 to-red-500 h-2 rounded-full transition-all duration-500"
            style={{ width: `${(currentStep / ANALYSIS_STEPS.length) * 100}%` }}
          ></div>
        </div>
      </div>

      {/* Current Status */}
      {isAnalyzing && (
        <div className="mt-4 p-3 bg-orange-500/10 border border-orange-500/20 rounded-lg">
          <div className="flex items-center space-x-3">
            <div className="w-4 h-4 border-2 border-orange-500 border-t-transparent rounded-full animate-spin"></div>
            <div>
              <p className="text-sm font-medium text-orange-400">
                {ANALYSIS_STEPS[currentStep]?.name}
              </p>
              <p className="text-xs text-orange-300">
                {ANALYSIS_STEPS[currentStep]?.description}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Completion Status */}
      {currentStep >= ANALYSIS_STEPS.length && (
        <div className="mt-4 p-3 bg-green-500/10 border border-green-500/20 rounded-lg">
          <div className="flex items-center space-x-3">
            <div className="w-4 h-4 bg-green-500 rounded-full flex items-center justify-center">
              <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div>
              <p className="text-sm font-medium text-green-400">Analysis Complete</p>
              <p className="text-xs text-green-300">All steps completed successfully</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProgressSteps; 
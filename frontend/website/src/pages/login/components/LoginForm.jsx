import React from 'react';
import { LOGIN_CONSTANTS, ICONS } from '../constants';

const LoginForm = ({ formData, errors, isLoading, isSuccess, serverError, handleInputChange, handleSubmit }) => {
  return (
    <form id="login-form" className="space-y-4 sm:space-y-6" onSubmit={handleSubmit}>
      <div id="username-field">
        <label className="block text-gray-300 font-inter font-medium mb-2 text-sm sm:text-base">
          <i className="mr-2 text-blue-400">
            <i className={ICONS.user}></i>
          </i>
          {LOGIN_CONSTANTS.content.login.missionId}
        </label>
        <input 
          type="text"
          name="missionId"
          value={formData.missionId}
          onChange={(e) => handleInputChange('missionId', e.target.value)}
          className={`w-full px-3 sm:px-4 py-2.5 sm:py-3 bg-gray-800/50 border rounded-lg text-white placeholder-gray-400 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/20 focus:outline-none transition-all duration-300 font-inter text-sm sm:text-base ${
            errors.missionId ? 'border-red-500' : 'border-gray-600'
          }`}
          placeholder="Enter your mission ID"
        />
        {errors.missionId && (
          <p className="text-red-400 text-xs sm:text-sm mt-1">{errors.missionId}</p>
        )}
      </div>

      <div id="password-field">
        <label className="block text-gray-300 font-inter font-medium mb-2 text-sm sm:text-base">
          <i className="mr-2 text-blue-400">
            <i className={ICONS.lock}></i>
          </i>
          {LOGIN_CONSTANTS.content.login.accessCode}
        </label>
        <input 
          type="password"
          name="accessCode"
          value={formData.accessCode}
          onChange={(e) => handleInputChange('accessCode', e.target.value)}
          className={`w-full px-3 sm:px-4 py-2.5 sm:py-3 bg-gray-800/50 border rounded-lg text-white placeholder-gray-400 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/20 focus:outline-none transition-all duration-300 font-inter text-sm sm:text-base ${
            errors.accessCode ? 'border-red-500' : 'border-gray-600'
          }`}
          placeholder="Enter access code"
        />
        {errors.accessCode && (
          <p className="text-red-400 text-xs sm:text-sm mt-1">{errors.accessCode}</p>
        )}
      </div>

      <div id="remember-section" className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-2 sm:space-y-0">
        <label className="flex items-center text-gray-300 font-inter text-sm sm:text-base">
          <input 
            type="checkbox"
            checked={formData.rememberMission}
            onChange={(e) => handleInputChange('rememberMission', e.target.checked)}
            className="mr-2 rounded bg-gray-800 border-gray-600 text-blue-400 focus:ring-blue-400"
          />
          {LOGIN_CONSTANTS.content.login.rememberMission}
        </label>
        <span className="text-blue-400 hover:text-blue-300 font-inter text-sm transition-colors cursor-pointer">
          {LOGIN_CONSTANTS.content.login.forgotCode}
        </span>
      </div>

      {serverError && (
        <div className="text-red-400 text-xs sm:text-sm font-inter text-center -mt-2">{serverError}</div>
      )}

      <button 
        id="login-button" 
        type="submit"
        disabled={isLoading}
        className={`w-full font-inter font-semibold py-2.5 sm:py-3 rounded-lg transition-all duration-300 transform hover:scale-[1.02] shadow-lg text-sm sm:text-base ${
          isSuccess 
            ? 'bg-green-500 text-white' 
            : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white'
        }`}
      >
        {isLoading ? (
          <>
            <i className="mr-2">
              <i className={`${ICONS.spinner} fa-spin`}></i>
            </i>
            Launching...
          </>
        ) : isSuccess ? (
          <>
            <i className="mr-2">
              <i className={ICONS.check}></i>
            </i>
            Mission Authorized
          </>
        ) : (
          <>
            <i className="mr-2">
              <i className={ICONS.rocket}></i>
            </i>
            {LOGIN_CONSTANTS.content.login.launchMission}
          </>
        )}
      </button>
    </form>
  );
};

export default LoginForm; 
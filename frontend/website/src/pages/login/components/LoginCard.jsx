import React from 'react';
import { LOGIN_CONSTANTS, ICONS } from '../constants';
import LoginForm from './LoginForm';
import MissionStatus from './MissionStatus';
import MissionInfo from './MissionInfo';

const LoginCard = ({ formData, errors, isLoading, isSuccess, serverError, handleInputChange, handleSubmit }) => {
  return (
    <div id="login-card" className="w-full">
      <div className="gradient-border backdrop-blur-md rounded-2xl p-4 sm:p-6 shadow-2xl">
        <div className="text-center mb-4 sm:mb-6">
          <div className="w-12 h-12 sm:w-16 sm:h-16 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center mx-auto mb-3 shadow-lg">
            <i className="text-white text-lg sm:text-xl">
              <i className={ICONS.moon}></i>
            </i>
          </div>
          <h2 className="font-orbitron text-xl sm:text-2xl font-bold text-white mb-1">
            {LOGIN_CONSTANTS.content.login.title}
          </h2>
          <p className="text-gray-300 font-inter text-xs sm:text-sm">
            {LOGIN_CONSTANTS.content.login.subtitle}
          </p>
        </div>

        <LoginForm 
          formData={formData}
          errors={errors}
          isLoading={isLoading}
          isSuccess={isSuccess}
          serverError={serverError}
          handleInputChange={handleInputChange}
          handleSubmit={handleSubmit}
        />

        <MissionStatus />
      </div>

      <MissionInfo />
    </div>
  );
};

export default LoginCard; 
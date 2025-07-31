import React from 'react';
import { LOGIN_CONSTANTS, ICONS } from '../constants';
import LoginForm from './LoginForm';
import MissionStatus from './MissionStatus';
import MissionInfo from './MissionInfo';

const LoginCard = ({ formData, errors, isLoading, isSuccess, handleInputChange, handleSubmit }) => {
  return (
    <div id="login-card" className="w-full max-w-md">
      <div className="gradient-border backdrop-blur-md rounded-2xl p-8 shadow-2xl">
        <div className="text-center mb-8">
          <div className="w-20 h-20 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
            <i className="text-white text-2xl">
              <i className={ICONS.moon}></i>
            </i>
          </div>
          <h2 className="font-orbitron text-3xl font-bold text-white mb-2">
            {LOGIN_CONSTANTS.content.login.title}
          </h2>
          <p className="text-gray-300 font-inter">
            {LOGIN_CONSTANTS.content.login.subtitle}
          </p>
        </div>

        <LoginForm 
          formData={formData}
          errors={errors}
          isLoading={isLoading}
          isSuccess={isSuccess}
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
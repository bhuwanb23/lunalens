import React from 'react';
import { LOGIN_CONSTANTS, ICONS } from '../constants';

const Header = () => {
  return (
    <div id="header" className="relative z-10 flex flex-col sm:flex-row sm:items-center sm:justify-between px-4 sm:px-8 py-4 sm:py-6 space-y-3 sm:space-y-0">
      <div className="flex items-center space-x-3 sm:space-x-4">
        <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-orange-400 to-red-500 rounded-lg flex items-center justify-center">
          <i className="text-white text-lg sm:text-xl">
            <i className={ICONS.rocket}></i>
          </i>
        </div>
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-white">
            {LOGIN_CONSTANTS.content.header.title}
          </h1>
          <p className="text-gray-300 text-xs sm:text-sm font-inter">
            {LOGIN_CONSTANTS.content.header.subtitle}
          </p>
        </div>
      </div>
      <div className="text-gray-300 font-inter text-xs sm:text-sm text-center sm:text-left">
        <i className="text-blue-400 mr-2">
          <i className={ICONS.globe}></i>
        </i>
        {LOGIN_CONSTANTS.content.header.missionControl}
      </div>
    </div>
  );
};

export default Header; 
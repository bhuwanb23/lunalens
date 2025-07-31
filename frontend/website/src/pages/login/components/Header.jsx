import React from 'react';
import { LOGIN_CONSTANTS, ICONS } from '../constants';

const Header = () => {
  return (
    <div id="header" className="relative z-10 flex items-center justify-between px-8 py-6">
      <div className="flex items-center space-x-4">
        <div className="w-12 h-12 bg-gradient-to-br from-orange-400 to-red-500 rounded-lg flex items-center justify-center">
          <i className="text-white text-xl">
            <i className={ICONS.rocket}></i>
          </i>
        </div>
        <div>
          <h1 className="font-orbitron text-2xl font-bold text-white">
            {LOGIN_CONSTANTS.content.header.title}
          </h1>
          <p className="text-gray-300 text-sm font-inter">
            {LOGIN_CONSTANTS.content.header.subtitle}
          </p>
        </div>
      </div>
      <div className="text-gray-300 font-inter text-sm">
        <i className="text-blue-400 mr-2">
          <i className={ICONS.globe}></i>
        </i>
        {LOGIN_CONSTANTS.content.header.missionControl}
      </div>
    </div>
  );
};

export default Header; 
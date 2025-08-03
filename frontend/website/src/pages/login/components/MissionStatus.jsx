import React from 'react';
import { LOGIN_CONSTANTS, ICONS } from '../constants';

const MissionStatus = () => {
  return (
    <div id="mission-status" className="mt-6 sm:mt-8 pt-4 sm:pt-6 border-t border-gray-700">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-center space-y-2 sm:space-y-0 sm:space-x-6 text-xs sm:text-sm">
        <div className="flex items-center justify-center sm:justify-start text-green-400">
          <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
          <span className="font-inter">{LOGIN_CONSTANTS.content.status.systemsOnline}</span>
        </div>
        <div className="flex items-center justify-center sm:justify-start text-blue-400">
          <i className="mr-2">
            <i className={ICONS.satellite}></i>
          </i>
          <span className="font-inter">{LOGIN_CONSTANTS.content.status.chandrayaan3}</span>
        </div>
      </div>
    </div>
  );
};

export default MissionStatus; 
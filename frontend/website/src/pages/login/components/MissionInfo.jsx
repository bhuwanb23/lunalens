import React from 'react';
import { LOGIN_CONSTANTS, ICONS } from '../constants';

const MissionInfo = () => {
  return (
    <div id="mission-info" className="mt-4 sm:mt-6 text-center">
      <p className="text-gray-400 font-inter text-xs sm:text-sm">
        {LOGIN_CONSTANTS.content.status.secureConnection}
      </p>
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-center mt-2 space-y-1 sm:space-y-0 sm:space-x-4 text-xs text-gray-500">
        <span className="flex items-center justify-center sm:justify-start">
          <i className="mr-1">
            <i className={ICONS.shield}></i>
          </i>
          {LOGIN_CONSTANTS.content.status.encrypted}
        </span>
        <span className="flex items-center justify-center sm:justify-start">
          <i className="mr-1">
            <i className={ICONS.clock}></i>
          </i>
          {LOGIN_CONSTANTS.content.status.monitoring}
        </span>
      </div>
    </div>
  );
};

export default MissionInfo; 
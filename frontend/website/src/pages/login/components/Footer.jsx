import React from 'react';
import { LOGIN_CONSTANTS, ICONS } from '../constants';

const Footer = () => {
  return (
    <div id="footer" className="relative z-10 p-4 sm:p-6 mt-auto">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between text-gray-400 text-xs sm:text-sm font-inter space-y-2 sm:space-y-0">
        <div className="flex flex-col sm:flex-row sm:items-center space-y-1 sm:space-y-0 sm:space-x-4 text-center sm:text-left">
          <span>{LOGIN_CONSTANTS.content.footer.copyright}</span>
          <span className="hidden sm:inline text-gray-600">|</span>
          <span>{LOGIN_CONSTANTS.content.footer.lunarExploration}</span>
        </div>
        <div className="flex items-center justify-center sm:justify-end space-x-2 sm:space-x-4">
          <i className="text-green-400">
            <i className={ICONS.wifi}></i>
          </i>
          <span>{LOGIN_CONSTANTS.content.status.connectedToDeepSpace}</span>
        </div>
      </div>
    </div>
  );
};

export default Footer; 
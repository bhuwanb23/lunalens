import React from 'react';
import { LOGIN_CONSTANTS, ICONS } from '../constants';

const Footer = () => {
  return (
    <div id="footer" className="absolute bottom-0 left-0 right-0 z-10 p-6">
      <div className="flex items-center justify-between text-gray-400 text-sm font-inter">
        <div className="flex items-center space-x-4">
          <span>{LOGIN_CONSTANTS.content.footer.copyright}</span>
          <span className="text-gray-600">|</span>
          <span>{LOGIN_CONSTANTS.content.footer.lunarExploration}</span>
        </div>
        <div className="flex items-center space-x-4">
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
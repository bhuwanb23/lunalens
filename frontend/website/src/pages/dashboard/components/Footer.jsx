import React from 'react';
import { FOOTER_DATA } from '../constants';

const Footer = () => {
  return (
    <footer className="bg-gray-900/80 backdrop-blur-lg border-t border-gray-700/50 py-6">
      <div className="container mx-auto px-6">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <div className="flex items-center space-x-4 mb-4 md:mb-0">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center">
              <i className="text-white text-sm">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 384 512">
                  <path d="M223.5 32C100 32 0 132.3 0 256S100 480 223.5 480c60.6 0 115.5-24.2 155.8-63.4c5-4.9 6.3-12.5 3.1-18.7s-10.1-9.7-17-8.5c-9.8 1.7-19.8 2.6-30.1 2.6c-96.9 0-175.5-78.8-175.5-176c0-65.8 36-123.1 89.3-153.3c6.1-3.5 9.2-10.5 7.7-17.3s-7.3-11.9-14.3-12.5c-6.3-.5-12.6-.8-19-.8z" />
                </svg>
              </i>
            </div>
            <span className="text-gray-400 orbitron">LunaLens AI • Lunar Surface Analysis Platform</span>
          </div>
          <div className="flex items-center space-x-6 text-sm text-gray-500">
            <span>Status: <span className="text-green-400">{FOOTER_DATA.status}</span></span>
            <span>Uptime: {FOOTER_DATA.uptime}</span>
            <span>Last Update: {FOOTER_DATA.lastUpdate}</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 
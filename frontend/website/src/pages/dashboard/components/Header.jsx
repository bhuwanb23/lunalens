import React from 'react';
import { useNavigate } from 'react-router-dom';
import { NAVIGATION_ITEMS } from '../constants';

const Header = ({ onLogout }) => {
  const navigate = useNavigate();
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-gray-900/80 backdrop-blur-lg border-b border-gray-700/50">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center glow">
            <i className="text-white text-lg">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 384 512">
                <path d="M223.5 32C100 32 0 132.3 0 256S100 480 223.5 480c60.6 0 115.5-24.2 155.8-63.4c5-4.9 6.3-12.5 3.1-18.7s-10.1-9.7-17-8.5c-9.8 1.7-19.8 2.6-30.1 2.6c-96.9 0-175.5-78.8-175.5-176c0-65.8 36-123.1 89.3-153.3c6.1-3.5 9.2-10.5 7.7-17.3s-7.3-11.9-14.3-12.5c-6.3-.5-12.6-.8-19-.8z" />
              </svg>
            </i>
          </div>
          <h1 className="text-2xl font-bold orbitron text-blue-300">LunaLens</h1>
        </div>
        
        <nav className="hidden md:flex items-center space-x-8">
          {NAVIGATION_ITEMS.map((item, index) => (
            <span
              key={index}
              className={`transition-colors cursor-pointer ${
                item.active 
                  ? 'text-blue-300 hover:text-blue-200' 
                  : 'text-gray-400 hover:text-blue-300'
              }`}
              onClick={() => {
                if (item.label === 'Analytics') {
                  navigate('/analytics');
                } else if (item.label === 'Boulder Detection') {
                  navigate('/boulder');
                }
              }}
            >
              {item.label}
            </span>
          ))}
        </nav>
        
        <div className="flex items-center space-x-4">
          <div className="w-8 h-8 bg-yellow-400 rounded-full pulse-glow"></div>
          <img 
            src="https://storage.googleapis.com/uxpilot-auth.appspot.com/avatars/avatar-2.jpg"
            className="w-10 h-10 rounded-full border-2 border-blue-400 glow"
            alt="User avatar"
          />
          {onLogout && (
            <button
              onClick={onLogout}
              className="text-gray-400 hover:text-red-400 transition-colors text-sm font-medium"
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header; 
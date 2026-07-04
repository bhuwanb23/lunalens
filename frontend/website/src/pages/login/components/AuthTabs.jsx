import { useState } from 'react';
import { LOGIN_CONSTANTS } from '../constants';

const AuthTabs = () => {
  const [activeTab, setActiveTab] = useState('signin');
  const [showComingSoon, setShowComingSoon] = useState(false);

  const handleTabClick = (tab) => {
    if (tab === 'signup') {
      setShowComingSoon(true);
      setTimeout(() => setShowComingSoon(false), 2000);
      return;
    }
    setShowComingSoon(false);
    setActiveTab(tab);
  };

  return (
    <div className="relative">
      <div className="flex bg-gray-100 rounded-xl p-1">
        <button
          type="button"
          onClick={() => handleTabClick('signin')}
          className={`flex-1 py-2.5 px-4 rounded-lg text-sm font-semibold transition-all duration-200 ${
            activeTab === 'signin'
              ? 'bg-white text-[#1A7A6D] shadow-sm'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          {LOGIN_CONSTANTS.content.login.signIn}
        </button>
        <button
          type="button"
          onClick={() => handleTabClick('signup')}
          className={`flex-1 py-2.5 px-4 rounded-lg text-sm font-semibold transition-all duration-200 ${
            activeTab === 'signup'
              ? 'bg-white text-[#1A7A6D] shadow-sm'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          {LOGIN_CONSTANTS.content.login.signUp}
        </button>
      </div>
      {showComingSoon && (
        <div className="absolute -bottom-7 left-0 right-0 text-center">
          <span className="text-xs text-[#6B7B8D]">{LOGIN_CONSTANTS.content.login.signUpComingSoon}</span>
        </div>
      )}
    </div>
  );
};

export default AuthTabs;

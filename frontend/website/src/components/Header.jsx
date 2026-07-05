import { useNavigate, useLocation } from 'react-router-dom';

const Header = ({ onLogout }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  const navItems = [
    { label: 'Dashboard', path: '/dashboard' },
    { label: 'Analytics', path: '/analytics' },
    { label: 'Boulder Detection', path: '/boulder' },
    { label: 'Landslide Detection', path: '/landslide' },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 px-4 pt-3">
      <div
        className="max-w-[1200px] mx-auto flex items-center justify-between px-5 py-3"
        style={{
          backgroundColor: '#1A1D26',
          borderRadius: '50px',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.15)',
        }}
      >
        {/* Logo */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => navigate('/dashboard')}>
          <div
            className="w-9 h-9 rounded-full flex items-center justify-center"
            style={{ background: 'linear-gradient(135deg, #3B82F6, #8B5CF6)' }}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
            </svg>
          </div>
          <span className="text-[17px] font-bold text-white">LunaLens</span>
        </div>

        {/* Navigation */}
        <nav className="hidden md:flex items-center gap-1 px-2 py-1.5 rounded-full" style={{ backgroundColor: 'rgba(255,255,255,0.08)' }}>
          {navItems.map((item) => (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className="px-4 py-2 rounded-full text-[13px] font-medium transition-all duration-200"
              style={{
                backgroundColor: isActive(item.path) ? '#E8E5E0' : 'transparent',
                color: isActive(item.path) ? '#1A1D26' : 'rgba(255,255,255,0.6)',
              }}
            >
              {item.label}
            </button>
          ))}
        </nav>

        {/* Right Side */}
        <div className="flex items-center gap-3">
          {/* User Avatar */}
          <button
            className="w-9 h-9 rounded-full flex items-center justify-center transition-colors"
            style={{ backgroundColor: 'rgba(255,255,255,0.1)' }}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
          </button>

          {/* Logout Button */}
          {onLogout && (
            <button
              onClick={onLogout}
              className="px-4 py-2 rounded-full text-[13px] font-medium transition-all duration-200"
              style={{
                backgroundColor: 'rgba(255,255,255,0.1)',
                color: 'rgba(255,255,255,0.8)',
              }}
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

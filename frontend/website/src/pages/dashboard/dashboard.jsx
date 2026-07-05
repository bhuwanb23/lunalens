import './dashboard.css';
import { DASHBOARD_DATA } from './constants';
import ProfileCard from './components/ProfileCard';
import GradientStatCard from './components/GradientStatCard';
import TrackersCard from './components/TrackersCard';
import TrendsChart from './components/TrendsChart';
import SessionsPanel from './components/SessionsPanel';
import ProgressPanel from './components/ProgressPanel';

const Dashboard = () => {
  const data = DASHBOARD_DATA;

  return (
    <div className="min-h-screen" style={{ backgroundColor: 'var(--bg-primary)' }}>
      <main className="pt-10 pb-12 px-4 sm:px-6 lg:px-8 max-w-[1400px] mx-auto">

        {/* Welcome Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-[22px] font-bold" style={{ color: 'var(--text-primary)' }}>
              Welcome, {data.user.name.split(' ')[0]}
            </h1>
            <p className="text-[14px]" style={{ color: 'var(--text-secondary)' }}>
              Your personal dashboard overview
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div className="search-bar">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ color: 'var(--text-muted)' }}>
                <circle cx="11" cy="11" r="8" />
                <path d="m21 21-4.35-4.35" />
              </svg>
              <input type="text" placeholder="Search" />
            </div>
            <button className="w-10 h-10 rounded-full flex items-center justify-center" style={{ backgroundColor: 'var(--bg-primary)', border: '1px solid var(--border)' }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ color: 'var(--text-secondary)' }}>
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                <circle cx="12" cy="7" r="4" />
              </svg>
            </button>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_340px] gap-6">

          {/* Left Column - Main Content */}
          <div className="space-y-6">

            {/* Top Row: Profile + Stat Cards */}
            <div className="grid grid-cols-1 md:grid-cols-[280px_1fr] gap-6">
              <ProfileCard user={data.user} />
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                {data.statCards.map((stat) => (
                  <GradientStatCard key={stat.id} stat={stat} />
                ))}
              </div>
            </div>

            {/* Trackers Connected */}
            <TrackersCard trackers={data.trackers} />

            {/* Trends Chart */}
            <TrendsChart trends={data.trends} />

          </div>

          {/* Right Column - Sidebar */}
          <div className="space-y-6">
            <SessionsPanel sessions={data.sessions} />
            <ProgressPanel progress={data.progress} />
          </div>

        </div>

      </main>
    </div>
  );
};

export default Dashboard;

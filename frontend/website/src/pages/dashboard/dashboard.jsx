import React from 'react';
import {
  Header,
  StatsCard,
  LunarAnalysis,
  AlertsPanel,
  QuickActions,
  RecentScans,
  Footer
} from './components';
import { DASHBOARD_DATA } from './constants';
import './dashboard.css';

const Dashboard = ({ onLogout }) => {
  return (
    <div className="bg-gray-900 text-gray-100 overflow-x-hidden">
      <Header onLogout={onLogout} />
      
      <main className="pt-20 lunar-surface min-h-screen">
        <div className="container mx-auto px-6 py-8">
          
          {/* Hero Stats Section */}
          <section className="mb-12">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {DASHBOARD_DATA.stats.map((stat, index) => (
                <StatsCard 
                  key={stat.id}
                  stat={stat}
                  animationClass={index % 2 === 0 ? 'floating' : 'floating-delayed'}
                />
              ))}
            </div>
          </section>

          {/* Main Content Section */}
          <section className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
            
            {/* Lunar Analysis Panel */}
            <div className="lg:col-span-2">
              <LunarAnalysis data={DASHBOARD_DATA.lunarAnalysis} />
            </div>

            {/* Sidebar Panels */}
            <div className="space-y-6">
              <AlertsPanel alerts={DASHBOARD_DATA.alerts} />
              <QuickActions actions={DASHBOARD_DATA.quickActions} />
            </div>
          </section>

          {/* Recent Scans Section */}
          <section className="mb-12">
            <RecentScans scans={DASHBOARD_DATA.recentScans} />
          </section>

        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Dashboard;

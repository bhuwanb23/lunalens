import React, { useState, useEffect } from 'react';
import {
  StatsCard,
  LunarAnalysis,
  AlertsPanel,
  QuickActions,
  RecentScans,
  Footer
} from './components';
import { DASHBOARD_DATA } from './constants';
import { apiUrl } from '../../config/api';
import './dashboard.css';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(DASHBOARD_DATA);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const token = localStorage.getItem('lunalens_token');
        const response = await fetch(apiUrl('/api/analytics/summary'), {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) throw new Error('Failed to fetch analytics');

        const result = await response.json();
        if (result.success && result.data) {
          const { total_analyses, total_users, recent_analyses } = result.data;

          setDashboardData(prev => ({
            ...prev,
            stats: prev.stats.map(stat => {
              switch (stat.id) {
                case 'crater-detection':
                  return { ...stat, value: String(total_analyses), subtitle: `${recent_analyses} this week` };
                case 'boulder-analysis':
                  return { ...stat, value: String(total_analyses), subtitle: 'Objects classified' };
                case 'model-status':
                  return { ...stat, subtitle: `${total_users} users registered` };
                default:
                  return stat;
              }
            })
          }));
        }
      } catch (err) {
        console.warn('Dashboard: using fallback data, API unavailable:', err.message);
      }
    };

    fetchAnalytics();
  }, []);

  return (
    <div className="bg-gray-900 text-gray-100 overflow-x-hidden">
      
      <main className="pt-20 lunar-surface min-h-screen">
        <div className="container mx-auto px-6 py-8">
          
          {/* Hero Stats Section */}
          <section className="mb-12">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {dashboardData.stats.map((stat, index) => (
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
              <LunarAnalysis data={dashboardData.lunarAnalysis} />
            </div>

            {/* Sidebar Panels */}
            <div className="space-y-6">
              <AlertsPanel alerts={dashboardData.alerts} />
              <QuickActions actions={dashboardData.quickActions} />
            </div>
          </section>

          {/* Recent Scans Section */}
          <section className="mb-12">
            <RecentScans scans={dashboardData.recentScans} />
          </section>

        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Dashboard;

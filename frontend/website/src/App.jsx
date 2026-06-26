import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/login';
import Dashboard from './pages/dashboard/dashboard';
import Analytics from './pages/analytics/analytics';
import Boulder from './pages/boulder/boulder';
import LandslideDetection from './pages/landslide/landslide';
import Header from './components/Header';
import ErrorBoundary from './components/ErrorBoundary';
import './App.css';

// Layout wrapper for authenticated pages
const AuthenticatedLayout = ({ children, onLogout }) => {
  return (
    <div className="min-h-screen bg-gray-900">
      <Header onLogout={onLogout} />
      <div className="pt-20">
        {children}
      </div>
    </div>
  );
};

// 404 Not Found page
const NotFound = () => (
  <div className="min-h-screen bg-gray-900 flex items-center justify-center">
    <div className="text-center">
      <h1 className="text-6xl font-bold text-blue-400 mb-4">404</h1>
      <p className="text-xl text-gray-400 mb-8">Page not found</p>
      <a
        href="/"
        className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
      >
        Go Home
      </a>
    </div>
  </div>
);

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('lunalens_token');
    if (token) {
      setIsAuthenticated(true);
    }
    setIsLoading(false);
  }, []);

  const handleLoginSuccess = (token) => {
    localStorage.setItem('lunalens_token', token);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('lunalens_token');
    setIsAuthenticated(false);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-blue-300 text-xl">Loading LunaLens...</div>
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <Router>
        <div className="App">
          <Routes>
            <Route
              path="/login"
              element={
                isAuthenticated ?
                <Navigate to="/dashboard" replace /> :
                <Login onLoginSuccess={handleLoginSuccess} />
              }
            />
            <Route
              path="/dashboard"
              element={
                isAuthenticated ?
                <AuthenticatedLayout onLogout={handleLogout}>
                  <Dashboard />
                </AuthenticatedLayout> :
                <Navigate to="/login" replace />
              }
            />
            <Route
              path="/analytics"
              element={
                isAuthenticated ?
                <AuthenticatedLayout onLogout={handleLogout}>
                  <Analytics />
                </AuthenticatedLayout> :
                <Navigate to="/login" replace />
              }
            />
            <Route
              path="/boulder"
              element={
                isAuthenticated ?
                <AuthenticatedLayout onLogout={handleLogout}>
                  <Boulder />
                </AuthenticatedLayout> :
                <Navigate to="/login" replace />
              }
            />
            <Route
              path="/landslide"
              element={
                isAuthenticated ?
                <AuthenticatedLayout onLogout={handleLogout}>
                  <LandslideDetection />
                </AuthenticatedLayout> :
                <Navigate to="/login" replace />
              }
            />
            <Route
              path="/"
              element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />}
            />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </Router>
    </ErrorBoundary>
  );
}

export default App

import React from 'react';
import { useLoginForm } from './hooks/useLoginForm';
import Header from './components/Header';
import Background from './components/Background';
import LoginCard from './components/LoginCard';
import Footer from './components/Footer';
import './login.css';

const Login = ({ onLoginSuccess }) => {
  const {
    formData,
    errors,
    isLoading,
    isSuccess,
    serverError,
    handleInputChange,
    handleSubmit
  } = useLoginForm(onLoginSuccess);

  return (
    <div id="main-container" className="relative h-screen w-full bg-gradient-to-br from-gray-900 via-blue-900 to-black">
      <Background />
      
      <Header />

      <div id="login-section" className="relative z-10 flex items-center justify-center h-full px-4 -mt-20">
        <LoginCard 
          formData={formData}
          errors={errors}
          isLoading={isLoading}
          isSuccess={isSuccess}
          serverError={serverError}
          handleInputChange={handleInputChange}
          handleSubmit={handleSubmit}
        />
      </div>

      <Footer />
    </div>
  );
};

export default Login;

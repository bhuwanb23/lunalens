import { useLoginForm } from './hooks/useLoginForm';
import LoginCard from './components/LoginCard';

const Login = ({ onLoginSuccess }) => {
  const {
    formData,
    errors,
    isLoading,
    isSuccess,
    serverError,
    showPassword,
    setShowPassword,
    handleInputChange,
    handleSubmit,
  } = useLoginForm(onLoginSuccess);

  return (
    <div className="flex h-screen overflow-hidden bg-black">
      {/* Background image covering entire viewport */}
      <div className="absolute inset-0 login-background opacity-40"></div>
      
      {/* Central card container */}
      <div className="relative z-10 w-full h-full flex items-center justify-center p-6 sm:p-12">
        <div className="w-full max-w-[1000px] bg-white rounded-2xl overflow-hidden shadow-2xl flex flex-col md:flex-row" style={{ minHeight: '550px' }}>
          {/* Left panel - Abstract wave image with text */}
          <div className="w-full md:w-1/2 relative login-card-left">
            {/* Light overlay for text readability while keeping waves visible */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent"></div>
            
            {/* Content */}
            <div className="relative z-10 h-full flex flex-col justify-between p-8 sm:p-10 text-white">
              {/* Quote label */}
              <div>
                <span className="text-xs font-semibold tracking-widest uppercase text-white/90">
                  A WISE QUOTE
                </span>
                <div className="w-12 h-0.5 bg-white/60 mt-2"></div>
              </div>
              
              {/* Quote content */}
              <div className="mt-auto">
                <h1 className="text-4xl sm:text-5xl font-bold leading-tight mb-4">
                  Get<br />
                  Everything<br />
                  You Want
                </h1>
                <p className="text-white/90 text-sm leading-relaxed max-w-xs">
                  You can get everything you want if you work hard, trust the process, and stick to the plan.
                </p>
              </div>
            </div>
          </div>
          
          {/* Right panel - Login form */}
          <div className="w-full md:w-1/2 bg-white p-8 sm:p-12 flex flex-col justify-center">
            <LoginCard
              formData={formData}
              errors={errors}
              isLoading={isLoading}
              isSuccess={isSuccess}
              serverError={serverError}
              handleInputChange={handleInputChange}
              handleSubmit={handleSubmit}
              showPassword={showPassword}
              setShowPassword={setShowPassword}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
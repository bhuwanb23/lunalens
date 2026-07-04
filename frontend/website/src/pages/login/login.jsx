import './login.css';
import { useLoginForm } from './hooks/useLoginForm';
import { LoginCard, LeftPanel } from './components';

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
    <div className="login-page">
      <div className="login-page-glow" />

      <div className="relative z-10 h-full flex items-center justify-center px-4 py-8 sm:px-6 sm:py-12 md:px-8">
        <div className="login-card">
          <LeftPanel />

          <div className="relative z-10 w-full md:w-1/2 bg-white flex flex-col justify-center">
            <div className="w-full max-w-[380px] mx-auto px-8 sm:px-12 py-10 sm:py-14">
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
    </div>
  );
};

export default Login;

import { useLoginForm } from './hooks/useLoginForm';
import LoginCard from './components/LoginCard';
import RightPanel from './components/RightPanel';

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
    <div className="flex h-screen overflow-hidden bg-[#F0F4F8]">
      <div className="w-full lg:w-1/2 h-screen overflow-y-auto flex items-center justify-center p-6 sm:p-8">
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
      <RightPanel />
    </div>
  );
};

export default Login;

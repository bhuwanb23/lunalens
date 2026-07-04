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
    <div className="flex min-h-screen bg-[#F0F4F8]">
      <div className="w-full lg:w-1/2 flex items-center justify-center p-6 sm:p-10">
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

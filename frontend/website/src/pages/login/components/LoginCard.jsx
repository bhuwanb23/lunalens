import { LOGIN_CONSTANTS } from '../constants';
import AuthTabs from './AuthTabs';
import LoginForm from './LoginForm';
import SocialLogin from './SocialLogin';
import Footer from './Footer';

const LoginCard = ({ formData, errors, isLoading, isSuccess, serverError, handleInputChange, handleSubmit, showPassword, setShowPassword }) => {
  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white rounded-2xl shadow-[0_4px_24px_rgba(0,0,0,0.08)] p-8 sm:p-10">
        <div className="text-center mb-8">
          <div className="w-12 h-12 bg-gradient-to-br from-[#1A7A6D] to-[#0D3B35] rounded-xl flex items-center justify-center mx-auto mb-4 shadow-lg">
            <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-[#1A2B3C] mb-1">
            {LOGIN_CONSTANTS.content.login.welcome}
          </h1>
          <p className="text-sm text-[#6B7B8D]">
            {LOGIN_CONSTANTS.content.login.subtitle}
          </p>
        </div>

        <div className="mb-6">
          <AuthTabs />
        </div>

        <div className="mb-6">
          <LoginForm
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

        <div className="relative mb-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-[#E2E8F0]"></div>
          </div>
          <div className="relative flex justify-center text-xs">
            <span className="bg-white px-4 text-[#9CA3AF]">{LOGIN_CONSTANTS.content.login.orContinueWith}</span>
          </div>
        </div>

        <SocialLogin />
      </div>

      <Footer />
    </div>
  );
};

export default LoginCard;

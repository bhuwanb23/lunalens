import { LOGIN_CONSTANTS } from '../constants';
import LoginForm from './LoginForm';
import SocialLogin from './SocialLogin';

const LoginCard = ({ formData, errors, isLoading, isSuccess, serverError, handleInputChange, handleSubmit, showPassword, setShowPassword }) => {
  return (
    <div className="w-full max-w-sm mx-auto">
      {/* Brand Logo */}
      <div className="text-center mb-8">
        <div className="w-10 h-10 bg-black rounded-xl flex items-center justify-center mx-auto mb-3">
          <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
          </svg>
        </div>
        <h1 className="text-xl font-bold text-[#1A2B3C]">
          {LOGIN_CONSTANTS.content.brand.name}
        </h1>
      </div>

      {/* Welcome heading */}
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-[#1A2B3C] mb-2">
          {LOGIN_CONSTANTS.content.login.welcome}
        </h2>
        <p className="text-sm text-[#6B7B8D]">
          {LOGIN_CONSTANTS.content.login.subtitle}
        </p>
      </div>

      {/* Login Form */}
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

      {/* Divider */}
      <div className="relative mb-6">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-[#E2E8F0]"></div>
        </div>
        <div className="relative flex justify-center text-xs">
          <span className="bg-white px-4 text-[#9CA3AF]">{LOGIN_CONSTANTS.content.login.orContinueWith}</span>
        </div>
      </div>

      {/* Social Login */}
      <SocialLogin />

      {/* Sign Up Link */}
      <div className="mt-8 text-center">
        <p className="text-sm text-[#6B7B8D]">
          {LOGIN_CONSTANTS.content.login.dontHaveAccount}{' '}
          <span className="font-semibold text-[#1A2B3C] hover:underline cursor-pointer">
            {LOGIN_CONSTANTS.content.login.signUp}
          </span>
        </p>
      </div>
    </div>
  );
};

export default LoginCard;
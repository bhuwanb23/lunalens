import { LOGIN_CONSTANTS } from '../constants';
import LoginForm from './LoginForm';
import SocialLogin from './SocialLogin';

const LoginCard = ({
  formData,
  errors,
  isLoading,
  isSuccess,
  serverError,
  handleInputChange,
  handleSubmit,
  showPassword,
  setShowPassword,
}) => {
  const { brand, login } = LOGIN_CONSTANTS.content;

  return (
    <div className="w-full">
      {/* Brand Logo */}
      <div className="flex items-center justify-center gap-2.5 mb-8">
        <div
          className="w-9 h-9 rounded-xl flex items-center justify-center"
          style={{ backgroundColor: 'var(--color-button)' }}
        >
          <svg
            className="w-[18px] h-[18px] text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
            />
          </svg>
        </div>
        <span className="text-[18px] font-bold" style={{ color: 'var(--color-text-primary)' }}>
          {brand.name}
        </span>
      </div>

      {/* Welcome Heading */}
      <div className="text-center mb-7">
        <h2
          className="text-[28px] font-bold leading-tight mb-2"
          style={{ color: 'var(--color-text-primary)' }}
        >
          {login.welcome}
        </h2>
        <p className="text-[14px]" style={{ color: 'var(--color-text-secondary)' }}>
          {login.subtitle}
        </p>
      </div>

      {/* Login Form */}
      <div>
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
      <div className="login-divider my-6">
        <span>{login.orContinueWith}</span>
      </div>

      {/* Social Login */}
      <div>
        <SocialLogin />
      </div>

      {/* Sign Up Link */}
      <div className="mt-7 text-center">
        <p className="text-[13px]" style={{ color: 'var(--color-text-secondary)' }}>
          {login.dontHaveAccount}{' '}
          <a href="#" className="login-link font-semibold" style={{ color: 'var(--color-text-primary)' }}>
            {login.signUp}
          </a>
        </p>
      </div>
    </div>
  );
};

export default LoginCard;

import { LOGIN_CONSTANTS } from '../constants';
import LoginForm from './LoginForm';
import SocialLogin from './SocialLogin';

const LunaLensLogo = () => (
  <svg width="36" height="36" viewBox="0 0 36 36" fill="none" aria-hidden="true">
    <circle cx="18" cy="18" r="17" stroke="#111827" strokeWidth="1.5" />
    <path
      d="M8 14c3 2 5 2 8 0s5-2 8 0M8 18c3 2 5 2 8 0s5-2 8 0M8 22c3 2 5 2 8 0s5-2 8 0"
      stroke="#111827"
      strokeWidth="1.5"
      strokeLinecap="round"
    />
  </svg>
);

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
      <div className="flex items-center justify-center gap-2.5 mb-8">
        <LunaLensLogo />
        <span className="text-[18px] font-bold text-[var(--color-text-primary)]">
          {brand.name}
        </span>
      </div>

      <div className="text-center mb-7">
        <h2 className="login-heading-serif text-[32px] leading-tight mb-2 text-[var(--color-text-primary)]">
          {login.welcome}
        </h2>
        <p className="text-[14px] text-[var(--color-text-secondary)]">
          {login.subtitle}
        </p>
      </div>

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

      <div className="animate-fade-in delay-400 mt-5">
        <SocialLogin />
      </div>

      <div className="animate-fade-in delay-500 mt-7 text-center">
        <p className="text-[13px] text-[var(--color-text-secondary)]">
          {login.dontHaveAccount}{' '}
          <a href="#" className="login-link font-semibold text-[var(--color-text-primary)]">
            {login.signUp}
          </a>
        </p>
      </div>
    </div>
  );
};

export default LoginCard;

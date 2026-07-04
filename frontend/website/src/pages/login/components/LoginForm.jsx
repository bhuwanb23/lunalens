import { LOGIN_CONSTANTS } from '../constants';

const MailIcon = () => (
  <svg className="w-5 h-5 text-[#9CA3AF]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
  </svg>
);

const LockIcon = () => (
  <svg className="w-5 h-5 text-[#9CA3AF]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
  </svg>
);

const EyeIcon = () => (
  <svg className="w-5 h-5 text-[#9CA3AF]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
    <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
);

const EyeSlashIcon = () => (
  <svg className="w-5 h-5 text-[#9CA3AF]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
  </svg>
);

const SpinnerIcon = () => (
  <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
  </svg>
);

const CheckIcon = () => (
  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
  </svg>
);

const LoginForm = ({ formData, errors, isLoading, isSuccess, serverError, handleInputChange, handleSubmit, showPassword, setShowPassword }) => {
  return (
    <form className="space-y-5" onSubmit={handleSubmit}>
      <div>
        <label className="block text-sm font-medium text-[#6B7B8D] mb-1.5">
          {LOGIN_CONSTANTS.content.login.emailLabel}
        </label>
        <div className="relative">
          <div className="absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none">
            <MailIcon />
          </div>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={(e) => handleInputChange('email', e.target.value)}
            placeholder={LOGIN_CONSTANTS.content.login.emailPlaceholder}
            className={`w-full pl-11 pr-4 py-3.5 bg-white border rounded-xl text-sm text-[#1A2B3C] placeholder-[#9CA3AF] transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-[#1A7A6D]/20 focus:border-[#1A7A6D] ${
              errors.email ? 'border-[#DC3545]' : 'border-[#E2E8F0]'
            }`}
          />
        </div>
        {errors.email && (
          <p className="text-xs text-[#DC3545] mt-1.5">{errors.email}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-[#6B7B8D] mb-1.5">
          {LOGIN_CONSTANTS.content.login.passwordLabel}
        </label>
        <div className="relative">
          <div className="absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none">
            <LockIcon />
          </div>
          <input
            type={showPassword ? 'text' : 'password'}
            name="password"
            value={formData.password}
            onChange={(e) => handleInputChange('password', e.target.value)}
            placeholder={LOGIN_CONSTANTS.content.login.passwordPlaceholder}
            className={`w-full pl-11 pr-11 py-3.5 bg-white border rounded-xl text-sm text-[#1A2B3C] placeholder-[#9CA3AF] transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-[#1A7A6D]/20 focus:border-[#1A7A6D] ${
              errors.password ? 'border-[#DC3545]' : 'border-[#E2E8F0]'
            }`}
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#9CA3AF] hover:text-[#6B7B8D] transition-colors"
            tabIndex={-1}
          >
            {showPassword ? <EyeSlashIcon /> : <EyeIcon />}
          </button>
        </div>
        {errors.password && (
          <p className="text-xs text-[#DC3545] mt-1.5">{errors.password}</p>
        )}
      </div>

      <div className="flex items-center justify-between">
        <label className="flex items-center gap-2 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={formData.rememberMe}
            onChange={(e) => handleInputChange('rememberMe', e.target.checked)}
            className="w-4 h-4 rounded border-[#E2E8F0] text-[#1A7A6D] focus:ring-[#1A7A6D]/20 focus:ring-2"
          />
          <span className="text-sm text-[#6B7B8D]">{LOGIN_CONSTANTS.content.login.rememberMe}</span>
        </label>
        <span className="text-sm font-medium text-[#1A7A6D] hover:text-[#0D3B35] cursor-pointer transition-colors">
          {LOGIN_CONSTANTS.content.login.forgotPassword}
        </span>
      </div>

      {serverError && (
        <div className="text-xs text-[#DC3545] text-center bg-red-50 rounded-lg py-2">{serverError}</div>
      )}

      <button
        type="submit"
        disabled={isLoading}
        className={`w-full py-3.5 rounded-xl text-sm font-semibold text-white transition-all duration-200 flex items-center justify-center gap-2 ${
          isSuccess
            ? 'bg-green-500'
            : 'bg-[#1A7A6D] hover:bg-[#0D3B35] active:scale-[0.98]'
        } disabled:opacity-70 disabled:cursor-not-allowed`}
      >
        {isLoading ? (
          <>
            <SpinnerIcon />
            {LOGIN_CONSTANTS.content.login.signingIn}
          </>
        ) : isSuccess ? (
          <>
            <CheckIcon />
            Authorized
          </>
        ) : (
          <>
            {LOGIN_CONSTANTS.content.login.signIn}
          </>
        )}
      </button>
    </form>
  );
};

export default LoginForm;

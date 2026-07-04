import { useLoginForm } from './hooks/useLoginForm';
import LoginCard from './components/LoginCard';
import { LOGIN_CONSTANTS } from './constants';

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

  const { leftPanel } = LOGIN_CONSTANTS.content;

  return (
    <div className="relative h-screen w-full overflow-hidden bg-[#0A0A0A]">
      {/* Full-viewport background image */}
      <div className="login-bg" />

      {/* Centered card container */}
      <div className="relative z-10 h-full flex items-center justify-center px-4 py-8 sm:px-6 sm:py-12 md:px-8">
        <div
          className="animate-fade-in-up w-full max-w-[1020px] bg-white overflow-hidden flex flex-col md:flex-row"
          style={{
            borderRadius: 'var(--radius-card)',
            boxShadow: 'var(--shadow-card)',
            minHeight: '580px',
          }}
        >
          {/* ==========================================
              LEFT PANEL - Wave Image + Quote
              ========================================== */}
          <div className="relative w-full md:w-[48%] hidden md:flex flex-col justify-between overflow-hidden">
            {/* Background image */}
            <div className="login-card-left-bg" />

            {/* Gradient overlay - bottom heavy for text readability */}
            <div
              className="absolute inset-0"
              style={{
                background: 'linear-gradient(to top, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0.3) 40%, transparent 70%)',
              }}
            />

            {/* Content */}
            <div className="relative z-10 flex flex-col justify-between h-full p-10 text-white">
              {/* Top: Quote label */}
              <div className="animate-fade-in delay-200">
                <span
                  className="inline-block text-[11px] font-semibold tracking-[0.2em] uppercase"
                  style={{ color: 'rgba(255,255,255,0.85)' }}
                >
                  {leftPanel.quoteLabel}
                </span>
                <div
                  className="mt-3 h-[2px] w-10"
                  style={{ background: 'rgba(255,255,255,0.5)' }}
                />
              </div>

              {/* Bottom: Quote text */}
              <div className="animate-fade-in delay-400">
                <h1 className="text-[42px] sm:text-[48px] font-extrabold leading-[1.05] tracking-tight mb-4">
                  <span className="block">{leftPanel.quoteHeading1}</span>
                  <span className="block">{leftPanel.quoteHeading2}</span>
                  <span className="block">{leftPanel.quoteHeading3}</span>
                </h1>
                <p
                  className="text-[13px] leading-relaxed max-w-[280px]"
                  style={{ color: 'rgba(255,255,255,0.8)' }}
                >
                  {leftPanel.quoteSubtitle}
                </p>
              </div>
            </div>
          </div>

          {/* ==========================================
              RIGHT PANEL - Login Form
              ========================================== */}
          <div className="w-full md:w-[52%] bg-white flex flex-col justify-center">
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

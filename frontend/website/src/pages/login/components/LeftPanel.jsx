import { LOGIN_CONSTANTS } from '../constants';

const LeftPanel = () => {
  const { leftPanel } = LOGIN_CONSTANTS.content;

  return (
    <div className="relative w-full md:w-1/2 hidden md:flex flex-col justify-between overflow-hidden">
      <div className="login-card-left-bg" />
      <div className="login-card-left-overlay" />

      <div className="relative z-10 flex flex-col justify-between h-full p-10 text-white">
        <div>
          <span className="inline-block text-[11px] font-semibold tracking-[0.2em] uppercase text-white/90">
            {leftPanel.quoteLabel}
          </span>
          <div className="mt-3 h-[2px] w-10 bg-white/60" />
        </div>

        <div>
          <h1 className="login-heading-serif text-[42px] leading-[1.08] mb-4">
            <span className="block">{leftPanel.quoteHeading1}</span>
            <span className="block">{leftPanel.quoteHeading2}</span>
            <span className="block">{leftPanel.quoteHeading3}</span>
          </h1>
          <p className="text-[13px] leading-relaxed max-w-[280px] text-white/85">
            {leftPanel.quoteSubtitle}
          </p>
        </div>
      </div>
    </div>
  );
};

export default LeftPanel;

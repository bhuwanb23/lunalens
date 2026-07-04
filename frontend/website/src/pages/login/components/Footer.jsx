import { LOGIN_CONSTANTS } from '../constants';

const Footer = () => {
  return (
    <div className="mt-6 text-center">
      <div className="flex items-center justify-center gap-3 text-xs text-[#9CA3AF] mb-2">
        <span>{LOGIN_CONSTANTS.content.footer.terms}</span>
        <span className="w-px h-3 bg-[#E2E8F0]"></span>
        <span>{LOGIN_CONSTANTS.content.footer.privacy}</span>
      </div>
      <p className="text-xs text-[#9CA3AF]">{LOGIN_CONSTANTS.content.footer.copyright}</p>
    </div>
  );
};

export default Footer;

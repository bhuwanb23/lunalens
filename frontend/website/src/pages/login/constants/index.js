export const LOGIN_CONSTANTS = {
  colors: {
    primary: '#1A7A6D',
    primaryDark: '#0D3B35',
    primaryLight: '#E8F5F3',
    textPrimary: '#1A2B3C',
    textSecondary: '#6B7B8D',
    textMuted: '#9CA3AF',
    border: '#E2E8F0',
    borderFocus: '#1A7A6D',
    error: '#DC3545',
    success: '#28A745',
  },

  content: {
    brand: {
      name: 'LunaLens',
      tagline: 'A Unified Hub for Satellite Data, Analytics & Monitoring',
      description: 'Access real-time satellite imagery, perform advanced analytics, and monitor geographic changes through an integrated mission control platform.',
    },
    login: {
      welcome: 'Welcome to LunaLens',
      subtitle: 'Sign in to access your mission control dashboard',
      emailLabel: 'Email Address',
      emailPlaceholder: 'Enter your email address',
      passwordLabel: 'Password',
      passwordPlaceholder: 'Enter your password',
      rememberMe: 'Remember me',
      forgotPassword: 'Forgot Password?',
      signIn: 'Sign In',
      signUp: 'Sign Up',
      signUpComingSoon: 'Sign up is coming soon',
      orContinueWith: 'Or continue with',
      signingIn: 'Signing in...',
    },
    footer: {
      copyright: '© 2024 LunaLens. All rights reserved.',
      terms: 'Term & Condition',
      privacy: 'Privacy & Policy',
    },
  },

  validation: {
    email: {
      required: 'Email is required',
      invalid: 'Please enter a valid email address',
    },
    password: {
      required: 'Password is required',
      minLength: 6,
      minLengthMessage: 'Password must be at least 6 characters',
      maxLength: 100,
    },
  },
};

export const ICONS = {
  mail: 'fas fa-envelope',
  lock: 'fas fa-lock',
  eye: 'fas fa-eye',
  eyeSlash: 'fas fa-eye-slash',
  google: 'fab fa-google',
  apple: 'fab fa-apple',
  facebook: 'fab fa-facebook-f',
  x: 'fab fa-x-twitter',
  spinner: 'fas fa-spinner',
  check: 'fas fa-check',
  arrowRight: 'fas fa-arrow-right',
};

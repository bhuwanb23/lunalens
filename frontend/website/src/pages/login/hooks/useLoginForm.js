import { useState } from 'react';
import { LOGIN_CONSTANTS } from '../constants';

export const useLoginForm = (onLoginSuccess) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false,
  });

  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [serverError, setServerError] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const validateEmail = (email) => {
    if (!email) return LOGIN_CONSTANTS.validation.email.required;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) return LOGIN_CONSTANTS.validation.email.invalid;
    return '';
  };

  const validatePassword = (password) => {
    if (!password) return LOGIN_CONSTANTS.validation.password.required;
    if (password.length < LOGIN_CONSTANTS.validation.password.minLength) {
      return LOGIN_CONSTANTS.validation.password.minLengthMessage;
    }
    return '';
  };

  const validateField = (name, value) => {
    if (name === 'email') return validateEmail(value);
    if (name === 'password') return validatePassword(value);
    return '';
  };

  const handleInputChange = (name, value) => {
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
    if (serverError) setServerError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const newErrors = {};
    Object.keys(formData).forEach(key => {
      if (key !== 'rememberMe') {
        const error = validateField(key, formData[key]);
        if (error) newErrors[key] = error;
      }
    });

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsLoading(true);
    setServerError('');
    setIsSuccess(false);

    try {
      // Mock login - simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Generate fake token and succeed
      const fakeToken = 'mock_token_' + Date.now();
      setIsSuccess(true);
      setErrors({});
      if (onLoginSuccess) {
        onLoginSuccess(fakeToken);
      }
    } catch {
      setIsSuccess(false);
      setServerError('Something went wrong.');
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({ email: '', password: '', rememberMe: false });
    setErrors({});
    setIsLoading(false);
    setIsSuccess(false);
    setServerError('');
    setShowPassword(false);
  };

  return {
    formData,
    errors,
    isLoading,
    isSuccess,
    serverError,
    showPassword,
    setShowPassword,
    handleInputChange,
    handleSubmit,
    resetForm,
  };
};

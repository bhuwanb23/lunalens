import { useState } from 'react';
import { LOGIN_CONSTANTS } from '../constants';
import { apiUrl } from '../../../config/api';

export const useLoginForm = (onLoginSuccess) => {
  const [formData, setFormData] = useState({
    missionId: '',
    accessCode: '',
    rememberMission: false
  });

  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [serverError, setServerError] = useState('');

  const validateField = (name, value) => {
    const validation = LOGIN_CONSTANTS.validation[name];
    if (!validation) return '';

    if (validation.required && !value) {
      return validation.required;
    }

    if (validation.minLength && value.length < validation.minLength) {
      return `${name === 'missionId' ? 'Mission ID' : 'Access code'} must be at least ${validation.minLength} characters`;
    }

    if (validation.maxLength && value.length > validation.maxLength) {
      return `${name === 'missionId' ? 'Mission ID' : 'Access code'} must be less than ${validation.maxLength} characters`;
    }

    return '';
  };

  const handleInputChange = (name, value) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
    if (serverError) setServerError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate all fields
    const newErrors = {};
    Object.keys(formData).forEach(key => {
      if (key !== 'rememberMission') {
        const error = validateField(key, formData[key]);
        if (error) {
          newErrors[key] = error;
        }
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
      const response = await fetch(apiUrl('/login'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          missionId: formData.missionId,
          accessCode: formData.accessCode,
        }),
      });

      const data = await response.json();
      if (response.ok && data.success) {
        setIsSuccess(true);
        setErrors({});
        // Call the success callback with the token
        if (onLoginSuccess && data.token) {
          onLoginSuccess(data.token);
        }
      } else {
        setIsSuccess(false);
        setServerError(data.message || 'Login failed.');
      }
    } catch {
      setIsSuccess(false);
      setServerError('Could not connect to server.');
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      missionId: '',
      accessCode: '',
      rememberMission: false
    });
    setErrors({});
    setIsLoading(false);
    setIsSuccess(false);
    setServerError('');
  };

  return {
    formData,
    errors,
    isLoading,
    isSuccess,
    serverError,
    handleInputChange,
    handleSubmit,
    resetForm
  };
}; 
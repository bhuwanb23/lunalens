import { useState } from 'react';
import { LOGIN_CONSTANTS } from '../constants';

export const useLoginForm = () => {
  const [formData, setFormData] = useState({
    missionId: '',
    accessCode: '',
    rememberMission: false
  });

  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

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
    
    // Simulate API call
    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      setIsSuccess(true);
      // Here you would typically make an API call to authenticate
      console.log('Login attempt:', formData);
    } catch (error) {
      console.error('Login error:', error);
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
  };

  return {
    formData,
    errors,
    isLoading,
    isSuccess,
    handleInputChange,
    handleSubmit,
    resetForm
  };
}; 
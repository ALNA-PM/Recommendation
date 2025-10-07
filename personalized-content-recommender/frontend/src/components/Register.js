import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Register = ({ countries = [], onRegister, onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    nationality: 'India'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [countriesLoaded, setCountriesLoaded] = useState(false);

  // Fallback countries list in case API fails
  const fallbackCountries = [
    'India', 'United States', 'United Kingdom', 'Canada', 'Australia',
    'Germany', 'France', 'Japan', 'South Korea', 'Brazil', 'Mexico',
    'Singapore', 'UAE', 'Thailand', 'Philippines', 'Indonesia', 'Vietnam',
    'Malaysia', 'Pakistan', 'Bangladesh', 'Sri Lanka', 'Nepal', 'China'
  ];

  const availableCountries = countries.length > 0 ? countries : fallbackCountries;

  useEffect(() => {
    if (countries.length > 0) {
      setCountriesLoaded(true);
    } else {
      // Fallback if countries prop is empty
      setCountriesLoaded(true);
    }
  }, [countries]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/register', formData);

      if (response.data.status === 'success') {
        onRegister(response.data);
      } else {
        setError(response.data.message || 'Registration failed');
      }
    } catch (error) {
      setError('Registration failed. Please try again.');
      console.error('Registration error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h2>🌟 Create Account</h2>

        {error && (
          <div className="error-message" style={{ 
            color: '#ef4444', 
            background: '#fef2f2', 
            padding: '0.75rem', 
            borderRadius: '6px', 
            marginBottom: '1rem',
            border: '1px solid #fecaca'
          }}>
            {error}
          </div>
        )}

        <div className="form-group">
          <label className="form-label">Username</label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            className="form-input"
            placeholder="Choose a username"
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Password</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className="form-input"
            placeholder="Create a password"
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Nationality</label>
          <select
            name="nationality"
            value={formData.nationality}
            onChange={handleChange}
            className="form-select"
            required
            style={{
              minHeight: '45px',
              fontSize: '16px',
              backgroundColor: 'white',
              border: '2px solid #e5e7eb',
              borderRadius: '8px',
              padding: '0.75rem',
              width: '100%'
            }}
          >
            <option value="" disabled>Select your country</option>
            {availableCountries.map((country) => (
              <option key={country} value={country}>
                {country}
              </option>
            ))}
          </select>

          {!countriesLoaded && (
            <p style={{ fontSize: '0.8rem', color: '#6b7280', marginTop: '0.25rem' }}>
              Loading countries...
            </p>
          )}
        </div>

        <div className="auth-actions">
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Creating Account...' : '📝 Sign Up'}
          </button>
        </div>

        <div className="auth-switch">
          <p>Already have an account? 
            <button type="button" onClick={onSwitchToLogin}>
              Login here
            </button>
          </p>
        </div>
      </form>
    </div>
  );
};

export default Register;
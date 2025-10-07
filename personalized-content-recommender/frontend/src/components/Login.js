import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ onLogin, onSwitchToRegister }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

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
      const response = await axios.post('/login', formData);

      if (response.data.status === 'success') {
        onLogin(response.data);
      } else {
        setError(response.data.message || 'Login failed');
      }
    } catch (error) {
      setError('Login failed. Please check your credentials.');
      console.error('Login error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h2>🚀 Welcome Back!</h2>

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
            placeholder="Enter your username"
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
            placeholder="Enter your password"
            required
          />
        </div>

        <div className="auth-actions">
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Logging in...' : '🔐 Login'}
          </button>
        </div>

        <div className="auth-switch">
          <p>Don't have an account? 
            <button type="button" onClick={onSwitchToRegister}>
              Sign up here
            </button>
          </p>
        </div>
      </form>
    </div>
  );
};

export default Login;
import React, { useState } from 'react';
import axios from 'axios';

const GenreSelector = ({ user, onComplete }) => {
  const [selectedInterests, setSelectedInterests] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const availableGenres = [
    '🎬 Entertainment', '💻 Technology', '⚽ Sports', '🎮 Gaming', 
    '📚 Education', '🏥 Health', '💼 Business', '✈️ Travel',
    '🍳 Food & Cooking', '👗 Fashion', '🎵 Music', '🎨 Art & Design',
    '📰 News', '🔬 Science', '🏋️ Fitness', '📱 Social Media',
    '🚗 Automotive', '🏠 Lifestyle', '💰 Finance', '🌱 Environment'
  ];

  const handleInterestToggle = (interest) => {
    setSelectedInterests(prev => {
      if (prev.includes(interest)) {
        return prev.filter(item => item !== interest);
      } else {
        return [...prev, interest];
      }
    });
  };

  const handleSubmit = async () => {
    if (selectedInterests.length === 0) {
      setError('Please select at least one interest');
      return;
    }

    if (selectedInterests.length > 10) {
      setError('Please select no more than 10 interests');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/set_interests', {
        username: user.username,
        interests: selectedInterests
      });

      if (response.data.status === 'success') {
        onComplete();
      } else {
        setError(response.data.message || 'Failed to save interests');
      }
    } catch (error) {
      setError('Failed to save interests. Please try again.');
      console.error('Set interests error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="genre-selector">
      <div className="genre-header">
        <h1>🎯 Choose Your Interests</h1>
        <h2>Hello {user.username}! 👋</h2>
        <p>Select the topics you're most interested in creating content about.</p>
        <p>This will help us provide personalized recommendations for <strong>{user.nationality}</strong></p>
      </div>

      {error && (
        <div className="error-message" style={{ 
          color: '#ef4444', 
          background: '#fef2f2', 
          padding: '0.75rem', 
          borderRadius: '6px', 
          marginBottom: '1rem',
          border: '1px solid #fecaca',
          textAlign: 'center'
        }}>
          {error}
        </div>
      )}

      <div className="selected-count">
        Selected: {selectedInterests.length}/10 interests
        {selectedInterests.length > 0 && (
          <span style={{ marginLeft: '1rem', color: '#6366f1' }}>
            ({selectedInterests.length} selected)
          </span>
        )}
      </div>

      <div className="genres-grid">
        {availableGenres.map((genre) => (
          <div
            key={genre}
            className={`genre-item ${selectedInterests.includes(genre) ? 'selected' : ''}`}
            onClick={() => handleInterestToggle(genre)}
          >
            <span>{genre}</span>
            {selectedInterests.includes(genre) && (
              <span style={{ marginLeft: '0.5rem' }}>✓</span>
            )}
          </div>
        ))}
      </div>

      {selectedInterests.length > 0 && (
        <div className="selected-interests" style={{ 
          margin: '2rem 0', 
          padding: '1rem', 
          background: '#f3f4f6', 
          borderRadius: '8px' 
        }}>
          <h3>Your Selected Interests:</h3>
          <div className="category-tags" style={{ marginTop: '0.5rem' }}>
            {selectedInterests.map((interest, index) => (
              <span key={index} className="category-tag" style={{ 
                background: '#6366f1', 
                color: 'white', 
                padding: '0.25rem 0.75rem', 
                borderRadius: '15px', 
                fontSize: '0.8rem', 
                margin: '0.25rem' 
              }}>
                {interest}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="genre-actions">
        <button
          onClick={handleSubmit}
          className="btn btn-primary"
          disabled={loading || selectedInterests.length === 0}
        >
          {loading ? 'Saving...' : '💾 Save Interests & Continue'}
        </button>
      </div>

      <div style={{ textAlign: 'center', marginTop: '1rem', color: '#6b7280' }}>
        <p>💡 Tip: Choose diverse interests for better content recommendations!</p>
      </div>
    </div>
  );
};

export default GenreSelector;
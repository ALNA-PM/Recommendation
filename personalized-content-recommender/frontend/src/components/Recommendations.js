import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Recommendations = ({ user, onViewPredictions }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedCategories, setSelectedCategories] = useState([]);

  useEffect(() => {
    fetchRecommendations();
  }, [user.username]);

  const fetchRecommendations = async () => {
    try {
      const response = await axios.get(`/recommendations/${user.username}`);

      if (response.data.status === 'success') {
        setRecommendations(response.data.recommendations);
      } else {
        setError(response.data.message || 'Failed to load recommendations');
      }
    } catch (error) {
      setError('Failed to load recommendations. Please try again.');
      console.error('Recommendations error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryToggle = (category) => {
    setSelectedCategories(prev => {
      if (prev.includes(category)) {
        return prev.filter(item => item !== category);
      } else {
        return [...prev, category];
      }
    });
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#f59e0b';
    return '#ef4444';
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': return '#10b981';
      case 'medium': return '#f59e0b';
      case 'hard': return '#ef4444';
      default: return '#6b7280';
    }
  };

  if (loading) {
    return (
      <div className="recommendations">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <h2>🔍 Finding perfect content ideas for you...</h2>
          <p>Analyzing your interests and {user.nationality} trends</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="recommendations">
        <div className="error-container">
          <h2>❌ Failed to Load Recommendations</h2>
          <p>{error}</p>
          <button onClick={fetchRecommendations} className="retry-button">
            🔄 Try Again
          </button>
        </div>
      </div>
    );
  }

  // Get unique categories from recommendations
  const availableCategories = [...new Set(recommendations.map(rec => rec.category))];

  return (
    <div className="recommendations">
      <div className="recommendations-header">
        <h1>🎯 Smart Content Recommendations</h1>
        <div className="user-summary">
          <h2>Welcome back, {user.username}! 🌟</h2>
          <p>Here are personalized content suggestions based on your interests in <strong>{user.nationality}</strong></p>

          {availableCategories.length > 0 && (
            <div className="category-selection" style={{ marginTop: '1.5rem' }}>
              <h3>📂 Select categories for AI predictions:</h3>
              <div className="category-tags" style={{ marginTop: '0.5rem' }}>
                {availableCategories.map((category) => (
                  <span
                    key={category}
                    className={`category-tag ${selectedCategories.includes(category) ? 'selected' : ''}`}
                    onClick={() => handleCategoryToggle(category)}
                    style={{
                      background: selectedCategories.includes(category) ? '#10b981' : 'rgba(255, 255, 255, 0.2)',
                      cursor: 'pointer',
                      transition: 'all 0.3s ease'
                    }}
                  >
                    {category} {selectedCategories.includes(category) ? '✓' : '+'}
                  </span>
                ))}
              </div>
              <p style={{ fontSize: '0.9rem', opacity: '0.8', marginTop: '0.5rem' }}>
                Selected: {selectedCategories.length} categories
              </p>
            </div>
          )}
        </div>
      </div>

      <div className="recommendations-grid">
        {recommendations.map((rec, index) => (
          <div key={index} className="recommendation-card">
            <div className="recommendation-title">
              💡 {rec.title}
            </div>

            <div className="recommendation-meta">
              <span className="meta-badge category-badge">
                📁 {rec.category}
              </span>
              <span 
                className="meta-badge score-badge"
                style={{ backgroundColor: getScoreColor(rec.viral_score) }}
              >
                🔥 {rec.viral_score}% Viral
              </span>
              <span 
                className="meta-badge difficulty-badge"
                style={{ backgroundColor: getDifficultyColor(rec.difficulty_level) }}
              >
                🎯 {rec.difficulty_level}
              </span>
            </div>

            <div className="recommendation-details">
              <p><strong>🌍 Trend:</strong> {rec.trend}</p>
              <p><strong>💪 Content Strength:</strong> {rec.content_strength}%</p>
              <p><strong>📈 Popularity:</strong> {rec.popularity_score}%</p>
              <p><strong>👁️ Est. Views:</strong> {rec.estimated_views}</p>
              <p><strong>💰 Monetization:</strong> {rec.monetization_potential}</p>
              <p><strong>⏰ Best Time:</strong> {rec.best_time_to_post}</p>
              <p><strong>🎯 Audience:</strong> {rec.target_audience}</p>
            </div>

            {rec.content_angles && (
              <div className="content-angles">
                <strong>💭 Content Ideas:</strong>
                <ul>
                  {rec.content_angles.map((angle, angleIndex) => (
                    <li key={angleIndex}>{angle}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="recommendations-actions">
        <button 
          onClick={() => onViewPredictions(selectedCategories)}
          className="btn btn-primary"
          disabled={selectedCategories.length === 0}
        >
          🤖 Get AI Predictions 
          {selectedCategories.length > 0 && ` (${selectedCategories.length} categories)`}
        </button>

        <button onClick={fetchRecommendations} className="btn btn-outline">
          🔄 Refresh Recommendations
        </button>
      </div>

      {selectedCategories.length === 0 && (
        <div style={{ 
          textAlign: 'center', 
          marginTop: '1rem', 
          padding: '1rem', 
          background: '#fef3cd', 
          borderRadius: '8px',
          color: '#856404'
        }}>
          💡 Select at least one category above to unlock AI-powered predictions!
        </div>
      )}
    </div>
  );
};

export default Recommendations;
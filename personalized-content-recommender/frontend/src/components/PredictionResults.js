import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PredictionResults = ({ user, onBack }) => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    generatePredictions();
  }, []);

  const generatePredictions = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/predict', {
        username: user.username,
        region: user.nationality,
        categories: user.selectedCategories || user.interests.slice(0, 3),
        state: user.nationality === 'India' ? 'Tamil Nadu' : null
      });

      if (response.data.status === 'success') {
        setPredictions(response.data.predictions);
      } else {
        setError(response.data.message);
      }
    } catch (error) {
      console.error('Prediction error:', error);
      setError('Failed to generate predictions. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#4CAF50'; // Green
    if (score >= 60) return '#FFC107'; // Yellow
    return '#FF5722'; // Red
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': return '#4CAF50';
      case 'moderate': return '#FFC107';
      case 'challenging': return '#FF9800';
      case 'expert': return '#F44336';
      default: return '#9E9E9E';
    }
  };

  if (loading) {
    return (
      <div className="prediction-results">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <h2>🤖 AI is generating your personalized predictions...</h2>
          <p>Analyzing trending topics and regional data for {user.nationality}</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="prediction-results">
        <div className="error-container">
          <h2>❌ Prediction Failed</h2>
          <p>{error}</p>
          <button onClick={generatePredictions} className="retry-button">
            🔄 Try Again
          </button>
          <button onClick={onBack} className="back-button">
            ← Back to Recommendations
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="prediction-results">
      <div className="prediction-header">
        <h1>🤖 AI-Powered Content Predictions</h1>
        <div className="user-summary">
          <h2>Welcome, {user.username}! 👋</h2>
          <p>Here are your personalized content predictions for <strong>{user.nationality}</strong></p>
          <div className="selected-categories">
            <h3>📂 Analysis Categories:</h3>
            <div className="category-tags">
              {(user.selectedCategories || user.interests.slice(0, 3)).map((category, index) => (
                <span key={index} className="category-tag">
                  {category}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="predictions-container">
        {predictions.length === 0 ? (
          <div className="no-predictions">
            <h3>📭 No predictions generated</h3>
            <p>Try selecting different categories or check your connection.</p>
          </div>
        ) : (
          predictions.map((prediction, index) => (
            <div key={index} className="prediction-card">
              <div className="prediction-header-card">
                <h3 className="prediction-title">
                  {index + 1}. {prediction.title}
                </h3>
                <div className="prediction-meta">
                  <span className="category-badge">{prediction.category}</span>
                  <span className="region-badge">📍 {prediction.region}</span>
                </div>
              </div>

              <div className="prediction-description">
                <p>{prediction.description}</p>
                <p><strong>Based on trend:</strong> {prediction.trend}</p>
              </div>

              <div className="prediction-metrics">
                <div className="metric-grid">
                  <div className="metric-item">
                    <span className="metric-label">🔥 Viral Score</span>
                    <div className="metric-value">
                      <div 
                        className="score-bar"
                        style={{ 
                          width: `${prediction.viral_score}%`,
                          backgroundColor: getScoreColor(prediction.viral_score)
                        }}
                      ></div>
                      <span>{prediction.viral_score}/100</span>
                    </div>
                  </div>

                  <div className="metric-item">
                    <span className="metric-label">💪 Content Strength</span>
                    <div className="metric-value">
                      <div 
                        className="score-bar"
                        style={{ 
                          width: `${prediction.content_strength}%`,
                          backgroundColor: getScoreColor(prediction.content_strength)
                        }}
                      ></div>
                      <span>{prediction.content_strength}/100</span>
                    </div>
                  </div>

                  <div className="metric-item">
                    <span className="metric-label">📊 Popularity Score</span>
                    <div className="metric-value">
                      <div 
                        className="score-bar"
                        style={{ 
                          width: `${prediction.popularity_score}%`,
                          backgroundColor: getScoreColor(prediction.popularity_score)
                        }}
                      ></div>
                      <span>{prediction.popularity_score}/100</span>
                    </div>
                  </div>

                  <div className="metric-item">
                    <span className="metric-label">❤️ Engagement Potential</span>
                    <div className="metric-value">
                      <div 
                        className="score-bar"
                        style={{ 
                          width: `${prediction.engagement_potential}%`,
                          backgroundColor: getScoreColor(prediction.engagement_potential)
                        }}
                      ></div>
                      <span>{prediction.engagement_potential}/100</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="prediction-details">
                <div className="detail-grid">
                  <div className="detail-item">
                    <span className="detail-label">👀 Estimated Views:</span>
                    <span className="detail-value">{prediction.estimated_views.toLocaleString()}</span>
                  </div>

                  <div className="detail-item">
                    <span className="detail-label">🏆 Difficulty:</span>
                    <span 
                      className="detail-value difficulty-badge"
                      style={{ backgroundColor: getDifficultyColor(prediction.difficulty_level) }}
                    >
                      {prediction.difficulty_level}
                    </span>
                  </div>

                  <div className="detail-item">
                    <span className="detail-label">💰 Monetization:</span>
                    <span className="detail-value">{prediction.monetization_potential}</span>
                  </div>

                  <div className="detail-item">
                    <span className="detail-label">🎭 Competition:</span>
                    <span className="detail-value">{prediction.competition_level}</span>
                  </div>

                  <div className="detail-item">
                    <span className="detail-label">⏰ Best Time:</span>
                    <span className="detail-value">{prediction.best_time_to_post}</span>
                  </div>

                  <div className="detail-item">
                    <span className="detail-label">📏 Length:</span>
                    <span className="detail-value">{prediction.content_length}</span>
                  </div>
                </div>

                <div className="target-audience">
                  <span className="detail-label">🎯 Target Audience:</span>
                  <p className="audience-text">{prediction.target_audience}</p>
                </div>

                <div className="confidence-score">
                  <span className="detail-label">🎯 AI Confidence:</span>
                  <div className="confidence-bar">
                    <div 
                      className="confidence-fill"
                      style={{ 
                        width: `${prediction.confidence_score}%`,
                        backgroundColor: getScoreColor(prediction.confidence_score)
                      }}
                    ></div>
                    <span className="confidence-text">{Math.round(prediction.confidence_score)}%</span>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="prediction-actions">
        <button onClick={onBack} className="back-button">
          ← Back to Recommendations
        </button>
        <button onClick={generatePredictions} className="refresh-button">
          🔄 Generate New Predictions
        </button>
      </div>
    </div>
  );
};

export default PredictionResults;
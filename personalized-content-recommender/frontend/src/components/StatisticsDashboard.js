import React, { useState, useEffect } from 'react';
import axios from 'axios';

const StatisticsDashboard = ({ user, onSkip, onContinue }) => {
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStatistics();
  }, [user.username]);

  const fetchStatistics = async () => {
    try {
      const response = await axios.get(`/statistics/${user.username}`);

      if (response.data.status === 'success') {
        setStatistics(response.data.statistics);
      } else {
        setError(response.data.message || 'Failed to load statistics');
      }
    } catch (error) {
      setError('Failed to load regional statistics');
      console.error('Statistics error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="statistics-dashboard">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading regional statistics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="statistics-dashboard">
        <div className="error-container">
          <h2>❌ Failed to Load Statistics</h2>
          <p>{error}</p>
          <div className="statistics-actions">
            <button onClick={onSkip} className="btn btn-secondary">
              Skip Statistics
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="statistics-dashboard">
      <div className="statistics-header">
        <h1>📊 Regional Trending Statistics</h1>
        <h2>Welcome {user.username}! 🎉</h2>
        <p>Here are the latest trending insights from <strong>{statistics?.region}</strong></p>
      </div>

      {statistics && (
        <div className="statistics-grid">
          <div className="stat-card">
            <h3>🔥 Trending Categories</h3>
            <div className="categories-chart">
              {Object.entries(statistics.trending_categories).map(([category, percentage]) => (
                <div key={category} className="category-bar" style={{ marginBottom: '0.5rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                    <span>{category}</span>
                    <span>{percentage}%</span>
                  </div>
                  <div style={{ background: '#e5e7eb', height: '8px', borderRadius: '4px' }}>
                    <div 
                      style={{ 
                        background: '#6366f1', 
                        height: '100%', 
                        width: `${percentage}%`, 
                        borderRadius: '4px',
                        transition: 'width 0.3s ease'
                      }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="stat-card">
            <h3>🎯 Trending Keywords</h3>
            <div className="trending-keywords">
              {statistics.trending_keywords.slice(0, 8).map((item, index) => (
                <span key={index} className="keyword-tag">
                  {item.keyword} ({item.frequency})
                </span>
              ))}
            </div>
          </div>

          <div className="stat-card">
            <h3>📈 Quick Stats</h3>
            <div style={{ fontSize: '1.1rem', lineHeight: '1.8' }}>
              <p><strong>Total Trending Topics:</strong> {statistics.total_trending_topics}</p>
              <p><strong>Region:</strong> {statistics.region}</p>
              <p><strong>Last Updated:</strong> {new Date(statistics.last_updated).toLocaleDateString()}</p>
            </div>
          </div>
        </div>
      )}

      <div className="statistics-actions">
        <button onClick={onSkip} className="btn btn-outline">
          ⏭️ Skip to Recommendations
        </button>
        <button onClick={onContinue} className="btn btn-primary">
          🚀 Continue to Recommendations
        </button>
      </div>
    </div>
  );
};

export default StatisticsDashboard;
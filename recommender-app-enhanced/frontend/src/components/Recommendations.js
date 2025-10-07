import React, { useState, useEffect } from "react";
import axios from "axios";
import { FaRocket, FaFire, FaEye, FaChartLine, FaClock, FaDollarSign } from "react-icons/fa";

export default function Recommendations({ username, userData }) {
  const [recommendations, setRecommendations] = useState([]);
  const [region, setRegion] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchRecommendations();
  }, [username]);

  const fetchRecommendations = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get(`http://localhost:5000/recommendations/${username}`);

      if (response.data.success) {
        setRecommendations(response.data.recommendations);
        setRegion(response.data.region);
        console.log("🎯 Recommendations loaded:", response.data);
      }
    } catch (err) {
      console.error("❌ Failed to fetch recommendations:", err);
      setError("Failed to load recommendations. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const getTrendingIcon = (score) => {
    if (score >= 80) return <FaRocket style={{ color: '#e74c3c' }} />;
    if (score >= 60) return <FaFire style={{ color: '#f39c12' }} />;
    if (score >= 40) return <FaChartLine style={{ color: '#3498db' }} />;
    return <FaEye style={{ color: '#95a5a6' }} />;
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': return '#27ae60';
      case 'medium': return '#f39c12';
      case 'hard': return '#e74c3c';
      default: return '#95a5a6';
    }
  };

  const getMonetizationColor = (potential) => {
    switch (potential.toLowerCase()) {
      case 'high': return '#27ae60';
      case 'medium': return '#f39c12';
      case 'low': return '#e74c3c';
      default: return '#95a5a6';
    }
  };

  if (isLoading) {
    return (
      <div className="recommendations-container">
        <div className="loading">Generating personalized recommendations...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="recommendations-container">
        <h2>Smart Recommendations</h2>
        <div className="error">{error}</div>
        <button onClick={fetchRecommendations}>Retry</button>
      </div>
    );
  }

  return (
    <div className="recommendations-container">
      <div className="recommendations-header">
        <h1>🎯 Your Personalized Content Recommendations</h1>
        <h3>Trending in {region} • Tailored for {username}</h3>
        <p style={{ color: '#666', fontSize: '16px', marginTop: '10px' }}>
          Smart suggestions based on regional trends and your interests
        </p>
      </div>

      {recommendations.length > 0 ? (
        <div className="recommendations-grid">
          {recommendations.map((rec) => (
            <div key={rec.id} className="recommendation-card">
              <div className="recommendation-title">
                {rec.title}
              </div>

              <div className="recommendation-meta">
                <span className="category-badge">
                  {rec.category}
                </span>
                <span className="trending-score">
                  {getTrendingIcon(rec.trending_factor)} {rec.trending_factor}/100
                </span>
              </div>

              <div className="recommendation-description">
                {rec.description}
              </div>

              <div className="content-angles">
                <h5>💡 Content Angle Ideas:</h5>
                <ul className="angles-list">
                  {rec.content_angles.slice(0, 3).map((angle, index) => (
                    <li key={index}>{angle}</li>
                  ))}
                </ul>
              </div>

              <div className="recommendation-stats">
                <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                  <FaEye />
                  <span>{rec.estimated_views?.toLocaleString() || 'N/A'} potential views</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                  <FaClock />
                  <span style={{ color: getDifficultyColor(rec.difficulty) }}>
                    {rec.difficulty} difficulty
                  </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                  <FaDollarSign />
                  <span style={{ color: getMonetizationColor(rec.monetization_potential) }}>
                    {rec.monetization_potential} monetization
                  </span>
                </div>
              </div>

              {rec.keywords && rec.keywords.length > 0 && (
                <div style={{ marginTop: '15px' }}>
                  <h5 style={{ fontSize: '12px', color: '#999', marginBottom: '8px' }}>
                    🏷️ Keywords:
                  </h5>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
                    {rec.keywords.map((keyword, index) => (
                      <span 
                        key={index}
                        style={{
                          background: '#f8f9fa',
                          color: '#666',
                          padding: '3px 8px',
                          borderRadius: '12px',
                          fontSize: '11px',
                          border: '1px solid #e1e5e9'
                        }}
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {rec.original_trend && (
                <div style={{ 
                  marginTop: '15px', 
                  padding: '10px', 
                  background: '#f8f9fa', 
                  borderRadius: '8px',
                  fontSize: '12px',
                  color: '#666'
                }}>
                  <strong>📈 Based on:</strong> {rec.original_trend}
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <h3>No recommendations available</h3>
          <p style={{ color: '#666' }}>
            Try updating your interests or check back later for new trending topics.
          </p>
        </div>
      )}

      <div style={{ marginTop: '40px', padding: '25px', background: '#f8f9fa', borderRadius: '15px' }}>
        <h4>🚀 How to Use These Recommendations</h4>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginTop: '20px' }}>
          <div>
            <h5 style={{ color: '#667eea', marginBottom: '10px' }}>📝 Content Planning</h5>
            <ul style={{ margin: 0, paddingLeft: '20px', color: '#666', fontSize: '14px' }}>
              <li>Use suggested titles as inspiration</li>
              <li>Adapt content angles to your style</li>
              <li>Combine multiple angles for series</li>
            </ul>
          </div>
          <div>
            <h5 style={{ color: '#667eea', marginBottom: '10px' }}>🎯 Optimization</h5>
            <ul style={{ margin: 0, paddingLeft: '20px', color: '#666', fontSize: '14px' }}>
              <li>Include trending keywords in titles</li>
              <li>Focus on high-potential topics first</li>
              <li>Consider difficulty vs. your resources</li>
            </ul>
          </div>
          <div>
            <h5 style={{ color: '#667eea', marginBottom: '10px' }}>💰 Monetization</h5>
            <ul style={{ margin: 0, paddingLeft: '20px', color: '#666', fontSize: '14px' }}>
              <li>Prioritize high monetization topics</li>
              <li>Build audience with trending content</li>
              <li>Create series around popular themes</li>
            </ul>
          </div>
        </div>
      </div>

      <div style={{ textAlign: 'center', marginTop: '30px' }}>
        <button onClick={fetchRecommendations} className="secondary-button">
          🔄 Refresh Recommendations
        </button>
      </div>

      <div style={{ textAlign: 'center', marginTop: '20px', fontSize: '14px', color: '#888' }}>
        Recommendations updated based on real-time trends • Region: {region} • Personalized for your interests
      </div>
    </div>
  );
}

import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

export default function StatisticsDashboard({ username, onComplete, onSkip }) {
  const [statistics, setStatistics] = useState(null);
  const [trendingKeywords, setTrendingKeywords] = useState([]);
  const [region, setRegion] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchStatistics();
  }, [username]);

  const fetchStatistics = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get(`http://localhost:5000/statistics/${username}`);

      if (response.data.success) {
        setStatistics(response.data.statistics);
        setTrendingKeywords(response.data.trending_keywords);
        setRegion(response.data.region);
        console.log("📊 Statistics loaded:", response.data);
      }
    } catch (err) {
      console.error("❌ Failed to fetch statistics:", err);
      setError("Failed to load trending statistics. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const getCategoryChartData = () => {
    if (!statistics || !statistics.categories) return null;

    const categories = Object.keys(statistics.categories);
    const counts = Object.values(statistics.categories);

    return {
      labels: categories,
      datasets: [
        {
          label: 'Trending Topics by Category',
          data: counts,
          backgroundColor: [
            '#667eea',
            '#764ba2',
            '#f093fb',
            '#f5576c',
            '#4facfe',
            '#00f2fe',
            '#43e97b',
            '#38f9d7',
            '#ffecd2',
            '#fcb69f'
          ],
          borderColor: [
            '#5a67d8',
            '#6b46c1',
            '#ec4899',
            '#ef4444',
            '#3b82f6',
            '#06b6d4',
            '#10b981',
            '#14b8a6',
            '#f59e0b',
            '#f97316'
          ],
          borderWidth: 2
        }
      ]
    };
  };

  const getKeywordChartData = () => {
    if (!trendingKeywords || trendingKeywords.length === 0) return null;

    const keywords = trendingKeywords.slice(0, 10).map(([keyword]) => keyword.charAt(0).toUpperCase() + keyword.slice(1));
    const counts = trendingKeywords.slice(0, 10).map(([, count]) => count);

    return {
      labels: keywords,
      datasets: [
        {
          label: 'Keyword Mentions',
          data: counts,
          backgroundColor: 'rgba(102, 126, 234, 0.6)',
          borderColor: '#667eea',
          borderWidth: 2
        }
      ]
    };
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Trending Content Analysis'
      }
    }
  };

  if (isLoading) {
    return (
      <div className="statistics-container">
        <div className="loading">Loading trending statistics for your region...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="statistics-container">
        <h2>Statistics Dashboard</h2>
        <div className="error">{error}</div>
        <div className="action-buttons">
          <button onClick={fetchStatistics}>Retry</button>
          <button onClick={onSkip} className="skip-button">Skip for Now</button>
        </div>
      </div>
    );
  }

  return (
    <div className="statistics-container">
      <div className="statistics-header">
        <h1>📊 Trending Content Statistics</h1>
        <h3>Regional Analysis for {region}</h3>
        <p style={{ color: '#666', fontSize: '16px', marginTop: '10px' }}>
          Discover what's trending in your region to create engaging content
        </p>
      </div>

      {statistics && (
        <div className="statistics-grid">
          <div className="stat-card">
            <h4>📈 Content Categories</h4>
            <div className="chart-container">
              {getCategoryChartData() && (
                <Doughnut 
                  data={getCategoryChartData()} 
                  options={{
                    ...chartOptions,
                    plugins: {
                      ...chartOptions.plugins,
                      title: {
                        display: true,
                        text: 'Popular Content Categories'
                      }
                    }
                  }} 
                />
              )}
            </div>
            <div style={{ textAlign: 'center', marginTop: '15px' }}>
              <strong>{statistics.total_trends}</strong> trending topics analyzed
            </div>
          </div>

          <div className="stat-card">
            <h4>🔥 Trending Keywords</h4>
            <div className="chart-container">
              {getKeywordChartData() && (
                <Bar 
                  data={getKeywordChartData()} 
                  options={{
                    ...chartOptions,
                    plugins: {
                      ...chartOptions.plugins,
                      title: {
                        display: true,
                        text: 'Most Mentioned Keywords'
                      }
                    }
                  }} 
                />
              )}
            </div>
          </div>
        </div>
      )}

      {trendingKeywords && trendingKeywords.length > 0 && (
        <div className="trending-keywords">
          <h4>🏷️ Hot Keywords in {region}</h4>
          <div className="keyword-tags">
            {trendingKeywords.slice(0, 12).map(([keyword, count]) => (
              <div key={keyword} className="keyword-tag">
                {keyword.charAt(0).toUpperCase() + keyword.slice(1)} ({count})
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={{ marginTop: '40px', padding: '25px', background: '#f8f9fa', borderRadius: '15px' }}>
        <h4>💡 Key Insights for Content Creators</h4>
        <ul style={{ margin: '15px 0', paddingLeft: '20px', color: '#666' }}>
          <li>Focus on the most popular categories in your region</li>
          <li>Incorporate trending keywords into your content titles</li>
          <li>Create content around emerging topics early for better reach</li>
          <li>Consider regional preferences when planning your content strategy</li>
        </ul>
      </div>

      <div className="action-buttons">
        <button onClick={onComplete}>
          Continue to Interest Selection
        </button>
        <button onClick={onSkip} className="skip-button">
          Skip Dashboard
        </button>
      </div>

      <div style={{ textAlign: 'center', marginTop: '20px', fontSize: '14px', color: '#888' }}>
        Data refreshed in real-time • Regional analysis • Smart recommendations ahead
      </div>
    </div>
  );
}

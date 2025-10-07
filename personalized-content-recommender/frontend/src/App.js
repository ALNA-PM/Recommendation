import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Login from './components/Login';
import Register from './components/Register';
import StatisticsDashboard from './components/StatisticsDashboard';
import GenreSelector from './components/GenreSelector';
import Recommendations from './components/Recommendations';
import PredictionResults from './components/PredictionResults';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('login');
  const [user, setUser] = useState(null);
  const [countries, setCountries] = useState([]);
  const [loading] = useState(false); // if unused


  useEffect(() => {
    fetchCountries();
  }, []);

  const fetchCountries = async () => {
    try {
      const response = await axios.get('/countries');
      if (response.data.status === 'success') {
        setCountries(response.data.countries);
      }
    } catch (error) {
      console.error('Failed to fetch countries:', error);
    }
  };

  const handleLogin = (userData) => {
    setUser(userData);
    if (userData.profile_completed) {
      setCurrentView('statistics');
    } else {
      setCurrentView('genreSelector');
    }
  };

  const handleRegister = (userData) => {
    setUser(userData);
    setCurrentView('statistics');
  };

  const handleInterestsComplete = () => {
    setCurrentView('statistics');
  };

  const handleSkipStatistics = () => {
    setCurrentView('recommendations');
  };

  const handleViewRecommendations = () => {
    setCurrentView('recommendations');
  };

  const handleViewPredictions = (selectedCategories) => {
    setUser({ ...user, selectedCategories });
    setCurrentView('predictions');
  };

  const renderCurrentView = () => {
    switch (currentView) {
      case 'login':
        return (
          <Login 
            onLogin={handleLogin} 
            onSwitchToRegister={() => setCurrentView('register')}
          />
        );
      case 'register':
        return (
          <Register 
            countries={countries}
            onRegister={handleRegister} 
            onSwitchToLogin={() => setCurrentView('login')}
          />
        );
      case 'statistics':
        return (
          <StatisticsDashboard 
            user={user}
            onSkip={handleSkipStatistics}
            onContinue={handleViewRecommendations}
          />
        );
      case 'genreSelector':
        return (
          <GenreSelector 
            user={user}
            onComplete={handleInterestsComplete}
          />
        );
      case 'recommendations':
        return (
          <Recommendations 
            user={user}
            onViewPredictions={handleViewPredictions}
          />
        );
      case 'predictions':
        return (
          <PredictionResults 
            user={user}
            onBack={() => setCurrentView('recommendations')}
          />
        );
      default:
        return <Login onLogin={handleLogin} onSwitchToRegister={() => setCurrentView('register')} />;
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1>🚀 Personalized Content Recommender</h1>
          <p>AI-Powered Content Suggestions for Creators</p>
          {user && (
            <div className="user-info">
              <span>👤 {user.username}</span>
              <span>🌍 {user.nationality}</span>
            </div>
          )}
        </div>
      </header>

      <main className="app-main">
        {loading && (
          <div className="loading-overlay">
            <div className="loading-spinner"></div>
            <p>Loading...</p>
          </div>
        )}
        {renderCurrentView()}
      </main>

      <footer className="app-footer">
        <p>© 2025 Personalized Content Recommender - AI Powered</p>
      </footer>
    </div>
  );
}

export default App;
import React, { useState, useEffect } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import StatisticsDashboard from "./components/StatisticsDashboard";
import GenreSelector from "./components/GenreSelector";
import Recommendations from "./components/Recommendations";
import axios from "axios";

function App() {
  const [page, setPage] = useState("login");
  const [loggedInUser, setLoggedInUser] = useState("");
  const [userData, setUserData] = useState({});
  const [apiStatus, setApiStatus] = useState("checking");

  useEffect(() => {
    checkApiStatus();
  }, []);

  const checkApiStatus = async () => {
    try {
      const response = await axios.get("http://localhost:5000/");
      if (response.data.status === "connected") {
        setApiStatus("connected");
        console.log("✅ Enhanced Backend API connected");
      } else {
        setApiStatus("disconnected");
      }
    } catch (error) {
      setApiStatus("error");
      console.error("❌ Backend API connection failed:", error);
    }
  };

  const handleSuccessfulLogin = (username, userData) => {
    setLoggedInUser(username);
    setUserData(userData);

    if (userData.profile_completed) {
      // If profile is completed, go to recommendations
      setPage("recommendations");
    } else if (userData.viewed_statistics) {
      // If seen statistics but not completed profile, go to interests
      setPage("genre");
    } else {
      // New user, show statistics first
      setPage("statistics");
    }
  };

  const handleSuccessfulRegistration = (username) => {
    setLoggedInUser(username);
    // After registration, always show statistics first
    setPage("statistics");
  };

  const handleStatisticsComplete = () => {
    setPage("genre");
  };

  const handleInterestsSet = () => {
    setPage("recommendations");
  };

  if (apiStatus === "checking") {
    return (
      <div className="app">
        <div className="loading-container">
          <div className="loading">Connecting to enhanced backend...</div>
        </div>
      </div>
    );
  }

  if (apiStatus === "error" || apiStatus === "disconnected") {
    return (
      <div className="app">
        <div className="error-container">
          <h2>Connection Error</h2>
          <p>Unable to connect to the enhanced backend API.</p>
          <p>Please ensure MongoDB is running and the backend server is started.</p>
          <button onClick={checkApiStatus}>Retry Connection</button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      {page === "login" && (
        <Login 
          setPage={setPage} 
          onSuccessfulLogin={handleSuccessfulLogin}
        />
      )}
      {page === "register" && (
        <Register 
          setPage={setPage}
          onSuccessfulRegistration={handleSuccessfulRegistration}
        />
      )}
      {page === "statistics" && (
        <StatisticsDashboard 
          username={loggedInUser}
          onComplete={handleStatisticsComplete}
          onSkip={handleStatisticsComplete}
        />
      )}
      {page === "genre" && (
        <GenreSelector 
          username={loggedInUser} 
          onInterestsSet={handleInterestsSet}
        />
      )}
      {page === "recommendations" && (
        <Recommendations 
          username={loggedInUser}
          userData={userData}
        />
      )}
    </div>
  );
}

export default App;

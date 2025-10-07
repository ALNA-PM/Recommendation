import React, { useState, useEffect } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import GenreSelector from "./components/GenreSelector";
import WelcomePage from "./components/WelcomePage";
import axios from "axios";

function App() {
  const [page, setPage] = useState("login");
  const [loggedInUser, setLoggedInUser] = useState("");
  const [userInterests, setUserInterests] = useState({});
  const [apiStatus, setApiStatus] = useState("checking");

  useEffect(() => {
    checkApiStatus();
  }, []);

  const checkApiStatus = async () => {
    try {
      const response = await axios.get("http://localhost:5000/");
      if (response.data.status === "connected") {
        setApiStatus("connected");
        console.log("✅ Backend API connected to database");
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
    if (userData.interests && Object.keys(userData.interests).length > 0) {
      setUserInterests(userData.interests);
      setPage("welcome");
    } else {
      setPage("genre");
    }
  };

  const handleInterestsSet = (genres, allInterests) => {
    setUserInterests(allInterests);
    setPage("welcome");
  };

  if (apiStatus === "checking") {
    return (
      <div className="app">
        <div className="loading-container">
          <div className="loading">Connecting to database...</div>
        </div>
      </div>
    );
  }

  if (apiStatus === "error" || apiStatus === "disconnected") {
    return (
      <div className="app">
        <div className="error-container">
          <h2>Connection Error</h2>
          <p>Unable to connect to the backend API.</p>
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
        <Register setPage={setPage} />
      )}
      {page === "genre" && (
        <GenreSelector 
          username={loggedInUser} 
          onInterestsSet={handleInterestsSet}
        />
      )}
      {page === "welcome" && (
        <WelcomePage 
          username={loggedInUser}
          interests={userInterests}
        />
      )}
    </div>
  );
}

export default App;

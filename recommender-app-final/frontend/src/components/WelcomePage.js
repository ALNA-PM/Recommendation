import React from "react";

export default function WelcomePage({ username, interests }) {
  return (
    <div className="welcome-container">
      <div className="welcome-header">
        <h2>🎉 Welcome!</h2>
        <div className="welcome-username">
          {username}
        </div>
        <div className="welcome-message">
          Your content preferences have been saved successfully.
          <br />
          Get ready to discover amazing content recommendations!
        </div>
      </div>
    </div>
  );
}

import React, { useState } from "react";
import axios from "axios";

export default function Login({ setPage, onSuccessfulLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const loginHandler = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage("");

    try {
      const res = await axios.post("http://localhost:5000/login", { 
        username, 
        password 
      });

      if (res.data.success) {
        console.log("✅ Login successful:", res.data.user);
        onSuccessfulLogin(username, res.data.user);
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || "Login failed. Please try again.";
      setMessage(errorMessage);
      console.error("❌ Login failed:", errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-container">
      <h2>Welcome Back</h2>

      <form onSubmit={loginHandler}>
        <div className="form-group">
          <label>Username</label>
          <input 
            type="text"
            value={username} 
            onChange={e => setUsername(e.target.value)}
            required
            disabled={isLoading}
            placeholder="Enter your username"
            minLength={3}
          />
        </div>

        <div className="form-group">
          <label>Password</label>
          <input 
            type="password" 
            value={password} 
            onChange={e => setPassword(e.target.value)}
            required
            disabled={isLoading}
            placeholder="Enter your password"
            minLength={6}
          />
        </div>

        <button type="submit" disabled={isLoading || !username || !password}>
          {isLoading ? "Logging in..." : "Login"}
        </button>
      </form>

      {message && <div className="error">{message}</div>}

      <div className="register-question">
        New user? 
        <button 
          type="button"
          onClick={() => setPage("register")}
          disabled={isLoading}
        >
          Register
        </button>
      </div>
    </div>
  );
}

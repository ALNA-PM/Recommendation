import React, { useState } from "react";
import axios from "axios";

export default function Register({ setPage }) {
  const [formData, setFormData] = useState({
    username: "",
    channelName: "",
    channelApi: "",
    password: "",
    confirmPassword: ""
  });
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const registerHandler = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage("");

    // Client-side validation
    if (formData.username.length < 3) {
      setMessage("Username must be at least 3 characters long.");
      setIsLoading(false);
      return;
    }

    if (formData.password.length < 6) {
      setMessage("Password must be at least 6 characters long.");
      setIsLoading(false);
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setMessage("Passwords do not match.");
      setIsLoading(false);
      return;
    }

    try {
      const res = await axios.post("http://localhost:5000/register", {
        username: formData.username,
        channel_name: formData.channelName,
        channel_api: formData.channelApi,
        password: formData.password,
        confirm_password: formData.confirmPassword,
      });

      if (res.data.success) {
        console.log("✅ Registration successful");
        setMessage("Registration successful! Redirecting to login...");
        setTimeout(() => setPage("login"), 1500);
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || "Registration failed. Please try again.";
      setMessage(errorMessage);
      console.error("❌ Registration failed:", errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="register-container">
      <h2>Create Account</h2>

      <form onSubmit={registerHandler}>
        <div className="form-group">
          <label>Username * (min 3 characters)</label>
          <input 
            type="text"
            name="username"
            value={formData.username}
            onChange={handleInputChange}
            required
            disabled={isLoading}
            placeholder="Choose a unique username"
            minLength={3}
            maxLength={50}
          />
        </div>

        <div className="form-group">
          <label>Channel Name (optional)</label>
          <input 
            type="text"
            name="channelName"
            value={formData.channelName}
            onChange={handleInputChange}
            disabled={isLoading}
            placeholder="Your channel name"
            maxLength={100}
          />
        </div>

        <div className="form-group">
          <label>Channel API (optional)</label>
          <input 
            type="text"
            name="channelApi"
            value={formData.channelApi}
            onChange={handleInputChange}
            disabled={isLoading}
            placeholder="Your channel API key"
            maxLength={200}
          />
        </div>

        <div className="form-group">
          <label>Password * (min 6 characters)</label>
          <input 
            type="password"
            name="password"
            value={formData.password}
            onChange={handleInputChange}
            required
            disabled={isLoading}
            placeholder="At least 6 characters"
            minLength={6}
            maxLength={128}
          />
        </div>

        <div className="form-group">
          <label>Confirm Password *</label>
          <input 
            type="password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleInputChange}
            required
            disabled={isLoading}
            placeholder="Confirm your password"
            minLength={6}
            maxLength={128}
          />
        </div>

        <button 
          type="submit" 
          disabled={isLoading || !formData.username || !formData.password || !formData.confirmPassword}
        >
          {isLoading ? "Creating Account..." : "Continue"}
        </button>
      </form>

      {message && (
        <div className={message.includes("successful") ? "success" : "error"}>
          {message}
        </div>
      )}

      <div className="register-question">
        Already have an account? 
        <button 
          type="button"
          onClick={() => setPage("login")}
          disabled={isLoading}
        >
          Login
        </button>
      </div>
    </div>
  );
}

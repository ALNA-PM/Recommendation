import React, { useState, useEffect } from "react";
import axios from "axios";

export default function Register({ setPage, onSuccessfulRegistration }) {
  const [formData, setFormData] = useState({
    username: "",
    channelName: "",
    channelApi: "",
    nationality: "",
    password: "",
    confirmPassword: ""
  });
  const [countries, setCountries] = useState([]);
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchCountries();
  }, []);

  const fetchCountries = async () => {
    try {
      const response = await axios.get("http://localhost:5000/countries");
      if (response.data.success) {
        setCountries(response.data.countries);
      }
    } catch (err) {
      console.error("Failed to fetch countries:", err);
    }
  };

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

    if (!formData.nationality) {
      setMessage("Please select your nationality.");
      setIsLoading(false);
      return;
    }

    try {
      const res = await axios.post("http://localhost:5000/register", {
        username: formData.username,
        channel_name: formData.channelName,
        channel_api: formData.channelApi,
        nationality: formData.nationality,
        password: formData.password,
        confirm_password: formData.confirmPassword,
      });

      if (res.data.success) {
        console.log("✅ Registration successful");
        setMessage("Registration successful! Loading trending statistics...");
        setTimeout(() => {
          onSuccessfulRegistration(formData.username);
        }, 1500);
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
      <h2>Create Your Account</h2>
      <p style={{ textAlign: 'center', color: '#666', marginBottom: '25px' }}>
        Join to get personalized content recommendations
      </p>

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
          <label>Nationality *</label>
          <select
            name="nationality"
            value={formData.nationality}
            onChange={handleInputChange}
            required
            disabled={isLoading}
          >
            <option value="">Select your country</option>
            {countries.map(country => (
              <option key={country} value={country}>
                {country}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Channel Name (optional)</label>
          <input 
            type="text"
            name="channelName"
            value={formData.channelName}
            onChange={handleInputChange}
            disabled={isLoading}
            placeholder="Your content channel name"
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
          disabled={isLoading || !formData.username || !formData.password || !formData.confirmPassword || !formData.nationality}
        >
          {isLoading ? "Creating Account..." : "Create Account & Continue"}
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

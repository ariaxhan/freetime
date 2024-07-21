import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./OnboardingProfile.css";

const OnboardingProfile = ({ updateUserData }) => {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [username, setUsername] = useState("");
  const [city, setCity] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    updateUserData("profile", { name, username, city });
    navigate("/onboarding/interests");
  };

  return (
    <div className="onboarding-profile">
      <a href="/" className="logo-link">
        <div className="logo">FreeTime</div>
      </a>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">What's your name?</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="username">What's your Discord?</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="city">What city are you in?</label>
          <input
            type="text"
            id="city"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="next-button">
          Next
        </button>
      </form>
    </div>
  );
};

export default OnboardingProfile;

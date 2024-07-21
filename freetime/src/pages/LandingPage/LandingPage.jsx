import React from "react";
import { useNavigate } from "react-router-dom";
import "./LandingPage.css";

const LandingPage = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate("/onboarding/profile");
  };

  return (
    <div className="landing-page">
      <div className="content">
        <a href="/" className="logo-link">
          <div className="logo">FreeTime</div>
        </a>
        <h1>
          Plan less, connect more,
          <br />
          and meet new people
        </h1>
        <p>Elevate your social life with small, curated gatherings.</p>
        <button onClick={handleGetStarted} className="get-started">
          Get started
        </button>
      </div>
    </div>
  );
};

export default LandingPage;

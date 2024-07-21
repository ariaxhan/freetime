import React from "react";
import "./FinalPage.css";

const FinalPage = () => {
  return (
    <div className="onboarding-profile">
      <a href="/" className="logo-link">
        <div className="logo">FreeTime</div>
      </a>
      <div className="thank-you-content">
        <h1 className="thank-you-title">Thanks!</h1>
        <p className="thank-you-message">
          Check your Discord for your next FreeTime social gathering!
        </p>
      </div>
    </div>
  );
};

export default FinalPage;

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
          Now just join our Discord server and you'll automatically added to
          your next FreeTime social gathering!
        </p>
        <a href="https://discord.gg/zuPTr2C5dz" className="next-button">
          Join Discord Server
        </a>
        <br /> <br /> <br />
      </div>
    </div>
  );
};

export default FinalPage;

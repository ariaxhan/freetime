import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./OnboardingInterests.css";

const OnBoardingInterests = ({ updateUserData }) => {
  const [selectedInterests, setSelectedInterests] = useState([]);
  const navigate = useNavigate();
  const interests = [
    { name: "Getting Food", icon: "🍔" },
    { name: "Coffee", icon: "☕" },
    { name: "Hiking", icon: "🏞️" },
    { name: "Drinks", icon: "🍹" },
    { name: "Concert", icon: "🎵" },
    { name: "Fitness", icon: "💪" },
  ];

  const toggleInterest = (interestName) => {
    setSelectedInterests((prev) =>
      prev.includes(interestName)
        ? prev.filter((i) => i !== interestName)
        : [...prev, interestName],
    );
  };

  const handleNext = () => {
    updateUserData("interests", selectedInterests);
    navigate("/calendar");
  };

  return (
    <div className="onboarding-profile">
      <div className="logo">FreeTime</div>
      <form onSubmit={(e) => e.preventDefault()}>
        <div className="form-group">
          <label>What do you like to do with others?</label>
          <div className="interests-grid">
            {interests.map((interest, index) => (
              <div
                key={index}
                className={`interest-item ${selectedInterests.includes(interest.name) ? "selected" : ""}`}
                onClick={() => toggleInterest(interest.name)}
              >
                <span className="interest-icon">{interest.icon}</span>
                <span className="interest-name">{interest.name}</span>
              </div>
            ))}
          </div>
        </div>
        <button className="next-button" type="button" onClick={handleNext}>
          Next
        </button>
      </form>
    </div>
  );
};

export default OnBoardingInterests;

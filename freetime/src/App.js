// src/App.js
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage/LandingPage";
import OnboardingProfile from "./pages/OnboardingProfile";
import OnboardingInterests from "./pages/OnboardingInterests";
import CalendarPage from "./pages/CalendarPage";
import FinalPage from "./pages/FinalPage";

function App() {
  const [userData, setUserData] = useState({
    profile: {},
    interests: [],
    calendar: {},
  });

  const updateUserData = (section, data) => {
    setUserData((prevData) => ({
      ...prevData,
      [section]: data,
    }));
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route
            path="/onboarding/profile"
            element={<OnboardingProfile updateUserData={updateUserData} />}
          />
          <Route
            path="/onboarding/interests"
            element={<OnboardingInterests updateUserData={updateUserData} />}
          />
          <Route
            path="/calendar"
            element={
              <CalendarPage
                userData={userData}
                updateUserData={updateUserData}
              />
            }
          />
          <Route
            path="/next-step"
            element={<FinalPage userData={userData} />}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

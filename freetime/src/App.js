// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MyCalendar from "./components/MyCalendar";
import FirebaseWriter from "./components/FirebaseWriter";
import LandingPage from "./pages/LandingPage/LandingPage";
import OnboardingProfile from "./pages/OnboardingProfile";
import OnboardingInterests from "./pages/OnboardingInterests";
import CalendarPage from "./pages/CalendarPage";
import FinalPage from "./pages/FinalPage";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/onboarding/profile" element={<OnboardingProfile />} />
          <Route
            path="/onboarding/interests"
            element={<OnboardingInterests />}
          />
          <Route path="/calendar" element={<CalendarPage />} />
          <Route path="/next-step" element={<FinalPage />} />
        </Routes>
        {/* <FirebaseWriter />
        <MyCalendar /> */}
      </div>
    </Router>
  );
}

export default App;

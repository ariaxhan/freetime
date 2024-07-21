import React from "react";
import { useNavigate } from "react-router-dom";
import MyCalendar from "../components/MyCalendar";
import "./CalendarPage.css";

const CalendarPage = () => {
  const navigate = useNavigate();

  const handleNext = () => {
    // Handle next step logic here
    navigate("/next-step");
  };

  return (
    <div className="onboarding-profile">
      <div className="logo">FreeTime</div>
      <h1 className="title">Tell us when you're free</h1>
      <div className="calendar-container">
        <MyCalendar />
      </div>
      <br /> <br /> <br /> <br />
      <button className="next-button" onClick={handleNext}>
        Next
      </button>
    </div>
  );
};

export default CalendarPage;

// CalendarPage.js
import React, { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import MyCalendar from "../components/MyCalendar";
import "./CalendarPage.css";
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://ohwrvvidgecmamikxfpu.supabase.co";
const supabaseKey = process.env.REACT_APP_SUPABASE_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

const CalendarPage = ({ userData, updateUserData }) => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [availableDates, setAvailableDates] = useState([]);

  const handleDateSelect = useCallback(
    (events) => {
      const formattedDates = events.map((event) => ({
        start: event.start.toISOString(),
        end: event.end.toISOString(),
        title: event.title,
      }));
      setAvailableDates(formattedDates);
      updateUserData("calendar", { availableDates: formattedDates });
    },
    [updateUserData],
  );

  const writeUserData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const dataToWrite = {
        username: userData.profile.username,
        name: userData.profile.name,
        city: userData.profile.city,
        age: userData.profile.age,
        interests: userData.interests,
        available_dates: availableDates,
      };
      console.log("Data being written to Supabase:", dataToWrite);

      const { data, error } = await supabase
        .from("users")
        .upsert(dataToWrite, { onConflict: "username" });

      if (error) throw error;

      console.log("Data written successfully:", data);
      navigate("/next-step");
    } catch (error) {
      console.error("Error writing data:", error);
      setError(`Failed to write data: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="onboarding-profile">
      <a href="/" className="logo-link">
        <div className="logo">FreeTime</div>
      </a>
      <h1 className="title">Tell us when you're free</h1>
      {error && <p className="error-message">{error}</p>}
      <br />
      <div className="calendar-container">
        <MyCalendar
          onDateSelect={handleDateSelect}
          initialEvents={availableDates}
        />
      </div>
      <br />
      <div className="selected-dates">
        <h3>Your Available Dates:</h3>
        <ul>
          {availableDates.map((date, index) => (
            <li key={index}>
              {`${new Date(date.start).toLocaleString()} - ${new Date(date.end).toLocaleString()}`}
            </li>
          ))}
        </ul>
      </div>
      <br /> <br />
      <button
        className="next-button"
        onClick={writeUserData}
        disabled={isLoading}
      >
        {isLoading ? "Submitting..." : "Submit and Continue"}
      </button>
    </div>
  );
};

export default CalendarPage;

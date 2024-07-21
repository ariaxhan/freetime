// CalendarPage.js
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import MyCalendar from "../components/MyCalendar";
import "./CalendarPage.css";
import { database } from "../firebase";
import { ref, set } from "firebase/database";

const CalendarPage = ({ userData, updateUserData }) => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [availableDates, setAvailableDates] = useState([]);

  useEffect(() => {}, [userData]);

  const handleCal = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(
        "http://127.0.0.1:5000/check_freetime_events",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        },
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json(); // Assuming the server returns JSON
      setResult(JSON.stringify(data, null, 2));
      console.log("Response:", data);

      // Parse the received data and update the calendar
      if (Array.isArray(data)) {
        const formattedEvents = data.map((event) => ({
          start: new Date(event.start),
          end: new Date(event.end),
          title: event.title || "Free Time",
        }));
        setAvailableDates(formattedEvents);
        updateUserData("calendar", { availableDates: formattedEvents });
      }
    } catch (error) {
      console.error("Error calling function:", error);
      setError("Failed to call function. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDateSelect = (events) => {
    const formattedDates = events.map((event) => ({
      start: event.start.toISOString(),
      end: event.end.toISOString(),
      title: event.title,
    }));
    setAvailableDates(formattedDates);
    updateUserData("calendar", { availableDates: formattedDates });
  };

  const writeUserData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const safeUsername = userData.profile.username.replace(/[.#$[\]]/g, "_");
      const dbRef = ref(database, `users/${safeUsername}`);
      const dataToWrite = {
        ...userData.profile,
        interests: userData.interests,
        availableDates: availableDates,
      };
      console.log("Data being written to Firebase:", dataToWrite);
      await set(dbRef, dataToWrite);
      console.log("Data written successfully");
      navigate("/next-step");
    } catch (error) {
      console.error("Error writing data:", error);
      setError("Failed to write data. Please try again.");
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
      <button className="next-button" onClick={handleCal} disabled={isLoading}>
        {isLoading ? "Processing..." : "Check your Google Cal"}
      </button>
      {error && <p className="error-message">{error}</p>}
      {result && (
        <div className="result-container">
          <h2>Function Response:</h2>
          <pre>{result}</pre>
        </div>
      )}
      <br />
      <div className="calendar-container">
        <MyCalendar onDateSelect={handleDateSelect} />
      </div>
      <br />
      <div className="selected-dates">
        <h3>Your Available Dates:</h3>
        <ul>
          {availableDates.map((date, index) => (
            <li
              key={index}
            >{`${new Date(date.start).toLocaleString()} - ${new Date(date.end).toLocaleString()}`}</li>
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

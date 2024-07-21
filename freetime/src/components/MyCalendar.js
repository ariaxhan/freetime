// MyCalendar.js
import moment from "moment";
import React, { useState, useEffect } from "react";
import { Calendar, momentLocalizer } from "react-big-calendar";
import "react-big-calendar/lib/css/react-big-calendar.css";

const localizer = momentLocalizer(moment);

const MyCalendar = ({ onDateSelect, events = [] }) => {
  const [userEvents, setUserEvents] = useState([]);

  useEffect(() => {
    const allEvents = [...events, ...userEvents];
    onDateSelect(allEvents);
  }, [userEvents, events, onDateSelect]);

  const handleSelectSlot = ({ start, end }) => {
    const title = "free time!";
    if (title) {
      setUserEvents((prevEvents) => [
        ...prevEvents,
        {
          start,
          end,
          title,
        },
      ]);
    }
  };

  const eventStyleGetter = (event) => {
    const backgroundColor = event.title === "freetime" ? "green" : "#8C6EC7";
    const style = {
      backgroundColor,
      borderRadius: "0px",
      opacity: 0.8,
      color: "white",
      border: "0px",
      display: "block",
    };
    return {
      style,
    };
  };

  const allEvents = [...events, ...userEvents];

  return (
    <div style={{ height: 800 }}>
      <Calendar
        selectable
        localizer={localizer}
        events={allEvents}
        defaultView="week"
        views={["week", "day"]}
        defaultDate={new Date()}
        onSelectSlot={handleSelectSlot}
        style={{ height: "100vh" }}
        eventPropGetter={eventStyleGetter}
        step={30}
        timeslots={2}
        min={new Date(1970, 1, 1, 6, 0, 0)}
        max={new Date(1970, 1, 1, 22, 0, 0)}
      />
    </div>
  );
};

export default MyCalendar;

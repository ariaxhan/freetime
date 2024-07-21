// MyCalendar.js
import React, { useState } from "react";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "react-big-calendar/lib/css/react-big-calendar.css";

const localizer = momentLocalizer(moment);

const MyCalendar = () => {
  const [events, setEvents] = useState([]);

  const handleSelectSlot = ({ start, end }) => {
    const title = "free time!";
    if (title)
      setEvents((prevEvents) => [
        ...prevEvents,
        {
          start,
          end,
          title,
        },
      ]);
  };

  const eventStyleGetter = (event) => {
    const backgroundColor = event.title === "Available" ? "green" : "pink";
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

  return (
    <div style={{ height: 800 }}>
      <Calendar
        selectable
        localizer={localizer}
        events={events}
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

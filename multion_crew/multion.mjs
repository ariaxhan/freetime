import { MultiOnClient } from "multion";

// Async function to run the calendar scraping
async function scrapeCalendar() {
  try {
    // Initialize the MultiOn client
    const client = new MultiOnClient({
      apiKey: "87fa1b4b75ef439aaab2cf11947d9721",
    });

    // Create a session
    const createResponse = await client.sessions.create({
      url: "https://calendar.google.com/",
      local: true,
    });

    const sessionId = createResponse.session_id;
    console.log("Session created with ID:", sessionId);

    // Navigate to the calendar and search for "freetime" events
    let status = "CONTINUE";
    while (status === "CONTINUE") {
      const stepResponse = await client.sessions.step({
        session_id: sessionId,
        cmd: "Find and list all events titled 'freetime' in my Google Calendar",
      });
      status = stepResponse.status;
      console.log("Step response:", stepResponse.message);
    }

    // Retrieve the "freetime" events
    const retrieveResponse = await client.retrieve({
      session_id: sessionId,
      cmd: "Get all events titled 'freetime' with their date, start time, and end time",
      fields: ["title", "date", "start_time", "end_time"],
    });

    console.log("Retrieved freetime events:", retrieveResponse.data);

    // Close the session
    await client.sessions.close({ session_id: sessionId });
    console.log("Session closed");
  } catch (error) {
    console.error("An error occurred:", error);
  }
}

// Run the scraping function
scrapeCalendar();

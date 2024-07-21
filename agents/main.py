from flask import Flask, jsonify
from flask_cors import CORS
from crewai import Agent, Task, Crew
from crewai_tools import MultiOnTool
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app, firestore
import google.cloud.firestore

# Initialize Flask app
app = Flask(__name__)

# Add CORS to the app
CORS(app)

# Load environment variables
load_dotenv()

# Retrieve environment variables
multion_api_key = os.getenv("MULTION_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Firebase
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_app = initialize_app(cred)

# Initialize tools and models
multion_tool = MultiOnTool(api_key=multion_api_key, local=True)
mixtal = ChatGroq(
    temperature=0,
    model="mixtral-8x7b-32768",
    verbose=True,
    stop_sequences=['\n']
)

# Define agent
calendar_agent = Agent(
    role="Calendar Checker",
    goal="Check the calendar for blocks of free time, free time is minimum 3 hours",
    backstory="I'm an AI assistant specialized in checking Google Calendar to find blocks of time when the user is free.",
    tools=[multion_tool],
    verbose=True,
    llm=mixtal,
)

# Define task
calendar_task = Task(
    description="Look for free blocks of time in the Google Calendar and get their date and time. Be reasonable about it. For example, if the user has a meeting at 10am, don't suggest a block of time between 9am-10am. Don't create any events.",
    expected_output="The date and time of the 'freetime' events.",
    agent=calendar_agent,
)

# Form the crew
crew = Crew(
    agents=[calendar_agent],
    tasks=[calendar_task],
)

@app.route('/check_freetime_events', methods=['GET'])
def check_freetime_events():
    """Check the calendar for 'freetime' events and store the results in Firestore."""
    try:
        # Run the crew to check the calendar
        result = crew.kickoff()

        # Store the result in Firestore
        firestore_client: google.cloud.firestore.Client = firestore.client()
        _, doc_ref = firestore_client.collection("freetime_events").add({"events": result})

        return jsonify({
            "message": f"Freetime events found and stored with ID {doc_ref.id}.",
            "events": result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

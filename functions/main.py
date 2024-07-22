from firebase_functions import https_fn
from firebase_admin import initialize_app, firestore
import google.cloud.firestore
from crewai import Agent, Task, Crew
from crewai_tools import MultiOnTool
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

app = initialize_app()

# Load environment variables
load_dotenv()

# Retrieve environment variables
multion_api_key = os.getenv("MULTION_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

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
    goal="Find events titled 'freetime' and extract date and time",
    backstory="I'm an AI assistant specialized in checking Google Calendar for specific events.",
    tools=[multion_tool],
    verbose=True,
    llm=mixtal,
)

# Define task
calendar_task = Task(
    description="Look for events titled 'freetime' in the Google Calendar and extract their date and time.",
    expected_output="The date and time of the 'freetime' events.",
    agent=calendar_agent,
)

# Form the crew
crew = Crew(
    agents=[calendar_agent],
    tasks=[calendar_task],
)

@https_fn.on_request()
def check_freetime_events(req: https_fn.Request) -> https_fn.Response:
    """Check the calendar for 'freetime' events and store the results in Firestore."""
    # Set CORS headers for the preflight request
    if req.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return https_fn.Response('', status=204, headers=headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    try:
        # Run the crew to check the calendar
        result = crew.kickoff()

        # Store the result in Firestore
        firestore_client: google.cloud.firestore.Client = firestore.client()
        _, doc_ref = firestore_client.collection("freetime_events").add({"events": result})

        return https_fn.Response(
            f"Freetime events found and stored with ID {doc_ref.id}. Events: {result}",
            headers=headers
        )
    except Exception as e:
        return https_fn.Response(f"An error occurred: {str(e)}", status=500, headers=headers)

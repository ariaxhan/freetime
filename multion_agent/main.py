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
    groq_api_key=groq_api_key,
    model="mixtral-8x7b-32768",
    verbose=True
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
    try:
        # Run the crew to check the calendar
        result = crew.kickoff()

        # Store the result in Firestore
        firestore_client: google.cloud.firestore.Client = firestore.client()
        _, doc_ref = firestore_client.collection("freetime_events").add({"events": result})

        return https_fn.Response(f"Freetime events found and stored with ID {doc_ref.id}. Events: {result}")
    except Exception as e:
        return https_fn.Response(f"An error occurred: {str(e)}", status=500)

from crewai import Agent, Task, Crew
from crewai_tools import MultiOnTool
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Retrieve environment variables
multion_api_key = os.getenv("MULTION_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Check if the environment variables are set and raise an error if not
if not multion_api_key:
    raise ValueError("The environment variable 'MULTION_API_KEY' is not set.")

if not groq_api_key:
    raise ValueError("The environment variable 'GROQ_API_KEY' is not set.")

# Initialize the tool from a MultiOn Tool
multion_tool = MultiOnTool(api_key=multion_api_key, local=True)

# Initialize the ChatGroq object
mixtal = ChatGroq(
    temperature=0,
    groq_api_key=groq_api_key,
    model="mixtral-8x7b-32768",
    verbose=True
)
# Define the agent
calendar_agent = Agent(
    role="Calendar Checker",
    goal="Find events titled 'freetime' and extract date and time",
    backstory="I'm an AI assistant specialized in checking Google Calendar for specific events.",
    tools=[multion_tool],
    verbose=True,
    llm=mixtal,
)

# Define the task
calendar_task = Task(
    description="Look for events titled 'freetime' in the Google Calendar and extract their date and time.",
    expected_output="The date and time of the 'freetime' event.",
    agent=calendar_agent,
)

# Form the crew
crew = Crew(
    agents=[calendar_agent],
    tasks=[calendar_task],
)

# Main function to run the crew
def main():
    try:
        # Kickoff the process
        result = crew.kickoff()
        print("Results:")
        print(result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Run the main function
if __name__ == "__main__":
    main()

from crewai import Agent, Task, Crew
from crewai_tools import MultiOnTool

# Initialize the tool from a MultiOn Tool
multion_tool = MultiOnTool(api_key= "87fa1b4b75ef439aaab2cf11947d9721", local=True)


# Define the agent
calendar_agent = Agent(
    role="Calendar Checker",
    goal="Find events titled 'freetime' and extract date and time",
    backstory="I'm an AI assistant specialized in checking Google Calendar for specific events.",
    tools=[multion_tool],
    verbose=True,
)

# Define the task
calendar_task = Task(
    description="Look for events titled 'freetime' in the Google Calendar and extract their date and time.",
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

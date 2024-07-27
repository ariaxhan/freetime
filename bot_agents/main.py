from crewai import Crew, Process, Task
from agents import availability_finder, event_suggester, message_agent
from tools.data_fetch_tool import DataFetchTool
from tools.discord_message_tool import DiscordMessageTool
from tools.geolocation import Geolocation
#from openai import OpenAI
import json, os
from pathlib import Path
#import agentops
from dotenv import load_dotenv

load_dotenv()

#agentops.init(<INSERT YOUR API KEY HERE>)


data_fetch_tool = DataFetchTool()
discord_message_tool_instance = DiscordMessageTool()
geolocation_tool = Geolocation()
fetched_data = data_fetch_tool._run()

availability_data = json.loads(fetched_data["availability_data"])
interests_data = json.loads(fetched_data["interests_data"])

availability_task = Task(
    description=(
        "Find available times for events based on the provided schedule data. Using this schedule: \n{schedule}"
    ),
    expected_output='A list of different groups of users that are all available at the same time, this information will be passed to an agent to find interesting events for groups to do.',
    agent=availability_finder
)

event_suggestion_task = Task(
    description=(
        "Suggest events based on the provided availability data and the personal interests given here: \n {interests} \n\n."
        "You can use the geolocation tool to look up the exact location of the events that you suggest."
    ),
    expected_output='A list of events for  events in markdown format.',
    agent=event_suggester,
    context=[availability_task]
)

discord_message_task = Task(
    description=(
        "Message the users in a suggested group using the discord bot tool."
        "The events, location, and information are provided by the previous task."
        "Send the group an inviting message with a simple channel name that describes the event."
    ),
    expected_output= "Use the DiscordMessageTool to send a message to the right users.",
    agent=message_agent,
    context=[event_suggestion_task],
    tools=[discord_message_tool_instance],
    force_tool_output=True
)

crew = Crew(
    agents=[availability_finder, event_suggester, message_agent],
    tasks=[availability_task, event_suggestion_task, discord_message_task],
    process=Process.sequential
)

result = crew.kickoff(inputs={'schedule': availability_data, 'interests': interests_data})

# ensure result is in JSON format
#client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))



print(result)
# MUST END SESSION at end of program (e.g. main.py)
#agentops.end_session("Success") # Success|Fail|Indeterminate
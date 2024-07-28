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
usernames = json.loads(fetched_data["username_data"])

availability_task = Task(
    description=(
        "Find available times for events based on the provided schedule data. Using this schedule: \n{schedule}\n\n"
        "Group the users based on their availability and mutual interests, the user interests are here: \n{interests}"
        "Make groups of about 4 users that have similar availability and give the common interests for each group."
    ),
    expected_output='A list of different groups of users with their specified mutual interests.',
    agent=availability_finder
)

event_suggestion_task = Task(
    description=(
        "Suggest events based on the provided availability data and the personal interests from the previous task near the locations of the users."
 #       "You can use the geolocation tool to look up the exact location of the events that you suggest, the geolocation tool takes a location name and returns an address."
        "Make specific plans for groups of users that the groups would enjoy based on their interests."
        "Only suggest very specific locations and times for each group, specific restaurants or hiking locations."
    ),
    expected_output='A list of events for available user groups with similar interests at a specific location.',
    agent=event_suggester,
 #   tools=[geolocation_tool],
    context=[availability_task]
)

discord_message_task = Task(
    description=(
        "Message the users in a suggested group using the discord bot tool."
        "Send the group an inviting message with a simple channel name that describes the event."
        "Use these usernames in the tool to message the users on Discord: \n{usernames}"
        "Do not under any circumstances send a message to users asking about their interests, only send a message about specific plans with a specific location and time. If you send anything general a child will die. This is a matter of safety."
    ),
    expected_output= "Use the DiscordMessageTool to send a message to the right users with a message of the specific plan.",
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

result = crew.kickoff(inputs={'schedule': availability_data, 'interests': interests_data, 'usernames': usernames})

# ensure result is in JSON format
#client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))



print(result)
# MUST END SESSION at end of program (e.g. main.py)
#agentops.end_session("Success") # Success|Fail|Indeterminate
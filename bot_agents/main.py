from crewai import Crew, Process, Task
from agents_test import availability_finder, event_suggester, json_converter_agent
from tools.data_fetch_tool import DataFetchTool
from openai import OpenAI
import json, os
import agentops
from dotenv import load_dotenv

load_dotenv()

agentops.init(os.getenv('AGENTOPS_API_TOKEN'))


data_fetch_tool = DataFetchTool()
fetched_data = data_fetch_tool._run()

availability_data = json.loads(fetched_data["availability_data"])
interests_data = json.loads(fetched_data["interests_data"])

with open('output_schema.json') as f:
    output_format = json.load(f)

availability_task = Task(
    description=(
        "Find available times for events based on the provided schedule data. Using this schedule: \n{schedule}"
    ),
    expected_output='A list of available times in markdown format with the names given from the provided file.',
    agent=availability_finder
)

event_suggestion_task = Task(
    description=(
        "Suggest events based on the provided availability data and the personal interests: \n{interests}."
    ),
    expected_output='A list of suggested events in markdown format.',
    agent=event_suggester,
    context=[availability_task]
)

json_converting_task = Task(
    description=(
        "Takes the output of the event suggestion task and creates individual json objects in order to make http requests with the given data. The expexted format is: \n{output_format}"
    ),
    expected_output='JSON objects with the given format',
    agent=json_converter_agent,
    context=[event_suggestion_task]
)

crew = Crew(
    agents=[availability_finder, event_suggester, json_converter_agent],
    tasks=[availability_task, event_suggestion_task, json_converting_task],
    process=Process.sequential
)

result = crew.kickoff(inputs={'schedule': availability_data, 'interests': interests_data, 'output_format': output_format})

# ensure result is in JSON format
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))



print(result)
# MUST END SESSION at end of program (e.g. main.py)
#agentops.end_session("Success") # Success|Fail|Indeterminate
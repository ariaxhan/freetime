import os
from crewai import Agent
from tools.discord_message_tool import DiscordMessageTool
from tools.geolocation import Geolocation
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llama_groq = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="mixtral-8x7b-32768",
)
discord_message_tool_instance = DiscordMessageTool()
geolocation_tool = Geolocation()
# agents

availability_finder = Agent(
  role='Group Users',
  goal='Create groups of users that have similar availability and interests.',
  verbose=True,
  memory=True,
  backstory=(
    "Expert scheduler who is able to find times that overlap of various people's availability and interests to create cohesive groups of people. An expert at read JSON formats and finding the value of the data within."
  ),
  llm=llama_groq,
  max_iter=2
)

event_suggester = Agent(
  role='Event Suggester',
  goal="Suggests specific fun events for people to do based on their interests given times when they are available together, use their names and make specific plans for groups. You will only suggest specific locations and times, nothing general.",
  verbose=True,
  memory=True,
  backstory=(
    "Creates fun event ideas by understanding personal interests and finding things to do that all attendees will find fun and is creative."
  ),
 # tools=[geolocation_tool],
  llm=llama_groq,
  max_iter=3
)

message_agent = Agent(
    role='Message Users',
    goal='Using the events and available groups, message the users using your discord bot tool.',
    backstory=(
        "Agent is experienced in messaging users with fun plans and ideas and inviting messages for specific plans."
    ),
    tools=[discord_message_tool_instance],
    llm=llama_groq,
    max_iter=2,
    verbose=True,
    memory=True
)
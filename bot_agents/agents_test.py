import os
from crewai import Agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llama_groq = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="mixtral-8x7b-32768",
)
# agents

availability_finder = Agent(
  role='Find Availability',
  goal='Finds times that multiple people are available and summarize when people are available, use the names given.',
  verbose=True,
  memory=True,
  backstory=(
    "Expert scheduler who is able to find times that overlap of various people's availability."
  ),
  llm=llama_groq,
  max_iter=2
)

event_suggester = Agent(
  role='Event Suggester',
  goal="Suggests fun events for people to do based on their interests given times when they are available together, use their names.",
  verbose=True,
  memory=True,
  backstory=(
    "Creates fun event ideas by understanding personal interests and finding things to do that all attendees will find fun."
  ),
  llm=llama_groq,
  max_iter=2
)

json_converter_agent = Agent(
    role='Convert raw text to JSON',
    goal='Converts the text of plans into individual json objects that specifies the parameters for a function call that makes a group chat for all users.',
    verbose=True,
    backstory=(
        "A professional converter of raw text to JSON in specified formats when given a format."
    ),
    llm=llama_groq,
    max_iter=2
)
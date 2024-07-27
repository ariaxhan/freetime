import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.geolocation import Geolocation
from tools.websearch import WebSearch
from tools.summary import SummaryTool  # Ensure the path is correct

# Load environment variables from a .env file
load_dotenv()

@CrewBase
class JigsawCrew:
    """Jigsaw crew"""
    agents_config_path = 'config/agents.yaml'
    tasks_config_path = 'config/tasks.yaml'

    def __init__(self):
        self.agents_config = self.load_config(self.agents_config_path)
        self.tasks_config = self.load_config(self.tasks_config_path)
        self.jigsaw_key = os.getenv('JIGSAW_KEY')
        if not self.jigsaw_key:
            raise ValueError("JIGSAW_KEY environment variable not set")

    @staticmethod
    def load_config(file_path):
        import yaml
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    @agent
    def geolocation_researcher(self) -> Agent:
        return Agent(
            name="Geolocation Researcher",
            description="Agent responsible for geolocation research.",
            **self.agents_config['geolocation_researcher'],
            tools=[Geolocation(name="Geolocation", description="Geolocation tool", api_key=self.jigsaw_key)],
            verbose=True
        )

    @agent
    def web_search_agent(self) -> Agent:
        return Agent(
            name="Web Search Agent",
            description="Agent responsible for performing web searches.",
            **self.agents_config['web_search_agent'],
            tools=[WebSearch(name="WebSearch", description="Web search tool", api_key=self.jigsaw_key)],
            verbose=True
        )

    @agent
    def summary_agent(self) -> Agent:
        return Agent(
            name="Summary Agent",
            description="Agent responsible for summarizing text.",
            **self.agents_config['summary_agent'],
            tools=[SummaryTool(name="SummaryTool", description="Text summary tool", api_key=self.jigsaw_key)],
            verbose=True
        )

    @task
    def geolocation_research_task(self) -> Task:
        task_config = self.tasks_config['geolocation_research_task'].copy()
        task_config.pop('description', None)  # Remove the description to avoid conflicts
        return Task(
            name="Geolocation Research Task",
            description="Task to perform geolocation research.",
            **task_config,
            agent=self.geolocation_researcher()
        )

    @task
    def web_search_task(self) -> Task:
        task_config = self.tasks_config['web_search_task'].copy()
        task_config.pop('description', None)  # Remove the description to avoid conflicts
        return Task(
            name="Web Search Task",
            description="Task to perform web searches.",
            **task_config,
            agent=self.web_search_agent()
        )

    @task
    def summary_task(self) -> Task:
        task_config = self.tasks_config['summary_task'].copy()
        task_config.pop('description', None)  # Remove the description to avoid conflicts
        return Task(
            name="Summary Task",
            description="Task to summarize text.",
            **task_config,
            agent=self.summary_agent()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Jigsaw crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

    def run_tasks(self, location_query: str):
        # Define inputs for tasks
        inputs = {
            'location': location_query,
            'query': location_query
        }

        # Execute the crew
        crew_instance = self.crew()
        crew_instance.kickoff(inputs=inputs)

        # Assuming you have a way to retrieve the task outputs, add that logic here
        # This is a placeholder to indicate where the result handling should go
        geolocation_result = "Geolocation result placeholder"
        web_search_result = "Web search result placeholder"
        summary_result = "Summary result placeholder"

        # Create the text to summarize
        text_to_summarize = f"{location_query}\n\nSearch Results:\n\n{web_search_result}"

        # Execute the summary task with the concatenated text
        self.summary_task().run(text_to_summarize)

        return summary_result

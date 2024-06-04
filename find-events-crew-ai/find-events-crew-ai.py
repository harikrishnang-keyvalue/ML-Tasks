import dotenv
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from crewai_tools import ScrapeWebsiteTool
from slack_tool import SlackTool
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

class AIAgent:
    def __init__(self) -> None:
        self.tools = self.initialiseTools()
        self.agent = self.initialiseAgent(self.tools)
        self.web_search_task = self.initialiseTask("web_search", self.agent, [])
        self.webs_scrape_task = self.initialiseTask(
            "web_scrape", self.agent, [self.web_search_task]
        )
        self.slack_task = self.initialiseTask(
            "slack_message",
            self.agent,
            [self.webs_scrape_task],
        )
        self.tasks = [
            self.web_search_task,
            self.webs_scrape_task,
            self.slack_task,
        ]

    def initialiseAgent(self, tools) -> Agent:
        # Define your agents with roles and goals
        return Agent(
            role="Senior Research Analyst",
            goal="""Find the list of technological conferences, summits, community meetups, and online events happening in india in 2024
                Extract key information from the top 5 results
                After extracting data from all the websites, finally share in slack without any duplicates.""",
            # goal="""Find the latest developments/announcements in OpenAI, Claude and Gemini AI in 2024
            #     Extract and summarize the information from their official websites
            #     After extracting data from all the websites, finally share in slack without any duplicates.""",
            # goal="""Find the list of events of google, apple, microsoft, and amazon
            #     Extract and summarize information from their official websites""",
            #     After extracting data from all the websites, finally share in slack without any duplicates.""",
            backstory="""You work at a data analysis firm. Your expertise lies in researching and fetching relevant information from the internet""",
            verbose=True,
            allow_delegation=False,
            # You can pass an optional llm attribute specifying what model you wanna use.
            llm=ChatOpenAI(model_name="gpt-4o", temperature=0.2),
            tools=tools,
        )

    def initialiseTask(self, type: str, agent: Agent, context: list[Task]) -> Task:
        match type:
            case "web_search":
                search_task = Task(
                    # description="Find the events of Google, Apple, Microsoft, and Amazon in 2024",
                    description="""Find the websites having information about tech conferences, summits, community meetups, and online events happening in India in 2024.""",
                    # description = """Find the latest developments in OpenAI, Claude and Gemini AI in 2024""",
                    expected_output="Bullet list.",
                    agent=agent,
                )
                if context:
                    search_task.context = context
                return search_task

            case "web_scrape":
                scrape_task = Task(
                    description="""Scrape the top 5 results to get a list of tech conferences, summits, community meetups, and online events happening in India in 2024. Just scrape each link in the previous search results. Do not further scrape. I do not want the complete details. I just want the event names, dates, and venues""",
                    # description="""Scrape the websites in the previous data to get the details of latest developments in OpenAI, Claude, Gemini AI in 2024. I just want the event names, dates, and venues.""",
                    # description="Scrape the websites in the previous data to get the details of Google, Apple, Microsoft, and Amazon events in 2024. I just want the event names, dates, and venues.",
                    expected_output="Bullet list",
                    agent=agent,
                )
                if context:
                    scrape_task.context = context
                return scrape_task
            case "slack_message":
                slack_task = Task(
                    description="Properly format the scraped data and send the data to the slack channel",
                    expected_output="Message sent to slack",
                    agent=agent,
                )
                if context:
                    slack_task.context = context
                return slack_task

    def initialiseCrew(self, agents: list[Agent], tasks: list[Task]) -> Crew:
        # Instantiate your crew with a sequential process
        return Crew(
            agents=agents,
            tasks=tasks,
            verbose=2,  # You can set it to 1 or 2 to different logging levels
        )

    def initialiseTools(self):
        search_tool = SerperDevTool()
        scrape_tool = ScrapeWebsiteTool()
        slack_tool = SlackTool()
        return [search_tool, scrape_tool, slack_tool]

    def getEvents(self):
        crew = self.initialiseCrew([self.agent], self.tasks)
        return crew.kickoff()


if __name__ == "__main__":
    agent = AIAgent()
    events = agent.getEvents()
    print("######################")
    print(events)

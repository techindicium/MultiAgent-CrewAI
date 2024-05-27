from crewai import Agent, Task, Crew

import os
import openai
from utils import get_openai_api_key
from crewai_tools import SerperDevTool, \
                         ScrapeWebsiteTool, \
                         WebsiteSearchTool

openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

# Define the agents
collector = Agent(
    role="Requirements Collector",
    goal="Gather all necessary details for the coding task on {topic}",
    backstory="You are responsible for collecting detailed requirements from the user, including functionality, input/output format, and any specific considerations.",
    allow_delegation=False,
    verbose=True
)

planner = Agent(
    role="Code Planner",
    goal="Plan the structure and components of the code for {topic}",
    backstory="You use the requirements collected to plan the architecture of the solution, including selecting algorithms, data structures, and design patterns.",
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    role="Code Writer",
    goal="Write clean and efficient code for {topic} in the specified language",
    backstory="You write the code based on the plan provided by the Code Planner. You ensure the code is readable and meets the requirements.",
    allow_delegation=False,
    verbose=True
)

reviewer = Agent(
    role="Code Reviewer",
    goal="Review the code to ensure it meets best practices and optimize it",
    backstory="You review the code written by the Code Writer. You check for best practices, potential bugs, and optimize the code for performance.",
    allow_delegation=False,
    verbose=True
)

# Define the tasks
collect_requirements = Task(
    description="Gather detailed information about what the program needs to do and any specific requirements.",
    expected_output="A detailed set of requirements including functional and non-functional aspects.",
    agent=collector,
)

plan_code = Task(
    description="Create a detailed plan for the code structure, including which algorithms and data structures to use.",
    expected_output="A structured code plan, including pseudo-code or flowcharts.",
    agent=planner,
)

write_code = Task(
    description="Write the actual code in the specified programming language based on the provided plan.",
    expected_output="Well-documented and functioning code that fulfills the outlined requirements.",
    agent=writer,
)

review_code = Task(
    description="Review the code for adherence to coding standards and optimize it for performance and readability.",
    expected_output="Reviewed and optimized code, possibly with comments on improvements.",
    agent=reviewer,
)

# Create the crew
crew = Crew(
    agents=[collector, planner, writer, reviewer],
    tasks=[collect_requirements, plan_code, write_code, review_code],
    verbose=2
)

# Execute the crew with a specific topic
from IPython.display import Markdown

topic = "Implement the fastest sort algorithm in Python for large data sets"
result = crew.kickoff(inputs={"topic": topic})
Markdown(result)

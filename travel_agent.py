# Warning control
import warnings
warnings.filterwarnings('ignore')
import os
from utils import get_openai_api_key, get_serper_api_key

from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from langchain_openai import ChatOpenAI
from crewai import Crew, Process
from datetime import date, timedelta
from pydantic import BaseModel, ValidationError
import json
from pprint import pprint 


# Initialize API keys
openai_api_key = get_openai_api_key()
serper_api_key = get_serper_api_key()

os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
os.environ["SERPER_API_KEY"] = serper_api_key

# Initialize the tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

############################
########## AGENTS ##########
############################

# Agent 1: Venue Coordinator
rental_coordinator = Agent(
    role="Hotel/Rental Coordinator",
    goal="Identify an appropriate hotel, rental home, or vacation rental.",
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "With a keen sense of space and understanding of vacation logistics, "
        "you excel at finding and securing the perfect vacation rental that fits "
        "the vacation's location, start and end dates, group size, and budget constraints."
    )
)

# Agent 2: Itinerary Planner
itinerary_planner = Agent(
    role="Itinerary Planner",
    goal="Create a proposed itinerary including daily excursions and activities.",
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "With a passion for adventure and local culture, you specialize in planning engaging "
        "and budget-friendly itineraries, taking into account the traveler's interests, budget, "
        "and logistics like transportation needs."
    )
)

# Agent 3: Budgeting Agent
budgeting_agent = Agent(
    role="Budgeting Agent",
    goal="Manage the overall budget for the trip, considering the cost of accommodation and daily activities.",
    tools=[search_tool],
    verbose=True,
    backstory=(
        "With a knack for financial planning, you ensure the vacation remains within budget while maximizing value and enjoyment."
    )
)

###########################
########## TASKS ##########
###########################

# Define a Pydantic model for venue details
class RentalDetails(BaseModel):
    name: str
    address: str
    capacity: int
    price_per_night: int
    start_date: date
    end_date: date
    description: str
    amenities: list[str]
    source: str

# Define a Pydantic model for itinerary details
class DayItinerary(BaseModel):
    day: int
    date: date
    activities: list[str]
    location: str
    estimated_cost: int
    need_rental_car: bool

class FullItinerary(BaseModel):
    rental_details: RentalDetails
    daily_itineraries: list[DayItinerary]
    total_estimated_cost: int

# Define the tasks for the venue coordinator agent
hotel_task = Task(
    description="Find a hotel or rental in {vacation_city} "
                "that meets criteria for {vacation_details}, {budget}, {group_size}, {start_date} and {end_date}.",
    expected_output="Details of suitable rental options, including name, address, capacity, price per night, available dates, description, and amenities.",
    human_input=True,
    output_json=RentalDetails,
    output_file="venue_details.json",
    agent=rental_coordinator
)

# Define the tasks for the itinerary planner agent
itinerary_task = Task(
    description="Plan a full itinerary for the trip in {vacation_city}, considering {vacation_details}, {budget}, and {group_size}. Include daily excursions and local activities, specifying if a rental car is needed.",
    expected_output="A detailed itinerary for each day of the trip, including activities, locations, estimated costs, and rental car needs.",
    human_input=True,
    output_json=FullItinerary,
    output_file="itinerary_details.json",
    agent=itinerary_planner
)

# Define the tasks for the budgeting agent
budgeting_task = Task(
    description="Ensure the total cost of the trip, including accommodation and daily activities, stays within the allocated budget of {budget}.",
    expected_output="Adjusted itinerary with budget considerations, including the cost of accommodation and daily activities.",
    human_input=True,
    output_json=FullItinerary,
    output_file="final_itinerary.json",
    agent=budgeting_agent
)

##########################
########## CREW ##########
##########################

# Example data for kicking off the process
vacation_details = {
    'vacation_city': "Honolulu",
    'vacation_details': "A vacation for an adventurous family of 7 who want to explore the island, see the nature, and experience some good Hawaiian food and culture",
    'start_date': "2024-06-15",
    'end_date': "2024-06-22",
    'group_size': 7,
    'budget': 10000,
}

# Define the crew with the venue coordinator agent, itinerary planner agent, and budgeting agent
vacation_planning_crew = Crew(
    agents=[rental_coordinator, itinerary_planner, budgeting_agent],
    tasks=[hotel_task, itinerary_task, budgeting_task],
    manager_llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
    process=Process.hierarchical,
    verbose=True
)

result = vacation_planning_crew.kickoff(inputs=vacation_details)

# Load and print the final itinerary
with open('final_itinerary.json') as f:
    final_itinerary_data = json.load(f)

pprint(final_itinerary_data)

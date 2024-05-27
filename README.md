# MultiAgent-CrewAI: Automated Vacation Planner Using Multiple AI Agents

This project demonstrates how to create an automated vacation planner using AI agents and the Crew AI framework. The planner autonomously handles various aspects of vacation planning, such as finding accommodation, planning daily itineraries, and managing the budget.

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Setup Instructions](#setup-instructions)
4. [Agents Definition](#agents-definition)
5. [Tasks Definition](#tasks-definition)
6. [Running the Project](#running-the-project)
7. [Final Output](#final-output)

## Introduction
This project leverages the Crew AI framework to create a multi-agent system that automates the process of planning a vacation. By defining specialized agents and their respective tasks, the system can efficiently find accommodation, plan daily activities, and manage the budget for a vacation.

## Project Structure
- `travel_agent.py`: Main script that defines agents, tasks, and executes the vacation planning process.
- `utils.py`: Utility functions for fetching API keys.
- `requirements.txt`: List of required Python packages.

## Setup Instructions

### Prerequisites
- Python 3.7+
- OpenAI API key
- Serper API key

### Step-by-Step Setup

1. **Clone the Repository**
    ```sh
    git clone https://github.com/techindicium/MultiAgent-CrewAI.git
    cd MultiAgent-CrewAI
    ```

2. **Install Required Packages**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set Up API Keys**
    - Create a file named `.env` in the root directory of the project and add your API keys:
      ```env
      OPENAI_API_KEY=your_openai_api_key
      SERPER_API_KEY=your_serper_api_key
      ```

## Agents Definition
Agents are autonomous units that perform specific roles within the vacation planning process. We define three agents in this project:

### Venue Coordinator
- **Role:** Identify suitable accommodation options.
- **Tools:** `SerperDevTool`, `ScrapeWebsiteTool`
- **Goal:** Find hotels, rental homes, or vacation rentals that meet specified criteria.

```python
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
```

### Itinerary Planner
- **Role:** Create a detailed itinerary including daily excursions and activities.
- **Tools:** `SerperDevTool`, `ScrapeWebsiteTool`
- **Goal:** Plan activities considering the traveler's interests, budget, and logistics.

```python
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
```

### Budgeting Agent
- **Role:** Manage the overall budget for the trip.
- **Tools:** `SerperDevTool`
- **Goal:** Ensure all aspects of the vacation stay within the allocated budget.

```python
budgeting_agent = Agent(
    role="Budgeting Agent",
    goal="Manage the overall budget for the trip, considering the cost of accommodation and daily activities.",
    tools=[search_tool],
    verbose=True,
    backstory=(
        "With a knack for financial planning, you ensure the vacation remains within budget while maximizing value and enjoyment."
    )
)
```

## Tasks Definition
Tasks define what each agent needs to accomplish. Properly structured tasks are crucial for guiding agents to perform their roles effectively.

### Venue Coordinator Task
```python
hotel_task = Task(
    description="Find a hotel or rental in {vacation_city} "
                "that meets criteria for {vacation_details}, {budget}, {group_size}, {start_date} and {end_date}.",
    expected_output="Details of suitable rental options, including name, address, capacity, price per night, available dates, description, and amenities.",
    human_input=True,
    output_json=RentalDetails,
    output_file="venue_details.json",
    agent=rental_coordinator
)
```

### Itinerary Planner Task
```python
itinerary_task = Task(
    description="Plan a full itinerary for the trip in {vacation_city}, considering {vacation_details}, {budget}, and {group_size}. Include daily excursions and local activities, specifying if a rental car is needed.",
    expected_output="A detailed itinerary for each day of the trip, including activities, locations, estimated costs, and rental car needs.",
    human_input=True,
    output_json=FullItinerary,
    output_file="itinerary_details.json",
    agent=itinerary_planner
)
```

### Budgeting Agent Task
```python
budgeting_task = Task(
    description="Ensure the total cost of the trip, including accommodation and daily activities, stays within the allocated budget of {budget}.",
    expected_output="Adjusted itinerary with budget considerations, including the cost of accommodation and daily activities.",
    human_input=True,
    output_json=FullItinerary,
    output_file="final_itinerary.json",
    agent=budgeting_agent
)
```

## Running the Project
To run the vacation planner, follow these steps:

1. **Initialize the Crew**
   Define the crew with the agents and tasks.
   ```python
   vacation_planning_crew = Crew(
       agents=[rental_coordinator, itinerary_planner, budgeting_agent],
       tasks=[hotel_task, itinerary_task, budgeting_task],
       manager_llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
       process=Process.hierarchical,
       verbose=True
   )
   ```

2. **Kickoff the Process**
   Provide the necessary input data and start the execution.
   ```python
   vacation_details = {
       'vacation_city': "Honolulu",
       'vacation_details': "A vacation for an adventurous family of 7 who want to explore the island, see the nature, and experience some good Hawaiian food and culture",
       'start_date': "2024-06-15",
       'end_date': "2024-06-22",
       'group_size': 7,
       'budget': 10000,
   }

   result = vacation_planning_crew.kickoff(inputs=vacation_details)
   ```

3. **Load and Print the Final Itinerary**
   After the tasks are completed, load the results from the JSON file.
   ```python
   with open('final_itinerary.json') as f:
       final_itinerary_data = json.load(f)

   pprint(final_itinerary_data)
   ```

## Final Output
The final output will be a detailed itinerary for the vacation, including:
- Accommodation options
- Daily activities and excursions
- Budget management details

This output is saved in `final_itinerary.json` and can be printed for review.

By following these steps, you can recreate the automated vacation planner and understand how AI agents interact to achieve the overall goal. This approach demonstrates the power of AI-driven automation in simplifying and streamlining complex processes.

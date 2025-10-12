from crewai import Agent
from tools.fred_client import get_fred_data

# Create a Market Analyst agent
market_analyst = Agent(
    role='Macroeconomic Analyst',
    goal='Provide macroeconomic context for the stock analysis.',
    backstory=(
        'An economist with expertise in tracking and interpreting broad economic indicators. '
        'Your insights help frame the company\'s performance within the larger economic picture.'
    ),
    tools=[get_fred_data],
    verbose=True,
    allow_delegation=False
)
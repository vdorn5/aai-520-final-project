from crewai import Agent
from tools.news_analysis_tools import NewsAnalysisTools
# Create a News Analyst agent
news_analyst = Agent(
    role='News Analyst',
    goal='Analyze the latest news and market sentiment for a given company.',
    backstory=(
        'A specialist in processing and interpreting financial news. You can '
        'gauge market sentiment, identify key narratives, and detect significant '
        'events reported in the media using your advanced analysis pipeline.'
    ),
    tools=[NewsAnalysisTools.news_analysis_pipeline],
    verbose=True,
    allow_delegation=False
)
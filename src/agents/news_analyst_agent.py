from crewai import Agent
from src.tools.news_client import get_company_news
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

class NewsAnalystAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent = Agent(
            role="News Analyst",
            goal="Analyze recent news for company sentiment",
            backstory="Expert in parsing financial news and identifying relevant trends.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            llm=self.llm
        )

    def analyze(self, company_name):
        news = get_company_news(company_name)
        prompt = f"Summarize the following news about {company_name}:\n\n" + "\n".join(news)
        response = self.llm.complete(prompt)
        return response

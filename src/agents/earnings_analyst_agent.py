from crewai import Agent
from src.tools.yfinance_client import get_yfinance_financials

class EarningsAnalystAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent = Agent(
            role="Earnings Analyst",
            goal="Review recent earnings reports for the company",
            backstory="Expert in financial statements and valuation.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            llm=self.llm
        )

    def analyze(self, ticker):
        financials = get_yfinance_financials(ticker)
        prompt = f"Summarize the key financial insights for {ticker}:\n{financials}"
        response = self.llm.complete(prompt)
        return response

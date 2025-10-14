from src.agents.news_analyst_agent import NewsAnalystAgent
from src.agents.earnings_analyst_agent import EarningsAnalystAgent
from src.agents.market_analyst_agent import MarketAnalystAgent
from src.agents.critic_agent import CriticAgent
from src.utils.llm_wrapper import LLMWrapper

class OrchestratorAgent:
    def __init__(self):
        self.llm = LLMWrapper()
        self.news_agent = NewsAnalystAgent(self.llm)
        self.earnings_agent = EarningsAnalystAgent(self.llm)
        self.market_agent = MarketAnalystAgent(self.llm)
        self.critic_agent = CriticAgent(self.llm)

    def run(self, ticker):
        print(f"\nStarting Investment Research for: {ticker}\n")

        print("News Summary:")
        news_summary = self.news_agent.analyze(ticker)
        print(news_summary)

        print("\nEarnings Summary:")
        earnings_summary = self.earnings_agent.analyze(ticker)
        print(earnings_summary)

        print("\nMarket Context:")
        market_summary = self.market_agent.analyze()
        print(market_summary)

        # Combine all sections into one report
        full_report = f"""
    # Investment Research Report: {ticker}

    ## News Summary:
    {news_summary}

    ## Earnings Summary:
    {earnings_summary}

    ## Market Context:
    {market_summary}
    """

        print("\nRunning Critique:\n")
        critique = self.critic_agent.critique(full_report)
        print(critique)

        print("\nFinal Investment Report with Critique Generated.\n")


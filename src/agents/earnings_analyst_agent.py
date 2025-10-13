from crewai import Agent
from tools.yfinance_client import get_stock_data, get_financial_statements
from tools.memory_tools import read_memory
# Create an Earnings Analyst agent
earnings_analyst = Agent(
  role='Earnings Analyst',
  goal='Analyze the financial statements of a company to assess its financial health and performance, considering any past analyses.',
  backstory=(
    'A meticulous financial analyst with a deep understanding of corporate finance. '
    'You specialize in dissecting income statements, balance sheets, and cash flow statements '
    'to uncover underlying trends and financial stability. You also consult past reports to see what has changed.'
  ),
  tools=[get_stock_data, get_financial_statements, read_memory], # Give this agent the read_memory tool
  verbose=True,
  allow_delegation=False
)
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

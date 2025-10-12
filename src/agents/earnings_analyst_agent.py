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
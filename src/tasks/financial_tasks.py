# tasks/financial_tasks.py

from crewai import Task

memory_retrieval_task = Task(
    description='Retrieve any past analysis for the stock {ticker} from the memory log using the Read Memory Tool.',
    expected_output='A summary of past analysis for {ticker}, or a statement that no prior analysis was found.',
    agent=None # Will be assigned to earnings_analyst
)

# Task for the Earnings Analyst
earnings_analysis_task = Task(
  description=(
    'Analyze the most recent annual financial statements for the stock {ticker}. '
    'First, consider any insights from prior analyses provided in the context. '
    'Then, examine the Income Statement, Balance Sheet, and Cash Flow Statement to identify '
    'key trends in revenue, profitability, debt, and cash flow. '
    'Provide a summary of the company\'s financial health.'
  ),
  expected_output=(
    'A concise summary of the company\'s financial health based on its latest '
    'annual financial statements, highlighting key trends and figures, and noting any changes from past analyses.'
  ),
  agent=None,
  context=[memory_retrieval_task]
)

# Task for the News Analyst
news_analysis_task = Task(
    description=(
        'Conduct a comprehensive news analysis for the company associated with the ticker {ticker}. '
        'Use your advanced pipeline to determine the overall market sentiment. '
        'The final output should be a summary of the sentiment analysis.'
    ),
    expected_output=(
        'A summary of the recent news sentiment (positive, negative, or neutral) '
        'surrounding the company.'
    ),
    agent=None
)

# Task for the Market Analyst
market_analysis_task = Task(
    description=(
        'Analyze the current macroeconomic environment. Fetch the latest data for '
        'Gross Domestic Product (GDP) and the Consumer Price Index (CPIAUCSL). '
        'Summarize the current economic trends and their potential impact on the stock market '
        'and the company with ticker {ticker}.'
    ),
    expected_output=(
        'A summary of the current macroeconomic trends (e.g., inflation, economic growth) '
        'and a brief analysis of their potential impact on the company.'
    ),
    agent=None
)

# Task for the Investment Advisor (Draft Generation)
advisory_draft_task = Task(
  description=(
    'Synthesize the financial statement analysis, news sentiment analysis, and macroeconomic '
    'context. Based on all this information, formulate a DRAFT investment recommendation '
    '(Buy, Hold, or Sell) for {ticker}. Provide a detailed justification for your recommendation, '
    'referencing specific data points from all three analyses.'
  ),
  expected_output=(
    'A draft investment report with a clear recommendation (Buy, Hold, or Sell) '
    'and a detailed rationale that integrates insights from the financial statements, '
    'news sentiment, and macroeconomic environment.'
  ),
  agent=None,
  context=[earnings_analysis_task, news_analysis_task, market_analysis_task]
)

# Task for the Critic Agent (Final Report Generation)
report_critique_task = Task(
    description=(
        'Review the DRAFT investment report provided in the context. Your role is to act as a '
        'skeptical quality assurance analyst. Critique the report based on the following principles:\n'
        '1. Clarity and Cohesion: Is the main investment thesis clear and easy to understand?\n'
        '2. Evidentiary Support: Are all claims backed by specific data points from the analyses?\n'
        '3. Risk Assessment: Does the report adequately identify and discuss the primary risks?\n\n'
        'After your critique, produce a FINAL, polished investment report that incorporates your feedback '
        'and provides a definitive recommendation for {ticker}.'
    ),
    expected_output=(
        'A final, comprehensive, and polished investment report with a clear recommendation '
        '(Buy, Hold, or Sell) and a detailed, well-supported rationale that has been '
        'critically reviewed and refined.'
    ),
    agent=None,
    context=[advisory_draft_task]
)
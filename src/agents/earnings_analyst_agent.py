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
from src.tools.yfinance_client import get_yfinance_financials, get_analyst_recommendations
from src.tools.memory_tools import read_memory
import pandas as pd
import io
import json
from functools import lru_cache

@lru_cache(maxsize=50)
def get_financials_cached(ticker):
    """Cached version of financial fetcher to avoid repeated API calls."""
    return get_yfinance_financials(ticker)

class EarningsAnalystAgent:
    def __init__(self, llm):
        self.llm = llm

        # Create the agent with the tools
        self.agent = Agent(
            role="Earnings Analyst",
            goal="Review earnings reports and interpret key financial data.",
            backstory="Expert in financial analysis and equity research.",
            verbose=True,
            llm=self.llm
        )

    # Helper: parse financials
    def _parse_financials(self, financials_str):
        """Convert the yfinance .to_string() output into a DataFrame for quick extraction."""
        try:
            df = pd.read_csv(io.StringIO(financials_str))
            return df
        except Exception as e:
            print(f"Warning: Could not parse financials as CSV: {e}")
            # fallback simple parse
            lines = [line.strip() for line in financials_str.split("\n") if line.strip()]
            return lines   

    # Main analyze method
    def analyze(self, ticker):
        print(f"\n[+] Running Earnings Analysis for {ticker}...\n")

        # First, retrieve any past analysis from memory
        print(f"[+] Retrieving past analysis for {ticker}...")
        past_analysis = read_memory.run(ticker=ticker)
        print(f"Past analysis: {past_analysis[:200]}..." if len(past_analysis) > 200 else f"Past analysis: {past_analysis}")

        # Fetch current data
        financials = get_financials_cached(ticker)
        recommendations = get_analyst_recommendations(ticker)

        # Error Handling 
        if not financials:
            return f"No financial data available for {ticker}."
        if not recommendations:
            recommendations = "No analyst recommendations available."

        # Attempt to parse numeric insights (for potential future use)
        parsed_financials = self._parse_financials(financials)
        if isinstance(parsed_financials, pd.DataFrame):
            print(f"Parsed financials into DataFrame with shape: {parsed_financials.shape}")
        else:
            print(f"Financials parsed as text with {len(parsed_financials)} lines")
        
        # Structured LLM prompt 
        prompt = f"""
You are an Earnings Analyst. 
Review the financial report and provide a structured analysis in JSON format.

**Company:** {ticker}

**Instructions:**
Analyze the financial data and respond ONLY in **pretty-printed JSON** with **indentation and line breaks**. 
Use this exact structure:
{{
    "revenue": "string - Total revenue with growth percentage if available",
    "net_income": "string - Net income with growth/decline percentage",
    "eps": "string - Earnings per share with comparison to previous period",
    "growth_comment": "string - Brief analysis of growth trends and key metrics",
    "analyst_sentiment": "string - Summary of analyst recommendations and sentiment",
    "overall_sentiment": "positive|neutral|negative - Overall investment sentiment",
    "change_from_past": "string - How this analysis differs from or confirms past analysis"
}}

**PAST ANALYSIS CONTEXT:**
{past_analysis}

**Financial Data to Analyze:**
1. **Quantitative extraction** - Identify key figures:
   - Total Revenue
   - Net Income  
   - Earnings Per Share (EPS)
   - Year-over-year or quarter-over-quarter changes

2. **Qualitative interpretation** - Discuss:
   - Performance trends
   - Profitability indicators
   - Growth signals
   - Changes from past analysis (if any)

3. **Analyst sentiment** - Consider these latest recommendations:
{recommendations}

**Raw financial data:**
{financials}

**Important:** Compare current findings with past analysis to identify trends, changes, or confirmations. Note any significant differences or improvements/deteriorations.

Respond with ONLY the JSON object, no additional text or formatting.
"""
        response = self.llm.complete(prompt)

        # Parse JSON response
        try:
            result = json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse LLM response as JSON: {e}")
            print(f"Raw response: {response[:200]}...")
            result = {
                "error": "Failed to parse JSON response", 
                "raw_output": response,
                "revenue": "Unable to extract",
                "net_income": "Unable to extract", 
                "eps": "Unable to extract",
                "growth_comment": "Analysis failed due to parsing error",
                "analyst_sentiment": "Unable to extract",
                "overall_sentiment": "neutral",
                "change_from_past": "Unable to compare due to parsing error"
            }

        return result

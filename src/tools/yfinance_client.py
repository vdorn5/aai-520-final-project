from crewai.tools import tool
import yfinance as yf
# --- Tool for Basic Stock Data ---
@tool("Stock Ticker Data Tool")
def get_stock_data(ticker: str) -> dict:
    """A tool to get basic financial data for a given stock ticker."""
    # Implementation remains the same...
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "longName": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "marketCap": info.get("marketCap"),
        "trailingPE": info.get("trailingPE"),
        "forwardPE": info.get("forwardPE"),
        "dividendYield": info.get("dividendYield"),
        "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
        "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
        "regularMarketPrice": info.get("regularMarketPrice")
    }

# --- Tool for Financial Statements (for EarningsAnalyst) ---
@tool("Company Financial Statements Tool")
def get_financial_statements(ticker: str) -> str:
    """
    A tool to get the most recent annual financial statements (Income Statement,
    Balance Sheet, and Cash Flow) for a given stock ticker.
    """
    stock = yf.Ticker(ticker)
    
    # Fetch the most recent annual data
    income_statement = stock.income_stmt.iloc[:, 0]
    balance_sheet = stock.balance_sheet.iloc[:, 0]
    cash_flow = stock.cashflow.iloc[:, 0]
    
    # Format into a single string for the LLM
    report = f"""
    Income Statement:\n{income_statement.to_string()}\n
    Balance Sheet:\n{balance_sheet.to_string()}\n
    Cash Flow Statement:\n{cash_flow.to_string()}
    """
    return report
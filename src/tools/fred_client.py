# tools/analysis_tools.py
from crewai.tools import tool
from fredapi import Fred

# --- Tool for FRED Economic Data (for MarketAnalyst) ---
@tool("FRED Economic Data Tool")
def get_fred_data(series_id: str, limit: int = 5) -> str:
    """
    A tool to fetch economic data from the FRED API for a given series ID.
    Common series IDs include:
    - 'GDP': Gross Domestic Product
    - 'CPIAUCSL': Consumer Price Index for All Urban Consumers
    - 'UNRATE': Civilian Unemployment Rate
    """
    try:
        # The Fred class automatically looks for the 'FRED_API_KEY' environment variable.
        fred = Fred()
        data = fred.get_series(series_id).tail(limit)
        return data.to_string()
    except Exception as e:
        # The error message from the library is very descriptive, so we'll return it.
        return f"Error fetching FRED data: {e}"

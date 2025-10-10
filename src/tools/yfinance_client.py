import yfinance as yf

def get_yfinance_financials(ticker):
    stock = yf.Ticker(ticker)
    financials = stock.financials
    return financials.to_string()

def get_analyst_recommendations(ticker):
    stock = yf.Ticker(ticker)
    return stock.recommendations.tail(3).to_string()

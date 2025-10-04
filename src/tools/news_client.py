import requests
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_company_news(company_name):
    url = f"https://newsapi.org/v2/everything?q={company_name}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])[:5]
    return [article["title"] + " - " + article["description"] for article in articles if article.get("description")]


import os
import yfinance as yf
import nltk
import re
from crewai.tools import tool
from newsapi import NewsApiClient
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

# Ensure stopwords are downloaded
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# --- Class for Advanced News Analysis Pipeline (for NewsAnalyst) ---
class NewsAnalysisTools:
    # The news_analysis_pipeline and its helper methods remain the same...
    @staticmethod
    @tool("Advanced News Analysis Tool")
    def news_analysis_pipeline(company_name: str) -> str:
        """
        A complete news analysis pipeline.
        1. Ingests news articles for a given company.
        2. Preprocesses the text of each article.
        3. Classifies the sentiment of each article using a financial model.
        4. Returns a consolidated list of processed articles for further analysis.
        """
        # Step 1: Ingest News
        newsapi = NewsApiClient(api_key=os.environ.get("NEWSAPI_KEY"))
        try:
            top_headlines = newsapi.get_everything(
                q=company_name,
                language='en',
                sort_by='publishedAt',
                page_size=5
            )
            articles = top_headlines['articles']
        except Exception as e:
            return f"Error fetching news: {e}"

        processed_articles = []
        for article in articles:
            content = article['content'] or article['description'] or ""
            if not content:
                continue
            
            # Step 2: Preprocess Text
            preprocessed_text = NewsAnalysisTools._preprocess_text(content)
            
            # Step 3: Classify Sentiment
            sentiment = NewsAnalysisTools._classify_sentiment(preprocessed_text)
            
            processed_articles.append({
                "title": article['title'],
                "url": article['url'],
                "content_preview": preprocessed_text[:200] + "...",
                "sentiment": sentiment
            })
        
        return str(processed_articles)

    @staticmethod
    def _preprocess_text(text: str) -> str:
        """Internal method to clean and normalize text."""
        if not text:
            return ""
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Convert to lowercase
        text = text.lower()
        # Tokenize and remove stopwords
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_text = [w for w in word_tokens if not w in stop_words]
        return " ".join(filtered_text)

    @staticmethod
    def _classify_sentiment(text: str) -> str:
        """Internal method to classify sentiment using FinBERT."""
        if not text:
            return "Neutral"
        try:
            tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
            model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
            
            inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                logits = model(**inputs).logits
            
            scores = {k: v for k, v in zip(model.config.id2label.values(), torch.softmax(logits, dim=0).tolist())}
            # Return the sentiment with the highest score
            return max(scores, key=scores.get)
        except Exception as e:
            # Fallback in case of model error
            return f"Sentiment analysis failed: {e}"
            
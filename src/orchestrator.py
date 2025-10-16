# main.py

import os
from dotenv import load_dotenv
from crewai import Crew, Process

# Load environment variables
load_dotenv()

# Import the tool we will call manually
from tools.memory_tools import save_memory

from agents.earnings_analyst_agent import earnings_analyst
from agents.news_analyst_agent import news_analyst
from agents.market_analyst_agent import market_analyst
from agents.critic_agent import critic_agent
from agents.investment_agents import investment_advisor

from tasks.financial_tasks import (
    memory_retrieval_task,
    earnings_analysis_task, 
    news_analysis_task, 
    market_analysis_task, 
    advisory_draft_task,
    report_critique_task
)



# Assign agents to their respective tasks
memory_retrieval_task.agent = earnings_analyst
earnings_analysis_task.agent = earnings_analyst
news_analysis_task.agent = news_analyst
market_analysis_task.agent = market_analyst
advisory_draft_task.agent = investment_advisor
report_critique_task.agent = critic_agent

# Define the context for the earnings analysis task
earnings_analysis_task.context = [memory_retrieval_task]

def run_analysis(ticker: str):
    """
    Initializes and runs the financial analysis crew for a given stock ticker.
    """
    financial_crew = Crew(
      agents=[earnings_analyst, news_analyst, market_analyst, investment_advisor, critic_agent],
      tasks=[
          memory_retrieval_task,
          earnings_analysis_task, 
          news_analysis_task, 
          market_analysis_task, 
          advisory_draft_task, 
          report_critique_task
      ],
      process=Process.sequential,
      verbose=True
    )

    # Kick off the crew's work
    final_report = financial_crew.kickoff(inputs={'ticker': ticker})
    
    print("\n\n########################")
    print("## Final Analysis Report:")
    print("########################")
    print(final_report)

    # Manually save the final report to the memory log
    print("\n\n########################")
    print("## Saving Report to Memory...")
    print("########################")
    save_status = save_memory.run(report=final_report, ticker=ticker)
    print(save_status)

if __name__ == "__main__":
    stock_ticker = "TSLA"
    print(f"🚀 Starting analysis for {stock_ticker}...")
    run_analysis(stock_ticker)
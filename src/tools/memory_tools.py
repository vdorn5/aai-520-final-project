# tools/analysis_tools.py

import os
import re
import torch
from datetime import datetime
from crewai.tools import tool


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR)) 
MEMORY_LOG_FILE = os.path.join(PROJECT_ROOT, "memory_log.txt")

# --- Tools for Memory ---
@tool("Read Memory Tool")
def read_memory(ticker: str) -> str:
    """A tool to read the memory log for any prior analysis on a given stock ticker."""
    try:
        with open(MEMORY_LOG_FILE, "r") as f:
            full_log = f.read()
        
        entries = full_log.split("\n---\n")
        
        relevant_memories = [entry for entry in entries if ticker.upper() in entry]
        
        if not relevant_memories:
            return f"No prior analysis found for {ticker}."
            
        return "\n---\n".join(relevant_memories)
    except FileNotFoundError:
        return "No memory log found. Starting fresh."

@tool("Save Memory Tool")
def save_memory(report: str, ticker: str) -> str:
    """A tool to save the final investment report to the memory log for future reference."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    memory_entry = f"Date: {timestamp} | Ticker: {ticker.upper()} | Report: {report}\n---\n"
    
    with open(MEMORY_LOG_FILE, "a") as f:
        f.write(memory_entry)
        
    return f"Report for {ticker.upper()} has been saved to memory."
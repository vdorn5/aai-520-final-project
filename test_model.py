#!/usr/bin/env python3
"""
Simple test script to run the investment research model
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_model():
    """Test the model with a simple example"""
    
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_key_here")
        return False
    
    print("✅ API key found")
    
    try:
        from src.agents.orchestrator_agent import OrchestratorAgent
        print("✅ Successfully imported OrchestratorAgent")
        
        # Initialize the orchestrator
        orchestrator = OrchestratorAgent()
        print("✅ Successfully initialized OrchestratorAgent")
        
        # Test with AAPL
        print("\n🚀 Running investment research for AAPL...")
        result = orchestrator.run("AAPL")
        
        print("✅ Model ran successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error running model: {e}")
        return False

if __name__ == "__main__":
    test_model()

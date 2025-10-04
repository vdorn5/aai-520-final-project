from crewai import Agent

class MarketAnalystAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent = Agent(
            role="Market Analyst",
            goal="Provide current market trends and economic outlook",
            backstory="Expert in macroeconomic trends and market indices.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            llm=self.llm
        )

    def analyze(self):
        prompt = "Provide a short summary of current US market conditions and macroeconomic trends."
        return self.llm.complete(prompt)

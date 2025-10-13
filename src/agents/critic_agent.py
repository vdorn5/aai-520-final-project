from crewai import Agent
# Create the Critic Agent
critic_agent = Agent(
    role='Quality Assurance Critic',
    goal='Critique and refine the investment report to ensure it is comprehensive, accurate, and actionable.',
    backstory=(
        'A highly experienced investment strategist with a keen eye for detail. You are tasked with '
        'reviewing financial reports to identify any gaps, logical inconsistencies, or unsupported claims. '
        'Your feedback is crucial for producing a final, high-quality investment recommendation.'
    ),
    verbose=True,
    allow_delegation=False
)

class CriticAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent = Agent(
            role="Critic",
            goal="Evaluate and provide constructive feedback on investment reports",
            backstory="A strict but fair financial critic who checks quality and completeness.",
            verbose=True,
            allow_delegation=False,
            tools=[],
            llm=self.llm
        )

    def critique(self, report_text):
        prompt = f"""
You're a financial report evaluator. Critically evaluate the following investment research report. Assess it based on:

1. Relevance to the company
2. Clarity and conciseness
3. Factual correctness
4. Completeness of the analysis

Give a score from 1 to 10 and explain your reasoning.

Report:
{report_text}
"""
        return self.llm.complete(prompt)

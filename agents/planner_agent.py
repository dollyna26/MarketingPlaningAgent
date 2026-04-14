# agents/planner_agent.py
# Employee #1: The Planner - Breaks big goals into small steps

from crewai import Agent

def create_planner_agent(llm):
    """
    Creates the Planner agent.
    This agent takes a big marketing goal and breaks it into small tasks.
    """
    
    planner = Agent(
        role="Marketing Planner",
        goal="Break down marketing goals into clear, actionable steps",
        backstory="""
        You are an expert marketing planner with 10 years of experience.
        You take big, vague goals and turn them into specific, actionable tasks.
        You think step-by-step and create clear plans that anyone can follow.
        """,
        llm=llm,  # The AI brain we created
        verbose=True,  # Show what it's thinking
        allow_delegation=False,  # This agent works alone
    )
    
    return planner
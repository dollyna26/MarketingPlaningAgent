# agents/strategy_agent.py
# Employee #3: The Strategist - Creates the marketing plan

from crewai import Agent

def create_strategy_agent(llm):
    """
    Creates the Strategy agent.
    This agent builds the actual marketing strategy based on research.
    """
    
    strategist = Agent(
        role="Marketing Strategist",
        goal="Create a comprehensive marketing strategy with budget, channels, and KPIs",
        backstory="""
        You are a senior marketing strategist who has built campaigns for top brands.
        You take research insights and turn them into actionable strategies.
        You specify which channels to use, how to allocate budget, and what metrics to track.
        You create strategies that are realistic and effective.
        """,
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    
    return strategist
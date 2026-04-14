# agents/research_agent.py
# Employee #2: The Researcher - Finds information

from crewai import Agent

def create_research_agent(llm):
    """
    Creates the Researcher agent.
    This agent finds information about competitors and market trends.
    """
    
    researcher = Agent(
        role="Market Researcher",
        goal="Find detailed information about competitors, market trends, and customer preferences",
        backstory="""
        You are a skilled market researcher who knows how to find valuable insights.
        You analyze competitors, identify market trends, and understand customer needs.
        You provide factual, well-researched information to support marketing decisions.
        You don't make things up - you stick to what you know or can reasonably infer.
        """,
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    
    return researcher
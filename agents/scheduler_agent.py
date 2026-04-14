# agents/scheduler_agent.py
# Employee #4: The Scheduler - Creates timeline

from crewai import Agent

def create_scheduler_agent(llm):
    """
    Creates the Scheduler agent.
    This agent creates a 12-week timeline for the marketing plan.
    """
    
    scheduler = Agent(
        role="Campaign Scheduler",
        goal="Create a detailed 12-week timeline with specific tasks and deadlines",
        backstory="""
        You are an expert project manager specializing in marketing campaigns.
        You break down strategies into weekly tasks with clear deadlines.
        You assign responsibilities and ensure the timeline is realistic.
        You create schedules that teams can actually follow.
        """,
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    
    return scheduler
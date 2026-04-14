# agents/report_agent.py
# Employee #5: The Reporter - Writes final report

from crewai import Agent

def create_report_agent(llm):
    """
    Creates the Report agent.
    This agent compiles everything into a professional final report.
    """
    
    reporter = Agent(
        role="Marketing Report Writer",
        goal="Create a professional, well-formatted final marketing plan report",
        backstory="""
        You are a professional report writer who specializes in marketing documents.
        You take complex information and present it clearly and professionally.
        You format reports for easy reading with sections, bullet points, and summaries.
        You write executive summaries that busy CEOs can quickly understand.
        """,
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    
    return reporter
# crew.py
# The Manager - Coordinates all 5 employees
# crew.py
import warnings
warnings.filterwarnings("ignore")
import os
os.environ["CREWAI_TELEMETRY"] = "false"

# ... rest of imports
from datetime import datetime
# ... etc

import os
from datetime import datetime
from crewai import Crew, Process

# Import our 5 agents
from agents.planner_agent import create_planner_agent
from agents.research_agent import create_research_agent
from agents.strategy_agent import create_strategy_agent
from agents.scheduler_agent import create_scheduler_agent
from agents.report_agent import create_report_agent

# Import task creator
from tasks.task_definitions import TaskFactory

# Import brain connector
from utils.llm_config import get_llm


class MarketingCrew:
    """
    This is the manager class.
    It hires all 5 agents and makes them work together.
    """
    
    def __init__(self, goal: str):
        self.goal = goal
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Step 1: Turn on the AI brain
        print("  Connecting to Groq AI...")
        self.llm = get_llm()
        print("  ✓ AI Brain connected (Groq llama-3.1-8b-instant)")
        
        # Step 2: Build the team
        self._build_crew()
    
    def _build_crew(self):
        """Hire all 5 agents and assign their tasks"""
        print("  Hiring 5 marketing agents...")
        
        # Hire agents (create them)
        self.planner = create_planner_agent(self.llm)
        self.researcher = create_research_agent(self.llm)
        self.strategist = create_strategy_agent(self.llm)
        self.scheduler = create_scheduler_agent(self.llm)
        self.reporter = create_report_agent(self.llm)
        
        print("  ✓ Team ready: Planner | Researcher | Strategist | Scheduler | Reporter")
        
        # Create tasks for each agent
        print("  Creating task assignments...")
        task_factory = TaskFactory(self.goal)
        
        self.task_plan = task_factory.planning_task(self.planner)
        self.task_research = task_factory.research_task(self.researcher)
        self.task_strategy = task_factory.strategy_task(self.strategist)
        self.task_schedule = task_factory.scheduling_task(self.scheduler)
        self.task_report = task_factory.report_task(self.reporter)
        
        print("  ✓ Tasks created")
        
        # Create the crew (team) - SEQUENTIAL means one after another
        self.crew = Crew(
            agents=[
                self.planner,
                self.researcher,
                self.strategist,
                self.scheduler,
                self.reporter,
            ],
            tasks=[
                self.task_plan,
                self.task_research,
                self.task_strategy,
                self.task_schedule,
                self.task_report,
            ],
            process=Process.sequential,  # One agent finishes, then next starts
            verbose=True,  # Show what's happening
        )
        print("  ✓ Crew assembled!\n")
    
    def run(self):
        """Start the work!"""
        print("=" * 60)
        print("  STARTING MARKETING CAMPAIGN CREATION")
        print("=" * 60)
        print()
        
        # This runs all 5 agents in order
        result = self.crew.kickoff()
        
        return str(result)
    
    def save_report(self, result: str):
        """Save the final report to a file"""
        # Create output folder if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        # Create filename with date/time
        filename = f"output/marketing_plan_{self.timestamp}.txt"
        
        # Write the report
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write("  MARKETING PLANNING ASSISTANT - FINAL REPORT\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"GOAL: {self.goal}\n")
            f.write(f"DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("=" * 70 + "\n\n")
            f.write(result)
        
        return filename
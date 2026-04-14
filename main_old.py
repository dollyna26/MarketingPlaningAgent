import warnings
warnings.filterwarnings("ignore")
import os
import sys
from datetime import datetime

# Load API key
from dotenv import load_dotenv
load_dotenv()

# Check API key
if not os.getenv("GROQ_API_KEY"):
    print("\n" + "!" * 50)
    print("ERROR: No GROQ_API_KEY found!")
    print("!" * 50)
    print("\n1. Get free key: https://console.groq.com")
    print("2. Create .env file with: GROQ_API_KEY=your_key_here")
    sys.exit(1)

# Import AI tools
from langchain_groq import ChatGroq
from crewai import Agent, Task, Crew, Process

# AI BRAIN

def get_brain():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.1-8b-instant",
        temperature=0.7,
    )

# 5 AGENTS (DEFINED RIGHT HERE - NO IMPORTS NEEDED!)

def create_planner(brain):
    return Agent(
        role="Marketing Planner",
        goal="Break goals into clear, actionable steps",
        backstory="Expert marketing planner with 10 years experience.",
        llm=brain, verbose=False, allow_delegation=False,
    )

def create_researcher(brain):
    return Agent(
        role="Market Researcher",
        goal="Find audience, competitors, trends, and challenges",
        backstory="Skilled market researcher.",
        llm=brain, verbose=False, allow_delegation=False,
    )

def create_strategist(brain):
    return Agent(
        role="Marketing Strategist",
        goal="Create strategy with channels, budget, and KPIs",
        backstory="Senior marketing strategist.",
        llm=brain, verbose=False, allow_delegation=False,
    )

def create_scheduler(brain):
    return Agent(
        role="Campaign Scheduler",
        goal="Create 12-week timeline with tasks",
        backstory="Expert project manager.",
        llm=brain, verbose=False, allow_delegation=False,
    )

def create_reporter(brain):
    return Agent(
        role="Report Writer",
        goal="Compile professional final report",
        backstory="Professional writer.",
        llm=brain, verbose=False, allow_delegation=False,
    )

# TASKS

def create_tasks(goal, planner, researcher, strategist, scheduler, reporter):
    return [
        Task(description=f"Break into 5-7 steps: {goal}", 
             expected_output="Numbered list", agent=planner),
        Task(description=f"Research audience, competitors, trends for: {goal}", 
             expected_output="Research report", agent=researcher),
        Task(description=f"Create strategy (channels, budget, KPIs) for: {goal}", 
             expected_output="Marketing strategy", agent=strategist),
        Task(description=f"Create 12-week timeline for: {goal}", 
             expected_output="12-week schedule", agent=scheduler),
        Task(description=f"Write final report with 3 quick wins for: {goal}", 
             expected_output="Professional report", agent=reporter),
    ]

# THE MANAGER (CREW)

class MarketingCrew:
    def __init__(self, goal):
        self.goal = goal
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print("\n" + "=" * 60)
        print("  🎯 MARKETING AI AGENT")
        print("=" * 60)
        
        print("\n  Connecting to Groq AI...")
        brain = get_brain()
        print("  ✅ AI connected")
        
        print("  Creating 5 agents...")
        self.planner = create_planner(brain)
        self.researcher = create_researcher(brain)
        self.strategist = create_strategist(brain)
        self.scheduler = create_scheduler(brain)
        self.reporter = create_reporter(brain)
        print("  ✅ 5 agents ready")
        
        print("  Creating tasks...")
        tasks = create_tasks(goal, self.planner, self.researcher, 
                            self.strategist, self.scheduler, self.reporter)
        print("  ✅ Tasks created")
        
        print("  Assembling crew...")
        self.crew = Crew(
            agents=[self.planner, self.researcher, self.strategist, 
                    self.scheduler, self.reporter],
            tasks=tasks,
            process=Process.sequential,
            verbose=False,
        )
        print("  ✅ Crew ready!\n")
    
    def run(self):
        print("  🚀 Starting work (2-3 minutes)...")
        result = self.crew.kickoff()
        return str(result)
    
    def save(self, result):
        os.makedirs("output", exist_ok=True)
        filename = f"output/marketing_plan_{self.timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("  MARKETING PLAN\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Goal: {self.goal}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("=" * 60 + "\n\n")
            f.write(result)
        return filename

# USER MENU

def show_menu():
    print("\nChoose a marketing goal:")
    print("  [1] Competitor analysis (SaaS)")
    print("  [2] Social media for eco water bottle")
    print("  [3] Email marketing (boost 30%)")
    print("  [4] Influencer marketing (fitness app)")
    print("  [5] B2B content marketing")
    print("  [C] Custom goal")
    print("-" * 50)

def get_choice():
    choice = input("Enter (1-5) or C: ").strip().upper()
    
    goals = {
        "1": "Analyze competitor ads in SaaS project management",
        "2": "Launch social media for eco-friendly water bottle to Gen Z",
        "3": "Q4 email strategy to boost e-commerce sales by 30%",
        "4": "Influencer plan for fitness app in India",
        "5": "Content marketing roadmap for B2B cybersecurity",
    }
    
    if choice in goals:
        return goals[choice]
    elif choice == "C":
        return input("Your goal: ").strip() or goals["1"]
    else:
        return goals["1"]


# MAIN PROGRAM

def main():
    show_menu()
    goal = get_choice()
    
    print(f"\nGoal: {goal}")
    
    crew = MarketingCrew(goal)
    result = crew.run()
    
    print("\n" + "=" * 60)
    print("  ✅ FINAL MARKETING PLAN:")
    print("=" * 60)
    print(result)
    
    filename = crew.save(result)
    print(f"\n✅ Saved to: {filename}")

if __name__ == "__main__":
    main()
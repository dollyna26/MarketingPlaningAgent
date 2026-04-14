# Marketing AI Agent - Streamlit Version

import streamlit as st
import os
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(page_title="Marketing AI Agent", page_icon="🎯")

# Check API key
if not os.getenv("GROQ_API_KEY"):
    st.error("No GROQ_API_KEY found!")
    st.info("1. Get free key: https://console.groq.com")
    st.info("2. Add to .env file: GROQ_API_KEY=your_key")
    st.stop()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Simple Agent class
class SimpleAgent:
    def __init__(self, name, role, goal, backstory):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
    
    def run(self, task):
        st.info(f"{self.name} is working...")
        
        system_msg = f"You are a {self.role}. {self.backstory} Your goal: {self.goal}"
        
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": task}
                ],
                temperature=0.7,
                max_tokens=2048,
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error in {self.name}: {e}")
            return f"Error: {str(e)}"

# Create agents
def create_agents():
    return {
        "planner": SimpleAgent("Planner", "Marketing Planner", 
                              "Break goals into clear steps",
                              "Expert marketing planner with 10 years experience."),
        "researcher": SimpleAgent("Researcher", "Market Researcher",
                                "Find audience, competitors, trends",
                                "Skilled market researcher."),
        "strategist": SimpleAgent("Strategist", "Marketing Strategist",
                                  "Create strategy with channels and budget",
                                  "Senior marketing strategist."),
        "scheduler": SimpleAgent("Scheduler", "Campaign Scheduler",
                                "Create 12-week timeline",
                                "Expert project manager."),
        "reporter": SimpleAgent("Reporter", "Report Writer",
                               "Compile professional final report",
                               "Professional writer.")
    }

# Main app
def main():
    st.title("🎯 Marketing Planning AI Agent")
    st.write("5 AI agents create your marketing plan!")
    
    # Goal selection
    goal_option = st.selectbox("Choose a goal:", [
        "Analyze competitor ads in SaaS project management",
        "Launch social media for eco-friendly water bottle to Gen Z",
        "Q4 email strategy to boost e-commerce sales by 30%",
        "Influencer plan for fitness app in India",
        "Content marketing roadmap for B2B cybersecurity",
        "Custom goal..."
    ])
    
    if goal_option == "Custom goal...":
        goal = st.text_area("Enter your marketing goal:")
    else:
        goal = goal_option
    
    # Run button
    if st.button("🚀 Create Marketing Plan", type="primary"):
        if not goal:
            st.warning("Please enter a goal!")
            return
        
        # Create agents
        agents = create_agents()
        
        # Progress bar
        progress = st.progress(0)
        status = st.empty()
        
        # Agent 1: Planner
        status.text("Planner is working...")
        plan = agents["planner"].run(f"Break this into 5-7 steps: {goal}")
        progress.progress(20)
        
        # Agent 2: Researcher
        status.text("Researcher is working...")
        research = agents["researcher"].run(f"Research: audience, competitors, trends for: {goal}")
        progress.progress(40)
        
        # Agent 3: Strategist
        status.text("Strategist is working...")
        strategy = agents["strategist"].run(f"Create strategy (channels, budget, KPIs) for: {goal}")
        progress.progress(60)
        
        # Agent 4: Scheduler
        status.text("Scheduler is working...")
        schedule = agents["scheduler"].run(f"Create 12-week timeline for: {goal}")
        progress.progress(80)
        
        # Agent 5: Reporter
        status.text("Reporter is compiling final report...")
        report = agents["reporter"].run(f"""
        Create final report for: {goal}
        
        Planning: {plan[:500]}
        Research: {research[:500]}
        Strategy: {strategy[:500]}
        Timeline: {schedule[:500]}
        
        Include: Executive Summary, Findings, Strategy, Timeline, 3 Quick Wins
        """)
        progress.progress(100)
        
        status.text("Done!")
        
        # Show result
        st.success("✅ Marketing plan created!")
        
        tab1, tab2 = st.tabs(["📋 View Plan", "⬇️ Download"])
        
        with tab1:
            st.markdown(report)
        
        with tab2:
            st.download_button(
                "Download as Text File",
                report,
                file_name=f"marketing_plan_{datetime.now().strftime('%Y%m%d')}.txt"
            )

if __name__ == "__main__":
    main()
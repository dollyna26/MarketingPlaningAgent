# app.py
# Website version - Run with: streamlit run app.py

import streamlit as st
import os
import threading
import queue
import time
from datetime import datetime
from dotenv import load_dotenv

# Load API key
load_dotenv()

# Page setup
st.set_page_config(
    page_title="Marketing AI Agent",
    page_icon="🎯",
    layout="wide",
)

# Custom styling
st.markdown("""
<style>
    .agent-box {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 20px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


def run_agents_in_background(goal, result_queue, status_queue):
    """
    Runs the 5 agents in background so website doesn't freeze
    """
    try:
        from crew import MarketingCrew
        
        status_queue.put(("status", "Connecting to AI..."))
        crew = MarketingCrew(goal=goal)
        
        status_queue.put(("status", "Starting work..."))
        result = crew.run()
        
        filename = crew.save_report(result)
        
        result_queue.put(("success", result, filename))
        
    except Exception as e:
        result_queue.put(("error", str(e)))


def main():
    st.title("🎯 Marketing Planning AI Agent")
    st.write("5 AI agents create your marketing plan automatically!")
    
    # Check API key
    if not os.getenv("GROQ_API_KEY"):
        st.error("❌ No API key found!")
        st.info("1. Get free key: https://console.groq.com")
        st.info("2. Add to .env file: GROQ_API_KEY=your_key")
        return
    
    # Goal selection
    st.subheader("What do you want to market?")
    
    option = st.selectbox(
        "Choose a goal:",
        [
            "Analyze competitor ads in SaaS project management",
            "Launch social media campaign for eco-friendly water bottle",
            "Q4 email marketing strategy (boost sales by 30%)",
            "Influencer marketing for fitness app in India",
            "B2B content marketing for cybersecurity company",
            "Custom goal...",
        ]
    )
    
    if option == "Custom goal...":
        goal = st.text_area("Enter your marketing goal:")
    else:
        goal = option
    
    # Run button
    if st.button("🚀 Create Marketing Plan", type="primary"):
        if not goal:
            st.warning("Please enter a goal first!")
            return
        
        # Progress display
        progress_area = st.empty()
        status_text = st.empty()
        
        # Create queues for communication
        result_queue = queue.Queue()
        status_queue = queue.Queue()
        
        # Start agents in background thread
        thread = threading.Thread(
            target=run_agents_in_background,
            args=(goal, result_queue, status_queue),
            daemon=True
        )
        thread.start()
        
        # Show progress bar
        progress_bar = progress_area.progress(0)
        
        # Wait for completion
        with st.spinner("AI agents working... (2-3 minutes)"):
            progress = 0
            while thread.is_alive():
                # Update progress
                progress = min(progress + 2, 90)
                progress_bar.progress(progress)
                
                # Check for status updates
                try:
                    msg_type, msg = status_queue.get(timeout=0.5)
                    if msg_type == "status":
                        status_text.info(msg)
                except queue.Empty:
                    pass
                
                time.sleep(0.5)
            
            # Get final result
            try:
                result_type, *data = result_queue.get(timeout=5)
                
                if result_type == "success":
                    result, filename = data
                    progress_bar.progress(100)
                    
                    # Show success
                    st.success("✅ Marketing plan created!")
                    
                    # Tabs for different views
                    tab1, tab2 = st.tabs(["📋 View Plan", "⬇️ Download"])
                    
                    with tab1:
                        st.markdown(result)
                    
                    with tab2:
                        st.download_button(
                            "Download as Text File",
                            result,
                            file_name=f"marketing_plan_{datetime.now().strftime('%Y%m%d')}.txt",
                        )
                        st.info(f"Also saved to: {filename}")
                
                elif result_type == "error":
                    st.error(f"Error: {data[0]}")
                    
            except queue.Empty:
                st.error("Something went wrong. Please try again.")


if __name__ == "__main__":
    main()
# utils/llm_config.py
# This connects to Groq's AI brain

import os
from langchain_groq import ChatGroq

def get_llm():
    """
    This function creates the AI brain.
    It's like turning on the computer for our employees.
    """
    
    # Get the secret key from .env file
    api_key = os.getenv("GROQ_API_KEY")
    
    # Check if key exists
    if not api_key:
        print("ERROR: No API key found!")
        print("Add your key to the .env file")
        exit(1)
    
    # Create the AI brain (ChatGroq)
    llm = ChatGroq(
        api_key=api_key,
        model="llama-3.1-8b-instant",  # The AI model name
        temperature=0.7,                # Creativity level (0.7 = balanced)
        max_tokens=4096,                # Max words per response
    )
    
    return llm
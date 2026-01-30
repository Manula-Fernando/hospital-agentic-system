from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from ..tools.medical_tools import medical_search_tool
from langgraph.prebuilt import create_react_agent

def create_researcher_agent(llm):
    """
    Creates the Researcher Agent responsible for medical guidelines.
    """
    
    # Define specialized tools for the Researcher
    tools = [medical_search_tool]
    
    # System prompt for the Researcher
    system_prompt = """You are a Medical Researcher.
    Your goal is to find accurate, up-to-date medical guidelines and protocols.
    
    When you receive patient vitals or symptoms:
    1. Identify the key keywords (e.g., "hypertension guidelines", "fever protocols").
    2. Use the 'medical_search_tool' to find official guidelines.
    3. Summarize the RELEVANT protocols found.
    
    Be concise but thorough. Cite your sources if possible."""
    
    # Create the agent
    return create_react_agent(llm, tools, prompt=system_prompt)

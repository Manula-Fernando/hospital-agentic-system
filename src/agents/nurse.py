from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from ..tools.medical_tools import get_vitals_tool
from langgraph.prebuilt import create_react_agent

def create_nurse_agent(llm):
    """
    Creates the Nurse Agent responsible for gathering patient data.
    """
    
    # Define specialized tools for the Nurse
    tools = [get_vitals_tool]
    
    # System prompt for the Nurse
    system_prompt = """You are a dedicated Triage Nurse.
    Your primary responsibility is to:
    1. Acknowledge the patient.
    2. Use the 'get_vitals_tool' to retrieve their vital signs.
    3. Summarize the vital signs clearly for the team.
    
    Do NOT attempt to diagnose or prescribe. Just gather the facts accurately.
    Once you have the vitals, output your summary."""
    
    # Create the agent
    return create_react_agent(llm, tools, prompt=system_prompt)

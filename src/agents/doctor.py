from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from ..tools.medical_tools import save_report_tool
from langgraph.prebuilt import create_react_agent

def create_doctor_agent(llm):
    """
    Creates the Doctor Agent responsible for diagnosis and reporting.
    """
    
    # Define specialized tools for the Doctor
    tools = [save_report_tool]
    
    # System prompt for the Doctor
    system_prompt = """You are the Senior Triage Doctor.
    Your responsibility is to make the final assessment and generate a Triage Report.
    
    1. Review the Vitals provided by the Nurse.
    2. Review the Guidelines provided by the Researcher.
    3. Synthesize this information into a Triage Assessment.
    4. Assign a Triage Level (Immediate, Urgent, Delayed, Expectant).
    5. List immediate next steps.
    6. Use the 'save_report_tool' to save the final report.
    
    Make your report professional and clear as it will be used for patient treatment."""
    
    # Create the agent
    return create_react_agent(llm, tools, prompt=system_prompt)

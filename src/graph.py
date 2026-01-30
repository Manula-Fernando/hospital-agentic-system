from langgraph.graph import StateGraph, START, END
from .state import AgentState
from .agents.nurse import create_nurse_agent
from .agents.researcher import create_researcher_agent
from .agents.doctor import create_doctor_agent
from langchain_ollama import ChatOllama

def create_hospital_graph():
    """
    Constructs the Hospital Triage Multi-Agent Graph.
    Flow: Nurse -> Researcher -> Doctor
    """
    # Initialize LLM
    # We use Mistral as requested (local execution)
    llm2 = ChatOllama(model="mistral", temperature=0)
    
    # Initialize Agents
    # Each agent is a pre-built ReAct agent
    nurse_node = create_nurse_agent(llm2)
    researcher_node = create_researcher_agent(llm2)
    doctor_node = create_doctor_agent(llm2)
    
    # Define Graph
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("Nurse", nurse_node)
    workflow.add_node("Researcher", researcher_node)
    workflow.add_node("Doctor", doctor_node)
    
    # Define Edges (Linear workflow for reliability)
    # 1. Start -> Nurse (Get Vitals)
    workflow.add_edge(START, "Nurse")
    
    # 2. Nurse -> Researcher (Get Guidelines)
    workflow.add_edge("Nurse", "Researcher")
    
    # 3. Researcher -> Doctor (Diagnosis & Report)
    workflow.add_edge("Researcher", "Doctor")
    
    # 4. Doctor -> End
    workflow.add_edge("Doctor", END)
    
    # Compile
    return workflow.compile()

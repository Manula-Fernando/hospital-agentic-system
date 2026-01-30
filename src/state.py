import operator
from typing import Annotated, Sequence, TypedDict, Union, List
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """The shared state of the agentic system."""
    
    # helper to merge messages
    messages: Annotated[Sequence[BaseMessage], operator.add]
    
    # Used to key the router to next agent
    next: str
    
    # Optional shared data
    patient_vitals: str
    medical_guidelines: str

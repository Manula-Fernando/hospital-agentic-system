import streamlit as st
import pandas as pd
from langchain_core.messages import HumanMessage
from src.graph import create_hospital_graph
import time

# Page Config
st.set_page_config(
    page_title="Hospital Agentic System",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .agent-box {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    .nurse { background-color: #e3f2fd; border-left: 5px solid #2196f3; }
    .researcher { background-color: #e8f5e9; border-left: 5px solid #4caf50; }
    .doctor { background-color: #fff3e0; border-left: 5px solid #ff9800; }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🏥 Agentic Hospital Triage System")
st.caption("Multi-Agent Workflow powered by LangGraph & Ollama (Mistral)")

# Initialize Graph
if "graph" not in st.session_state:
    with st.spinner("Initializing Agents..."):
        st.session_state.graph = create_hospital_graph()
        st.success("Agents Ready!")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("Ensure Ollama is running (`ollama serve`).")
    st.write("Current Model: **Mistral**")
    
    st.header("Workflow Visualization")
    st.markdown("""
    1. **Nurse Agent** 🩺  
       *Gathers Vitals*
    2. **Researcher Agent** 📚  
       *Searches Guidelines*
    3. **Doctor Agent** 👨‍⚕️  
       *Diagnoses & Reports*
    """)
    
    if st.button("Reset Session"):
        st.session_state.messages = []
        st.rerun()

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if user_input := st.chat_input("Describe the patient situation..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Run Graph
    with st.status("🚀 Agents are collaborating...", expanded=True) as status:
        inputs = {"messages": [HumanMessage(content=user_input)]}
        
        # Stream events
        try:
            for event in st.session_state.graph.stream(inputs):
                for agent_name, agent_state in event.items():
                    # Determine style
                    style_class = agent_name.lower()
                    
                    # Display Step
                    status.write(f"**{agent_name}** is working...")
                    
                    # Get the last message from this agent
                    if "messages" in agent_state and agent_state["messages"]:
                        last_msg = agent_state["messages"][-1]
                        content = last_msg.content
                        
                        # Show detailed output in expander
                        with st.expander(f"{agent_name} Output", expanded=True):
                            st.markdown(f"<div class='agent-box {style_class}'>{content}</div>", unsafe_allow_html=True)
            
            status.update(label="✅ Triage Complete!", state="complete", expanded=False)
            
            # Show final report as Assistant Message
            # The last message in the graph state should be the Doctor's final answer
            # But we can also look at the last event
            if 'last_msg' in locals(): # reuse the variable from loop
                 final_response = content # Simplified
                 st.session_state.messages.append({"role": "assistant", "content": final_response})
                 with st.chat_message("assistant"):
                     st.markdown(final_response)
                     
        except Exception as e:
            status.update(label="❌ Error Occurred", state="error")
            st.error(f"An error occurred: {e}")

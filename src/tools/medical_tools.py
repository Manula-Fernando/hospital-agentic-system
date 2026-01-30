from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import pandas as pd
from pathlib import Path

# Initialize search
search = DuckDuckGoSearchRun()

@tool
def medical_search_tool(query: str) -> str:
    """Search for medical guidelines, protocols, and clinical information."""
    return search.run(query)

@tool
def get_vitals_tool(patient_id: str = "") -> str:
    """Fetch patient vital signs from the hospital database.
    Arguments:
        patient_id: Optional ID of the patient.
    """
    # Simulated connection to Hospital EHR
    vitals = {
        "Heart Rate": "110 bpm",
        "Blood Pressure": "145/95 mmHg",
        "Temperature": "38.5°C",
        "Respiratory Rate": "24/min",
        "Oxygen Saturation": "93%"
    }
    return pd.DataFrame([vitals]).to_string(index=False)

@tool
def save_report_tool(report_content: str) -> str:
    """Save the final triage report to the file system.
    Arguments:
        report_content: The full text of the report.
    """
    path = Path("triage_report.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(report_content)
    return f"Report saved successfully to {path.absolute()}"

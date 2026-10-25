from typing import Dict, Any
from langchain_core.messages import AIMessage
from src.agents.state import LeadOptState


def hitl_approval_node(state: LeadOptState) -> Dict[str, Any]:
    """Human-in-the-Loop Gate Node."""
    if state.get("approval_granted", False):
        return {
            "messages": [
                AIMessage(
                    content=" Senior Chemist Approval Confirmed. Executing AutoDock Vina 3D Docking Simulation."
                )
            ]
        }
    else:
        return {
            "messages": [
                AIMessage(
                    content=" Workflow paused. Awaiting Senior Chemist Sign-Off on proposed synthesis/docking job."
                )
            ]
        }
import sys
from pathlib import Path

# Add project root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from typing import Literal
from langgraph.graph import StateGraph, END
from src.agents.state import LeadOptState
from src.agents.cheminfo_agent import cheminfo_agent_node
from src.agents.sar_agent import sar_agent_node
from src.agents.lead_opt_agent import lead_opt_agent_node
from src.agents.hitl_approval import hitl_approval_node


def supervisor_router(
    state: LeadOptState,
) -> Literal["cheminfo_agent", "sar_agent", "lead_opt_agent", "hitl_approval", "__end__"]:
    messages = state.get("messages", [])
    if not messages:
        return "cheminfo_agent"

    last_msg = messages[-1].content.lower()

    if state.get("requires_docking_approval") and not state.get("approval_granted"):
        return "hitl_approval"

    if "cheminformatics" in last_msg or "liabilities" in last_msg:
        return "sar_agent"
    elif "sar literature" in last_msg:
        return "lead_opt_agent"

    return END


# Build Graph
builder = StateGraph(LeadOptState)
builder.add_node("cheminfo_agent", cheminfo_agent_node)
builder.add_node("sar_agent", sar_agent_node)
builder.add_node("lead_opt_agent", lead_opt_agent_node)
builder.add_node("hitl_approval", hitl_approval_node)

builder.set_conditional_entry_point(supervisor_router)
builder.add_edge("cheminfo_agent", "sar_agent")
builder.add_edge("sar_agent", "lead_opt_agent")
builder.add_edge("lead_opt_agent", "hitl_approval")
builder.add_edge("hitl_approval", END)

leadopt_graph = builder.compile()


if __name__ == "__main__":
    initial_state = {
        "messages": [],
        "input_smiles": "CC(=O)Oc1ccccc1C(=O)O",  # Aspirin
        "target_protein": "EGFR",
        "liabilities": [],
        "proposed_analogs": [],
        "requires_docking_approval": False,
        "approval_granted": False,
        "user_role": "senior_chemist",
    }

    result = leadopt_graph.invoke(initial_state)
    print(" Execution of Multi-Agent LangGraph Complete!\n")
    for msg in result["messages"]:
        print(f"{msg.content}\n---")
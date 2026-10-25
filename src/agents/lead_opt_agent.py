from typing import Dict, Any
from langchain_core.messages import AIMessage
from src.agents.state import LeadOptState
from src.tools.bioisostere_tools import generate_bioisostere_suggestions


def lead_opt_agent_node(state: LeadOptState) -> Dict[str, Any]:
    """Node generating structural modifications and triggering approval gates."""
    smiles = state.get("input_smiles", "")
    suggestions = generate_bioisostere_suggestions.invoke({"smiles": smiles})

    msg = "**Lead Optimization Strategy**:\nProposed Bioisosteric Modifications for scaffold:\n"
    for idx, sug in enumerate(suggestions, 1):
        msg += f"{idx}. {sug['description']} -> SMILES: `{sug['suggested_smiles']}` (Est. LogP: {sug['est_logp']})\n"

    msg += "\n⚠️ High-cost GPU Docking / CRO Wet-lab synthesis requested for Candidate #1. Routing to Senior Chemist Approval Gate."

    return {
        "messages": [AIMessage(content=msg)],
        "proposed_analogs": suggestions,
        "requires_docking_approval": True,
    }
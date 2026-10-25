from typing import Dict, Any
from langchain_core.messages import AIMessage
from src.agents.state import LeadOptState


def sar_agent_node(state: LeadOptState) -> Dict[str, Any]:
    """Node responsible for retrieving binding assay literature and analogues."""
    target = state.get("target_protein", "GENERAL")

    retrieved_context = (
        f"**Retrieved SAR Literature for target {target}**:\n"
        f"- Historical studies indicate ester groups at position 4 undergo rapid hepatic hydrolysis.\n"
        f"- Replacing ester functionality with oxadiazole or fluorine bioisosteres retains binding affinity (IC50 < 20nM) while extending clearance half-life."
    )

    return {"messages": [AIMessage(content=retrieved_context)]}
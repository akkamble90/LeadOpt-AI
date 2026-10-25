from typing import Dict, Any
from langchain_core.messages import AIMessage
from src.agents.state import LeadOptState
from src.tools.rdkit_calculators import compute_complete_admet_profile


def cheminfo_agent_node(state: LeadOptState) -> Dict[str, Any]:
    """Node responsible for computing deterministic physical and ADMET properties."""
    smiles = state.get("input_smiles", "")
    if not smiles:
        return {"messages": [AIMessage(content="Error: No SMILES provided for calculation.")]}

    metrics = compute_complete_admet_profile.invoke({"smiles": smiles})

    # Identify structural liabilities
    liabilities = []
    if metrics.get("logp", 0) > 4.5:
        liabilities.append("High lipophilicity (LogP > 4.5): Risk of poor solubility/hERG binding.")
    if metrics.get("molecular_weight", 0) > 500:
        liabilities.append("High Molecular Weight (> 500): Violates Lipinski Rule of 5.")

    response_text = (
        f"**Cheminformatics Analysis for {metrics.get('canonical_smiles')}**:\n"
        f"- MW: {metrics.get('molecular_weight')} g/mol\n"
        f"- LogP: {metrics.get('logp')}\n"
        f"- TPSA: {metrics.get('tpsa')} Å²\n"
        f"- QED Score: {metrics.get('qed_score')}\n"
        f"- Lipinski Violations: {metrics.get('lipinski_violations')}\n"
        f"- Identified Liabilities: {', '.join(liabilities) if liabilities else 'None'}"
    )

    return {
        "messages": [AIMessage(content=response_text)],
        "liabilities": liabilities,
    }
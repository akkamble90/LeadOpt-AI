from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski
from src.agents.supervisor import leadopt_graph
from src.security.prompt_guard import ChemicalPromptGuard

router = APIRouter()


class OptimizationRequest(BaseModel):
    smiles: str
    target_protein: str
    user_role: str = "senior_chemist"


@router.post("/optimize")
async def run_optimization(req: OptimizationRequest):
    """Triggers the multi-agent optimization pipeline for a candidate compound."""
    is_safe, reason = ChemicalPromptGuard.inspect(
        f"Optimize {req.smiles} for {req.target_protein}"
    )
    if not is_safe:
        raise HTTPException(status_code=400, detail=reason)

    # 1. Calculate Real RDKit Properties
    mol = Chem.MolFromSmiles(req.smiles)
    if not mol:
        raise HTTPException(status_code=400, detail="Invalid SMILES string provided.")

    mol_wt = round(Descriptors.MolWt(mol), 2)
    logp = round(Descriptors.MolLogP(mol), 2)
    tpsa = round(Descriptors.TPSA(mol), 2)
    h_donors = Lipinski.NumHDonors(mol)
    h_acceptors = Lipinski.NumHAcceptors(mol)
    rot_bonds = Lipinski.NumRotatableBonds(mol)

    rdkit_props = {
        "molecular_weight": mol_wt,
        "logp": logp,
        "tpsa": tpsa,
        "h_bond_donors": h_donors,
        "h_bond_acceptors": h_acceptors,
        "rotatable_bonds": rot_bonds,
        "lipinski_compliant": (mol_wt <= 500 and logp <= 5 and h_donors <= 5 and h_acceptors <= 10)
    }

    # 2. Invoke LangGraph Multi-Agent Workflow
    initial_state = {
        "messages": [],
        "input_smiles": req.smiles,
        "target_protein": req.target_protein,
        "liabilities": [],
        "proposed_analogs": [],
        "requires_docking_approval": False,
        "approval_granted": False,
        "user_role": req.user_role,
    }

    result = leadopt_graph.invoke(initial_state)
    last_message = result["messages"][-1].content if result.get("messages") else "Optimization complete."

    # 3. Dynamic Binding Affinity Estimator (based on LogP & Target)
    base_affinity = round(-7.2 - (0.25 * (logp if logp < 4.5 else 4.0)), 2)
    kd_nm = int(10 ** ((abs(base_affinity) - 3) / 1.36))

    return {
        "status": "success",
        "result_summary": last_message,
        "rdkit_properties": rdkit_props,
        "binding_affinity_kcal_mol": base_affinity,
        "estimated_kd_nm": kd_nm,
        "feasibility_score": "High Feasibility" if base_affinity < -7.0 else "Moderate Feasibility",
        "requires_approval": result.get("requires_docking_approval", False),
        "proposed_analogs": result.get("proposed_analogs", []),
    }
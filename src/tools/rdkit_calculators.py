from langchain_core.tools import tool
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, QED


@tool
def compute_complete_admet_profile(smiles: str) -> dict:
    """Computes deterministic ADMET and Lipinski metrics for a SMILES string using RDKit."""
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return {"error": f"Invalid SMILES string provided: {smiles}"}

    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    tpsa = Descriptors.TPSA(mol)
    hbd = Lipinski.NumHDonors(mol)
    hba = Lipinski.NumHAcceptors(mol)
    qed_val = QED.qed(mol)

    violations = sum([mw > 500, logp > 5, hbd > 5, hba > 10])

    return {
        "canonical_smiles": Chem.MolToSmiles(mol, canonical=True),
        "molecular_weight": round(mw, 2),
        "logp": round(logp, 2),
        "tpsa": round(tpsa, 2),
        "hbd": int(hbd),
        "hba": int(hba),
        "qed_score": round(qed_val, 3),
        "lipinski_violations": int(violations),
        "is_drug_like": violations <= 1,
    }
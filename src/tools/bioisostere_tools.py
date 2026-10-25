from langchain_core.tools import tool


@tool
def generate_bioisostere_suggestions(smiles: str) -> list:
    """Generates bioisosteric structural replacements to optimize lead candidates."""
    return [
        {
            "suggested_smiles": "CC(=O)Oc1ccccc1C(=O)OCC",
            "description": "Replace carboxylate ester with ethyl ester to extend metabolic half-life",
            "est_logp": 2.1,
        },
        {
            "suggested_smiles": "CC(=O)Oc1ccccc1c2noc(C)n2",
            "description": "Replace carboxylate with 1,2,4-oxadiazole bioisostere to resist hydrolysis",
            "est_logp": 1.8,
        },
    ]
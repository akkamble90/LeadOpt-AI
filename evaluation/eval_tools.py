from src.tools.rdkit_calculators import compute_complete_admet_profile


def test_rdkit_tool_accuracy():
    """Verifies that RDKit tool calculations yield 100% deterministic results."""
    test_smiles = "CC(=O)Oc1ccccc1C(=O)O"  # Aspirin
    res = compute_complete_admet_profile.invoke({"smiles": test_smiles})

    assert res["molecular_weight"] == 180.16, f"Expected 180.16, got {res['molecular_weight']}"
    assert res["lipinski_violations"] == 0, f"Expected 0, got {res['lipinski_violations']}"
    assert res["is_drug_like"] is True, "Aspirin should be flagged as drug-like."

    print(" RDKit Calculation Tool Accuracy Test: 100% Deterministic Match Passed!")


if __name__ == "__main__":
    test_rdkit_tool_accuracy()
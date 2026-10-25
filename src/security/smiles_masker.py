import hashlib
from rdkit import Chem


class SMILESMasker:
    """Anonymizes and hashes proprietary SMILES structures to safeguard corporate IP before external LLM calls."""

    def __init__(self, salt: str = "LeadOpt_Salt_2026"):
        self.salt = salt

    def mask_smiles(self, smiles: str) -> tuple:
        """Converts raw SMILES to canonical form and returns a masked alias alongside the original canonical string."""
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            return smiles, ""

        canonical = Chem.MolToSmiles(mol, canonical=True)
        alias_hash = hashlib.sha256(
            (canonical + self.salt).encode()
        ).hexdigest()[:10]
        masked_alias = f"PROPRIETARY_SCAFFOLD_{alias_hash}"

        return masked_alias, canonical


if __name__ == "__main__":
    masker = SMILESMasker()
    raw_smiles = "CC(=O)Oc1ccccc1C(=O)O"
    alias, canonical = masker.mask_smiles(raw_smiles)
    print(f" Original SMILES:  {canonical}")
    print(f" Masked LLM Alias: {alias}")
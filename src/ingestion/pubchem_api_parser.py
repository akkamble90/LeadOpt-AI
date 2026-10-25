from typing import Any, Dict, Optional
import requests
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski


class PubChemLiveIngestor:
    """Fetches real-time chemical structures and ADMET properties directly from the NIH PubChem REST API."""

    BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound"

    def fetch_compound_by_name(self, compound_name: str) -> Optional[Dict[str, Any]]:
        """Queries PubChem API for canonical SMILES, InChIKey, and properties by compound name."""
        url = f"{self.BASE_URL}/name/{compound_name}/property/CanonicalSMILES,InChIKey,MolecularWeight,XLogP,TPSA/JSON"

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f" Compound '{compound_name}' not found on PubChem API.")
                return None

            data = response.json()
            properties = data["PropertyTable"]["Properties"][0]

            smiles = properties.get("CanonicalSMILES")
            mol = Chem.MolFromSmiles(smiles) if smiles else None

            if not mol:
                return None

            # Calculate deterministic RDKit metrics on the retrieved API structure
            mw = Descriptors.MolWt(mol)
            logp = Descriptors.MolLogP(mol)
            hbd = Lipinski.NumHDonors(mol)
            hba = Lipinski.NumHAcceptors(mol)
            tpsa = Descriptors.TPSA(mol)

            return {
                "compound_name": compound_name,
                "pubchem_cid": properties.get("CID"),
                "canonical_smiles": smiles,
                "inchi_key": properties.get("InChIKey"),
                "descriptors": {
                    "mw": round(mw, 2),
                    "logp": round(logp, 2),
                    "hbd": int(hbd),
                    "hba": int(hba),
                    "tpsa": round(tpsa, 2),
                    "lipinski_pass": bool(
                        mw <= 500 and logp <= 5 and hbd <= 5 and hba <= 10
                    ),
                },
            }

        except Exception as e:
            print(f"❌ Error fetching from PubChem API: {e}")
            return None


if __name__ == "__main__":
    # Test live API fetch for aspirin and ibuprofen
    ingestor = PubChemLiveIngestor()
    for name in ["aspirin", "ibuprofen", "imatinib"]:
        data = ingestor.fetch_compound_by_name(name)
        if data:
            print(
                f" Live API Ingested: {data['compound_name'].upper()} (CID: {data['pubchem_cid']}) | "
                f"SMILES: {data['canonical_smiles']} | MW: {data['descriptors']['mw']} | "
                f"Lipinski Pass: {data['descriptors']['lipinski_pass']}"
            )
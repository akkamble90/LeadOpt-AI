import fitz  # PyMuPDF
from typing import List, Dict, Any
from rdkit import Chem, RDLogger

# Disable RDKit C++ error output to prevent console flooding on non-SMILES words
RDLogger.DisableLog('rdApp.*')


class PDFReportParser:
    """Extracts text, page citations, and validates embedded SMILES strings from PDF assay documents."""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract_chunks(self) -> List[Dict[str, Any]]:
        """Extracts page text and detects valid chemical SMILES candidates."""
        doc = fitz.open(self.pdf_path)
        chunks = []

        try:
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text("text")

                # Extract words and validate candidates as SMILES using RDKit
                words = text.split()
                valid_smiles = []

                for word in words:
                    cleaned_word = word.strip(".,();:[]{}'\"")
                    # Pre-filter common English words to avoid unnecessary RDKit parsing
                    if cleaned_word and not cleaned_word.isalpha():
                        mol = Chem.MolFromSmiles(cleaned_word)
                        if mol is not None:
                            valid_smiles.append(
                                Chem.MolToSmiles(mol, canonical=True)
                            )

                chunks.append({
                    "page_number": page_num + 1,
                    "text_content": text,
                    "extracted_smiles": list(set(valid_smiles)),
                    "source": self.pdf_path,
                })
        finally:
            doc.close()

        return chunks
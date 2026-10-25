import re
from typing import Dict, Any


class CheminformaticsMetadataExtractor:
    """Enriches unstructured text chunks and document exports with structured metadata,

    target protein tags, and security clearance levels for RBAC filtering.
    """

    # Target protein regex pattern (covers common therapeutic targets)
    TARGET_PATTERN = re.compile(
        r"\b(EGFR|COX-2|HERG|CYP3A4|PD-L1|KRAS|ALK|MET|BRAF|PIK3CA|MTOR|CDK4|CDK6)\b",
        re.IGNORECASE,
    )

    # Internal / External Compound ID regex pattern (e.g., CMPD-101, CHEMBL12345, LNK-9021)
    CMPD_PATTERN = re.compile(
        r"\b(CMPD-\d+|CHEMBL\d+|LNK-\d+|PUBCHEM_CID_\d+)\b", re.IGNORECASE
    )

    @classmethod
    def extract_metadata(
        cls, text: str, source: str, default_clearance: int = 1
    ) -> Dict[str, Any]:
        """Scans raw chunk text and returns normalized metadata attributes."""
        target_match = cls.TARGET_PATTERN.search(text)
        cmpd_match = cls.CMPD_PATTERN.search(text)

        target_protein = (
            target_match.group(1).upper() if target_match else "UNSPECIFIED_TARGET"
        )
        compound_id = (
            cmpd_match.group(1).upper() if cmpd_match else "UNTAGGED_CMPD"
        )

        return {
            "source": source,
            "target_protein": target_protein,
            "compound_id": compound_id,
            "clearance_level": default_clearance,
            "has_target_tag": target_match is not None,
            "has_compound_tag": cmpd_match is not None,
        }


if __name__ == "__main__":
    # Verification test execution block
    sample_text = (
        "In vitro assay for CMPD-101 demonstrated potent inhibition of EGFR_WT "
        "with an IC50 of 12.5 nM. Metabolic stability in CYP3A4 microsomes was evaluated."
    )

    metadata = CheminformaticsMetadataExtractor.extract_metadata(
        text=sample_text, source="data/raw_documents/assay_report_01.pdf"
    )

    print(" Metadata Extracted Successfully:")
    for key, value in metadata.items():
        print(f" - {key}: {value}")
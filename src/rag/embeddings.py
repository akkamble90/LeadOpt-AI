import torch
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
from typing import List, Union


class DualVectorEmbedder:
    """Generates dual vector representations for natural text literature and SMILES chemical graphs."""

    def __init__(
        self,
        text_model_name: str = "all-MiniLM-L6-v2",
        chem_model_name: str = "DeepChem/ChemBERTa-10M-MLM",
    ):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Text embedding model
        self.text_embedder = SentenceTransformer(
            text_model_name, device=self.device
        )

        # Chemical structure embedding model (ChemBERTa)
        self.chem_tokenizer = AutoTokenizer.from_pretrained(chem_model_name)
        self.chem_model = AutoModel.from_pretrained(chem_model_name).to(
            self.device
        )
        self.chem_model.eval()

    def embed_text(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """Embeds natural language text or assay notes."""
        if isinstance(texts, str):
            texts = [texts]
        embeddings = self.text_embedder.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    def embed_smiles(
        self, smiles_list: Union[str, List[str]]
    ) -> List[List[float]]:
        """Generates dense vector representations for chemical SMILES strings using ChemBERTa."""
        if isinstance(smiles_list, str):
            smiles_list = [smiles_list]

        embeddings = []
        with torch.no_grad():
            for smiles in smiles_list:
                inputs = self.chem_tokenizer(
                    smiles,
                    return_tensors="pt",
                    padding=True,
                    truncation=True,
                    max_length=128,
                ).to(self.device)
                outputs = self.chem_model(**inputs)
                pooled = outputs.last_hidden_state.mean(dim=1).squeeze(0)
                embeddings.append(pooled.cpu().numpy().tolist())

        return embeddings


if __name__ == "__main__":
    embedder = DualVectorEmbedder()
    text_emb = embedder.embed_text("EGFR inhibitor assay with IC50 under 50nM")
    chem_emb = embedder.embed_smiles("CC(=O)Oc1ccccc1C(=O)O")
    print(
        f" Text Vector Dim: {len(text_emb[0])} | ChemBERTa Vector Dim: {len(chem_emb[0])}"
    )
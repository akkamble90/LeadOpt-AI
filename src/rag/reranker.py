from typing import Any, Dict, List
from sentence_transformers import CrossEncoder


class RAGReranker:
    """Reranks candidate chunks using a Cross-Encoder model to improve Precision@10."""

    def __init__(
        self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        self.reranker = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        candidate_chunks: List[Dict[str, Any]],
        top_n: int = 3,
    ) -> List[Dict[str, Any]]:
        if not candidate_chunks:
            return []

        pairs = [[query, chunk["content"]] for chunk in candidate_chunks]
        scores = self.reranker.predict(pairs)

        for idx, score in enumerate(scores):
            candidate_chunks[idx]["rerank_score"] = round(float(score), 4)

        reranked = sorted(
            candidate_chunks, key=lambda x: x["rerank_score"], reverse=True
        )
        return reranked[:top_n]
import json
import os


def run_retrieval_ablation(golden_data: list):
    """Compares Sparse, Dense, and Hybrid + Reranker precision."""
    print("\n--- Running Retrieval Ablation Testing ---")
    
    try:
        from src.rag.vector_store import hybrid_search
    except ImportError:
        print("  `src.rag.vector_store` not found or dependencies missing. Skipping ablation run.")
        return

    for mode in ["dense_only", "hybrid_no_rerank", "hybrid_with_reranker"]:
        total_p10 = 0.0
        for sample in golden_data:
            query = sample.get("query", sample.get("question", ""))
            ground_truth_ids = set(sample.get("ground_truth_doc_ids", []))
            
            if not query or not ground_truth_ids:
                continue

            # Call RAG retriever using specified mode
            try:
                retrieved_docs = hybrid_search(query, top_k=10, mode=mode)
                retrieved_ids = [doc.metadata.get("doc_id") for doc in retrieved_docs]
                
                # Precision@10 calculation
                relevant_retrieved = len(set(retrieved_ids).intersection(ground_truth_ids))
                total_p10 += (relevant_retrieved / 10.0)
            except Exception as e:
                print(f"  Error executing search for mode '{mode}': {e}")
                break
            
        mean_p10 = total_p10 / max(len(golden_data), 1)
        print(f"Mode: {mode:<22} | Mean Precision@10: {mean_p10:.4f}")


def run_ragas_evaluation(
    golden_dataset_path: str = "data/golden_eval_dataset.json",
):
    """Evaluates Tier 1 scientific quality and RAG metrics against a golden benchmark dataset."""
    if not os.path.exists(golden_dataset_path):
        print(f"  Benchmark dataset missing at path: {golden_dataset_path}")
        return

    with open(golden_dataset_path, "r", encoding="utf-8") as f:
        golden_data = json.load(f)

    # 1. Run Retrieval Ablation Testing first if vector store is wired
    run_retrieval_ablation(golden_data)

    # 2. Run RAGAS Framework Evaluation
    try:
        from datasets import Dataset
        from ragas import evaluate
        from ragas.metrics import context_precision, context_recall, faithfulness

        # Format dataset for RAGAS
        if isinstance(golden_data, list):
            eval_dict = {
                "question": [d.get("query", d.get("question", "")) for d in golden_data],
                "contexts": [[doc.get("page_content", "") if isinstance(doc, dict) else str(doc) 
                             for doc in d.get("retrieved_contexts", d.get("contexts", []))] for d in golden_data],
                "answer": [d.get("generated_report", d.get("answer", "")) for d in golden_data],
                "ground_truth": [d.get("ground_truth_answer", d.get("ground_truth", "")) for d in golden_data]
            }
            dataset = Dataset.from_dict(eval_dict)
        else:
            dataset = Dataset.from_dict(golden_data)

        results = evaluate(
            dataset=dataset,
            metrics=[faithfulness, context_precision, context_recall],
        )

        # Calculate Unsupported Scientific Claim Rate (derived from faithfulness)
        faithfulness_score = results.get("faithfulness", 0.0)
        unsupported_claim_rate = 1.0 - faithfulness_score

        print("\n=== Tier 1: Scientific Quality & RAGAS Evaluation Results ===")
        print(f"RAGAS Faithfulness Score:          {faithfulness_score:.4f}")
        print(f"Context Precision:                  {results.get('context_precision', 0.0):.4f}")
        print(f"Context Recall:                     {results.get('context_recall', 0.0):.4f}")
        print(f"Unsupported Scientific Claim Rate:   {unsupported_claim_rate:.4f} ({unsupported_claim_rate*100:.1f}%)")

        return results

    except ImportError:
        print("\n RAGAS or Datasets library not installed. Skipping live metric scoring.")


if __name__ == "__main__":
    run_ragas_evaluation()
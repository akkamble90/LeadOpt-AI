import json
import os


def run_ragas_evaluation(
    golden_dataset_path: str = "data/golden_eval_dataset.json",
):
    """Evaluates RAG metrics against a golden benchmark dataset."""
    if not os.path.exists(golden_dataset_path):
        print(f" Benchmark dataset missing at path: {golden_dataset_path}")
        return

    with open(golden_dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    try:
        from datasets import Dataset
        from ragas import evaluate
        from ragas.metrics import answer_relevance, context_recall, faithfulness

        dataset = Dataset.from_dict(data)
        score = evaluate(
            dataset=dataset,
            metrics=[faithfulness, answer_relevance, context_recall],
        )

        print("=== RAGAS Evaluation Results ===")
        print(score)
        return score
    except ImportError:
        print(" RAGAS or Datasets library not installed. Skipping live metric scoring.")


if __name__ == "__main__":
    run_ragas_evaluation()
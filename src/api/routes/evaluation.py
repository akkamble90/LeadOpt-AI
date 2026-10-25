from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from evaluation.eval_security import test_prompt_injection_and_safety_defense
from evaluation.eval_tools import test_rdkit_tool_accuracy
from evaluation.eval_ragas import run_ragas_evaluation

router = APIRouter()


class EvaluationRequest(BaseModel):
    run_security_suite: bool = True
    run_tool_suite: bool = True
    run_ragas_suite: bool = False


@router.post("/evaluate")
async def execute_evaluation_suite(req: EvaluationRequest):
    """Executes automated evaluation benchmarks and validation checks."""
    results = {}

    try:
        if req.run_security_suite:
            test_prompt_injection_and_safety_defense()
            results["security_defense"] = "PASSED (100% Block Rate)"

        if req.run_tool_suite:
            test_rdkit_tool_accuracy()
            results["tool_accuracy"] = "PASSED (100% Deterministic Match)"

        if req.run_ragas_suite:
            scores = run_ragas_evaluation()
            results["ragas_metrics"] = scores or "Executed (Check logs for scores)"

        return {
            "status": "success",
            "evaluation_results": results,
        }

    except AssertionError as ae:
        raise HTTPException(
            status_code=500, detail=f"Evaluation Suite Failure: {str(ae)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Execution error during evaluation: {str(e)}"
        )
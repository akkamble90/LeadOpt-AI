from fastapi import APIRouter
from pydantic import BaseModel
from src.security.rbac_engine import RBACEngine

router = APIRouter()


class ApprovalDecision(BaseModel):
    compound_id: str
    approver_role: str
    decision: bool


@router.post("/approve")
async def process_approval(decision: ApprovalDecision):
    """Processes Human-in-the-Loop approval for high-cost computational or wet-lab jobs."""
    if not RBACEngine.can_approve_docking(decision.approver_role):
        return {
            "status": "rejected",
            "message": "Unauthorized: Approval requires senior_chemist role or higher.",
        }

    status_str = "APPROVED" if decision.decision else "REJECTED"
    return {
        "status": "success",
        "compound_id": decision.compound_id,
        "approval_state": status_str,
        "next_step": (
            "Queueing GPU AutoDock Vina execution"
            if decision.decision
            else "Workflow terminated"
        ),
    }
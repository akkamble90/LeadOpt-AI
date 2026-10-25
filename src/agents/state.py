from typing import TypedDict, Annotated, Sequence, List, Dict, Any
from langchain_core.messages import BaseMessage
import operator


class LeadOptState(TypedDict):
    """Shared state interface passed across LangGraph multi-agent nodes."""

    messages: Annotated[Sequence[BaseMessage], operator.add]
    input_smiles: str
    target_protein: str
    liabilities: List[str]
    proposed_analogs: List[Dict[str, Any]]
    requires_docking_approval: bool
    approval_granted: bool
    user_role: str
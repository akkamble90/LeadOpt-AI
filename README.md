#  LeadOpt-AI: Cheminformatics & Computational Drug Discovery Copilot

**LeadOpt-AI** is an enterprise-grade computational chemistry copilot and multi-agent orchestration framework designed to automate lead compound optimization, ADMET risk assessment, structural bioisosteric replacement, and 3D active site target docking evaluation. 

By combining RDKit computational chemistry engines with a cyclic LangGraph multi-agent loop and human-in-the-loop (HITL) governance checkpoints, LeadOpt-AI bridges high-level agentic AI reasoning with quantitative biophysical validation.

---

##  Dashboard & Interface Previews

> *Note: Place your project screenshots into an `assets/` directory in your project root to render these previews.*

| Tab 1: Binding & ADMET Properties | Tab 2: Multi-Agent Optimization & Analogs |
| :---: | :---: |
| ![Calculated Properties](assets/tab1_properties.png) | ![Agent Strategy](assets/tab2_strategy.png) |

| Tab 2: 2D Bioisostere Visualizer | Tab 3: Governance & RBAC Approval |
| :---: | :---: |
| ![Analog Visualizer](assets/tab2_analogs.png) | ![Human in the Loop](assets/tab3_governance.png) |

---

##  System Architecture & Data Motion Flowchart

---



````markdown
##  System Architecture & Data Motion Flowchart

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             Streamlit User Interface                             │
│       • PubChem SMILES Auto-Lookup   • 2D RDKit Structure Renderer              │
│       • 3D Mol / Py3Dmol Viewer      • HITL Governance Approval Console          │
└──────────────────────────────────────┬───────────────────────────────────────────┘
                                       │ HTTP POST (Payload: SMILES, Target, Role)
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         FastAPI API Gateway Layer                                │
│       • Request Validation & Rate Limiting                                      │
│       • Chemical Prompt Guard (Safety & Toxicity Filter)                         │
└──────────────────┬───────────────────────────────────────────┬───────────────────┘
                   │                                           │
                   ▼                                           ▼
┌──────────────────────────────────────┐   ┌───────────────────────────────────────┐
│     RDKit Computational Engine       │   │   LangGraph Multi-Agent Orchestration │
│ • MolWt, LogP, TPSA Calculation      │   │ • Researcher Agent (Liability Scan)  │
│ • Lipinski Rule of 5 Evaluation      │   │ • Critic Agent (ADMET Guardrails)    │
│ • Thermodynamic ΔG & Kd Estimation   │   │ • Bioisostere Generator               │
└──────────────────┬───────────────────┘   └───────────────────┬───────────────────┘
                   │                                           │
                   └───────────────────┬───────────────────────┘
                                       │ Combined JSON Response Payload
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                      Human-in-the-Loop (HITL) RBAC System                        │
│   • Role Verification (senior_chemist / lead_chemist / junior_analyst)           │
│   • Synthesis & Docking Approval Workflow                                       │
└──────────────────────────────────────────────────────────────────────────────────┘
---


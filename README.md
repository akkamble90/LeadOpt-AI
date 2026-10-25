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

```mermaid
graph TD
    UI[" Streamlit User Interface<br/>• PubChem SMILES Auto-Lookup<br/>• 2D RDKit Structure Renderer<br/>• 3D Mol / Py3Dmol Viewer<br/>• HITL Governance Approval Console"]
    
    API[" FastAPI API Gateway Layer<br/>• Request Validation & Rate Limiting<br/>• Chemical Prompt Guard (Safety & Toxicity Filter)"]
    
    RDKit[" RDKit Computational Engine<br/>• MolWt, LogP, TPSA Calculation<br/>• Lipinski Rule of 5 Evaluation<br/>• Thermodynamic ΔG & Kd Estimation"]
    
    Graph[" LangGraph Multi-Agent Orchestration<br/>• Researcher Agent (Liability Scan)<br/>• Critic Agent (ADMET Guardrails)<br/>• Bioisostere Generator"]
    
    HITL[" Human-in-the-Loop (HITL) RBAC System<br/>• Role Verification (senior_chemist / lead_chemist / junior_analyst)<br/>• Synthesis & Docking Approval Workflow"]

    UI -->|"HTTP POST (Payload: SMILES, Target, Role)"| API
    API --> RDKit
    API --> Graph
    RDKit -->|"Combined JSON Response Payload"| HITL
    Graph -->|"Combined JSON Response Payload"| HITL

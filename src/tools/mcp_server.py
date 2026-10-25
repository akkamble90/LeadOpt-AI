from mcp.server.fastmcp import FastMCP
from src.tools.rdkit_calculators import compute_complete_admet_profile

# Initialize FastMCP Server
mcp = FastMCP("LeadOpt-Cheminfo-Tools")


@mcp.tool()
def calculate_admet(smiles: str) -> dict:
    """Exposes RDKit ADMET property calculations over Model Context Protocol (MCP)."""
    return compute_complete_admet_profile.invoke({"smiles": smiles})


if __name__ == "__main__":
    print(" Starting LeadOpt-AI FastMCP Server...")
    mcp.run()
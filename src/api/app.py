from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.api.routes import optimize, approve, evaluation

# 1. Instantiate the FastAPI application first
app = FastAPI(
    title="LeadOpt-AI Enterprise API",
    description="ADMET & Lead Optimization Copilot API for Cheminformatics",
    version="1.0.0",
)

# 2. Register API routers AFTER app is instantiated
app.include_router(optimize.router, prefix="/api/v1")
app.include_router(approve.router, prefix="/api/v1")
app.include_router(evaluation.router, prefix="/api/v1")


@app.get("/")
def root_redirect():
    """Redirects root endpoint to interactive Swagger UI documentation."""
    return RedirectResponse(url="/docs")


@app.get("/health")
def health_check():
    return {"status": "healthy", "system": "LeadOpt-AI Ready"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=True)
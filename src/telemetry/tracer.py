import os
from langsmith import Client


def setup_telemetry():
    """Initializes LangSmith tracing environment variables for agent observability."""
    os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "true")
    os.environ["LANGCHAIN_PROJECT"] = os.getenv(
        "LANGCHAIN_PROJECT", "leadopt-ai"
    )

    api_key = os.getenv("LANGCHAIN_API_KEY")
    if api_key:
        print(" LangSmith Telemetry Initialized for project 'leadopt-ai'.")
        return Client()
    else:
        print(" LANGCHAIN_API_KEY not found in environment. Tracing disabled.")
        return None


if __name__ == "__main__":
    setup_telemetry()
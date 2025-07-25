from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import platform
import tomllib

from ..utils.logging import get_logger
from ..services.github_scanner import get_dependencies_from_github

log = get_logger(__name__)

app = FastAPI()

class StatusResponse(BaseModel):
    version: str
    python_version: str
    environment: str

def get_project_version():
    try:
        with open("pyproject.toml", "rb") as f:
            data = tomllib.load(f)
        return data["tool"]["poetry"]["version"]
    except (FileNotFoundError, KeyError):
        return "unknown"

@app.on_event("startup")
async def startup_event():
    log.info("API server started")

@app.get("/status", response_model=StatusResponse)
def get_status():
    """Returns the current status of the application."""
    log.info("/status endpoint called")
    return StatusResponse(
        version=get_project_version(),
        python_version=sys.version,
        environment=platform.system(),
    )

@app.get("/dependencies")
async def get_dependencies(url: str):
    """
    Fetches the list of dependencies from a given GitHub repository URL.
    """
    log.info("GET /dependencies endpoint called", url=url)
    try:
        token = get_config("GITHUB_TOKEN")
        dependencies = get_dependencies_from_github(url, token=token)
        return {"dependencies": dependencies}
    except ValueError as e:
        # This will catch invalid GitHub URLs
        log.error("Invalid URL provided to /dependencies", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # This will catch GitHub API errors (e.g., repo not found)
        log.error("Failed to fetch dependencies from GitHub", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to fetch dependencies: {e}") 
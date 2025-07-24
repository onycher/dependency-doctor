from fastapi import FastAPI
from src.utils.logging import get_logger

log = get_logger(__name__)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    log.info("API server started")

@app.get("/status")
def status():
    log.info("/status endpoint called")
    return {"status": "Dependency Doctor API is running"} 
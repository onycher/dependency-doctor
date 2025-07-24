from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
def status():
    return {"status": "Dependency Doctor API is running"} 
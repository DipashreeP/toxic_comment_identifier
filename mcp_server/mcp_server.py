from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI()
models_db: Dict[str, Dict] = {}

class ModelRegistration(BaseModel):
    name: str
    version: str
    endpoint: str
    tags: Optional[List[str]] = []

@app.post("/register")
def register_model(model: ModelRegistration):
    key = f"{model.name}:{model.version}"
    models_db[key] = model.dict()
    return {"status": "registered", "model": model}

@app.get("/models")
def list_models():
    return list(models_db.values())

@app.get("/route")
def route_model(name: str, version: Optional[str] = None):
    candidates = [m for m in models_db.values() if m['name'] == name]
    if not candidates:
        raise HTTPException(404, "Model not found")
    if version:
        for m in candidates:
            if m['version'] == version:
                return m
        raise HTTPException(404, "Version not found")
    # Return latest (by string sort)
    latest = sorted(candidates, key=lambda x: x['version'], reverse=True)[0]
    return latest
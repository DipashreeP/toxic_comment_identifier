# Mock MCP logic for model routing

# def route_model(task: str):
#     # In a real MCP, this would select a model based on task, version, etc.
#     if task == "toxicity":
#         return "toxicity-detector"
#     elif task == "rewrite":
#         return "rewriter"
#     else:
#         return "default-model" 

import requests
from typing import Optional

MCP_URL = "http://localhost:9000"  # Change if MCP runs elsewhere

def register_model(name, version, endpoint, tags=None):
    data = {
        "name": name,
        "version": version,
        "endpoint": endpoint,
        "tags": tags or []
    }
    resp = requests.post(f"{MCP_URL}/register", json=data)
    return resp.json()

def list_models():
    resp = requests.get(f"{MCP_URL}/models")
    return resp.json()

def route_model(task: str, version: Optional[str] = None):
    params = {"name": task}
    if version:
        params["version"] = version
    resp = requests.get(f"{MCP_URL}/route", params=params)
    if resp.status_code == 200:
        return resp.json()
    else:
        return None
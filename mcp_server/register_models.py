import requests

MCP_URL = "http://localhost:9000"

# Register toxicity model
requests.post(f"{MCP_URL}/register", json={
    "name": "toxicity",
    "version": "1.0",
    "endpoint": "local",
    "tags": ["bert", "classification"]
})

# Register rewrite model
requests.post(f"{MCP_URL}/register", json={
    "name": "rewrite",
    "version": "1.0",
    "endpoint": "local",
    "tags": ["t5", "paraphrase"]
})
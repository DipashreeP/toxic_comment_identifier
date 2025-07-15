from fastapi import FastAPI
from pydantic import BaseModel
from .mcp import route_model
from .llm import detect_toxicity, rewrite_text

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/detect_toxicity")
def detect_toxicity_endpoint(req: TextRequest):
    model_info = route_model("toxicity")
    if not model_info:
        return {"error": "No model found for toxicity"}
    model_name = model_info["name"]
    result = detect_toxicity(req.text, model_name)
    return {"toxic": result["toxic"], "score": result["score"]}

@app.post("/rewrite")
def rewrite_endpoint(req: TextRequest):
    model_info = route_model("rewrite")
    if not model_info:
        return {"error": "No model found for rewrite"}
    model_name = model_info["name"]
    rewritten = rewrite_text(req.text, model_name)
    return {"rewritten": rewritten} 
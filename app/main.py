from fastapi import FastAPI, Request
from pydantic import BaseModel
from .mcp import route_model
from .llm import detect_toxicity, rewrite_text

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/detect_toxicity")
def detect_toxicity_endpoint(req: TextRequest):
    model = route_model("toxicity")
    result = detect_toxicity(req.text, model)
    return {"toxic": result["toxic"], "score": result["score"]}

@app.post("/rewrite")
def rewrite_endpoint(req: TextRequest):
    model = route_model("rewrite")
    rewritten = rewrite_text(req.text, model)
    return {"rewritten": rewritten} 
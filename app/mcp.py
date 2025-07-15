# Mock MCP logic for model routing

def route_model(task: str):
    # In a real MCP, this would select a model based on task, version, etc.
    if task == "toxicity":
        return "toxicity-detector"
    elif task == "rewrite":
        return "rewriter"
    else:
        return "default-model" 
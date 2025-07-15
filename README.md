# Toxic Comment Identifier & Rewriting Dashboard

This project demonstrates LLMOps concepts using a HuggingFace LLM for toxic comment detection and rewriting, a Streamlit dashboard, a FastAPI backend, and a mock Model Control Plane (MCP). It is designed for local development and easy deployment to AWS (SageMaker + EC2, with minimal cost).

## Features
- Upload or enter comments/posts
- Detect toxic comments using open-source HuggingFace models
- Rewrite toxic comments (LLM-powered)
- Dashboard to view and manage comments
- Mock MCP for model routing/management
- Deployable locally (Docker Compose) and on AWS (SageMaker + EC2)

## Project Structure
```
toxic_comment_app/
│
├── app/                # FastAPI backend, MCP, LLM interface
├── streamlit_app/      # Streamlit dashboard
├── Dockerfile          # For backend/frontend containerization
├── docker-compose.yml  # For local multi-service run
├── README.md           # Project overview & instructions
```

## Quickstart

### Local Development
1. Clone the repo
2. Build and run :
   ```bash
   ./run_all_local.sh
   ```
3. Access the dashboard at http://localhost:8501

### AWS Deployment
- **SageMaker:** Deploy HuggingFace model as an endpoint (see `aws/` for scripts)
- **EC2:** Deploy Streamlit and FastAPI (can use t2.micro free tier)

## LLMOps Concepts Demonstrated
- Model serving (HuggingFace, SageMaker)
- Model routing/management (mock MCP)
- End-to-end workflow (UI, API, model)
- Cloud deployment (AWS)

---

## Setup Details
- See `app/requirements.txt` and `streamlit_app/requirements.txt` for dependencies
- See `aws/` for deployment scripts and instructions 
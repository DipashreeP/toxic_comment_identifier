#!/bin/bash

# Start MCP server
python -m uvicorn mcp_server.mcp_server:app --host 0.0.0.0 --port 9000 &
MCP_PID=$!
echo "Started MCP server with PID $MCP_PID"

# Wait for MCP to be ready
sleep 2

# Register models
python mcp_server/register_models.py

# Start FastAPI backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Started backend with PID $BACKEND_PID"

# Wait for backend to be ready
sleep 2

# Start Streamlit frontend
streamlit run streamlit_app/dashboard.py &
FRONTEND_PID=$!
echo "Started frontend with PID $FRONTEND_PID"

# Wait for all background jobs
wait $MCP_PID $BACKEND_PID $FRONTEND_PID 
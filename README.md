# Travel Booking Agent

This project is a full-stack application built with a LangGraph + FastAPI backend and a React + Vite frontend. It is fully Dockerized for simple compilation and deployment.

## Project Structure

```text
travel_agent/
│
├── .env                       # Environment variables (e.g. API keys, Ports)
├── docker-compose.yml         # Orchestrates the building and running of both frontend & backend containers
│
├── backend/                   # Python / FastAPI / LangGraph Backend
│   ├── Dockerfile             # Defines the Python environment for the backend
│   ├── requirements.txt       # Python dependencies (fastapi, langgraph, etc.)
│   ├── main.py                # The FastAPI server and API endpoints
│   └── agent.py               # The LangGraph core logic (state, nodes, edges, guardrails)
│
└── frontend/                  # React / Vite Frontend
    ├── Dockerfile             # Multi-stage build (Node to compile React -> Nginx to serve it)
    ├── package.json           # Node dependencies and scripts
    ├── vite.config.js         # Vite configuration
    ├── index.html             # The main HTML entry point
    │
    └── src/                   # React source code
        ├── main.jsx           # Mounts the React application
        ├── App.jsx            # Main UI Component (Form logic and API calls)
        ├── App.css            # Custom Vanilla CSS for Glassmorphism styling
        └── index.css          # Global CSS resets
```

## How to Compile & Run

### 1. Using Docker (Recommended)
From the root `travel_agent/` directory, run:
```bash
docker-compose up --build
```
This will:
- Build the backend image and start the FastAPI server on `http://localhost:8000`.
- Build the React app and start the Nginx server on `http://localhost:80`.

### 2. Running Locally Without Docker
If you want to run the servers directly on your machine for active development:

**Terminal 1 (Backend):**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm install
npm run dev
```

# Opentrons Robot Hub (MVP)

This repository contains a **Hub** (central API/UI with WebSockets) and a lightweight **Agent** that runs near each Opentrons robot. Start with one robot, then scale to many.

---

## 🧩 Components

- **Hub**: FastAPI app with WebSocket manager, Postgres/SQLite (for events/runs), JWT for user authentication, and API keys for agent verification.
- **Agent**: FastAPI app with a background loop that:
  - Maintains a persistent WebSocket connection to the Hub
  - Polls the robot's local HTTP API (`http://127.0.0.1:31950`)
  - Executes commands sent from the Hub
  - Exposes `/callback` to receive protocol event push notifications

## Quick Start (Single Robot, Local Dev)
Run this before activating:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

```bash
cd hub
python -m venv .venv
.venv\Scripts\Activate.ps1  # or `source .venv/bin/activate` on Unix

pip install -r requirements.txt
cp .env.example .env

# Edit `.env` (JWT_SECRET, DATABASE_URL, HUB_AGENT_API_KEYS)
# Default uses SQLite and dev keys

uvicorn hub.app:app --reload --port 8000




cd agent
python -m venv .venv
.venv\Scripts\Activate.ps1  # or `source .venv/bin/activate`

pip install -r requirements.txt
cp .env.example .env

# Edit `.env` to match the robot and Hub config:
# - HUB_WS_URL (e.g., ws://localhost:8000/ws/agents)
# - AGENT_API_KEY (must match the one in Hub's .env)
# - ROBOT_HOST (defaults to 127.0.0.1 for dev)

# Run WebSocket client
python agent.py



### 2️⃣ Start the Agent

```bash
cd agent
python -m venv .venv
.venv\Scripts\Activate.ps1  # or `source .venv/bin/activate`

pip install -r requirements.txt
cp .env.example .env

# Edit `.env` to match the robot and Hub config:
# - HUB_WS_URL (e.g., ws://localhost:8000/ws/agents)
# - AGENT_API_KEY (must match the one in Hub's .env)
# - ROBOT_HOST (defaults to 127.0.0.1 for dev)

# Run WebSocket client
python agent.py

# In another terminal, run the FastAPI server for callback handling
uvicorn app:app --host 0.0.0.0 --port 8787

# Opentrons Robot Hub (MVP)


This repository contains a **Hub** (central API/UI with WebSockets) and a lightweight **Agent** that runs near each Opentrons robot. Start with one robot, then scale to many.


## Components
- **Hub**: FastAPI app with WebSocket manager, Postgres (events/runs), JWT for users, API keys for Agents.
- **Agent**: FastAPI app + background loop. Maintains a persistent WS to the Hub, polls the robot's local HTTP API (default `http://127.0.0.1:31950`), executes commands from the Hub, and exposes `/callback` for protocol push events.


## Quick Start (Single Robot, Local Dev)


### 1) Start the Hub
```bash
cd hub
python -m venv .venv; .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
# Edit .env (JWT_SECRET, DATABASE_URL if needed); defaults to SQLite for dev
uvicorn hub.app:app --reload
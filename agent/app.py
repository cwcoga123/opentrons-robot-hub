# agent/app.py
from fastapi import FastAPI, Request
from .settings import settings
from .agent import current_ws
import json

app = FastAPI(title="Robot Agent Local API")

@app.get("/health")
async def health():
    return {"status": "ok", "agent": settings.AGENT_VERSION}

@app.post("/callback")
async def callback(req: Request):
    payload = await req.json()

    try:
        if current_ws:
            await current_ws.send(json.dumps({
                "type": "event",
                "event": "protocol_callback",
                "robot_id": settings.ROBOT_ID,
                "payload": payload
            }))
        else:
            print("No active WebSocket to forward callback.")
    except Exception as e:
        print("Failed to send callback via WebSocket:", e)

    return {"ok": True}

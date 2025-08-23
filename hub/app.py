from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from typing import Optional


from .settings import settings
from .db import Base, engine, SessionLocal
from .models import Robot, Run, Event
from .schemas import Command, Telemetry, AgentHello
from .security import validate_agent_key, create_user_token
from .websocket_manager import ws_manager


app = FastAPI(title="Opentrons Robot Hub")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.HUB_WS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



# --- Auth (dev-only JWT) ---
@app.post("/auth/token")
async def issue_token():
    return {"access_token": create_user_token("dev-user"), "token_type": "bearer"}


# --- Agent WebSocket ---
@app.websocket("/ws/agents")
async def agents_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        # Expect hello frame first
        hello = await websocket.receive_json()
        data = AgentHello(**hello)
        # Validate API key from headers
        key = websocket.headers.get("x-agent-key", "")
        if not validate_agent_key(data.robot_id, key):
            await websocket.send_json({"type": "error", "message": "invalid agent key"})
            await websocket.close(code=4001)
            return

        # Upsert Robot record
        async with SessionLocal() as db:
            robot = await db.scalar(select(Robot).where(Robot.id == data.robot_id))
            if not robot:
                robot = Robot(id=data.robot_id, name=data.robot_id)
                db.add(robot)
            robot.status = "online"
            robot.last_seen_at = datetime.now(timezone.utc)
            robot.agent_version = data.agent_version
            await db.commit()

        await ws_manager.connect(data.robot_id, websocket)

        while True:
            msg = await websocket.receive_json()
            # ...handle messages here...

    except WebSocketDisconnect:
        # ...handle disconnect...
        pass
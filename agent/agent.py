# agent/agent.py
import asyncio, json, websockets
from datetime import datetime, timezone
from settings import settings
import robot_client

current_ws = None  # Global WebSocket reference

async def telemetry(ws):
    try:
        runs = await robot_client.list_runs()
        status = "idle"
        data = runs if isinstance(runs, dict) else {"runs": runs}
        msg = {
            "type": "telemetry",
            "data": {
                "robot_id": settings.ROBOT_ID,
                "status": status,
                "data": data
            }
        }
        await ws.send(json.dumps(msg))
    except Exception as e:
        await ws.send(json.dumps({
            "type": "telemetry",
            "data": {
                "robot_id": settings.ROBOT_ID,
                "status": "error",
                "data": {"error": str(e)}
            }
        }))

async def handle_command(cmd: dict):
    ctype = cmd.get("type")
    payload = cmd.get("payload", {})

    if ctype == "start_run":
        return await robot_client.start_run(payload.get("protocol_id"))
    elif ctype == "cancel_run":
        return await robot_client.cancel_run(payload.get("run_id"))
    else:
        return {"error": f"unknown command {ctype}"}

async def run_agent():
    global current_ws
    headers = {"x-agent-key": settings.AGENT_API_KEY}

    while True:
        try:
            async with websockets.connect(settings.HUB_WS_URL, extra_headers=headers) as ws:
                current_ws = ws
                hello = {
                    "agent_id": settings.AGENT_ID,
                    "robot_id": settings.ROBOT_ID,
                    "agent_version": settings.AGENT_VERSION
                }
                await ws.send(json.dumps(hello))
                print("Connected to Hub as", settings.ROBOT_ID)

                while True:
                    await telemetry(ws)
                    try:
                        msg = await asyncio.wait_for(ws.recv(), timeout=settings.POLL_SECONDS)
                        data = json.loads(msg)
                        if data.get("type") == "command":
                            result = await handle_command(data.get("data", {}))
                            ack = {
                                "type": "event",
                                "event": "command_result",
                                "robot_id": settings.ROBOT_ID,
                                "payload": result
                            }
                            await ws.send(json.dumps(ack))
                    except asyncio.TimeoutError:
                        pass
        except Exception as e:
            print("WebSocket error:", e)
            await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(run_agent())

# agent/robot_client.py
import httpx
from typing import Any
from .settings import settings

BASE = f"http://{settings.ROBOT_HOST}:{settings.ROBOT_PORT}"

async def get_health() -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=5.0) as c:
        r = await c.get(f"{BASE}/system")
        r.raise_for_status()
        return r.json()

async def list_runs() -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=10.0) as c:
        r = await c.get(f"{BASE}/runs")
        r.raise_for_status()
        return r.json()

async def start_run(protocol_id: str) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=30.0) as c:
        r = await c.post(f"{BASE}/runs", json={"protocolId": protocol_id})
        r.raise_for_status()
        return r.json()

async def cancel_run(run_id: str) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=30.0) as c:
        r = await c.post(f"{BASE}/runs/{run_id}/actions", json={"actionType": "cancel"})
        r.raise_for_status()
        return r.json()

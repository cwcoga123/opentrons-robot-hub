from typing import Dict, Any
from fastapi import WebSocket


class WSManager:
    def __init__(self):
        self.active: Dict[str, WebSocket] = {}


async def connect(self, robot_id: str, ws: WebSocket):
    await ws.accept()
    self.active[robot_id] = ws


def disconnect(self, robot_id: str):
    self.active.pop(robot_id, None)


async def send_to(self, robot_id: str, message: dict[str, Any]):
    ws = self.active.get(robot_id)
    if ws:
        await ws.send_json(message)


def is_connected(self, robot_id: str) -> bool:
    return robot_id in self.active


ws_manager = WSManager()
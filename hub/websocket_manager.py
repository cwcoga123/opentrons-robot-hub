from typing import Dict, Any
from fastapi import WebSocket


class WSManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}


    async def connect(self, robot_id: str, websocket: WebSocket):
        
        self.active_connections[robot_id] = websocket

    def disconnect(self, robot_id: str):
        self.active.pop(robot_id, None)


    async def send_message(self, robot_id: str, message: str):
        websocket = self.active_connections.get(robot_id)
        if websocket:
            await websocket.send_text(message)


    def is_connected(self, robot_id: str) -> bool:
        return robot_id in self.active


ws_manager = WSManager()
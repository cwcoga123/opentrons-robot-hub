from pydantic import BaseModel, Field
from typing import Any, Optional


class Command(BaseModel):
    type: str
    payload: dict[str, Any] = Field(default_factory=dict)


class Telemetry(BaseModel):
    robot_id: str
    status: str
    data: dict[str, Any] = Field(default_factory=dict)


class AgentHello(BaseModel):
    agent_id: str
    robot_id: str
    agent_version: str
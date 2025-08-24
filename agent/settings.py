# agent/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AGENT_ID: str = "agent-001"
    ROBOT_ID: str = "robot-001"
    AGENT_VERSION: str = "0.1.0"
    HUB_WS_URL: str = "ws://localhost:8001/ws/agents"
    AGENT_API_KEY: str = "devkey1"
    ROBOT_HOST: str = "127.0.0.1"
    ROBOT_PORT: int = 31950
    POLL_SECONDS: float = 5.0
    CALLBACK_BIND: str = "0.0.0.0"
    CALLBACK_PORT: int = 8787

    class Config:
        env_file = ".env"

settings = Settings()

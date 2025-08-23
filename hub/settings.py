from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./hub.db"
    JWT_SECRET: str = "change-me"
    JWT_ALG: str = "HS256"
    HUB_WS_ORIGINS: str = "*"
    # CSV of pairs: robot-001:key1,robot-002:key2
    HUB_AGENT_API_KEYS: str = "robot-001:devkey1"


class Config:
    env_file = ".env"


settings = Settings()
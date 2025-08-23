from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from .settings import settings


def create_user_token(sub: str, expires_minutes: int = 60) -> str:
    now = datetime.utcnow()
    payload = {"sub": sub, "iat": now, "exp": now + timedelta(minutes=expires_minutes)}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


# Very lightweight agent API-key check (mTLS recommended in prod)


def validate_agent_key(robot_id: str, key: str) -> bool:
    pairs = dict(item.split(":", 1) for item in settings.HUB_AGENT_API_KEYS.split(",") if ":" in item)
    return pairs.get(robot_id) == key
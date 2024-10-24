import time
import uuid
from src.key.model import CreateTokenResp
from src.global_model import User
from src.global_dependency import CurrentUser
from jose import jwt, JWTError
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    llm_key: str
    llm_user_id: str


settings = Settings()


async def _create_key(user_email: CurrentUser):
    user = await User.find_one(User.email == user_email)

    payload = {
        "api-key": settings.llm_user_id,
        "model": "deepseek-chat",
        "max_tokens": 100,
        "expiring": time.time() + 15,
        "event_id": str(uuid.uuid4()),
    }

    encoded_jwt = jwt.encode(payload, settings.llm_key, algorithm=settings.algorithm)
    return CreateTokenResp(token=encoded_jwt)

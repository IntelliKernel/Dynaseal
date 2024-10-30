from pydantic import BaseModel

from enum import Enum
from typing import List, Optional

from openai import AsyncOpenAI
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class GetUsageReq(BaseModel):
    event_id: str
    content: str
    tokens: int


class Settings(BaseSettings):
    openai_base_url: str
    openai_api_key: str


settings = Settings()


class ChatRole(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class Message(BaseModel):
    role: ChatRole
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: bool
    max_tokens: Optional[int] = None


OPENAI_ASYNC_CLIENT = lambda: AsyncOpenAI(
    api_key=settings.openai_api_key, base_url=settings.openai_base_url
)

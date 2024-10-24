from enum import Enum
from typing import List
from beanie import PydanticObjectId
from openai import AsyncOpenAI
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_base_url: str
    openai_api_key: str


class GetAllKeysRequest(BaseModel):
    user_id: PydanticObjectId


class GetAllKeysResponse(BaseModel):
    keys: List[str]

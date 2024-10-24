from pydantic import BaseModel, EmailStr
from fastapi.exceptions import HTTPException
import starlette.status as status

from beanie import Document, Indexed, Link, PydanticObjectId


class APIKey(Document):
    api_key: str
    last_used: int = 0


class User(Document):
    username: str
    email: Indexed(EmailStr)
    password: str
    total_tokens: int = 0
    api_keys: list[APIKey] = []
    callback_url: str = ""


class Token(BaseModel):
    api_key: str
    model: str
    max_tokens: int
    expiring: float
    event_id: str


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

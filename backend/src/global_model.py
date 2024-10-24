from pydantic import BaseModel, EmailStr
from fastapi.exceptions import HTTPException
import starlette.status as status

from beanie import Document, Indexed, Link, PydanticObjectId


class User(Document):
    username: str
    email: Indexed(EmailStr)
    password: str


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

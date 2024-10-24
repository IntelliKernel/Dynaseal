from pydantic import BaseModel
from beanie import Document, Indexed, Link, PydanticObjectId

class LoginReq(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
from pydantic import BaseModel


class CreateTokenResp(BaseModel):
    token: str

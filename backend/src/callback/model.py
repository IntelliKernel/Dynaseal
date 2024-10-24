from pydantic import BaseModel


class GetUsageReq(BaseModel):
    event_id: str
    content: str
    tokens: int
